import os
import subprocess as sp
from seq2neo.function.GATK_Best_Practice import SortBam_Commandline, IndexBam_Commandline
from seq2neo.function.TPMCalculator import TPMCalculatorCommandLine


def tpm_calculation(args, tmpPATH, resultsPATH):

    print("Executing RNA Sort bam Command Line")
    starfusion_out = os.path.join(tmpPATH, 'star_fusion_outdir')
    rna_unsorted_bam = os.path.join(starfusion_out, 'Aligned.out.bam')
    rna_sorted_bam = os.path.join(starfusion_out, "Aligned.out.sorted.bam")
    rna_sorted_cmd = SortBam_Commandline(threads=args.threadN,
                                         o=rna_sorted_bam,
                                         i=rna_unsorted_bam)
    rna_sorted_cmd()

    print("Executing RNA Index sorted bam Command Line")
    rna_index_sorted_bam = os.path.join(starfusion_out, "Aligned.out.sorted.bai")
    rna_index_cmd = IndexBam_Commandline(threads=args.threadN,
                                         i=rna_sorted_bam,
                                         o=rna_index_sorted_bam)
    rna_index_cmd()

    print("Executing TPMCalculator Command Line")
    gtf_file = os.path.join(args.genome_lib_dir, 'ref_annot.gtf')
    output = os.path.join(resultsPATH, 'tpm.log')
    tpm_cal_cmd = TPMCalculatorCommandLine(g=gtf_file,
                                           b=rna_sorted_bam,
                                           k='gene_name',
                                           c=args.mrna,
                                           p="p")
    tpm_cal_cmd(stdout=output, stderr=output)
    os.remove(output)  # 删除日志文件，太大了

    # 将文件移动到resultsPATH
    workdir = os.getcwd()
    files = os.path.join(workdir, 'Aligned.out.sorted_genes.*')
    mv_cmd = 'mv %s %s' % (files, resultsPATH)
    sp.check_call(mv_cmd, shell=True)
