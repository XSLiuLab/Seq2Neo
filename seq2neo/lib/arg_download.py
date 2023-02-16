import argparse


class DownloadArgumentParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Run download module",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="seq2neo download"
        )

        parser.add_argument(
            '--build',
            type=str,
            help='which build to download, hg38 / hg19',
            choices=['hg19', 'hg38'],
            default="hg38")

        # 默认是当前目录
        parser.add_argument(
            '--dir',
            type=str,
            help='where to store',
            nargs='?', const='.', default='.')

        self.parser = parser
