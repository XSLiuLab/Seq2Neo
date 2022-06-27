from Bio.Application import _Option, _Switch
from Bio.Application import AbstractCommandline


class TPMCalculatorCommandLine(AbstractCommandline):
    """TPMCalculator command line detail: https://github.com/ncbi/TPMCalculator"""

    def __init__(self, cmd="TPMCalculator", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _Option(
                ["-g", "g"],
                "GTF File",
                equate=False,
                checker_function=lambda x: isinstance(x, str),
                filename=True,
            ),
            _Option(
                ["-b", "b"],
                "BAM File",
                equate=False,
                checker_function=lambda x: isinstance(x, str),
                filename=True,
            ),
            _Option(
                ["-c", "c"],
                "Smaller size allowed for an intron created for genes. Default: 16. We recommend to use the reads "
                "length",
                equate=False,
                checker_function=lambda x: isinstance(x, int)
            ),
            _Switch(
                ["-p", "p"],
                "Use only properly paired reads. Default: No. Recommended for paired-end reads.",
            ),
            _Option(
                ["-k", "k"],
                "Gene key to use from GTF file. Default: gene_id",
                equate=False,
                checker_function=lambda x: isinstance(x, str)
            ),
        ]

        AbstractCommandline.__init__(self, cmd, **kwargs)
