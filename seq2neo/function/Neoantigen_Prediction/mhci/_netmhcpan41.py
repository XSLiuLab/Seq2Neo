from Bio.Application import AbstractCommandline
from Bio.Application import _Option, _Switch


class NetMHCpan41CommandLine(AbstractCommandline):
    """
    Command line wrapper for NetMHCpan-4.1
    prediction of peptides binding to specified MHC molecules
    see https://services.healthtech.dtu.dk/service.php?NetMHCpan-4.1 for more details
    """

    def __init__(self, cmd="netMHCpan", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _Option(
                ["-f", "f"],
                "File name with input",
                filename=True,
                equate=False
            ),
            _Option(
                ["-p", "p"],
                "Use peptide input",
                filename=True,
                equate=False
            ),
            _Switch(
                ["-BA", "BA"],
                "Include Binding affinity prediction",
            ),
            _Switch(
                ["-s", "s"],
                "Sort output on descending affinity"
            ),
            _Switch(
                ["-xls", "xls"],
                "Save output to xls file"
            ),
            _Option(
                ["-a", "a"],
                "MHC allele",
                equate=False
            ),
            _Option(
                ["-l", "l"],
                "peptide length",
                equate=False
            ),
            _Option(
                ["-xlsfile", "xlsfile"],
                "Filename for xls dump",
                filename=True,
                equate=False
            )
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
