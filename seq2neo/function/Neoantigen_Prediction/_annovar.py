from Bio.Application import _Option, _Argument, _Switch
from Bio.Application import AbstractCommandline


class AnnovarConvertCommandline(AbstractCommandline):     # 最终命令行展示顺序以此为基础
    def __init__(self, cmd="convert2annovar.pl", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _Option(
                ["--format", "format"],
                "input format (default: pileup)",
                equate=False,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Option(
                ["--filter", "filter"],
                "output variants with this filter",
                checker_function=lambda x: isinstance(x, str),
                equate=False
            ),
            _Option(
                ["--outfile", "outfile"],
                "output file name prefix",
                filename=True,
                equate=False,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Argument(
                ["input", "input_file"],
                "Input File Name",
                filename=True,
                is_required=True
            ),
            _Switch(
                ["--allsample", "allsample"],
                "process all samples in file with separate output files (for vcf4 format)"
            )
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)


class AnnovarAnnotationCommandline(AbstractCommandline):
    def __init__(self, cmd="annotate_variation.pl", **kwargs):
        self.program_name = cmd,
        self.parameters = [
            _Switch(
                ["--geneanno", "geneanno"],
                "annotate variants by gene-based annotation",
            ),
            _Switch(
                ["--regionanno", "regionanno"],
                "annotate variants by region-based annotation"
            ),
            _Switch(
                ["--filter", "filter"],
                "annotate variants by filter-based annotation"
            ),
            _Option(
                ["--buildver", "buildver"],
                "specify genome build version (default: hg18 for human)",
                is_required=True,
                equate=False,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Option(
                ["--outfile", "outfile"],
                "output file prefix",
                is_required=True,
                filename=True,
                equate=False
            ),
            _Switch(
                ["--comment", "comment"],
                "print out comment line "
            ),
            _Argument(
                ["Input", "input"],
                "Input File Name",
                is_required=True,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Argument(
                ["database", "db"],
                "Database Path",
                checker_function=lambda x: isinstance(x, str)
            )
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)


class GetCodingChangeCommandline(AbstractCommandline):
    def __init__(self, cmd="coding_change.pl", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _Switch(
                ["--onlyAltering", "onlyAltering"],
                "ignore synonymous SNPs only includesnp specified"
            ),
            _Switch(
                ["--includesnp", "includesnp"],
                "Include SNP"
            ),
            _Switch(
                ["--mrnaseq", "mrnaseq"],
                "output mrna sequence rather than protein sequence"
            ),
            _Switch(
                ["--codingseq", "codingseq"],
                "output mrna sequence without UTR sequence only mrnaseq specified"
            ),
            _Argument(
                ["exonic_variant", "input"],
                "Input File",
                is_required=True,
                filename=True,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Argument(
                ["gene_def_file", "ref_gene_file"],
                "Gene Def File",
                is_required=True,
                filename=True
            ),
            _Argument(
                ["fasta_ref_file", "ref_fasta_file"],
                "Ref Fasta File",
                filename=True,
                is_required=True
            )
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
