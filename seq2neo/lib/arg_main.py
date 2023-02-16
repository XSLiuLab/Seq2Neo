import argparse
from seq2neo.model import *   # 引入model子文件夹的相关子命令函数


class MainArgumentParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="A pipeline from sequence to neoantigen prediction",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog='seq2neo',
            epilog="Thanks for using Seq2Neo",
        )
        subparsers = parser.add_subparsers()

        # run pipeline
        run_whole = subparsers.add_parser(
            "whole",
            help="Run whole pipeline(Seq2Neo) with fastq/bam/sam/vcf file",
            add_help=False
        )
        run_whole.set_defaults(func=whole)

        # run immunogenicity prediction
        run_immunoprediction = subparsers.add_parser(
            "immuno",
            help="Run immunogenicity prediction with specified peptides and MHCs",
            add_help=False
        )
        run_immunoprediction.set_defaults(func=immunoprediction)

        # downloading reference genome
        run_download = subparsers.add_parser(
            "download",
            help="downloading human reference genome from GATK and building indexes",
            add_help=False
        )
        run_download.set_defaults(func=download)

        self.parser = parser
