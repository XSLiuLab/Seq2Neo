# Seq2Neo: a comprehensive pipeline for cancer neoantigen immunogenicity prediction

## Overview

Neoantigens derived from somatic DNA alterations are ideal cancer-specific targets. However, not all somatic DNA mutations can result in immunogenicity in cancer cells, and efficient tools for predicting the immunogenicity of neoepitope are still urgently needed. Here we present the Seq2Neo pipeline, which provides a one-stop solution for neoepitope features prediction from raw sequencing data, and neoantigens derived from different types of genome DNA alterations, including point mutations, insertion deletions, and gene fusions are supported. Importantly a convolutional neural networks (CNN) based model has been trained to predict the immunogenicity of neoepitope. And this model shows improved performance compared with currently available tools in immunogenicity prediction in independent datasets.

## Installation

Seq2Neo runs on a Linux operation system like the CentOS system (recommended), and it is open-source software under an academic free license (AFL) v3.0.

### Conda

We strongly recommend using the conda command line for installation as this will solve dependencies automatically. The web of the package is https://anaconda.org/liuxslab/seq2neo. 

1. Firstly, you need to install the [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html#) (recommended), and set channels in the `~/.condarc` file like this:

   ```
   channels:
     - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
     - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda
     - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/menpo
     - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
     - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
     - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
     - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch
     - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/simpleitk
   ```
   
   You can replace Tsinghua mirrors with other convenient mirrors.
   
2. Secondly, you should execute the following commands to create a new environment named Seq2Neo or other on your Linux system, and then activate it:

   ``` shell
   conda create -n Seq2Neo
   conda activate Seq2Neo
   ```

3. Thirdly, you can install the package through the following conda command:

   ```shell
   conda install -c liuxslab seq2neo
   ```

4. Finally, please installation of following packages manually due to the reasons of permission or others:

   - Annovar == latest  [ANNOVAR website (openbioinformatics.org)](https://www.openbioinformatics.org/annovar/annovar_download_form.php)
   - HLAHD == 1.4.0  [HLA-HD (kyoto-u.ac.jp)](https://www.genome.med.kyoto-u.ac.jp/HLA-HD/)
   - netCTLpan == 1.1.b [NetCTLpan - 1.1 - Services - DTU Health Tech](https://services.healthtech.dtu.dk/service.php?NetCTLpan-1.1)
   - netMHCpan == 4.1.b  [NetMHCpan - 4.1 - Services - DTU Health Tech](https://services.healthtech.dtu.dk/service.php?NetMHCpan-4.1)
   - STAR-Fusion == 1.10.1 [STAR-Fusion/STAR-Fusion: STAR-Fusion codebase (github.com)](https://github.com/STAR-Fusion/STAR-Fusion)

   Following corresponding official instructions to install those packages on your system. 

### Docker

We also provide docker image ([liuxslab/seq2neo - Docker Image | Docker Hub](https://hub.docker.com/r/liuxslab/seq2neo)) that contains all packages dependencies.  You need to install docker in advance on your system. Then the command `docker pull liuxslab/seq2neo:latest` will pull the seq2neo image into your local machine. You can put resource files required by BWA, Mutect2, and others in one folder **resource_files**, which has several classified folders like **bqsr_resource**, **mutect2_resource**, **starfusion_resource**, **ref_genome** (a reference to the section of "The module of whole"), then execute the following commands to start a docker container and activate Seq2Neo conda environment including seq2neo and its dependencies:

```
docker run -it -v /path/to/resource_files:/home/resource_files liuxslab/seq2neo:latest /bin/bash
cd /home/seq2neo
conda activate Seq2Neo
```

 In the Seq2Neo environment, you can run seq2neo commands, please refer to the following section of "The module of whole".

### Pip (not recommended)

You can install the stable release of **Seq2Neo** with:

> pip install Seq2Neo

However, you should install all of the dependencies manually. It includes the following softwares and packages that should be installed in advance:

``` plain
- bamtools=2.5.1
- bwa=0.7.17
- fastp=0.23.2
- perl=5.26.2=h470a237_0
- samtools=1.15.1
- star=2.7.8a
- tpmcalculator=0.0.4
- vcftools=0.1.16
- bowtie2 == 2.3.5
- gatk == 4.2.5
```

Then, you should also install the packages mentioned in the Conda section.

## Usage

Seq2Neo consists of 3 modules, which are whole, download, and immuno. The module of whole is responsible for running the entire process, the download module can download a specified version of a reference genome from the Ensembl database and index, and the last module of immuno supports the prediction of immunogenicity score of specified peptides and MHCs:

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
                        directory to BQSR known sites (default: None)
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

1. You need to download the necessary reference files before running Seq2Neo:

   - Downloading three BQSR known sites files used to recalibrate base quality score, those files should be put in a directory like **bqsr_resource**, and index files are needed to accelerate the speed of Seq2Neo.  The commands are following:

     ```
     mkdir bqsr_resource && cd bqsr_resource
     prefix=ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/hg38/
     wget ${prefix}dbsnp_146.hg38.vcf.gz
     wget ${prefix}dbsnp_146.hg38.vcf.gz.tbi
     wget ${prefix}1000G_phase1.snps.high_confidence.hg38.vcf.gz
     wget ${prefix}1000G_phase1.snps.high_confidence.hg38.vcf.gz.tbi
     wget ${prefix}Mills_and_1000G_gold_standard.indels.hg38.vcf.gz
     wget ${prefix}Mills_and_1000G_gold_standard.indels.hg38.vcf.gz.tbi
     ```

   - Downloading hg38 datasets of annovar via the following commands:

     ```
     cd /path/to/annovar
     perl annotate_variation.pl --downdb --webfrom annovar --buildver hg38 refGene humandb/
     ```

   - Downloading the necessary reference files used to call Mutect2, those files should be put in a directory like **mutect2_resource**, and index files are needed to accelerate the speed of Seq2Neo.  The commands are following:

     ```
     mkdir mutect2_resource && cd mutect2_resource
     prefix=ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/Mutect2/
     wget ${prefix}af-only-gnomad.hg38.vcf.gz
     wget ${prefix}af-only-gnomad.hg38.vcf.gz.tbi
     wget ${prefix}GetPileupSummaries/small_exac_common_3.hg38.vcf.gz
     wget ${prefix}GetPileupSummaries/small_exac_common_3.hg38.vcf.gz.tbi
     ```

   - Downloading the AGFusion database and pyensembl reference genome, we select the max release of 95 to download:

     ```
     pyensembl install --species homo_sapiens --release 95
     agfusion download -g hg38 --release 95 
     ```

   - Downloading the genome library of STAR-Fusion (1.10.1) to call gene fusions via the following commands:

     ```
     ref=GRCh38_gencode_v37_CTAT_lib_Mar012021.plug-n-play.tar.gz
     wget https://data.broadinstitute.org/Trinity/CTAT_RESOURCE_LIB/__genome_libs_StarFv1.10/${ref}
     tar -zxvf ${ref}
     ```

     The size of the compressed genome library is about 31 G, Chinese researchers can download it at a higher speed by using some useful tools like Thunder [Official Website](https://www.xunlei.com/).

   - Downloading the reference genome and indexing via the following command lines:

     ```
     mkdir ref_genome && cd ref_genome
     seq2neo download --species homo_sapiens --build GRCh38 --release 105 --dir .
     ```

2. Suppose you have downloaded three files, they are tumor RNA-seq and WES data, normal WES data. Specifically, SRR2603346 is for tumor RNA-seq, SRR2601737 is for tumor WES, and SRR2601758 is for normal WES. Then you can run Seq2Neo via the following command line to obtain potential neoantigens (running on a machine with more than 50G memory and 512G hard disk space):

   ```
   seq2neo whole --ref ref_genome/Homo_sapiens_assembly38.fasta --normal-dna SRR2601758_1.fastq SRR2601758_2.fastq --tumor-dna SRR2601737_1.fastq SRR2601737_2.fastq --tumor-rna SRR2603346_1.fastq SRR2603346_2.fastq --normal-name SRR2601758 --tumor-name SRR2601737 --known-site-dir bqsr_resource/ --mutect2-dataset-dir mutect2_resource/ --annovar-db-dir /path/to/annovar/humandb/ --genome-lib-dir /path/to/GRCh38_gencode_v37_CTAT_lib_Mar012021.plug-n-play/ctat_genome_lib_build_dir/ --agfusion-db agfusion.homo_sapiens.95.db --out out/ --len 8 9 10 11 --threadN 20 --java-options '"-Xmx40G"' --hlahd-dir /path/to/hlahd
   ```
   
3. The final result of the module whole is in the folder of **final_result**, including **final_results_neo.txt** and **filtered_neo.txt**. The final_results_neo.txt includes all peptides from the detected mutation sites. After applying the criteria of TAP>0, TPM>0, immunogenicity>0.5 and IC50<=500, filtered_neo.txt is acquired (ranking by IC50).

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

This module will help users download and index reference genomes from the Ensembl database. The usage of the module is:

```
seq2neo download --species homo_sapiens --build GRCh38 --release 105 --dir .
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

The module allows users to predict the immunogenicity scores of provided peptides and HLAs.

For example, if you want to query a single epitope (peptide + HLA), you want to query peptide SVQIISCQY along with HLA-A30:02. You need to type:

```
seq2neo immuno --mode single --epitope SVQIISCQY --hla HLA-A30:02
```

If you want to query multiple epitopes, you just need to prepare a csv format file like this:

```
Pep,HLA
ADTSEARPFW,HLA-B44:02
ADVLSPVLVK,HLA-A03:01
AELEEVSSY,HLA-B44:02
AELLAKQLY,HLA-B44:02
AEQQGACPGL,HLA-B44:02
AEVSVLYTV,HLA-B44:02
AEYQDMHSY,HLA-B44:02
AINRPTVLK,HLA-A03:01
```

Then you run:

```
seq2neo --mode multiple --inputfile data/test_input.csv --outdir data/
```

You will get two files, **immuno_input_file.csv** and **cnn_results.csv**. The former includes the predictions of TAP and IC50 performed by netCTLpan and netMHCpan4.1b, respectively, and the latter is the final results including immunogenicity scores.
