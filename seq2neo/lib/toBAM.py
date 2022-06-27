import os
import subprocess as sp
from Bio.Sequencing.Applications import BwaMemCommandline
from seq2neo.function.GATK_Best_Practice import *
from seq2neo.function.HLA_typing import *
from seq2neo.function import *


def toBAM_dna_normal(args, tmpPATH, resultsPATH):

    if args.data_type == 'fastq':
        normal_sorted_bam = fastq_part_normal(args, tmpPATH, resultsPATH)
    elif args.data_type == 'sam':
        normal_sorted_bam = sam_part_normal(args, tmpPATH)
    else:
        normal_sorted_bam = args.normal_sorted_bam

    # MarkDuplicate
    print("MarkDuplicate normal sorted bam")
    normal_marked_bam = os.path.join(tmpPATH, "normal_marked.bam")
    normal_metric_file = os.path.join(tmpPATH, "normal.rmdup.metric")
    normal_mark_cmd = MarkDuplicatesCommandline(I=normal_sorted_bam,
                                                O=normal_marked_bam,
                                                M=normal_metric_file,
                                                VALIDATION_STRINGENCY="LENIENT",
                                                MAX_FILE_HANDLES=8000,
                                                CREATE_INDEX=True,
                                                java_options=args.java_options)
    normal_mark_cmd()
    # BQSR
    print("BQSR normal marked bam")
    normal_bqsr_out = os.path.join(tmpPATH, "normal_BQSR.bam")
    known_sites = []
    for dirpath, dirnames, filenames in os.walk(args.known_site_dir):
        for filename in filenames:
            if not filename.endswith("tbi"):
                known_sites.append(os.path.join(dirpath, filename))

    normal_bqsr_cmd = BQSR(ref=args.ref, Input=normal_marked_bam,
                           known_sites=known_sites,
                           out_bam=normal_bqsr_out, java_options=args.java_options)
    normal_bqsr_cmd.baserecalibrator()
    normal_bqsr_cmd.applybqsr()

    # delete unimportant tmp files
    rm_cmd = '''find %s -type f -not -name "*BQSR*" -print0 | xargs -0 rm -f''' % tmpPATH
    sp.check_call(rm_cmd, shell=True)


def toBAM_dna_tumor(args, tmpPATH):

    if args.data_type == 'fastq':
        tumor_sorted_bam = fastq_part_tumor(args, tmpPATH)
    elif args.data_type == 'sam':
        tumor_sorted_bam = sam_part_tumor(args, tmpPATH)
    else:
        tumor_sorted_bam = args.tumor_sorted_bam

    # MarkDuplicate
    print("MarkDuplicate tumor sorted bam")
    tumor_marked_bam = os.path.join(tmpPATH, "tumor_marked.bam")
    tumor_metric_file = os.path.join(tmpPATH, "tumor.rmdup.metric")
    tumor_mark_cmd = MarkDuplicatesCommandline(I=tumor_sorted_bam,
                                               O=tumor_marked_bam,
                                               M=tumor_metric_file,
                                               VALIDATION_STRINGENCY="LENIENT",
                                               MAX_FILE_HANDLES=8000,
                                               CREATE_INDEX=True,
                                               java_options=args.java_options)
    tumor_mark_cmd()
    # BQSR
    print("BQSR tumor marked bam")
    tumor_bqsr_out = os.path.join(tmpPATH, "tumor_BQSR.bam")
    known_sites = []
    for dirpath, dirnames, filenames in os.walk(args.known_site_dir):
        for filename in filenames:
            if not filename.endswith("tbi"):
                known_sites.append(os.path.join(dirpath, filename))

    tumor_bqsr_cmd = BQSR(ref=args.ref, Input=tumor_marked_bam,
                          known_sites=known_sites,
                          out_bam=tumor_bqsr_out, java_options=args.java_options)
    tumor_bqsr_cmd.baserecalibrator()
    tumor_bqsr_cmd.applybqsr()

    # delete unimportant tmp files
    rm_cmd = '''find %s -type f -not -name "*BQSR*" -print0 | xargs -0 rm -f''' % tmpPATH
    sp.check_call(rm_cmd, shell=True)


