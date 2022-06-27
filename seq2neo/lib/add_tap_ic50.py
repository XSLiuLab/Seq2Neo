import os
import pandas as pd
import subprocess as sp
from concurrent.futures import ProcessPoolExecutor  # 并行化计算加快速度
from seq2neo.function.Neoantigen_Prediction.mhci import NetMHCpan41CommandLine
from seq2neo.function.Neoantigen_Prediction.tap import NetCTLpanCommandLine


# 策略：一个个循环，创建一个临时文件夹存放，计算完毕后删除
# 在当前文件夹产生的临时文件，随后删除
# 免疫原性模块的HLA的形式与netMHCpan和netCTLpan相同，直接用即可
def ic50_cal(peps: list, mhcs: list, dir):
    # 最大工作20
    pool = ProcessPoolExecutor(max_workers=20)
    prefix = os.path.join(dir, 'immuno_ic50_')

    # 计数
    count = 1
    for pair in list(zip(peps, mhcs)):
        infile = prefix + str(count) + '.pep'
        with open(infile, 'w') as f:  # 向inflie内写入肽段
            f.write(pair[0])
        outfile = prefix + str(count) + '.txt'
        netmhcpan41_cmd = NetMHCpan41CommandLine(
            p=infile,
            BA="BA",
            a=pair[1]
        )
        pool.submit(netmhcpan41_cmd, stdout=outfile)
        count = count + 1
    pool.shutdown()  # 暂停直到子进程结束


def tap_cal(peps: list, mhcs: list, dir):
    # 最大工作20
    pool = ProcessPoolExecutor(max_workers=20)
    prefix = os.path.join(dir, 'immuno_tap_')

    # 计数
    count = 1
    for pair in list(zip(peps, mhcs)):
        infile = prefix + str(count) + '.fa'
        with open(infile, 'w') as f:
            f.write('>tap' + str(count) + '\n')
            f.write(pair[0])
        outfile = prefix + str(count) + '.txt'
        netctlpan_cmd = NetCTLpanCommandLine(
            f=infile,
            a=pair[1],
            l=len(pair[0])  # 求出肽长
        )
        pool.submit(netctlpan_cmd, stdout=outfile)
        count = count + 1
    pool.shutdown()


# def tap_cal(files: list, mhcs: list):
def mutiple_cal(args):
    # 创建一个临时文件夹
    os.makedirs('tmp', exist_ok=True)
    dir = os.path.join('.', 'tmp')
    prefix_ic50 = os.path.join(dir, 'immuno_ic50_')
    prefix_tap = os.path.join(dir, 'immuno_tap_')

    outfile = os.path.join(args.outdir, 'immuno_input_file.csv')
    df = pd.read_csv(args.inputfile)

    peps = list(df.iloc[:, 0])
    mhcs = list(df.iloc[:, 1])
    count = len(peps)  # 计算数量

    # 执行预测
    ic50_cal(peps, mhcs, dir)
    tap_cal(peps, mhcs, dir)

    # 收集预测结果
    affs = []
    for i in range(count):
        i = i + 1
        aff = NetMHCpanconvert(prefix_ic50 + str(i) + '.txt')  # 获取
        affs.append(aff)
    taps = []
    for i in range(count):
        i = i + 1
        tap = NetCTLpanconvert(prefix_tap + str(i) + '.txt')  # 获取
        taps.append(tap)

    # 整合至文件
    df["IC50"] = affs
    df["TAP"] = taps
    df.to_csv(outfile, index=False)

    # 删除临时文件夹
    rm_cmd = "rm -rf %s" % dir
    sp.run(rm_cmd, shell=True)

    return outfile


def single_cal(args, type="ic50"):
    if type == "ic50":
        infile = 'immuno_ic50.pep'
        with open(infile, 'w') as f:  # 向inflie内写入肽段
            f.write(args.epitope)
        outfile = 'immuno_ic50.txt'
        netmhcpan41_cmd = NetMHCpan41CommandLine(
            p=infile,
            BA="BA",
            a=args.hla
        )
        netmhcpan41_cmd(stdout=outfile)
        ic50 = NetMHCpanconvert(outfile)
        os.remove(infile)
        os.remove(outfile)
        return ic50
    else:
        infile = 'immuno_tap.fa'
        with open(infile, 'w') as f:  # 向inflie内写入肽段
            f.write('>tap single\n')
            f.write(args.epitope)
        outfile = 'immuno_tap.txt'
        netctlpan_cmd = NetCTLpanCommandLine(
            f=infile,
            a=args.hla,
            l=len(args.epitope)
        )
        netctlpan_cmd(stdout=outfile)
        tap = NetCTLpanconvert(outfile)
        os.remove(infile)
        os.remove(outfile)
        return tap


def NetMHCpanconvert(filename):
    with open(filename, "r") as f:
        lines = f.readlines()  # 会读入末尾的换行符
        for l in lines:
            if l.startswith("#") or l.startswith("---") or len(l) == 1 or "Aff" in l:
                continue
            elif l.split()[0].isdigit():
                if l.endswith("B\n"):
                    l = ",".join(l.split()[:-2])
                    break
                else:
                    l = ",".join(l.split())
                    break

    aff = l.split(',')[-1]
    return float(aff)  # 返回IC50值


def NetCTLpanconvert(filename):
    with open(filename, "r") as f:
        lines = f.readlines()  # 会读入末尾的换行符
        for l in lines:
            if l.startswith("#") or l.startswith("---") or len(l) == 1:
                continue
            elif l.split()[0].isdigit():
                if l.endswith("E\n"):
                    l = ",".join(l.split()[:-1])
                    break
                else:
                    l = ",".join(l.split())
                    break

    tap = l.split(',')[5]
    return float(tap)  # 返回tap值
