import os
import subprocess as sp
from seq2neo.function.Mutation_Calling import *


def toVCF_mutect2(args, tmpPATH, resultsPATH):
    f1r2_gz_file = os.path.join(tmpPATH, "f1r2.tar.gz")
    normal_name = args.normal_name
    
    if normal_name:
        input = [os.path.join(tmpPATH, 'tumor_BQSR.bam'), os.path.join(tmpPATH, "normal_BQSR.bam")]
    else:
        input = [os.path.join(tmpPATH, 'tumor_BQSR.bam')]
    
    print("Executing Mutect2 Command Line")
    out = os.path.join(tmpPATH, "somatic.vcf")
    germline_resource = os.path.join(args.mutect2_dataset_dir, "af-only-gnomad.hg38.vcf.gz")  # 生殖突变
    mutect2_cmd = Mutect2Commandline(ref=args.ref,
                                     Input=input,
                                     Output=out,
                                     f1r2_gz_file=f1r2_gz_file,
                                     Normal_name=normal_name,
                                     threads=args.threadN,
                                     java_options=args.java_options,
                                     germline_resource=germline_resource,
                                     pon=args.pon)
    mutect2_cmd.run_mutect2()

    # GetPileupSummaries
    interval_list = os.path.join(args.mutect2_dataset_dir, "small_exac_common_3.hg38.vcf.gz")
    V = os.path.join(args.mutect2_dataset_dir, "small_exac_common_3.hg38.vcf.gz")
    
    # tumor GetPileupSummaries
    print("Executing tumor GetPileupSummaries Command Line")
    O = os.path.join(tmpPATH, "tumor.pileups.table")
    tumor_GetPileupSummaries_cmd = GetPileupSummariesCommandline(
        I=input[0],
        L=interval_list,
        V=V,
        O=O,
        java_options=args.java_options)
    tumor_GetPileupSummaries_cmd()

    # normal GetPileupSummaries
    if normal_name:
        normal_pileup = os.path.join(tmpPATH, "normal.pileups.table")
        print("Executing normal GetPileupSummaries Command Line")
        normal_GetPileupSummaries_cmd = GetPileupSummariesCommandline(
            I=input[1],
            L=interval_list,
            V=V,
            O=normal_pileup,
            java_options=args.java_options)
        normal_GetPileupSummaries_cmd()

    # CalculateContamination
    print("Executing CalculateContamination Command Line")
    output_table = os.path.join(tmpPATH, "contamination.table")
    if normal_name:
        CalculateContamination_cmd = CalculateContaminationCommandline(
            I=O,
            matched=normal_pileup,
            O=output_table,
            java_options=args.java_options)
    else:
        CalculateContamination_cmd = CalculateContaminationCommandline(
            I=O,
            O=output_table,
            java_options=args.java_options)
    CalculateContamination_cmd()

    # LearnReadOrientationModel
    print("Executing LearnReadOrientationModel Command Line")
    prior_file = os.path.join(tmpPATH, "tumor-artifact-prior.tar.gz")
    LearnReadOrientationModel_cmd = LearnReadOrientationModelCommandline(
        I=f1r2_gz_file,
        O=prior_file,
        java_options=args.java_options)
    LearnReadOrientationModel_cmd()

    # Filter mutations
    print("Executing Filter mutations Command Line")
    filtered_vcf = os.path.join(tmpPATH, "filtered.vcf")
    filter_cmd = FilterMutectCallsCommandline(
        R=args.ref,
        V=out,
        O=filtered_vcf,
        contamination=output_table,
        ob_priors=prior_file,
        java_options=args.java_options)
    filter_cmd()

    # Select PASS
    print("Executing Select PASS Command Line")
    out = os.path.join(resultsPATH, "pass")
    select_cmd = SelectPassMutationCommandline(
        remove_filtered_all="remove-filtered-all",
        vcf=filtered_vcf,
        out=out,
        recode="recode")
    select_cmd()

    # norm
    print("Executing Norm VCF Command Line")
    unnorm_vcf = os.path.join(resultsPATH, 'pass.recode.vcf')
    norm_vcf = os.path.join(resultsPATH, 'pass.recode.norm.vcf')
    norm_cmd = "cat %s | \
                bcftools norm --multiallelics -both --output-type v - | \
                bcftools norm --fasta-ref %s --output-type v - > %s" % (unnorm_vcf, args.ref, norm_vcf)
    sp.check_call(norm_cmd, shell=True)
