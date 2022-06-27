from Bio.Application import _Option
from Bio.Application import AbstractCommandline


class StarFusionCommandLine(AbstractCommandline):
    """STAR-Fusion command line detail: https://github.com/STAR-Fusion/STAR-Fusion/wiki"""

    def __init__(self, cmd="STAR-Fusion", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _Option(
                ["--left_fq", "left_fq"],
                "Read 1",
                equate=False,
                checker_function=lambda x: isinstance(x, str),
                filename=True,
                is_required=True
            ),
            _Option(
                ["--right_fq", "right_fq"],
                "Read 2",
                equate=False,
                checker_function=lambda x: isinstance(x, str),
                filename=True,
            ),
            _Option(
                ["--genome_lib_dir", "genome_lib_dir"],
                "directory containing genome lib",
                equate=False,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Option(
                ["--output_dir", "output_dir"],
                "output directory",
                equate=False,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Option(
                ["--CPU", "CPU"],
                "number of threads for running STAR (default: 4)",
                equate=False,
                checker_function=lambda x: isinstance(x, int)
            ),
        ]

        AbstractCommandline.__init__(self, cmd, **kwargs)
