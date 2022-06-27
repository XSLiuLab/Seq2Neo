import sys
import pandas as pd
from seq2neo.lib import *
from seq2neo.function.immuno_Prediction import *


def define_parser():
    return ImmunoArgumentParser().parser


def main(args_input=None):
    if args_input is None:
        args_input = sys.argv[1:]
    parser = define_parser()
    args = parser.parse_args(args_input)

    # 判断模式
    mode = args.mode
    if mode == 'single':
        print("mode is single")
        epitope = args.epitope
        print("queried epitope is {}".format(epitope))
        hla = args.hla
        print("queried hla is {}".format(hla))
        # 计算IC50和TAP
        IC50 = single_cal(args, "ic50")
        TAP = single_cal(args, "tap")
        score = computing_sigle(epitope, hla, IC50, TAP)
        print("The immunogenicity score of the peptide is", score[0, 0])
    elif mode == 'multiple':
        print("mode is multiple")
        print("input file is {}".format(args.inputfile))
        outFolder = args.outdir
        print("output file will be in {}".format(outFolder))
        # 处理数据得到IC50和TAP
        inputFile = mutiple_cal(args)
        input_df = pd.read_csv(inputFile)
        file_process(input_df, outFolder)
        print("Running successfully, thanks for using Seq2Neo!!!")
