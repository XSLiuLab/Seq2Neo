from Bio.Application import _Option, _StaticArgument
from Bio.Application import AbstractCommandline


class FilterMutectCallsCommandline(AbstractCommandline):
    '''
	text
	'''

    def __init__(self, cmd="gatk", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _StaticArgument("FilterMutectCalls"),
            _Option(
                ["-V", "V"],
                "A VCF file containing variants",
                filename=True,
                is_required=True,
                equate=False
            ),
            _Option(
                ["-O", "O"],
                "The output filtered VCF file",
                is_required=True,
                filename=True,
                equate=False
            ),
            _Option(
                ["-R", "R"],
                "Reference sequence file",
                is_required=True,
                filename=True,
                equate=False
            ),
            _Option(
                ["--contamination-table",
                 "contamination"],
                "Tables containing contamination information.",
                filename=True,
                equate=False
            ),
            _Option(
                ["-ob-priors", "ob_priors"],
                "One or more .tar.gz files \n" +
                "containing tables of prior artifact probabilities \n" +
                "for the read orientation filter model, \n" +
                "one table per tumor sample",
                filename=True,
                equate=False
            ),
            _Option(
                ["--min-allele-fraction",
                 "min_allele_fraction"],
                "Minimum allele fraction required",
                equate=False
            ),
            _Option(
                ["--java-options", "java_options"],
                "set config for java",
                equate=False
            ),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
