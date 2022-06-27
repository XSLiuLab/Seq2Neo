import os
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

from seq2neo.function.Neoantigen_Prediction import *
from ._toTable import GettingHLA, Integration_tpm
from seq2neo.function.immuno_Prediction import *
from seq2neo.function.Neoantigen_Prediction import MakePeptideFasta_fusion


def binding_Prediction(args, resultsPATH):
    pool = ProcessPoolExecutor(max_workers=4)
    # 建立一个neo文件夹，存放预测结果
    filepath = os.path.join(resultsPATH, "neo")
    os.makedirs(filepath, exist_ok=True)

    print("Making binding & tap prediction")
    sample_id = args.tumor_name

    # 暂时只采用NetMHCpan
    method = ["NetMHCpan"]

    if args.data_type == "fastq":
        hlas = GettingHLA(os.path.join(resultsPATH, '%s_final.result.txt' % args.tumor_name))  # 获取并解析HLAHD的分型结果
    else:
        hlas = args.hla

    print("HLAs are %s" % hlas)  # 显示样本的HLA信息

    for l in args.len:
        pool.submit(mutiProcessor_Prediction, l, hlas, resultsPATH, args.tumor_name, filepath, sample_id, method)
    pool.shutdown()  # 等待，直到子进程执行完毕


def binding_Prediction_fusion(args, agfusion_dir, resultsPATH):  # 预测genefusion的免疫原型并整合

    MakePeptideFasta_fusion(args, agfusion_dir, resultsPATH)  # 处理gene fusion并提取突变肽

    # 预测binding & tap
    print("Making binding & tap prediction (gene fusion)")
    filepath = os.path.join(resultsPATH, "neo")
    os.makedirs(filepath, exist_ok=True)

    pool = ProcessPoolExecutor(max_workers=4)  # 创建进程池
    sample_id = args.tumor_name

    # 暂时只采用NetMHCpan
    method = ["NetMHCpan"]

    if args.data_type == "fastq":
        hlas = GettingHLA(os.path.join(resultsPATH, '%s_final.result.txt' % args.tumor_name))  # 获取并解析HLAHD的分型结果
    else:
        hlas = args.hla

    for l in args.len:
        pool.submit(mutiProcessor_Prediction_fusion, l, hlas, resultsPATH, args.tumor_name, filepath, sample_id,
                    method)
    pool.shutdown()


def immunoPrediction(resultsPATH):  # 预测免疫原性并整合

    print("Making Immunogenicity prediction")

    filepath = os.path.join(resultsPATH, 'neo/combination_mhci_tap.csv')
    df = pd.read_csv(filepath)

    df1 = df.loc[:, ["Peptide", "HLA", "IC50", "TAP"]]
    df1.rename(columns={'Peptide': 'Pep'}, inplace=True)

    file_process(input_df=df1, outdir=os.path.join(resultsPATH, 'neo'))

    df2 = pd.read_csv(os.path.join(resultsPATH, 'neo/cnn_results.csv'))

    df3 = pd.concat([df, df2["immunogenicity"]], axis=1)  # 横向合并（顺序一致）
    df3.to_csv(os.path.join(resultsPATH, 'neo/all.csv'), index=False, encoding='utf-8')


def filterNeo(finalPATH, resultsPATH):
    print("Making Neoantigen Filtering")

    final_file = os.path.join(finalPATH, 'filtered_neo.txt')  # 筛选过后的新抗原

    final_df = Integration_tpm(finalPATH, resultsPATH)  # 获取未经过滤的结果

    # 过滤条件，TAP>0, immunogenicity>0.5, TPM>0, 按照IC50排序
    final_df = final_df[final_df.TAP > 0]
    final_df = final_df[final_df.immunogenicity > 0.5]
    final_df = final_df[final_df.TPM > 0]
    final_df = final_df[final_df.IC50 <= 500]
    final_df = final_df.sort_values(by="IC50", ascending=True)

    final_df.to_csv(final_file, index=False, encoding="utf-8")


def mutiProcessor_Prediction(l, hlas, resultsPATH, tumor_name, filepath, sample_id, method):
    length = [l]
    Input_file = {'tmp' + '_' + str(l): os.path.join(resultsPATH, "%s_tmp_%s.fasta" % (tumor_name, l)),
                  'tmpindel' + '_' + str(l): os.path.join(resultsPATH, "%s_tmpindel_%s.fasta" % (tumor_name, l))}
    predict_binding_affinity(filepath=filepath,
                             Input_file=Input_file,
                             sample_name=sample_id,
                             methods=method,
                             hlas=hlas,
                             length=length,
                             cla="classI")

    predict_TAP(filepath=filepath, Input_file=Input_file, sample_name=sample_id, hlas=hlas, length=length)


def mutiProcessor_Prediction_fusion(l, hlas, resultsPATH, tumor_name, filepath, sample_id, method):
    length = [l]
    Input_file = {
        'tmpgenefusion' + '_' + str(l): os.path.join(resultsPATH, "%s_tmpgenefusion_%s.fasta" % (tumor_name, l))}
    predict_binding_affinity(filepath=filepath,
                             Input_file=Input_file,
                             sample_name=sample_id,
                             methods=method,
                             hlas=hlas,
                             length=length,
                             cla="classI")

    predict_TAP(filepath=filepath, Input_file=Input_file, sample_name=sample_id, hlas=hlas, length=length)
