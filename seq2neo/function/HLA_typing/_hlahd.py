from Bio.Application import _Option, _Argument
from Bio.Application import AbstractCommandline


class HLAHDCommandLine(AbstractCommandline):
    """HLA-HD command line detail: https://www.genome.med.kyoto-u.ac.jp/HLA-HD/"""

    def __init__(self, cmd="hlahd.sh", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _Option(
                ["-t", "t"],
                "Thread",
                equate=False,
                checker_function=lambda x: isinstance(x, int),
                is_required=False
            ),
            _Option(
                ["-c", "c"],
                "rate_of_cutting",
                equate=False,
                is_required=False
            ),
            _Option(
                ["-m", "m"],
                "minmum_tag_size",
                is_required=False,
                equate=False
            ),
            _Option(
                ["-n", "n"],
                "number of mismatch",
                equate=False,
                is_required=False
            ),
            _Option(
                ["-f", "f"],
                "freq_dir",
                is_required=True,
                equate=False,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Option(
                ["-N", "N"],
                "size of ambiguous charactor",
                is_required=False,
                equate=False
            ),
            _Argument(
                ["--fasta_file1", "fasta_file1"],
                "Input File1 Name",
                is_required=True,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Argument(
                ["--fasta_file2", "fasta_file2"],
                "Input File2 Name",
                is_required=False,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Argument(
                ["--gene_split", "gene_split_file"],
                "Gene Split File",
                is_required=True,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Argument(
                ["--HLA_fasta_dir", "HLA_fasta_dir"],
                "HLA Fasta Dictionary",
                is_required=True,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Argument(
                ["--sampleID", "sampleID"],
                "Sample ID",
                checker_function=lambda x: isinstance(x, str)
            ),
            _Argument(
                ["--out_dir", "out_dir"],
                "Output Directory",
                is_required=True,
                checker_function=lambda x: isinstance(x, str)
            )
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
