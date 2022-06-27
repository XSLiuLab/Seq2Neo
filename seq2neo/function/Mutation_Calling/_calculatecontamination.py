from Bio.Application import _Option, _StaticArgument
from Bio.Application import AbstractCommandline


class CalculateContaminationCommandline(AbstractCommandline):
    """
	Command line wrapper for GATK CalculateContamination
    Run a CalculateContamination alignment, equivalent to:

    Tumor only mode
        $ gatk CalculateContamination \
                -I pileups.table \
                -O contamination.table
    Matched normal mode
        $ gatk CalculateContamination \
            -I tumor-pileups.table \
            -matched normal-pileups.table \
            -O contamination.table
    See https://gatk.broadinstitute.org/hc/en-us/articles/360036888972-CalculateContamination for details.
	"""

    def __init__(self, cmd="gatk", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _StaticArgument("CalculateContamination"),
            _Option(
                ["-I", "I"],
                "The input table",
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
                ["-matched", "matched"],
                "The matched normal input table",
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
