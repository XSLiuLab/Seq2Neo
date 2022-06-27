from Bio.Application import AbstractCommandline
from Bio.Application import _Option, _Switch


class NetCTLpanCommandLine(AbstractCommandline):
    """
    Command line wrapper for NetCTLpan-1.1
    prediction of peptides binding to specified MHC molecules
    see https://services.healthtech.dtu.dk/service.php?NetCTLpan-1.1 for more details
    """

    def __init__(self, cmd="netCTLpan", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _Option(
                ["-f", "f"],
                "File name with input",
                filename=True,
                equate=False
            ),
            _Switch(
                ["-xls", "xls"],
                "Save output to xls file"
            ),
            _Option(
                ["-a", "a"],
                "HLA allele",
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
