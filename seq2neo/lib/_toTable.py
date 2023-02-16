"""
convert raw results to standard tables
"""
import os
import sys
import math
import pandas as pd
import numpy as np
from bisect import bisect_left
from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)


def NetMHCpanconvert(filename, outdir):
    with open(filename, "r") as f:
        lines = f.readlines()  # 会读入末尾的换行符
        n = 0
        info = []
        for l in lines:
            if l.startswith("#") or l.startswith("---") or len(l) == 1:
                continue
            elif "Aff" in l and n == 0:
                header = ",".join(l.split()[:-1]) + '\n'
                n = n + 1
            elif l.split()[0].isdigit():
                if l.endswith("B\n"):
                    l = ",".join(l.split()[:-2])
                    info.append(l + '\n')
                else:
                    l = ",".join(l.split())
                    info.append(l + '\n')

    path = os.path.join(outdir, os.path.basename(filename))

    with open(path, "w") as result:
        result.write(header)
        for l in info:
            result.write(l)


def PickPocketconvert(filename, outdir):
    with open(filename, "r") as f:
        lines = f.readlines()
        n = 0
        info = []
        for l in lines:
            if l.startswith("#") or l.startswith("---") or len(l) == 1:
                continue
            elif "1-log50k(aff)" in l and n == 0:
                tmp = l.split()[:-1]
                tmp.append("affinity")
                header = ",".join(tmp) + '\n'
                n = n + 1
            elif l.split()[0].isdigit():
                logaff = float(l.split()[-1])
                aff = str(math.pow(50000, 1 - logaff))
                tmp = l.split()[:-1]
                tmp.append(aff)
                l = ",".join(tmp)
                info.append(l + '\n')

    path = os.path.join(outdir, os.path.basename(filename))

    with open(path, "w") as result:
        result.write(header)
        for l in info:
            result.write(l)


def NetMHCIIconvert(filename, outdir):
    with open(filename, "r") as f:
        lines = f.readlines()
        n = 0
        info = []
        for l in lines:
            if l.startswith("#") or l.startswith("---") or len(l) == 1:
                continue
            elif "affinity(nM)" in l and n == 0:
                header = ",".join(l.split()[:-2]) + '\n'
                n = n + 1
            elif l.split()[1].isdigit():
                if l.endswith("B\n"):
                    l = ",".join(l.split()[:-1])
                    info.append(l + '\n')
                else:
                    l = ",".join(l.split())
                    info.append(l + '\n')

    path = os.path.join(outdir, os.path.basename(filename))

    with open(path, "w") as result:
        result.write(header)
        for l in info:
            result.write(l)


def MixMHC2predconvert(filename, outdir):
    with open(filename, "r") as f:
        lines = f.readlines()
        info = []
        for l in lines:
            if l.startswith("#"):
                continue
            else:
                l = ",".join(l.split())
                info.append(l + '\n')

    path = os.path.join(outdir, os.path.basename(filename))

    with open(path, "w") as result:
        for l in info:
            result.write(l)


def NetCTLpanconvert(filename, outdir):
    with open(filename, "r") as f:
        lines = f.readlines()  # 会读入末尾的换行符
        info = []
        for l in lines:
            if l.startswith("#") or l.startswith("---") or len(l) == 1:
                continue
            elif l.split()[0].isdigit():
                if l.endswith("E\n"):
                    l = ",".join(l.split()[:-1])
                    info.append(l + '\n')
                else:
                    l = ",".join(l.split())
                    info.append(l + '\n')

    path = os.path.join(outdir, os.path.basename(filename))

    with open(path, "w") as result:
        result.write("N,Sequence Name,Allele,Peptide,MHC,TAP,Cle,Comb,%Rank" + '\n')
        for l in info:
            result.write(l)


