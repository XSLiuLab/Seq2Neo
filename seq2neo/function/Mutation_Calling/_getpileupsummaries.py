from Bio.Application import AbstractCommandline
from Bio.Application import _Option, _StaticArgument


class GetPileupSummariesCommandline(AbstractCommandline):
    def __init__(self, cmd="gatk", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _StaticArgument("GetPileupSummaries"),
            _Option(
                ["-I", "I"],
                "BAM/SAM/CRAM file containing reads",
                filename=True,
                is_required=True,
                equate=False
            ),
            _Option(
                ["-L", "L"],
                "One or more genomic intervals over which to operate",
                filename=True,
                is_required=True,
                equate=False
            ),
            _Option(
                ["-O", "O"],
                "The output table",
                filename=True,
                is_required=True,
                equate=False
            ),
            _Option(
                ["-V", "V"],
                "A VCF file containing variants and allele frequencies",
                is_required=True,
                filename=True,
                equate=False
            ),
            _Option(
                ["--java-options", "java_options"],
                "set config for java",
                equate=False
            ),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
