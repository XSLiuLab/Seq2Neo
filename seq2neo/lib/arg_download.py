import argparse


class DownloadArgumentParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Run download module",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="seq2neo download"
        )

        parser.add_argument(
            '--species',
            type=str,
            help='which species to download',
            default="homo_sapiens")

        parser.add_argument(
            '--build',
            type=str,
            help='which build to download',
            default="GRCh38")

        parser.add_argument(
            '--release',
            type=int,
            help='which release to download',
            default=105)

        # 默认是当前目录
        parser.add_argument(
            '--dir',
            type=str,
            help='where to store',
            nargs='?', const='.', default='.')

        self.parser = parser
