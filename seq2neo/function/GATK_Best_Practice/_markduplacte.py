from Bio.Application import _Option
from Bio.Application import AbstractCommandline
from Bio.Application import _StaticArgument


class MarkDuplicatesCommandline(AbstractCommandline):
	"""Command line wrapper for gatk MarkDuplicatesSpark
	Extract/print all or sub alignments"""
	def __init__(self, cmd="gatk", **kwargs):
		self.program_name = cmd
		self.parameters = [
			_StaticArgument("MarkDuplicates"),
			_Option(
				["-I", "I"],
				"BAM/SAM/CRAM file containing reads, Must be coordinate sorted.",
				filename=True,
				equate=False,
				is_required=True
			),
			_Option(
				["-O", "O"],
				"the output bam",
				filename=True,
				equate=False,
				is_required=True
			),
			_Option(
				["-M", "M"], "File to write duplication metrics to",
				filename=True,
				equate=False,
				is_required=True
			),
			_Option(
				["--VALIDATION_STRINGENCY", "VALIDATION_STRINGENCY"],
				"""Validation stringency for all SAM/BAM/CRAM/SRA files read by this program. 
				The default stringency value SILENT can improve performance when processing a BAM file 
				in which variable-length data (read, qualities, tags) do not otherwise need to be decoded.

				STRICT
				LENIENT
				SILENT
				
				default is SILENT""",

				equate=False
			),
			_Option(
				["-MAX_FILE_HANDLES", "MAX_FILE_HANDLES"],
				"If true, create a BAM index when writing a coordinate-sorted BAM file.",
				equate=False,
				checker_function=lambda x:isinstance(x, int)
			),
			_Option(
				["--CREATE_INDEX", "CREATE_INDEX"],
				"Whether to create a BAM index when writing a coordinate-sorted BAM file.",
				equate=False
			),
			_Option(
				["--java-options", "java_options"],
				"set config for java",
				equate=False
			),
		]
		AbstractCommandline.__init__(self, cmd, **kwargs)
