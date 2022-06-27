import os
from seq2neo.function.Mutation_Calling import *


def toVCF_mutect2(args, tmpPATH, resultsPATH):
    f1r2_gz_file = os.path.join(tmpPATH, "f1r2.tar.gz")
    input = [os.path.join(tmpPATH, 'tumor_BQSR.bam'), os.path.join(tmpPATH, "normal_BQSR.bam")]
    normal_name = args.normal_name
    out = os.path.join(tmpPATH, "somatic.vcf")
    germline_resource = os.path.join(args.mutect2_dataset_dir, "af-only-gnomad.hg38.vcf.gz")  # 生殖突变

    print("Executing Mutect2 Command Line")
    mutect2_cmd = Mutect2Commandline(ref=args.ref,
                                     Input=input,
                                     Output=out,
                                     f1r2_gz_file=f1r2_gz_file,
                                     Normal_name=normal_name,
                                     threads=args.threadN,
                                     java_options=args.java_options,
                                     germline_resource=germline_resource)

    mutect2_cmd.run_mutect2()

    # GetPileupSummaries
    interval_list = os.path.join(args.mutect2_dataset_dir, "small_exac_common_3.hg38.vcf.gz")
    V = os.path.join(args.mutect2_dataset_dir, "small_exac_common_3.hg38.vcf.gz")
    # tumor GetPileupSummaries
    O = os.path.join(tmpPATH, "tumor.pileups.table")

    print("Executing tumor GetPileupSummaries Command Line")
    tumor_GetPileupSummaries_cmd = GetPileupSummariesCommandline(
        I=input[0],
        L=interval_list,
        V=V,
        O=O,
        java_options=args.java_options
    )
    tumor_GetPileupSummaries_cmd()

    # normal GetPileupSummaries
    normal_pileup = os.path.join(tmpPATH, "normal.pileups.table")

    print("Executing normal GetPileupSummaries Command Line")
    normal_GetPileupSummaries_cmd = GetPileupSummariesCommandline(
        I=input[1],
        L=interval_list,
        V=V,
        O=normal_pileup,
        java_options=args.java_options
    )
    normal_GetPileupSummaries_cmd()

    # CalculateContamination
    output_table = os.path.join(tmpPATH, "contamination.table")

    print("Executing CalculateContamination Command Line")
    CalculateContamination_cmd = CalculateContaminationCommandline(
        I=O,
        matched=normal_pileup,
        O=output_table,
        java_options=args.java_options
    )
    CalculateContamination_cmd()

    # LearnReadOrientationModel
    prior_file = os.path.join(tmpPATH, "tumor-artifact-prior.tar.gz")

    print("Executing LearnReadOrientationModel Command Line")
    LearnReadOrientationModel_cmd = LearnReadOrientationModelCommandline(
        I=f1r2_gz_file,
        O=prior_file,
        java_options=args.java_options
    )
    LearnReadOrientationModel_cmd()

    # Filter mutations
    filtered_vcf = os.path.join(tmpPATH, "filtered.vcf")

    print("Executing Filter mutations Command Line")
    filter_cmd = FilterMutectCallsCommandline(
        R=args.ref,
        V=out,
        O=filtered_vcf,
        contamination=output_table,
        ob_priors=prior_file,
        java_options=args.java_options
    )
    filter_cmd()

    # Select PASS
    out = os.path.join(resultsPATH, "pass")

    print("Executing Select PASS Command Line")
    select_cmd = SelectPassMutationCommandline(
        remove_filtered_all="remove-filtered-all",
        vcf=filtered_vcf,
        out=out,
        recode="recode",
    )
    select_cmd()
