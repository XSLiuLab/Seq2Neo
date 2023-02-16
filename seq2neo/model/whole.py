import sys
import os
from seq2neo.lib import *


def define_parser():
    return WholeArgumentParser().parser


# 定义规则
def define_rules(args):
    if args.data_type == 'fastq':
        if not (args.normal_dna and args.tumor_dna and args.tumor_rna and args.normal_name):
            print("need files or normal name lost")
            sys.exit(-1)
    if args.data_type == 'sam':
        if not (args.normal_sam and args.tumor_sam and args.tumor_rna and args.normal_name):
            print("need files or normal name lost")
            sys.exit(-1)
        if not args.hlas:
            print("--hlas missed")
            sys.exit(-1)
    if args.data_type == 'sort_bam':
        if not (args.normal_sorted_bam and args.tumor_sorted_bam and args.tumor_rna and args.normal_name):
            print("need files or normal name lost")
            sys.exit(-1)
        if not args.hlas:
            print("--hlas missed")
            sys.exit(-1)
    
    if args.data_type == 'without-normal-dna':
        if not (args.tumor_dna and args.tumor_rna):
            print("need files lost")
            sys.exit(-1)
        if args.normal_name:
            print("do not provide normal-name")
            sys.exit(-1)
    if args.data_type == 'without-tumor-rna':
        if not (args.tumor_dna and args.normal_dna and args.normal_name):
            print("need files or normal name lost")
            sys.exit(-1)
    if args.data_type == 'only-tumor-dna':
        if not args.tumor_dna:
            print("need files lost")
            sys.exit(-1)
        if args.normal_name:
            print("do not provide normal-name")
            sys.exit(-1)
    
    if args.data_type == 'vcf':
        if not (args.vcf and args.hlas):
            print("need vcf and hlas")
            sys.exit(-1)
        if args.normal_name:
            print("do not provide normal-name")
            sys.exit(-1)
    return None     


def checkHLA(file: str):
    hlas = GettingHLA(file)
    print(f"HLAs are {hlas}")
    if len(hlas) == 0:
        print("The result of HLAHD is error!")
        sys.exit(-1)


def main(args_input=None):
    if args_input is None:
        print("No argument specified!")
        sys.exit(-1)
    
    parser = define_parser()
    args = parser.parse_args(args_input)
    
    # 检查参数设置情况
    define_rules(args)

    # 创建 tmp 和 results 文件夹
    os.makedirs(args.out, exist_ok=True)
    tmpPATH = os.path.join(args.out, "tmp")
    resultsPATH = os.path.join(args.out, "results")
    os.makedirs(tmpPATH, exist_ok=True)
    os.makedirs(resultsPATH, exist_ok=True)

    if args.data_type != 'vcf':
        hlahd_file = os.path.join(resultsPATH, '%s_final.result.txt' % args.tumor_name)
        # DNA-seq数据处理
        if args.normal_name:
            toBAM_dna_normal(args, tmpPATH, resultsPATH)
            if args.data_type not in ['sam', 'sort_bam', 'vcf'] and args.hlas is None:  # 检查下HLAHD是否call出结果
                checkHLA(hlahd_file)
        toBAM_dna_tumor(args, tmpPATH, resultsPATH)
        if args.data_type not in ['sam', 'sort_bam', 'vcf'] and args.hlas is None:
            checkHLA(hlahd_file)
        toVCF_mutect2(args, tmpPATH, resultsPATH)

    # 对vcf进行注释，并提取neoantigens
    toFasta_annovar(args, resultsPATH)

    # RNA-seq数据处理
    if args.data_type not in ['without-tumor-rna', 'only-tumor-dna', 'vcf']:
        toGeneFusion_rna(args, tmpPATH, resultsPATH)
        tpm_calculation(args, tmpPATH, resultsPATH)
    else:
        print("Ignoring Tumore RNA, gene-fusion based neoantigens and expression info will be removed.")

    # 数据预测，整合处理
    filepath = os.path.join(resultsPATH, "neo")
    finalPATH = os.path.join(args.out, "final_result")
    os.makedirs(finalPATH, exist_ok=True)  # 创建存储最终结果的文件夹

    # 执行最终预测
    # 对SNV和Indel进行预测
    binding_Prediction(args, resultsPATH)
    if args.data_type not in ['without-tumor-rna', 'only-tumor-dna', 'vcf']:
        # 对Gene Fusion进行预测
        agfusion_dir = os.path.join(resultsPATH, 'agfusion_dir')
        binding_Prediction_fusion(args, agfusion_dir, resultsPATH)
    Integration(inputdir=filepath, outdir=filepath)  # 整合转换
    immunoPrediction(resultsPATH)
    filterNeo(args, finalPATH, resultsPATH)  # 筛选预测的新抗原

    print("Running successfully, thanks for using Seq2Neo!!!")


if __name__ == '__main__':
    main()
