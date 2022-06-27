from Bio.Application import _Option, AbstractCommandline


class FastpCommandline(AbstractCommandline):
    """Command line wrapper for Fastp
    Run a Fastp alignment, with single- or paired-end reads, equivalent to::
        $ fastp -i in.fq -o out.fq
        $ fastp -i in.R1.fq.gz -I in.R2.fq.gz -o out.R1.fq.gz -O out.R2.fq.gz
    See https://github.com/OpenGene/fastp for details.

    """

    def __init__(self, cmd="fastp", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _Option(
                ["-i", "i"],
                "read1 input file name",
                filename=True,
                is_required=True,
                equate=False,
            ),
            _Option(
                ["-o", "o"],
                "read1 output file name",
                filename=True,
                is_required=True,
                equate=False,
            ),
            _Option(["-I", "I"], "read2 input file name", equate=False),
            _Option(["-O", "O"], "read2 output file name", equate=False),
            _Option(
                ["-j", "j"],
                "the json format report file name (string [=fastp.json])",
                equate=False,
            ),
            _Option(
                ["-h", "h"],
                "the html format report file name (string [=fastp.html])",
                equate=False,
            ),
            _Option(
                ["-w", "w"],
                "worker thread number, default is 3 (int [=3])",
                equate=False,
            )
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
