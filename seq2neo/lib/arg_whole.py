import argparse


class WholeArgumentParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Run whole pipeline(Seq2Neo) with fastq/bam file",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            prog="seq2neo whole"
        )

        # 选择从哪里运行
        parser.add_argument(
            "--data-type",
            default="fastq",
            choices=["fastq", "sam", "sort_bam",
                     "without-tumor-rna", "without-normal-dna", "only-tumor-dna", "vcf"],
            help="Select your input files format, default:fastq; \
                  fastq: start from fastq files; need files: tumor dna, normal dna, tumor rna; \
                  sam: start from sam files; need files: tumor dna, normal dna, tumor rna; \
                  sort_bam: start from sort_bam files; need files: tumor dna, normal dna, tumor rna; \
                  without-tumor-rna: start from fastq files; need files: tumor dna, normal dna; \
                  without-normal-dna: start from fastq files; need files: tumor dna, tumor rna; \
                  only-tumor-dna: start from fastq files; need files: tumor dna; \
                  vcf: start from vcf file, dont need tumor rna",
            type=str)
        
        # 输入文件
        parser.add_argument(
            "--ref",
            metavar="path_to_reference",
            required=True,
            help="Path to reference genomic data",
            type=str)
        parser.add_argument(
            "--normal-dna", help="Normal DNA sample files<Pair End>",
            metavar=("normal_dna_1.fq", "normal_dna_2.fq"), nargs=2)
        parser.add_argument(
            "--tumor-dna", help="Tumor DNA sample files<Pair End>",
            metavar=("tumor_dna_1.fq", "tumor_dna_2.fq"), nargs=2)
        parser.add_argument(
            "--tumor-rna", help="Tumor RNA sample files<Pair End>",
            metavar=("tumor_rna_1.fq", "tumor_rna_2.fq"), nargs=2)
        parser.add_argument(
            "--normal-sam", help="Normal DNA sam file", metavar="normal.sam", type=str)
        parser.add_argument(
            "--tumor-sam", help="Tumor DNA sam file", metavar="tumor.sam", type=str)
        parser.add_argument(
            "--normal-sorted-bam", help="Normal DNA sorted bam file", metavar="normal_sorted.bam", type=str)
        parser.add_argument(
            "--tumor-sorted-bam", help="Tumor DNA sorted bam file", metavar="tumor_sorted.bam", type=str)
        
        parser.add_argument("--vcf", help="a VCF file containing mutated sites", metavar="xxx.vcf", type=str)

        # sample name
        parser.add_argument("--normal-name", metavar="normal_sample_name",
                            help="If the file is XXX_1.fq, the --normal-name should be XXX")
        parser.add_argument("--tumor-name", required=True, metavar="tumor_sample_name",
                            help="If the file is XXX_1.fq, the --tumor-name should be XXX")

        # 公共资源数据库
        parser.add_argument("--annovar-db-dir", required=True, help="The absolute directory to annovar human database",
                            metavar="annovar_db_dir", type=str)
        parser.add_argument("--known-site-dir", help="The absolute directory to BQSR known sites files",
                            metavar="known_site_dir", type=str)
        parser.add_argument("--mutect2-dataset-dir", help="The absolute directory to mutect2 needed dataset files",
                            metavar="mutect2_dataset_dir", type=str)
        parser.add_argument("--genome-lib-dir", type=str,
                            help="The absolute directory to STAR-Fusion genome database (see http://STAR-Fusion.github.io)",
                            metavar="genome_lib_dir")
        parser.add_argument("--agfusion-db", help="The absolute path to AGFusion database", metavar="agfusion_db", type=str)
        # 用户可以自定义pon
        parser.add_argument("--pon", help="The absolute path to panel-of-normals dataset", metavar="pon.vcf.gz", type=str)

        # 运行配置
        parser.add_argument("--len", help="Length of neoantigens, default is 8 9 10 11", default=(8, 9, 10, 11),
                            nargs='*', type=int)
        parser.add_argument("--threadN", help="The number of threads used in Seq2Neo, default is 4",
                             type=int, default=4, metavar="thread_num")
        parser.add_argument("--mdna", help="Minimal length of DNA reads(normal dna)", default=100, type=int, metavar="min_length")
        parser.add_argument("--mrna", help="Minimal length of RNA reads(rna)", default=100, type=int, metavar="min_length")
        parser.add_argument("--java-options", help="Set a config for java", type=str, default="-Xmx8G", metavar="java_options")
        parser.add_argument("--hlas", help="if you not use fastq files as inputs, please provide hlas, just like \
                                            --hlas HLA-A01:01; in addition, hlas would not been calculated if --hlas used", 
                             type=str, nargs='*')
        
        # 软件配置
        parser.add_argument("--hlahd-dir", help="The absolute directory to hlahd software", type=str, metavar="hlahd_dir")
        
        # 输出文件夹
        parser.add_argument(
            "--out", help="Output directory for saving prediction results, default is working directory",
             default=".", metavar="out_dir", type=str)

        self.parser = parser
