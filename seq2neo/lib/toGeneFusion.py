import os
import pandas as pd
from seq2neo.function import *
from seq2neo.function.STAT_Fusion import *
from seq2neo.function.Agfusion import *


def toGeneFusion_rna(args, tmpPATH, resultsPATH):

    print("Executing Tumor RNA Fastp Command Line")
    rna_out1 = os.path.join(tmpPATH, "rna_1_qc.fastq")
    rna_out2 = os.path.join(tmpPATH, "rna_2_qc.fastq")
    rna_json = os.path.join(tmpPATH, "rna.json")
    rna_html = os.path.join(tmpPATH, "rna.html")

    rna_fastp_cmd = FastpCommandline(i=args.tumor_rna[0],
                                     I=args.tumor_rna[1],
                                     o=rna_out1,
                                     O=rna_out2,
                                     j=rna_json,
                                     h=rna_html,
                                     w=args.threadN)
    rna_fastp_cmd()

    print("Executing STAR-Fusion Command Line")
    output = os.path.join(tmpPATH, 'star_fusion_outdir')
    star_fusion_cmd = StarFusionCommandLine(left_fq=rna_out1,
                                            right_fq=rna_out2,
                                            genome_lib_dir=args.genome_lib_dir,
                                            output_dir=output,
                                            CPU=args.threadN)
    star_fusion_cmd()

    print("Executing AgFusion Command Line")
    filepath = os.path.join(output, 'star-fusion.fusion_predictions.abridged.tsv')
    df = pd.read_csv(filepath, sep="\t")
    df = df.loc[:, ["#FusionName", "JunctionReadCount", "SpanningFragCount", "SpliceType", "LeftGene", "LeftBreakpoint",
                    "RightGene", "RightBreakpoint", "LargeAnchorSupport"]]  # 将数据整理成AGfusion接受的形式
    df.to_csv(filepath, sep='\t', index=False)

    outpath = os.path.join(resultsPATH, 'agfusion_dir')
    agfusion_cmd = AGFusionCommandLine(file=filepath,
                                       algorithm='starfusion',
                                       database=args.agfusion_db,
                                       out=outpath,
                                       middlestar="middlestar")
    agfusion_cmd()
