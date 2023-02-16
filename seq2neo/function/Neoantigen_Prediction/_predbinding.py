import subprocess
import os
from concurrent.futures import ThreadPoolExecutor

from seq2neo.lib import NetMHCpanconvert, NetCTLpanconvert
from .mhci import NetMHCpan41CommandLine
from .tap import NetCTLpanCommandLine


def predict_bindingI(method, hla, length, file, outfile):  # 传入的length应该为一个列表
    if method not in ["NetMHCpan", "mhcflurry", "Pickpocket", "NetMHC"]:
        print("Seq2Neo doesn't have this method!!!")
        return

    elif method == "NetMHCpan":
        length = ",".join([str(i) for i in length])  # 满足命令行的要求
        netmhcpan41_cmd = NetMHCpan41CommandLine(
            f=file,
            BA="BA",
            l=length,
            a=hla)
        print(netmhcpan41_cmd)
        netmhcpan41_cmd(stdout=outfile)

        outdir = "/".join(outfile.split("/")[:-2])  # 返回上一个目录
        outdir = os.path.join(outdir, 'mhci')
        os.makedirs(outdir, exist_ok=True)

        NetMHCpanconvert(outfile, outdir)


def predict_binding_affinity(filepath, Input_file,
                             sample_name, methods: list,
                             hlas: list, length: list, cla):  # cla (classI or classII)
    pool = ThreadPoolExecutor(max_workers=12)  # 最大分配12个进程
    checks = dict.fromkeys(Input_file.keys())

    for key, value in Input_file.items():
        cmd = "wc -l %s" % value  # values 是一个文件
        pipe = subprocess.Popen(cmd,
                                shell=True,
                                stdout=subprocess.PIPE).stdout
        k = int(pipe.read().decode("utf-8").lstrip(" ").split(" ")[0])  # k 指的是 文件所拥有的 行数
        checks[key] = k

    if len(methods) > 0:
        for key, value in Input_file.items():
            if checks[key] > 0:  # 文件行数大于0才代表有内容
                for method in methods:
                    for hla in hlas:
                        pool.submit(mutiThread_predict_binding_affinity, key, value, method, hla,
                                    length, filepath, sample_name, cla)
            else:
                print(f"Dont find any peptides in {value}")
        pool.shutdown()  # 等待所有进程执行完毕
    else:
        print("Choose at least one prediction method")


def predict_TAP(filepath, Input_file, sample_name, hlas: list, length: list):

    pool = ThreadPoolExecutor(max_workers=12)  # 创建进程池
    checks = dict.fromkeys(Input_file.keys())

    for key, value in Input_file.items():
        cmd = "wc -l %s" % value  # values 是一个文件
        pipe = subprocess.Popen(cmd,
                                shell=True,
                                stdout=subprocess.PIPE).stdout
        k = int(pipe.read().decode("utf-8").lstrip(" ").split(" ")[0])  # k 指的是 文件所拥有的 行数
        checks[key] = k

    length = ",".join([str(i) for i in length])  # 满足命令行的要求
    path = os.path.join(filepath, 'tap')
    os.makedirs(path, exist_ok=True)

    for key, value in Input_file.items():
        if checks[key] > 0:  # 文件行数大于0才代表有内容
            for hla in hlas:
                pool.submit(mutiThread_predict_TAP, key, value, hla, length, filepath, sample_name, path)
        else:
            print(f"Dont find any peptides in {value}")
    pool.shutdown()  # 等待线程执行完毕


def mutiThread_predict_TAP(key, value, hla, length, filepath, sample_name, path):

    outfile = os.path.join(filepath, "tmp/%s_%s_%s_%s_%s.txt" % (sample_name,
                                                                 key,
                                                                 'netCTLpan',
                                                                 length,
                                                                 hla))
    os.makedirs(os.path.dirname(outfile), exist_ok=True)  # 制造tmp文件

    netctlpan_cmd = NetCTLpanCommandLine(
        f=value,
        l=length,
        a=hla)
    print(netctlpan_cmd)
    netctlpan_cmd(stdout=outfile)

    NetCTLpanconvert(outfile, path)


def mutiThread_predict_binding_affinity(key, value, method, hla, length, filepath, sample_name, cla):

    outfile = os.path.join(filepath, "tmp/%s_%s_%s_%s_%s.txt" % (sample_name,
                                                                 key,
                                                                 method,
                                                                 "_".join([str(i) for i in length]),
                                                                 hla))
    os.makedirs(os.path.dirname(outfile), exist_ok=True)  # 制造tmp文件

    if cla == "classI":
        predict_bindingI(method, hla, length, value, outfile)