def fastq_part_normal(args, tmpPATH, resultsPATH):

    print("Executing Normal Fastp Command Line")
    normal_out1 = os.path.join(tmpPATH, "normal_1_qc.fastq")
    normal_out2 = os.path.join(tmpPATH, "normal_2_qc.fastq")
    normal_json = os.path.join(tmpPATH, "normal.json")
    normal_html = os.path.join(tmpPATH, "normal.html")

    normal_fastp_cmd = FastpCommandline(i=args.normal_dna[0],
                                        I=args.normal_dna[1],
                                        o=normal_out1,
                                        O=normal_out2,
                                        j=normal_json,
                                        h=normal_html,
                                        w=args.threadN)
    normal_fastp_cmd()

    print("Executing HLATyping Command Line")
    freq_data = os.path.join(args.hlahd_dir, 'freq_data')
    gene_split = os.path.join(args.hlahd_dir, 'HLA_gene.split.txt')
    dictionary = os.path.join(args.hlahd_dir, 'dictionary')
    hlahd_cmd = HLAHDCommandLine(t=args.threadN,
                                 m=args.mdna,
                                 f=freq_data,
                                 fasta_file1=normal_out1,
                                 fasta_file2=normal_out2,
                                 gene_split_file=gene_split,
                                 HLA_fasta_dir=dictionary,
                                 sampleID=args.tumor_name,
                                 out_dir=tmpPATH)
    hlahd_cmd()

    result_path = os.path.join(tmpPATH, '%s/result/%s_final.result.txt' % (args.tumor_name, args.tumor_name))
    mv_cmd = 'cp %s %s' % (result_path, resultsPATH)
    sp.check_call(mv_cmd, shell=True)

    print("Executing Normal BWA-MEM Command Line")
    normal_out = os.path.join(tmpPATH, "normal.sam")
    normal_R = '"@RG\\tID:%s\\tSM:%s\\tPL:Illumina\\tLB:WES"' % (args.normal_name, args.normal_name)

    normal_bwa_cmd = BwaMemCommandline(
        t=args.threadN, R=normal_R, M="M", a="a",
        reference=args.ref,
        read_file1=normal_out1, read_file2=normal_out2
    )
    normal_bwa_cmd(stdout=normal_out)

    print("Executing Normal SAM2BAM Command Line")
    normal_bam = os.path.join(tmpPATH, "normal.bam")

    normal_samtools_cmd = SamtoolsViewCommandline_thread(input=normal_out,
                                                         b="b",
                                                         S="S", o=normal_bam,
                                                         threads=args.threadN)
    normal_samtools_cmd()

    # sort bam
    print("Executing Normal Sort bam Command Line")
    normal_sorted_bam = os.path.join(tmpPATH, "normal_sorted.bam")
    normal_sorted_cmd = SortBam_Commandline(threads=args.threadN,
                                            o=normal_sorted_bam,
                                            i=normal_bam)
    normal_sorted_cmd()

    print("Executing Normal Index sorted bam Command Line")
    normal_index_sorted_bam = os.path.join(tmpPATH, "normal_sorted.bai")
    normal_index_cmd = IndexBam_Commandline(threads=args.threadN,
                                            i=normal_sorted_bam,
                                            o=normal_index_sorted_bam)
    normal_index_cmd()

    return normal_sorted_bam


def sam_part_normal(args, tmpPATH):

    print("Executing Normal SAM2BAM Command Line")
    normal_input = args.normal_sam
    normal_bam = os.path.join(tmpPATH, "normal.bam")

    normal_samtools_cmd = SamtoolsViewCommandline_thread(input=normal_input,
                                                         b="b",
                                                         S="S", o=normal_bam,
                                                         threads=args.threadN)
    normal_samtools_cmd()

    # sort bam
    print("Executing Normal Sort bam Command Line")
    normal_sorted_bam = os.path.join(tmpPATH, "normal_sorted.bam")
    normal_sorted_cmd = SortBam_Commandline(threads=args.threadN,
                                            o=normal_sorted_bam,
                                            i=normal_bam)
    normal_sorted_cmd()

    print("Executing Normal Index sorted bam Command Line")
    normal_index_sorted_bam = os.path.join(tmpPATH, "normal_sorted.bai")
    normal_index_cmd = IndexBam_Commandline(threads=args.threadN,
                                            i=normal_sorted_bam,
                                            o=normal_index_sorted_bam)
    normal_index_cmd()

    return normal_sorted_bam


