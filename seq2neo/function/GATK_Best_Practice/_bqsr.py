import subprocess as sp


class BQSR:
    def __init__(self, ref, Input, known_sites, out_bam, java_options):

        self.ref = ref
        self.Input = Input
        self.known_sites = known_sites
        self.RecalData = out_bam + ".recal_data.table"
        self.out_bam = out_bam
        self.java_options = java_options
        self.need_files = self.known_sites.copy()
        self.need_files.extend([self.ref, self.Input, self.RecalData, self.java_options])

    def baserecalibrator(self):

        if len(self.known_sites) < 1:
            print("At least one known site file")
        else:
            baserecalibrator_cmd = ("gatk BaseRecalibrator"
                                    + " --known-sites %s" * len(self.known_sites)
                                    + " -R %s -I %s"
                                    + " -O %s"
                                    + " --java-options %s 1>/dev/null") % tuple(self.need_files)
            # print("Running " + baserecalibrator_cmd)

            sp.check_call(baserecalibrator_cmd, shell=True, stdout=sp.DEVNULL)

    def applybqsr(self):
        applybqsr_cmd = f"gatk ApplyBQSR" \
                        + f" -R {self.ref} -I {self.Input}" \
                        + f" --bqsr-recal-file {self.RecalData}" \
                        + f" -O {self.out_bam}" \
                        + f" --java-options {self.java_options} 1>/dev/null"
        # print("Running " + applybqsr_cmd)
        sp.check_call(applybqsr_cmd, shell=True, stdout=sp.DEVNULL)
