import os

import pandas as pd
from Bio import SeqIO
import re


# get mutation peptides and WT peptides

def reformat_fatsa(InFasta):
    out_fatsa = InFasta.replace(".fasta", "_pre.fasta")

    with open(InFasta, "r") as in_fasta:
        with open(out_fatsa, "w") as newfasta:
            for line in in_fasta.readlines():
                if ">" in line:
                    line = " ".join(line.split())
                    newfasta.write(line.replace(" ", ";"))
                    newfasta.write("\n")
                else:
                    newfasta.write(line)

    return out_fatsa


# extract mut peptides sequence
def extract_SNV_FS_peptides(seq, pos: int,
                            n: int, FrameShift=False):
    if FrameShift:  # 移码突变
        if pos < n:
            protein_seq = seq[0:len(seq)]
        else:
            protein_seq = seq[(pos - n):len(seq)]
    else:  # 非移码突变
        if pos < n:
            protein_seq = seq[0:pos - 1 + n]
        elif len(seq) - pos < n:
            protein_seq = seq[(pos - n):len(seq)]  # (pos-1)-(n-1)=pos-n
        else:
            protein_seq = seq[pos - n:pos - 1 + n]

    # 后续处理
    if '*' in protein_seq:
        protein_seq = protein_seq.replace('*', '')  # 针对gene_fusion
    elif 'X' in protein_seq:
        protein_seq = protein_seq.split('X')[0]  # unknown

    return protein_seq


