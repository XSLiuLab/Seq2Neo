import os
from seq2neo.function.Neoantigen_Prediction import *


def toFasta_annovar(args, resultsPATH):
    uncovert_vcf = os.path.join(resultsPATH, 'pass.recode.vcf')  # 从toVCF.py而来
    output_prefix = os.path.join(resultsPATH, 'variant')

    # Convert to Annovar input files
    print("Executing AnnovarConvert Command Line")
    covert_cmd = AnnovarConvertCommandline(
        input_file=uncovert_vcf,
        format="vcf4",
        filter="pass",
        allsample="allsample",
        outfile=output_prefix
    )
    covert_cmd()

    # Annotation with Annovar
    print("Executing AnnovarAnnotation Command Line")
    inputfile_name = 'variant.' + args.tumor_name + '.avinput'
    annotation_file = os.path.join(resultsPATH, inputfile_name)
    prefix = os.path.join(resultsPATH, args.tumor_name)
    annotation_cmd = AnnovarAnnotationCommandline(
        input=annotation_file,
        geneanno="geneanno",
        buildver="hg38",
        comment="comment",
        outfile=prefix,
        db=args.annovar_db_dir
    )
    annotation_cmd()

    # get coding change
    print("Executing GetCodingChange Command Line")
    coding_input = os.path.join(resultsPATH, args.tumor_name + '.exonic_variant_function')
    ref_gene_txt = os.path.join(args.annovar_db_dir, 'hg38_refGene.txt')
    ref_fasta_file = os.path.join(args.annovar_db_dir, 'hg38_refGeneMrna.fa')
    out = os.path.join(resultsPATH, args.tumor_name + '.fasta')
    out_mrna = os.path.join(resultsPATH, args.tumor_name + '_mrna.fasta')

    # protein sequence
    coding_change_cmd = GetCodingChangeCommandline(
        input=coding_input,
        ref_gene_file=ref_gene_txt,
        ref_fasta_file=ref_fasta_file,
        onlyAltering="onlyAltering",
        includesnp="includesnp"
    )
    coding_change_cmd(stdout=out)

    # mrna sequence
    coding_change_mrna_cmd = GetCodingChangeCommandline(
        input=coding_input,
        ref_gene_file=ref_gene_txt,
        ref_fasta_file=ref_fasta_file,
        mrnaseq="mrnaseq",
        codingseq="codingseq",
        onlyAltering="onlyAltering",
        includesnp="includesnp",
    )
    coding_change_mrna_cmd(stdout=out_mrna)

    # make a dictionary
    createDictionary(Input_File=coding_input, Output_File=os.path.join(resultsPATH, 'dictionary.txt'))

    # format conversion
    reformat_fatsa(InFasta=out)

    # 会输出一个dictionary_wt_mt.txt字典，后续会用到
    reformated_fasta = out.replace(".fasta", "_pre.fasta")
    MakePeptideFasta(reformated_fasta, Peptide_Len=args.len, dic_path=resultsPATH)

    # make a mrna dictionary
    reformat_fatsa(InFasta=out_mrna)  # seqIO模块特殊需求
    reformated_mrna_fasta = out_mrna.replace(".fasta", "_pre.fasta")
    createDictionary_mrna(reformated_mrna_fasta, resultsPATH, os.path.join(resultsPATH, 'dictionary_wt_mt.txt'), args.len)
