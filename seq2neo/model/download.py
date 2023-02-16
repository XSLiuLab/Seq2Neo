# Download ftp://ftp.ensembl.org/pub
import os
import argparse
import sys
import subprocess as sp
from seq2neo.lib._make_dir import mkdir as mk
from seq2neo.lib import *

'''
GATK 提供的谷歌云，包括需要的基本文件
https://console.cloud.google.com/storage/browser/genomics-public-data/resources/broad/hg38
'''


def define_parser():
    return DownloadArgumentParser().parser


class Reference:
    def __init__(self, arg):
        self.arg = arg
        self.build = arg.build
        self.dir = os.path.expanduser(arg.dir)
        self.refName = None

    def download_dna_ref(self):
        dna_url = "https://github.com/broadinstitute/gatk/raw/master/src/test/resources/large/Homo_sapiens_assembly{build}.fasta.gz".format(
            build=self.build[-2:]
        )

        print("Download Reference sequence data from GATK")
        mk(self.dir)
        dl = sp.run(["wget %s -P %s" % (dna_url, self.dir)], shell=True)
        if dl.returncode == 0:
            print("Successfully download " + dna_url)
            self.refName = dna_url.split("/")[-1]
            print("uncompress the " + self.refName)
            sp.run("gunzip %s" % self.refName, shell=True)  # 解压，直接覆盖原来的压缩包
            print("Successfully uncompress the " + self.refName)
            # 重新命名
            self.refName = '.'.join(self.refName.split('.')[:-1])
        else:
            print("Error download " + dna_url)

    def make_bwa_index(self):
        print("Make index for %s" % self.refName)
        sp.run("cd %s" % self.dir, shell=True)
        sp.run("bwa index -a bwtsw %s" % self.refName, shell=True)

    def make_faidx(self):
        print("Make fai index for %s" % self.refName)
        sp.run("cd %s" % self.dir, shell=True)
        sp.run("samtools faidx %s" % self.refName, shell=True)

    def make_dict_index(self):
        print("Make dict index for %s" % self.refName)
        out = self.refName.split(".")
        out[-1] = "dict"
        out = ".".join(out)
        sp.run("cd %s" % self.dir, shell=True)
        sp.run("gatk CreateSequenceDictionary -R %s -O %s" % (self.refName, out), shell=True)


def main(args_input=None):
    if args_input is None:
        print("No argument specified!")
        sys.exit(-1)
    
    parser = define_parser()
    args = parser.parse_args(args_input)

    ref = Reference(args)
    ref.download_dna_ref()

    ref.make_bwa_index()
    ref.make_faidx()
    ref.make_dict_index()

    print("Running successfully, thanks for using Seq2Neo!!!")


if __name__ == '__main__':
    main()
