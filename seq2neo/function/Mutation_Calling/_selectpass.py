from Bio.Application import _Option, _Switch
from Bio.Application import AbstractCommandline


class SelectPassMutationCommandline(AbstractCommandline):

    def __init__(self, cmd="vcftools", **kwargs):
        self.program_name = cmd
        self.parameters = [
            _Option(
                ["--vcf", "vcf"],
                "This option defines the VCF file to be processed.",
                filename=True,
                equate=False,
                is_required=True
            ),
            _Switch(
                ["--remove-filtered-all",
                 "remove_filtered_all"],
                "Removes all sites with a FILTER flag other than PASS.",
            ),
            _Option(
                ["--out", "out"],
                "This option defines the output filename prefix for all files generated by vcftools.",
                filename=True,
                equate=False,
                is_required=True
            ),
            _Switch(
                ["--recode-INFO-all",
                 "recode_INFO_all"],
                "recode_INFO_all"
            ),
            _Switch(
                ["--recode", "recode"],
                "recode"
            ),
        ]
        AbstractCommandline.__init__(self, cmd, **kwargs)
