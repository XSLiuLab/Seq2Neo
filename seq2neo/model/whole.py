import sys
import os
from seq2neo.lib import *


def define_parser():
    return WholeArgumentParser().parser


def main(args_input=None):
    if args_input is None:
        args_input = sys.argv[1:]
    parser = define_parser()
    args = parser.parse_args(args_input)

    os.makedirs(args.out, exist_ok=True)
    tmpPATH = os.path.join(args.out, "tmp")
    resultsPATH = os.path.join(args.out, "results")
    os.makedirs(tmpPATH, exist_ok=True)
    os.makedirs(resultsPATH, exist_ok=True)

    # DNA-seq数据处理
    toBAM_dna_normal(args, tmpPATH, resultsPATH)
    toBAM_dna_tumor(args, tmpPATH)
    toVCF_mutect2(args, tmpPATH, resultsPATH)
    toFasta_annovar(args, resultsPATH)

    # RNA-seq数据处理
    toGeneFusion_rna(args, tmpPATH, resultsPATH)
    tpm_calculation(args, tmpPATH, resultsPATH)

    # 数据预测，整合处理
    agfusion_dir = os.path.join(resultsPATH, 'agfusion_dir')
    filepath = os.path.join(resultsPATH, "neo")
    finalPATH = os.path.join(args.out, "final_result")
    os.makedirs(finalPATH, exist_ok=True)  # 创建存储最终文件的文件夹

    binding_Prediction(args, resultsPATH)
    binding_Prediction_fusion(args, agfusion_dir, resultsPATH)
    Integration(inputdir=filepath, outdir=filepath)  # 整合转换
    immunoPrediction(resultsPATH)
    filterNeo(finalPATH, resultsPATH)  # 筛选预测的新抗原

    print("Running successfully, thanks for using Seq2Neo!!!")


if __name__ == '__main__':
    main()