def Integration(inputdir, outdir):
    mhci = os.path.join(inputdir, "mhci")
    df1 = pd.DataFrame(columns=['MHC', 'Peptide', 'Aff(nM)'])  # 首先赋值空值待用
    tap = os.path.join(inputdir, "tap")
    df2 = pd.DataFrame(columns=["Sequence Name", "Allele", "Peptide", "TAP"])

    for _, __, files in os.walk(mhci):  # 调用os.listdir()，返回文件列表的顺序是任意的
        for file in sorted(files):  # 将文件排序
            if os.path.getsize(os.path.join(mhci, file)) < 200:  # 文件为空，代表MHC不存在于软件中
                HLA = file.split('_')[6].split('.')[0]
                print(f'{HLA} is not in netMHCpan, will be ignored')
                continue
            df = pd.read_csv(os.path.join(mhci, file))
            df = df.loc[:, ['MHC', 'Peptide', 'Aff(nM)']]
            df1 = pd.concat([df1, df], axis=0, ignore_index=True)

    for _, __, files in os.walk(tap):
        for file in sorted(files):
            if os.path.getsize(os.path.join(tap, file)) < 200:
                HLA = file.split('_')[6].split('.')[0]
                print(f'{HLA} is not in netCTLpan, will be ignored')
                continue
            df = pd.read_csv(os.path.join(tap, file))
            df = df.loc[:, ["Sequence Name", "Allele", "Peptide", "TAP"]]
            df2 = pd.concat([df2, df], axis=0, ignore_index=True)
    
    if df1.size == 0 or df2.size == 0:
        print("There is nothing, seq2neo will be end!!!")
        sys.exit(-1)

    df3 = pd.concat([df2, df1['Aff(nM)']], axis=1)
    df3.columns = ["line", "HLA", "Peptide", "TAP", "IC50"]
    df3.HLA = df3.HLA.apply(lambda x: x.replace('*', '', 1))  # HLA列去除’*‘

    result1 = os.path.join(outdir, "mhci.csv")
    result2 = os.path.join(outdir, "tap.csv")
    result3 = os.path.join(outdir, "combination_mhci_tap.csv")

    df1.to_csv(result1, index=False, encoding="utf-8")
    df2.to_csv(result2, index=False, encoding="utf-8")
    df3.to_csv(result3, index=False, encoding="utf-8")


