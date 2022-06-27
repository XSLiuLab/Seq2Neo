from Bio.Application import AbstractCommandline
from Bio.Application import _Option, _StaticArgument, _Argument


class SortBamCommandline(AbstractCommandline):
    """Command line wrapper for GATK Best Practice

    SortSam or SortBam
    
    $ gatk SortSam \
        INPUT=input.bam \
        OUTPUT=sorted.bam \
        SORT_ORDER=coordinate

    See https://gatk.broadinstitute.org/hc/en-us/articles/360036510732-SortSam-Picard- for details.
    """

    def __init__(self, cmd="gatk", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _StaticArgument("SortSam"),
            _Option(
                ["-I", "I"],
                "Input BAM or SAM file to sort.  Required.",
                is_required=True,
                filename=True,
                equate=False
            ),
            _Option(
                ["-O", "O"],
                "Sorted BAM or SAM output file.  Required.",
                is_required=True,
                filename=True,
                equate=False
            ),
            _Option(
                ["-SO", "SO"],
                "Sort order of output file.  Required.",
                is_required=True,
                equate=False
            ),
            _Option(
                ["--java-options", "java_options"],
                "set config for java",
                equate=False
            ),
            _Option(
                ["--CREATE_INDEX", "CREATE_INDEX"],
                "Whether to create a BAM index when writing a coordinate-sorted BAM file.",
                equate=False
            )
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)


class SortBam_Commandline(AbstractCommandline):
    """Command line wrapper for samtools sort
    """

    def __init__(self, cmd="samtools", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _StaticArgument("sort"),
            _Option(
                ["--threads", "threads"],
                "Number of additional threads to use [0]",
                equate=False,
                checker_function=lambda x: isinstance(x, int),
            ),
            _Option(
                ["-o", "o"],
                "Output file",
                filename=True,
                equate=False,
                checker_function=lambda x: isinstance(x, str),
            ),
            _Argument(
                ["-i", "i"],
                "Input file",
                filename=True,
                checker_function=lambda x: isinstance(x, str),
            ),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)


class IndexBam_Commandline(AbstractCommandline):
    """Command line wrapper for samtools sort
    """

    def __init__(self, cmd="samtools", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _StaticArgument("index"),
            _Option(
                ["-@", "threads"],
                "Number of additional threads to use [0]",
                equate=False,
                checker_function=lambda x: isinstance(x, int),
            ),
            _Argument(
                ["-i", "i"],
                "Input file",
                filename=True,
                checker_function=lambda x: isinstance(x, str),
            ),
            _Argument(
                ["-o", "o"],
                "Output file",
                filename=True,
                checker_function=lambda x: isinstance(x, str),
            ),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
