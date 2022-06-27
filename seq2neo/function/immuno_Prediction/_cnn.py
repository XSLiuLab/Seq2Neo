# -*- coding: utf-8 -*-
import os
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import layers
from tensorflow.keras.layers import *
import numpy as np
import pandas as pd
import argparse
import warnings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
warnings.filterwarnings("ignore", category=Warning)

basepath = os.path.abspath(__file__)  # 获取当前文件的绝对路径
folder = os.path.dirname(basepath)
weight_path = os.path.join(folder, 'data/weights/cnn/')
weights = os.path.join(weight_path, "success_weight_test")
pseudosequences = os.path.join(folder, 'data/class1_pseudosequences.csv')


# 更改后的CNN模型
def seperateCNN():
    input1 = keras.Input(shape=(11, 20, 1))  # 输入3维数据
    input2 = keras.Input(shape=(34, 20, 1))
    ic50 = keras.Input(shape=(1,))
    tap = keras.Input(shape=(1,))

    x = layers.Conv2D(filters=16, kernel_size=(2, 20))(input1)  # 10
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)
    x = layers.Conv2D(filters=32, kernel_size=(3, 1))(x)  # 8
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)
    x = layers.MaxPool2D(pool_size=(2, 1), strides=(2, 1))(x)  # 4
    x = layers.Flatten()(x)  # 展平
    x = keras.Model(inputs=input1, outputs=x)

    y = layers.Conv2D(filters=16, kernel_size=(3, 20))(input2)  # 32
    y = layers.BatchNormalization()(y)
    y = keras.activations.relu(y)
    y = layers.MaxPool2D(pool_size=(2, 1), strides=(2, 1))(y)  # 16
    y = layers.Conv2D(filters=32, kernel_size=(9, 1))(y)  # 8
    y = layers.BatchNormalization()(y)
    y = keras.activations.relu(y)
    y = layers.MaxPool2D(pool_size=(2, 1), strides=(2, 1))(y)  # 4
    y = layers.Flatten()(y)
    y = keras.Model(inputs=input2, outputs=y)

    combined = layers.concatenate([x.output, y.output])  # 连接
    print(combined.shape)  # 打印出形状
    z = layers.Dense(1024, activation='relu')(combined)
    z = layers.Dense(512, activation='relu')(z)
    z = layers.Dense(256, activation='relu')(z)

    total = layers.concatenate([z, ic50, tap])  # 数据合并

    z = layers.Dense(128, activation='relu')(total)
    z = layers.Dropout(0.2)(z)
    z = layers.Dense(1, activation='sigmoid')(z)

    model = keras.Model(inputs=[input1, input2, ic50, tap], outputs=z)
    return model


letterDict = {"A": 0, "C": 1, "D": 2, "E": 3, "F": 4,
              "G": 5, "H": 6, "I": 7, "K": 8, "L": 9,
              "M": 10, "N": 11, "P": 12, "Q": 13, "R": 14,
              "S": 15, "T": 16, "V": 17, "W": 18, "Y": 19}


def encode(peptides: str, maxlen):
    # code peptide by using onehot

    len_peptides = len(peptides)
    onehot = np.zeros((maxlen, len(letterDict)))
    if len_peptides <= maxlen:
        k = maxlen - len_peptides
        peptides = peptides + 'X' * k
        for i, peptide in enumerate(peptides):
            if peptide == "X":
                i = i + 1
                continue
            else:
                onehot[i][letterDict[peptide]] = 1
        return onehot
    else:
        onehot = ["NaN"]
        return onehot


def reshape(x, maxlen):
    code = encode(x, maxlen)
    return code


def pre_pep(df):
    series = []
    for i in range(len(df)):
        pep_encoded = reshape(df["Peptide"].iloc[i], 11)
        series.append(pep_encoded)
    series = np.array(series)
    series = series[..., None]
    return series


def pre_hla(df):
    series = []
    for i in range(len(df)):
        hla_encoded = reshape(df["pseudosequence"].iloc[i], 34)
        series.append(hla_encoded)
    series = np.array(series)
    series = series[..., None]
    return series


def pre_number(df, col):
    series = []
    for i in range(len(df)):
        series.append(df[col].iloc[i])
    series = np.array(series)
    return series


def standard(df, col="IC50"):
    if col not in ["IC50", "TAP"]:
        print("Error: Wrong column name")
    elif col == "IC50":
        # min ic50 = 1.48
        # max ic50 = 48039.45
        df[col] = (df[col] - 1.48) / (48039.45 - 1.48)
    else:
        # min tap = -2.888
        # max tap = 3.624
        df[col] = (df[col] + 2.888) / (3.624 + 2.888)

    return df


def hlatopseudoseq(input):
    pseudoseq = pd.read_csv(pseudosequences, sep=",")
    pseudoseq.columns = ["HLA", "pseudosequence"]
    input["HLA"] = [a.replace("*", "") for a in input["HLA"]]  # 去除HLA的星号（’*‘）

    # merge后，主数据的顺序会改变（很隐蔽），所以构建辅助列进行排序
    input["row_index"] = list(input.index)
    # 合并 并 排序 成主数据顺序
    input = pd.merge(input, pseudoseq, on="HLA", how="inner")
    input = input.sort_values(by="row_index", ascending=True)
    input.pop("row_index")

    return input


# class weight
# weight for class 0: 0.84
# weight for class 1: 1.24


def file_process(input_df, outdir):
    cnn_model = seperateCNN()
    cnn_model.load_weights(weights).expect_partial()  # 加上expect_partial()禁止输出Warning信息

    origin_input = input_df
    origin_input.columns = ["Peptide", "HLA", "IC50", "TAP"]

    origin_input = hlatopseudoseq(origin_input)
    origin_input = standard(df=origin_input)
    origin_input = standard(df=origin_input, col="TAP")

    input1 = pre_pep(df=origin_input)
    input2 = pre_hla(df=origin_input)
    IC50 = pre_number(df=origin_input, col="IC50")
    TAP = pre_number(df=origin_input, col="TAP")

    scoring = cnn_model.predict([input1, input2, IC50, TAP])
    origin_input["immunogenicity"] = scoring  # 顺序并没有改变

    origin_input.to_csv(os.path.join(outdir, "cnn_results.csv"),
                        index=None)


def computing_sigle(peptides, mhc, IC50, TAP):
    ic50 = []
    tap = []
    Pep = []
    Hla = []

    pseudoseq = pd.read_csv(pseudosequences, sep=",")
    hla = pseudoseq.loc[pseudoseq["allele"] == mhc]["pseudosequence"]
    hla = hla.values[0]

    cnn_model = seperateCNN()
    cnn_model.load_weights(weights).expect_partial()

    pep_encoded = reshape(peptides, 11)
    Pep.append(pep_encoded)
    hla_encoded = reshape(hla, 34)
    Hla.append(hla_encoded)

    ic50.append((IC50 - 1.48) / (48039.45 - 1.48))
    tap.append((TAP + 2.888) / (3.624 + 2.888))

    scoring = cnn_model.predict([np.array(Pep), np.array(Hla),
                                 np.array(ic50), np.array(tap)])
    return scoring
