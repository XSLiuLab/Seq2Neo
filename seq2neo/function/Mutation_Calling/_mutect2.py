import subprocess as sp


class Mutect2Commandline:
    def __init__(self, ref, Input, Output, f1r2_gz_file, threads, java_options, germline_resource, pon, Normal_name=None):
        self.ref = ref
        self.Input = Input
        self.Ouput = Output
        self.need_files = Input.copy()
        self.normal_name = Normal_name
        self.f1r2 = f1r2_gz_file
        self.java_options = java_options
        self.threads = threads
        self.germline_resource = germline_resource
        self.pon = pon
        if self.normal_name:
            self.need_files.extend([self.ref, self.Ouput, self.normal_name, self.f1r2, 
                                    self.germline_resource, self.pon, self.threads, self.java_options])
            self.mutect2_cmd = ("gatk Mutect2"
                                + " -I %s" * len(Input)
                                + " -R %s"
                                + " -O %s"
                                + " -normal %s"
                                + " --f1r2-tar-gz %s"
                                + " --germline-resource %s"
                                + " --panel-of-normals %s"
                                + " --native-pair-hmm-threads %s"
                                + " --java-options %s") % tuple(self.need_files)
        else:
            self.need_files.extend([self.ref, self.Ouput, self.f1r2, self.germline_resource, self.pon, self.threads, self.java_options])
            self.mutect2_cmd = ("gatk Mutect2"
                                + " -I %s" * len(Input)
                                + " -R %s"
                                + " -O %s"
                                + " --f1r2-tar-gz %s"
                                + " --germline-resource %s"
                                + " --panel-of-normals %s"
                                + " --native-pair-hmm-threads %s"
                                + " --java-options %s") % tuple(self.need_files)

    def __str__(self):
        return self.mutect2_cmd

    def run_mutect2(self):
        sp.check_call(self.mutect2_cmd, shell=True, stdout=sp.DEVNULL)
