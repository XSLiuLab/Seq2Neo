import argparse


class ImmunoArgumentParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Seq2Neo-CNN command line(one part of Seq2Neo)",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="seq2neo immuno"
        )

        parser.add_argument(
            '--mode',
            type=str,
            default='single',
            help='single mode or multiple mode')

        parser.add_argument(
            '--epitope',
            type=str,
            default='SVQIISCQY',
            help='if single mode, specifying your epitope')

        parser.add_argument(
            '--hla',
            type=str,
            default='HLA-A30:02',
            help='if single mode, specifying your HLA allele')

        parser.add_argument(
            '--inputfile',
            type=str, default=None,
            help='if multiple mode, specifying the path to your input file')

        parser.add_argument(
            '--outdir',
            type=str,
            default=None,
            help='if multiple mode, specifying the path to your output folder')

        self.parser = parser
