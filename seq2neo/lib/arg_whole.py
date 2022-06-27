import argparse


class WholeArgumentParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Run whole pipeline(Seq2Neo) with fastq/bam file",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="seq2neo whole"
        )

        parser.add_argument(
            "--data-type",
            default="fastq",
            choices={"fastq", "sam", "sort_bam"},
            help="Select your input file format(fastq/sam/sort_bam), default:fastq",
            type=str
        )
        parser.add_argument(
            "--ref",
            metavar="path_to_reference",
            required=True,
            help="Path to reference genomic data",
        )
        parser.add_argument(
            "--normal-dna", help="Normal sample files",
            metavar=("normal_dna_1.fq", "normal_dna_2.fq"), nargs=2,
        )
        parser.add_argument(
            "--tumor-dna", help="Tumor dna sample files",
            metavar=("tumor_dna_1.fq", "tumor_dna_2.fq"), nargs=2,
        )
        parser.add_argument(
            "--tumor-rna", required=True, help="Tumor rna sample files",
            metavar=("tumor_rna_1.fq", "tumor_rna_2.fq"), nargs=2,
        )
        parser.add_argument(
            "--normal-sam", help="Normal dna sam files", metavar="normal.sam", type=str
        )
        parser.add_argument(
            "--tumor-sam", help="Tumor dna sam files", metavar="tumor.sam", type=str
        )
        parser.add_argument(
            "--normal-sorted-bam", help="Normal dna sorted bam files", metavar="normal_sorted.bam", type=str
        )
        parser.add_argument(
            "--tumor-sorted-bam", help="Tumor dna sorted bam files", metavar="tumor_sorted.bam", type=str
        )

        parser.add_argument("--normal-name", required=True, metavar="normal_name",
                            help="if the file is XXX_1.fq, the normal name should be XXX")
        parser.add_argument("--tumor-name", required=True, metavar="tumor_name",
                            help="if the file is XXX_1.fq, the tumor name should be XXX")

        # 数据库
        parser.add_argument("--known-site-dir", required=True, help="directory to BQSR known site",
                            metavar="known_site_dir")
        parser.add_argument("--mutect2-dataset-dir", required=True, help="directory to mutect2 needed dataset file",
                            metavar="mutect2_dataset_dir")
        parser.add_argument("--annovar-db-dir", required=True, help="directory to annovar database",
                            metavar="annovar_db_dir")
        parser.add_argument("--genome-lib-dir", required=True,
                            help="directory containing genome lib (see http://STAR-Fusion.github.io)",
                            metavar="genome_lib_dir")
        parser.add_argument("--agfusion-db", help="Path to the AGFusion database", required=True, metavar="agfusion_db")

        parser.add_argument(
            "--out", help="Output directory to save prediction results, default is current directory",
            default=".", metavar="out_dir", type=str
        )
        parser.add_argument("--len", help="length of peptides, default is 8 9 10 11", default=(8, 9, 10, 11),
                            nargs='*', type=int)

        parser.add_argument(
            "--threadN", help="the number of thread used in Seq2Neo, default is 4",
            type=int, default=4, metavar="thread_num"
        )
        parser.add_argument("--mdna", help="length of reads(normal dna)", default=100, type=int, metavar="min_length")
        parser.add_argument("--mrna", help="length of reads(rna)", default=100, type=int, metavar="min_length")
        parser.add_argument(
            "--java-options", help="set config for java", type=str, default="-Xmx8G", metavar="java_options"
        )
        parser.add_argument("--hlahd-dir", help="the path to hlahd software", type=str,
                            required=True, metavar="hlahd_dir")
        parser.add_argument("--hla", help="if you use bam and sorted sam as input, please provide hlas, like"
                                          "--hla HLA-A01:01 HLA-A03:03", type=str, nargs='*', default='HLA-A01:01')

        self.parser = parser