def fastq_part_tumor(args, tmpPATH):

    print("Executing Tumor Fastp Command Line")
    tumor_out1 = os.path.join(tmpPATH, "tumor_1_qc.fastq")
    tumor_out2 = os.path.join(tmpPATH, "tumor_2_qc.fastq")
    tumor_json = os.path.join(tmpPATH, "tumor.json")
    tumor_html = os.path.join(tmpPATH, "tumor.html")

    tumor_fastp_cmd = FastpCommandline(i=args.tumor_dna[0],
                                       I=args.tumor_dna[1],
                                       o=tumor_out1,
                                       O=tumor_out2,
                                       j=tumor_json,
                                       h=tumor_html,
                                       w=args.threadN)
    tumor_fastp_cmd()

    print("Executing Tumor BWA-MEM Command Line")
    tumor_out = os.path.join(tmpPATH, "tumor.sam")
    tumor_R = '"@RG\\tID:%s\\tSM:%s\\tPL:Illumina\\tLB:WES"' % (args.tumor_name, args.tumor_name)

    tumor_bwa_cmd = BwaMemCommandline(
        t=args.threadN, R=tumor_R, M="M", a="a",
        reference=args.ref,
        read_file1=tumor_out1, read_file2=tumor_out2
    )
    tumor_bwa_cmd(stdout=tumor_out)

    print("Executing Tumor SAM2BAM Command Line")
    tumor_bam = os.path.join(tmpPATH, "tumor.bam")

    tumor_samtools_cmd = SamtoolsViewCommandline_thread(input=tumor_out,
                                                        b="b",
                                                        S="S", o=tumor_bam,
                                                        threads=args.threadN)
    tumor_samtools_cmd()

    # sort bam
    print("Executing Tumor Sort bam Command Line")
    tumor_sorted_bam = os.path.join(tmpPATH, "tumor_sorted.bam")
    tumor_sorted_cmd = SortBam_Commandline(threads=args.threadN,
                                           o=tumor_sorted_bam,
                                           i=tumor_bam)
    tumor_sorted_cmd()

    print("Executing Tumor Index sorted bam Command Line")
    tumor_index_sorted_bam = os.path.join(tmpPATH, "tumor_sorted.bai")
    tumor_index_cmd = IndexBam_Commandline(threads=args.threadN,
                                           i=tumor_sorted_bam,
                                           o=tumor_index_sorted_bam)
    tumor_index_cmd()

    return tumor_sorted_bam


def sam_part_tumor(args, tmpPATH):

    print("Executing Tumor SAM2BAM Command Line")
    tumor_input = args.tumor_sam
    tumor_bam = os.path.join(tmpPATH, "tumor.bam")

    tumor_samtools_cmd = SamtoolsViewCommandline_thread(input=tumor_input,
                                                        b="b",
                                                        S="S", o=tumor_bam,
                                                        threads=args.threadN)
    tumor_samtools_cmd()

    # sort bam
    print("Executing Tumor Sort bam Command Line")
    tumor_sorted_bam = os.path.join(tmpPATH, "tumor_sorted.bam")
    tumor_sorted_cmd = SortBam_Commandline(threads=args.threadN,
                                           o=tumor_sorted_bam,
                                           i=tumor_bam)
    tumor_sorted_cmd()

    print("Executing Tumor Index sorted bam Command Line")
    tumor_index_sorted_bam = os.path.join(tmpPATH, "tumor_sorted.bai")
    tumor_index_cmd = IndexBam_Commandline(threads=args.threadN,
                                           i=tumor_sorted_bam,
                                           o=tumor_index_sorted_bam)
    tumor_index_cmd()

    return tumor_sorted_bam
