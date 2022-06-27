from Bio.Application import AbstractCommandline
from Bio.Application import _Option, _Argument, _Switch
from Bio.Application import _StaticArgument


class SamtoolsViewCommandline_thread(AbstractCommandline):
    """Command line wrapper for samtools view.
    Extract/print all or sub alignments in SAM or BAM format, equivalent to::
        $ samtools view [-bchuHS] [-t in.refList] [-o output] [-f reqFlag]
                        [-F skipFlag] [-q minMapQ] [-l library] [-r readGroup]
                        [-R rgFile] <in.bam>|<in.sam> [region1 [...]]
    See http://samtools.sourceforge.net/samtools.shtml for more details
    """

    def __init__(self, cmd="samtools", **kwargs):
        """Initialize the class."""
        self.program_name = cmd
        self.parameters = [
            _StaticArgument("view"),
            _Switch(["-b", "b"], "Output in the BAM format"),
            _Switch(
                ["-c", "c"],
                """Instead of printing the alignments, only count them and
                    print the total number.
                    All filter options, such as '-f', '-F' and '-q',
                    are taken into account""",
            ),
            _Switch(["-h", "h"], "Include the header in the output"),
            _Switch(
                ["-u", "u"],
                """Output uncompressed BAM.
                    This option saves time spent on compression/decompression
                    and is thus preferred when the output is piped to
                    another samtools command""",
            ),
            _Switch(["-H", "H"], "Output the header only"),
            _Switch(
                ["-S", "S"],
                """Input is in SAM.
                    If @SQ header lines are absent,
                    the '-t' option is required.""",
            ),
            _Option(
                ["-t", "t"],
                """This file is TAB-delimited.
                    Each line must contain the reference name and the
                    length of the reference, one line for each
                    distinct reference; additional fields are ignored.
                    This file also defines the order of the reference
                    sequences in sorting.
                    If you run   'samtools faidx <ref.fa>',
                    the resultant index file <ref.fa>.fai can be used
                    as this <in.ref_list> file.""",
                filename=True,
                equate=False,
                checker_function=lambda x: isinstance(x, str),
            ),
            _Option(
                ["-o", "o"],
                "Output file",
                filename=True,
                equate=False,
                checker_function=lambda x: isinstance(x, str),
            ),
            _Option(
                ["-f", "f"],
                """Only output alignments with all bits in
                    INT present in the FLAG field""",
                equate=False,
                checker_function=lambda x: isinstance(x, int),
            ),
            _Option(
                ["-F", "F"],
                "Skip alignments with bits present in INT",
                equate=False,
                checker_function=lambda x: isinstance(x, int),
            ),
            _Option(
                ["-q", "q"],
                "Skip alignments with MAPQ smaller than INT",
                equate=False,
                checker_function=lambda x: isinstance(x, int),
            ),
            _Option(
                ["-r", "r"],
                "Only output reads in read group STR",
                equate=False,
                checker_function=lambda x: isinstance(x, str),
            ),
            _Option(
                ["-R", "R"],
                "Output reads in read groups listed in FILE",
                filename=True,
                equate=False,
                checker_function=lambda x: isinstance(x, str),
            ),
            _Option(
                ["-l", "l"],
                "Only output reads in library STR",
                equate=False,
                checker_function=lambda x: isinstance(x, str),
            ),
            _Option(
                ["--threads", "threads"],
                "Number of additional threads to use [0]",
                equate=False,
                checker_function=lambda x: isinstance(x, int),
            ),
            _Switch(
                ["-1", "fast_bam"],
                "Use zlib compression level 1 to compress the output",
            ),
            _Argument(
                ["input", "input_file"],
                "Input File Name",
                filename=True,
                is_required=True,
            ),
            _Argument(["region"], "Region", is_required=False),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
