# -*- coding: utf-8 -*
# 提取fasta文件的突变肽
def sliding_window(filename, windows_lens, outfile=None):
    peptides = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for l in lines:
            if l.startswith(">"):
                continue
            else:
                peptides.append(l[:-1])  # 去除最后的 换行符

    result = dict.fromkeys(peptides, None)  # 注意，此处None换成[]会导致浅复制（shallow copy）
    lengths = dict.fromkeys(windows_lens, None)

    for windows_len in windows_lens:
        for pre_pep in peptides:
            pep = []
            tmp = windows_len
            pre_len = len(pre_pep)
            pep_number = pre_len - windows_len

            if pep_number < 0:  # 只提示，并不终止程序运行
                print("WARNING: the length of %s is less than %s" % (pre_pep, windows_len))

            for i in range(pep_number + 1):
                tmp_pep = pre_pep[i: windows_len]
                pep.append(tmp_pep + '\n')
                windows_len += 1

            result[pre_pep] = pep
            windows_len = tmp

        lengths[windows_len] = deep_flatten(list(result.values()))

    if outfile:
        with open(outfile, "w") as f:
            for windows_len in windows_lens:
                lines = lengths[windows_len]
                f.writelines(lines)
    else:
        print("This is no output path, "
              "a dictionary filled with peptides of specified lengths is returned!!!")
        return lengths


# 展平列表
def spread(arg):
    ret = []
    for i in arg:
        if isinstance(i, list):
            ret.extend(i)
        else:
            ret.append(i)
    return ret


def deep_flatten(arr):
    result = []
    result.extend(
        spread(list(map(lambda x: deep_flatten(x) if type(x) == list else x, arr))))
    return result
