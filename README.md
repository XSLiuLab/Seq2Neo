# Seq2Neo: a comprehensive pipeline for cancer neoantigen immunogenicity prediction

## Overview
Neoantigens derived from somatic DNA alterations are ideal cancer specific targets. However, not all somatic DNA mutations can cause immunogenicity to cancer cell, and efficient tools for predicting the immunogenicity of neo-peptide is still urgently needed. Here we present the **Seq2Neo** pipeline, which provides a one-stop solution for neo-peptide features prediction with HLA class I from raw sequencing data, and neoantigens derived from different types of genome DNA alterations, including point mutations, insertion deletions, and gene fusions are supported. Importantly a convolutional neural networks (CNN) based model has been trained to predict the immunogenicity of neoepitope. And this model shows improved performance compared with currently available tools in immunogenicity prediction in independent datasets.

## Installation:
Seq2Neo runs on Linux operation, and it is an open source software under academic free license (AFL) v3.0.

### Conda

We strongly recommend that you use conda command line for installation as this will solve dependencies automatically. The web of the package is https://anaconda.org/liuxslab/seq2neo. 

1. Firstly, you need to install [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html#) (recommended). 

2. Secondly, you should execute the following command to create a new environment named Seq2Neo or other on your system, and then activate it:

   ``` shell
   conda create -n Seq2Neo
   conda activate Seq2Neo
   ```

3. Thirdly, you can install the package through the following conda command:

   ```shell
   conda install -c liuxslab seq2neo
   ```

4. Finally, please installation of following packages manually due to the reason of permission or others:

   - Annovar == latest  [ANNOVAR website (openbioinformatics.org)](https://www.openbioinformatics.org/annovar/annovar_download_form.php)
   - HLAHD == 1.4.0  [HLA-HD (kyoto-u.ac.jp)](https://www.genome.med.kyoto-u.ac.jp/HLA-HD/)
   - netCTLpan == 1.1.b [NetCTLpan - 1.1 - Services - DTU Health Tech](https://services.healthtech.dtu.dk/service.php?NetCTLpan-1.1)
   - netMHCpan == 4.1.b  [NetMHCpan - 4.1 - Services - DTU Health Tech](https://services.healthtech.dtu.dk/service.php?NetMHCpan-4.1)
   - STAR-Fusion == 1.10.1 [STAR-Fusion/STAR-Fusion: STAR-Fusion codebase (github.com)](https://github.com/STAR-Fusion/STAR-Fusion)
   
   Please following corresponding official instructions to install those packages on your system.

### Docker

stand by

### Pip (not recommended)

You can install the stable release of **Seq2Neo** with:

> pip install Seq2Neo

However, you should install all of dependencies manually. It includes the following softwares and packages that should be installed in advance:

``` plain
- bamtools=2.5.1
- bwa=0.7.17
- fastp=0.23.2
- perl=5.26.2=h470a237_0
- samtools=1.15.1
- star=2.7.8a
- tpmcalculator=0.0.4
- vcftools=0.1.16
- Bowtie2 == 2.3.5
- GATK == 4.2.5
```

Then, you should also install packages mentioned in the Conda section.

## Usage

Seq2Neo consists of 3 modules, which are whole, download and immuno. The module of whole is responsible for running the whole process, download module can download specified version of reference genome from ensembl database and index, the last module of immuno supports the prediction of immunogenicity score of specified peptides and MHCs:

``` plain
usage: seq2neo [-h] {whole,immuno,download} ...

A pipeline from mutation to neoantigen prediction

positional arguments:
  {whole,immuno,download}
    whole               Run whole pipeline (Seq2Neo) with fastq/bam/sam file
    immuno              Run immunogenicity prediction with peptides
    download            downloading reference genome

optional arguments:
  -h, --help            show this help message and exit

Thanks for using Seq2Neo
```

-----------------------

**The module of whole:**

```plain
usage: seq2neo whole [-h] [--data-type {sort_bam,sam,fastq}] --ref
                     path_to_reference
                     [--normal-dna normal_dna_1.fq normal_dna_2.fq]
                     [--tumor-dna tumor_dna_1.fq tumor_dna_2.fq] --tumor-rna
                     tumor_rna_1.fq tumor_rna_2.fq [--normal-sam normal.sam]
                     [--tumor-sam tumor.sam]
                     [--normal-sorted-bam normal_sorted.bam]
                     [--tumor-sorted-bam tumor_sorted.bam] --normal-name
                     normal_name --tumor-name tumor_name --known-site-dir
                     known_site_dir --mutect2-dataset-dir mutect2_dataset_dir
                     --annovar-db-dir annovar_db_dir --genome-lib-dir
                     genome_lib_dir --agfusion-db agfusion_db [--out out_dir]
                     [--len [LEN [LEN ...]]] [--threadN thread_num]
                     [--mdna min_length] [--mrna min_length]
                     [--java-options java_options] --hlahd-dir hlahd_dir
                     [--hla [HLA [HLA ...]]]

Run whole pipeline (Seq2Neo) with fastq/bam file

optional arguments:
  -h, --help            show this help message and exit
  --data-type {sort_bam,sam,fastq}
                        Select your input file format(fastq/sam/sort_bam),
                        default:fastq (default: fastq)
  --ref path_to_reference
                        Path to reference genomic data (default: None)
  --normal-dna normal_dna_1.fq normal_dna_2.fq
                        Normal sample files (default: None)
  --tumor-dna tumor_dna_1.fq tumor_dna_2.fq
                        Tumor dna sample files (default: None)
  --tumor-rna tumor_rna_1.fq tumor_rna_2.fq
                        Tumor rna sample files (default: None)
  --normal-sam normal.sam
                        Normal dna sam files (default: None)
  --tumor-sam tumor.sam
                        Tumor dna sam files (default: None)
  --normal-sorted-bam normal_sorted.bam
                        Normal dna sorted bam files (default: None)
  --tumor-sorted-bam tumor_sorted.bam
                        Tumor dna sorted bam files (default: None)
  --normal-name normal_name
                        if the file is XXX_1.fq, the normal name should be XXX
                        (default: None)
  --tumor-name tumor_name
                        if the file is XXX_1.fq, the tumor name should be XXX
                        (default: None)
  --known-site-dir known_site_dir
                        directory to BQSR known site (default: None)
  --mutect2-dataset-dir mutect2_dataset_dir
                        directory to mutect2 needed dataset file (default:
                        None)
  --annovar-db-dir annovar_db_dir
                        directory to annovar database (default: None)
  --genome-lib-dir genome_lib_dir
                        directory containing genome lib (see http://STAR-
                        Fusion.github.io) (default: None)
  --agfusion-db agfusion_db
                        Path to the AGFusion database (default: None)
  --out out_dir         Output directory to save prediction results, default
                        is current directory (default: .)
  --len [LEN [LEN ...]]
                        length of peptides, default is 8 9 10 11 (default: (8,
                        9, 10, 11))
  --threadN thread_num  the number of thread used in Seq2Neo, default is 4
                        (default: 4)
  --mdna min_length     length of reads(normal dna) (default: 100)
  --mrna min_length     length of reads(rna) (default: 100)
  --java-options java_options
                        set config for java (default: -Xmx8G)
  --hlahd-dir hlahd_dir
                        the path to hlahd software (default: None)
  --hla [HLA [HLA ...]]
                        if you use bam and sorted sam as input, please provide
                        hlas, like--hla HLA-A01:01 HLA-A03:03 (default:
                        HLA-A01:01)
```



-----------------------

**The module of download:**

``` plain
usage: seq2neo download [-h] [--species SPECIES] [--build BUILD]
                        [--release RELEASE] [--dir [DIR]]

Run download module

optional arguments:
  -h, --help         show this help message and exit
  --species SPECIES  which species to download (default: homo_sapiens)
  --build BUILD      which build to download (default: GRCh38)
  --release RELEASE  which release to download (default: 105)
  --dir [DIR]        where to store (default: .)
```

-------------

**The module of immuno:**

```
usage: seq2neo immuno [-h] [--mode MODE] [--epitope EPITOPE] [--hla HLA]
                      [--inputfile INPUTFILE] [--outdir OUTDIR]

Seq2Neo-CNN command line(one part of Seq2Neo)

optional arguments:
  -h, --help            show this help message and exit
  --mode MODE           single mode or multiple mode (default: single)
  --epitope EPITOPE     if single mode, specifying your epitope (default:
                        SVQIISCQY)
  --hla HLA             if single mode, specifying your HLA allele (default:
                        HLA-A30:02)
  --inputfile INPUTFILE
                        if multiple mode, specifying the path to your input
                        file (default: None)
  --outdir OUTDIR       if multiple mode, specifying the path to your output
                        folder (default: None)
```

