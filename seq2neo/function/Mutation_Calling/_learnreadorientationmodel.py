from Bio.Application import _Option, _StaticArgument
from Bio.Application import AbstractCommandline


class LearnReadOrientationModelCommandline(AbstractCommandline):
    """
	Learn the prior probability of read orientation artifact
	from the output of CollectF1R2Counts of Mutect2
	Details of the model may be found in :
	https://gatk.broadinstitute.org/hc/en-us/articles/360051305331-LearnReadOrientationModel
	"""

    def __init__(self, cmd="gatk", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _StaticArgument("LearnReadOrientationModel"),
            _Option(
                ["-I", "I"],
                "One or more .tar.gz containing outputs of CollectF1R2Counts",
                filename=True,
                is_required=True,
                equate=False
            ),
            _Option(
                ["-O", "O"],
                "tar.gz of artifact prior tables",
                filename=True,
                is_required=True,
                equate=False
            ),
            _Option(
                ["--java-options", "java_options"],
                "set config for java",
                equate=False
            ),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