def Integration_tpm(args, finalPATH, resultsPATH):

    if args.data_type not in ['without-tumor-rna', 'only-tumor-dna', 'vcf']:
        have_tumor_rna = True
        # 读入TPM
        tpm_file = os.path.join(resultsPATH, 'Aligned.out.sorted_genes.ent')
        tpm_df = pd.read_csv(tpm_file, sep="\t")
        tpm_df = tpm_df.loc[:, ["Gene_Id", "start", "end", "TPM", "Type"]]
        tpm_df.columns = ["GeneName", "start", "end", "TPM", "Type"]
        
        # 读入gene fusion字典
        dictionary_fusion = os.path.join(resultsPATH, 'dictionary_fusion.txt')
        dic_fusion_df = pd.read_csv(dictionary_fusion)
    else:
        have_tumor_rna = False

    # 读入snv和indels字典
    dictionary = os.path.join(resultsPATH, 'dictionary.txt')
    dic_df = pd.read_csv(dictionary)
    dic_df.drop('Alias', axis=1, inplace=True)  # 只删除Alias列，保留其它列

    # 读入之前整合的文件，准备加入TPM和其它信息
    neopeptides = os.path.join(resultsPATH, 'neo/all.csv')
    neopeptides_df = pd.read_csv(neopeptides)
    neopeptides_df["length"] = neopeptides_df.Peptide.str.len()  # 增加一列，得出字符串的长度

    # 读入mrna字典和mt_wt字典
    dictionary_mrna = os.path.join(resultsPATH, 'dictionary_mrna.txt')
    dictionary_mt_wt = os.path.join(resultsPATH, 'dictionary_wt_mt.txt')
    dic_mrna_df = pd.read_csv(dictionary_mrna)
    dic_mt_wt_df = pd.read_csv(dictionary_mt_wt)
    dic_mrna_mt_wt_df = pd.merge(dic_mt_wt_df, dic_mrna_df, how="inner", on=["line", "length"])  # 合并成新字典
    dic_mrna_mt_wt_df.drop(["isFrameShift_x", "isFrameShift_y"], axis=1, inplace=True)  # 去除无用的列

    if have_tumor_rna:
        # 将gene fusion和snv/indel区分开，便于后续操作
        series_mask = neopeptides_df.line.str.startswith('line')  # str属性可以对字符串列以向量化的方式处理
        mask = list(series_mask)
        rmask = list(series_mask == False)
        snv_indel_df = neopeptides_df[mask]  # 挑选snv_indel的数据
        fusion_df = neopeptides_df[rmask]  # 挑选gene fusion的数据；没有gene fusion的数据时，为空数据框
    else:
        snv_indel_df = neopeptides_df

    if have_tumor_rna:
        # 读入处理后的tpm_df
        tpm_new_df = GettingTPM(dic_df, dic_fusion_df, tpm_df, resultsPATH)

    # 为snv_indel_df补充信息
    snv_indel_new_df = pd.merge(snv_indel_df, dic_df, how="inner", on="line")
    if have_tumor_rna:
        snv_indel_new_df = pd.merge(snv_indel_new_df, tpm_new_df, how="inner", on=["line", "GeneName"])
    snv_indel_new_df = pd.merge(snv_indel_new_df, dic_mrna_mt_wt_df, how="inner", on=["line", "length"])
    snv_indel_new_df.pop("line")

    if have_tumor_rna:
        # 为gene fusion补充信息，两个基因的平均TPM
        fusion_df.rename(columns={'line': 'GeneName'}, inplace=True)
        fusion_new_df = pd.merge(fusion_df, tpm_new_df, how="inner", on="GeneName")
        fusion_new_df.rename(columns={'line': 'influence'}, inplace=True)  # line包含gene fusion 是out-of-frame还是in-frame
        fusion_new_df["amino_change"] = "###"
        fusion_new_df["mutation_type"] = "Gene Fusion"
        fusion_new_df["chr"] = "###"  # 暂时将这些设为未知
        fusion_new_df["ref"] = "###"
        fusion_new_df["mut"] = "###"
        fusion_new_df["location"] = "###"
        fusion_new_df["mtseq"] = "###"
        fusion_new_df["wtseq"] = "###"
        fusion_new_df["mt_mrna_seq"] = "###"
        fusion_new_df["wt_mrna_seq"] = "###"

    # 调整列的顺序，合并输出
    if have_tumor_rna:
        snv_indel_new_df = snv_indel_new_df.loc[:, ["HLA", "Peptide", "length", "TAP", "IC50", "immunogenicity",
                                                    "TPM", "GeneName", "amino_change", "influence", "mutation_type",
                                                    "chr", "ref", "mut", "location", "mtseq", "wtseq", "mt_mrna_seq",
                                                    "wt_mrna_seq"]]
        fusion_new_df = fusion_new_df.loc[:, ["HLA", "Peptide", "length", "TAP", "IC50", "immunogenicity",
                                              "TPM", "GeneName", "amino_change", "influence", "mutation_type",
                                              "chr", "ref", "mut", "location", "mtseq", "wtseq", "mt_mrna_seq",
                                              "wt_mrna_seq"]]
        final_df = pd.concat([snv_indel_new_df, fusion_new_df], axis=0, ignore_index=True)  # 合并
    else:
        snv_indel_new_df = snv_indel_new_df.loc[:, ["HLA", "Peptide", "length", "TAP", "IC50", "immunogenicity",
                                                    "GeneName", "amino_change", "influence", "mutation_type",
                                                    "chr", "ref", "mut", "location", "mtseq", "wtseq", "mt_mrna_seq",
                                                    "wt_mrna_seq"]]
        final_df = snv_indel_new_df
    
    final_df.to_csv(os.path.join(finalPATH, 'final_results_neo.csv'), index=False, encoding="utf-8")  # 保存
    return final_df


