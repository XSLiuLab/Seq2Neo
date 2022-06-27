from Bio.Application import _Option, _StaticArgument, _Switch
from Bio.Application import AbstractCommandline


class AGFusionCommandLine(AbstractCommandline):
    """AGFusion command line detail: https://github.com/murphycj/AGFusion#installation"""

    def __init__(self, cmd="agfusion", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _StaticArgument("batch"),
            _Option(
                ["--file", "file"],
                "Output file from fusion-finding algorithm.",
                equate=False,
                checker_function=lambda x: isinstance(x, str),
                filename=True,
                is_required=True
            ),
            _Option(
                ["--algorithm", "algorithm"],
                """The fusion-finding algorithm. Can be one of the + 
                    following: bellerophontes, breakfusion, chimerascan, +
                    chimerscope, defuse, ericscript, fusioncatcher, +
                    fusionhunter, fusionmap, fusioninspector, infusion, +
                    jaffa, mapsplice, starfusion, tophatfusion.""",
                equate=False,
                checker_function=lambda x: isinstance(x, str),
            ),
            _Option(
                ["--database", "database"],
                "Path to the AGFusion database",
                equate=False,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Option(
                ["--out", "out"],
                "Directory to save results",
                equate=False,
                checker_function=lambda x: isinstance(x, str)
            ),
            _Switch(
                ["--middlestar", "middlestar"],
                "Insert a * at the junction position for the cdna, cds, and protein sequences (default False)."
            ),
        ]

        AbstractCommandline.__init__(self, cmd, **kwargs)