# extract mut mrna sequence
def extract_SNV_FS_mrna(seq, pos: int, n: int, FrameShift=False):
    # 判断突变位点在密码子的第几位
    site = pos % 3
    if site == 0:
        site = 3  # 正好位于第三个密码子上
    previous_amino = pos // 3
    if site == 3:
        previous_amino = previous_amino - 1
    after_amino = (len(seq) // 3) - previous_amino - 1
    pos_index_start = pos - site  # 代表pos所在的密码子起始index
    pos_index_end = pos - site + 2  # 代表pos所在的密码子结束index

    # 增加特殊符号以快速定位到所需位置
    if FrameShift:
        if previous_amino < (n-1):
            mrna_seq = seq[0:pos_index_start] + '>>>' + seq[pos_index_start:len(seq)]
        else:
            mrna_seq = seq[pos_index_start-(n-1)*3:pos_index_start] + '>>>' + seq[pos_index_start:len(seq)]
            # mrna_seq = seq[pos_index_start-(n-1)*3:len(seq)]
    else:
        if previous_amino < (n-1):
            middle = seq[pos_index_start:pos_index_start+3]
            mrna_seq = seq[0:pos_index_start] + '<' + middle + '>' + seq[pos_index_start+3:pos_index_end+(n-1)*3+1]
            # mrna_seq = seq[0:pos_index_end+(n-1)*3+1]
        elif after_amino < (n-1):
            middle = seq[pos_index_start:pos_index_start+3]
            mrna_seq = seq[pos_index_start-(n-1)*3:pos_index_start] + '<' + middle + '>' + seq[pos_index_start+3:len(seq)]
            # mrna_seq = seq[pos_index_start-(n-1)*3:len(seq)]
        else:
            middle = seq[pos_index_start:pos_index_start + 3]
            mrna_seq = seq[pos_index_start-(n-1)*3:pos_index_start] + '<' + middle + '>' + seq[pos_index_start+3:pos_index_end+(n-1)*3+1]
            # mrna_seq = seq[pos_index_start-(n-1)*3:pos_index_end+(n-1)*3+1]

    return mrna_seq


def MakePeptideFasta(Input_file, Peptide_Len: list, dic_path):
    # extract mut peptides
    snvpep = {n: 0 for n in Peptide_Len}  # 分别对 snvpep 和 indelpep 构建字典
    indelpep = {n: 0 for n in Peptide_Len}

    dic_wt_mt = os.path.join(dic_path, 'dictionary_wt_mt.txt')  # 创建wt及对应的mt的字典
    dic_records = []  # 记录着对应行

    for n in Peptide_Len:
        SNV_Seq = []
        Indel_Seq = []
        with open(Input_file) as handle:
            for record in SeqIO.parse(handle, "fasta"):
                if "WILDTYPE" in record.id:
                    wt_seq_all = str(record.seq)  # 转化成字符串

                if "WILDTYPE" not in record.id and 'immediate' not in record.id.lower() and 'silent' not in record.id.lower() and 'startloss' not in record.id.lower():
                    pos = int(record.id.split(";")[6].split("-")[0])  # 突变的起始位置
                    if 'fs' in record.id:  # 只有fs才令FrameShift=True，其它的一律当作“点突变”对待
                        seq = extract_SNV_FS_peptides(str(record.seq), pos, n, True)
                        seq_wt = extract_SNV_FS_peptides(wt_seq_all, pos, n, True)
                        dic_records.append(
                            ','.join([record.id.split(";")[0].replace('>', '', 1), seq, seq_wt, str(n), '1']) + '\n')
                        if len(seq) <= 1000:  # 注意，太长的frameshift应该是出错了
                            Indel_Seq.append(">" + record.id.split(";")[0] + "\n" + seq + "\n")
                    else:
                        seq = extract_SNV_FS_peptides(str(record.seq), pos, n)
                        seq_wt = extract_SNV_FS_peptides(wt_seq_all, pos, n)
                        dic_records.append(
                            ','.join([record.id.split(";")[0].replace('>', '', 1), seq, seq_wt, str(n), '0']) + '\n')
                        SNV_Seq.append(">" + record.id.split(";")[0] + "\n" + seq + "\n")

        snvpep[n] = SNV_Seq
        indelpep[n] = Indel_Seq

    # write mut/wt peptide fasta
    tmpfile = {}  # 记录着文件名
    for n in Peptide_Len:
        tmpSNVfasta = Input_file.replace("_pre.fasta", "_tmp_%s.fasta" % n)
        tmpIndelFasta = Input_file.replace("_pre.fasta", "_tmpindel_%s.fasta" % n)

        tmpfile.update({str(n): tmpSNVfasta})
        tmpfile.update({str(n) + "_indel": tmpIndelFasta})

        with open(tmpSNVfasta, "w") as snvfile:
            for line in snvpep[n]:
                snvfile.write(line)
        with open(tmpIndelFasta, "w") as indelfile:
            for line in indelpep[n]:
                indelfile.write(line)

    # write dic_records to the dictionary
    with open(dic_wt_mt, "w") as dic:
        dic.write("line,mtseq,wtseq,length,isFrameShift\n")
        dic.writelines(dic_records)

    return tmpfile


def MakePeptideFasta_fusion(args, agfusion_dir, resultsPATH):
    # 创建fusion.fasta文件并写入fusion protein
    filepath = os.path.join(resultsPATH, 'fusion_tmp.fasta')
    with open(filepath, 'w') as fusion_file:
        files = []  # 存储文件路径
        for dirpath, dirnames, filenames in os.walk(agfusion_dir):
            for file in filenames:
                if file.endswith('_protein.fa'):
                    files.append(os.path.join(dirpath, file))

        for file in files:  # 将文件全部写入
            f = open(file, 'r')
            content = f.read()
            fusion_file.write(content)
            f.close()

    filepath_new = os.path.join(resultsPATH, 'fusion.fasta')  # 更改fasta的文件描述信息
    with open(filepath_new, 'w') as fusion_file_new:
        with open(filepath, 'r') as fusion_file:
            lines = []
            dictionary = []
            contents = fusion_file.readlines()
            for l in contents:
                if l.startswith('>'):
                    nl = l.split(',')[4]
                    if 'in-frame' in l.split(',')[5]:
                        fs = 'in-frame'
                    else:
                        fs = 'out-of-frame'
                    nl = nl.replace('genes: ', '')
                    lines.append('>' + nl.strip() + ';' + fs + '\n')  # 必须用;否则biopython读不出来后续的东西
                    dictionary.append(nl.strip() + ',Gene_Fusion' + ',' + fs + '\n')
                else:
                    lines.append(l)
            fusion_file_new.writelines(lines)

    dic_path = os.path.join(resultsPATH, 'dictionary_fusion.txt')  # 创建gene fusion字典, 保存
    with open(dic_path, 'w') as f:
        f.write("GeneFusion_Name,Type,influence\n")
        f.writelines(dictionary)

    # 提取突变肽
    gene_fusion_pep = {n: 0 for n in args.len}  # 对 gene_fusion 构建字典
    for n in args.len:
        GeneFusion_Seq = []
        with open(filepath_new) as handle:
            for record in SeqIO.parse(handle, "fasta"):
                pos = str(record.seq).index('*') + 1  # gene junction的位置
                if 'out-of-frame' in record.id:  # 只有out-of-frame才令FrameShift=True，in-frame当作“点突变”对待
                    seq = extract_SNV_FS_peptides(str(record.seq), pos, n, True)
                    GeneFusion_Seq.append(">" + record.id.split(';')[0] + "\n" + seq + "\n")
                else:
                    seq = extract_SNV_FS_peptides(str(record.seq), pos, n)
                    GeneFusion_Seq.append(">" + record.id.split(';')[0] + "\n" + seq + "\n")
        gene_fusion_pep[n] = GeneFusion_Seq  # 如果fusion不存在，则GeneFusion_Seq为空列表

    for n in args.len:
        tmpGeneFusionFasta = os.path.join(resultsPATH, '%s_tmpgenefusion_%s.fasta' % (args.tumor_name, n))
        with open(tmpGeneFusionFasta, "w") as genefusion_file:
            genefusion_file.writelines(gene_fusion_pep[n])


def makeWTFasta(Input_File, Peptide_len):
    WT = []
    with open(Input_File) as handle:
        for record in SeqIO.parse(handle, "fasta"):
            wt_acid = record.id.split(";")[9]
            mu_acid = record.id.split(";")[11][0]
            print(mu_acid)
            seq = str(record.seq)
            print(seq[Peptide_len - 1])
            if seq[Peptide_len - 1] == mu_acid:
                tmp = list(seq)
                tmp[Peptide_len - 1] = wt_acid  # 替换成”野生型“
                seq = ''.join(tmp)
                WT.append(">" + record.id[0:100] + ";WILDTYPE" + "\n" + seq + "\n")

    tmpWTfasta = Input_File.replace("_tmp", "_tmp_wt")
    with open(tmpWTfasta, 'w') as wtfile:
        for line in WT:
            wtfile.write(line)


# 创建字典
def createDictionary(Input_File, Output_File):
    contents = []
    with open(Input_File, 'r') as Input:
        for line in Input.readlines():
            if 'stopgain' not in line and 'unknown' not in line and 'stoploss' not in line:
                segmentation = line.split()

                site = segmentation[0]
                influence = segmentation[1]  # 突变所造成的影响
                mutation_type = segmentation[2]  # 突变的类型
                obj = segmentation[3]
                chr_num = segmentation[4]  # 突变所处的染色体
                location = segmentation[5]  # 变异位置
                ref = segmentation[7]  # 参考碱基
                mut = segmentation[8]  # 突变碱基

                GeneName_Alias = ','.join(obj.split(":")[0:2])
                info = site + ',' + influence + ',' + mutation_type + ',' + \
                       GeneName_Alias + ',' + location + ',' + chr_num + ',' + ref + ',' + mut

                first = obj.split(',')[0]  # 取列表的第一项元素
                last_item = first.split(':')[-1]  # 取最后一项元素，即氨基酸的变化信息
                if last_item.startswith('p.'):
                    amino_change = last_item.replace('p.', '', 1)
                else:
                    amino_change = '#'

                contents.append(info + ',' + amino_change + '\n')
            else:
                continue

    with open(Output_File, 'w') as Output:
        Output.write("line,influence,mutation_type,GeneName,Alias,location,chr,ref,mut,amino_change" + '\n')
        contents = set(contents)  # 消除重复
        Output.writelines(contents)


def createDictionary_mrna(Input_File, Output_Dir, dic_path, Peptide_Len: list):
    df_dic = pd.read_csv(dic_path)
    end = round(len(df_dic) / len(Peptide_Len))  # 因为有可能有很多的
    filtered_lines = list(df_dic.line)[0:end]  # 存有需要的line
    isFS = list(df_dic.isFrameShift)[0:end]  # 存储是否是fs，不是为0，是为1

    dic_wt_mt = os.path.join(Output_Dir, 'dictionary_mrna.txt')  # 创建wt及对应的mt的字典(mrna)
    dic_records = []  # 记录着对应行

    for n in Peptide_Len:
        with open(Input_File) as handle:
            for record in SeqIO.parse(handle, "fasta"):
                line = record.id.split(';')[0].replace('>', '', 1)  # 获取当前循环的line号
                if "WILDTYPE" in record.id and line in filtered_lines:
                    wt_seq_all = str(record.seq)  # 转化成字符串

                if "WILDTYPE" not in record.id and line in filtered_lines:
                    pos = int(re.findall(r"\d+", record.id.split(';')[4])[0])  # 突变的起始位置
                    fs_label = isFS[filtered_lines.index(line)]  # 是否为fs，不是为0，是为1
                    if fs_label == 1:
                        seq = extract_SNV_FS_mrna(str(record.seq), pos, n, True)
                        seq_wt = extract_SNV_FS_mrna(wt_seq_all, pos, n, True)
                        dic_records.append(','.join([line, seq, seq_wt, str(n), '1']) + '\n')
                    else:
                        seq = extract_SNV_FS_mrna(str(record.seq), pos, n)
                        seq_wt = extract_SNV_FS_mrna(wt_seq_all, pos, n)
                        dic_records.append(','.join([line, seq, seq_wt, str(n), '0']) + '\n')

    with open(dic_wt_mt, "w") as dic:
        dic.write("line,mt_mrna_seq,wt_mrna_seq,length,isFrameShift\n")
        dic.writelines(dic_records)