def GettingTPM(dic_df, dic_fusion_df, tpm_df, resultsPATH):
    tpm_new_df = pd.DataFrame(columns=["line", "GeneName", "TPM"])  # 创建一个字典便于使用

    dic_df = dic_df.loc[:, ["line", "GeneName", "location"]]  # 后续依赖于这三列的信息

    for i in range(0, dic_df.shape[0]):
        line = list(dic_df.iloc[i, :])  # 获取当前行
        loc = int(line[2])  # 获取当前gene的突变位置
        mask = list(map(lambda x: str(x) == line[1], list(tpm_df.GeneName)))
        tmp_df = tpm_df[mask]  # 取得中间df用于计算
        # 按行循环tmp_df，找出需要的外显子对应的TPM值
        if tmp_df.shape[0] == 0:
            row = pd.Series({'line': line[0], 'GeneName': line[1], 'TPM': 0.0})  # 如果gene不存在于tpm_df中，直接将TPM设为0
            tpm_new_df = tpm_new_df.append(row, ignore_index=True)
        else:
            for c in range(0, tmp_df.shape[0]):
                new_line = list(tmp_df.iloc[c, :])  # 获取当前行
                zone = new_line[1:3]
                if bisect_left(zone, loc) == 1 or loc == zone[0]:  # 检测loc是否位于zone内，是的话返回1
                    row = pd.Series({'line': line[0], 'GeneName': new_line[0], 'TPM': new_line[3]})
                    tpm_new_df = tpm_new_df.append(row, ignore_index=True)
                    break  # 只要检测到一个外显子符合，就终止当前循环

    for i in range(0, dic_fusion_df.shape[0]):
        fusion_gene = str(dic_fusion_df.iloc[i, 0])
        fusion_type = str(dic_fusion_df.iloc[i, 2])  # 是out-of-frame，还是in-frame
        genes = fusion_gene.split('_')  # 获取融合基因列表

        mask1 = list(map(lambda x: str(x) == genes[0], list(tpm_df.GeneName)))
        tmp1_df = tpm_df[mask1]
        mask2 = list(map(lambda x: str(x) == 'exon', list(tmp1_df.Type)))
        tpm1_exon_df = tmp1_df[mask2]
        if not np.isnan(np.mean(tpm1_exon_df.TPM)):
            tpm1 = np.mean(tpm1_exon_df.TPM)
        else:
            tpm1 = 0

        mask3 = list(map(lambda x: str(x) == genes[1], list(tpm_df.GeneName)))
        tmp2_df = tpm_df[mask3]
        mask4 = list(map(lambda x: str(x) == 'exon', list(tmp2_df.Type)))
        tpm2_exon_df = tmp2_df[mask4]
        if not np.isnan(np.mean(tpm2_exon_df.TPM)):
            tpm2 = np.mean(tpm2_exon_df.TPM)
        else:
            tpm2 = 0

        row = pd.Series({'line': fusion_type, 'GeneName': fusion_gene, 'TPM': np.mean([tpm1, tpm2])})
        tpm_new_df = tpm_new_df.append(row, ignore_index=True)

    # 写入文件保存
    tpm_new_df.to_csv(os.path.join(resultsPATH, 'dictionary_tpm.txt'), index=False)

    return tpm_new_df


def GettingHLA(filepath: str):
    with open(filepath, 'r') as f:
        contents = f.readlines()[0:3]  # 只考虑I类MHC
        mhci = []
        for mhcs in contents:
            tmp = mhcs.split()[1:3]  # 考虑可能性最大的
            for mhc in tmp:
                if mhc.startswith('HLA'):
                    mhc = mhc.replace('*', '')
                    mhc = mhc[0:10]  # 精度为2位
                    mhci.append(mhc)
                else:
                    continue

    mhci_final = []  # 最终返回的HLA列表
    # 去除pipeline中不存在的HLA
    print("Removing HLAs not exsiting in Seq2Neo pipeline!!!")
    basepath = os.path.abspath(__file__)  # 获取当前文件的绝对路径
    folder = '/'.join(basepath.split('/')[:-2])  # 此时是seq2neo文件目录
    file_path = os.path.join(folder, 'function/immuno_Prediction/data/class1_pseudosequences.csv')
    df = pd.read_csv(file_path)
    mhc_list = list(df.allele)  # 返回存在的HLA列表
    for mhc in mhci:
        if mhc in mhc_list:
            mhci_final.append(mhc)

    return mhci_final
