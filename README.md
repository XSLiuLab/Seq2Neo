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
     - conda-forge
     - bioconda
     - menpo
     - main
     - r
     - msys2
     - pytorch
     - pytorch-lts
     - simpleitk
   show_channel_urls: true
   ```
   
   You can replace those with Tsinghua mirrors or others.
   
2. Secondly, you should execute the following commands to create a new environment named Seq2Neo or other you like on your Linux system, and then activate it:

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

We also provide a docker image ([liuxslab/seq2neo - Docker Image | Docker Hub](https://hub.docker.com/r/liuxslab/seq2neo)) that contains all package dependencies.  You need to install docker in advance on your system. Then the command `docker pull liuxslab/seq2neo:latest` will pull the latest seq2neo image into your local machine. You can put resource files required by BWA, Mutect2, and others in one folder **resource_files**, which has several classified folders like **bqsr_resource**, **mutect2_resource**, **starfusion_resource**, **ref_genome** ( reference to the section of "The module of whole"), then execute the following commands to start a docker container and activate Seq2Neo conda environment including seq2neo and its dependencies:

```
docker run -it -v /path/to/resource_files:/home/resource_files liuxslab/seq2neo:latest /bin/bash
cd /home/seq2neo
cd biosoft/hlahd.1.4.0/ && sh install.sh && cd ../../ # installation of HLAHD 1.4.0
conda activate Seq2Neo
```

 In the Seq2Neo environment, you can run seq2neo commands, please refer to the following section of "The module of whole".

### Pip (not recommend)

You can install the stable release of **Seq2Neo** with:

> pip install Seq2Neo

However, you should install all of the dependencies manually. It includes the following softwares and packages that should be installed in advance:

```
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

Seq2Neo consists of 3 modules, which are whole, download, and immuno. The module of **whole** is responsible for running the entire process, and contains several subprocesses. The **download** module can download a specified version of human reference genome (hg19 / hg38) from the GATK and index it. The last module of **immuno** supports the prediction of immunogenicity score of specified peptides and MHCs:

``` plain
usage: seq2neo [-h] {whole,immuno,download} ...

A pipeline from sequence to neoantigen prediction

positional arguments:
  {whole,immuno,download}
    whole               Run whole pipeline(Seq2Neo) with fastq/bam/sam/vcf file
    immuno              Run immunogenicity prediction with specified peptides and MHCs
    download            downloading human reference genome from GATK and building indexes

optional arguments:
  -h, --help            show this help message and exit

Thanks for using Seq2Neo
```

## The module of whole

### How to download necessary reference files

You need to download the necessary reference files before running Seq2Neo:

- Download three BQSR known sites files used to recalibrate base quality score, those files should be put in a directory like **bqsr_resource**, and index files are needed to accelerate the speed of Seq2Neo.  The commands are following:

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

- Download hg38 datasets of annovar via the following commands:

  ```
  cd /path/to/annovar
  perl annotate_variation.pl --downdb --webfrom annovar --buildver hg38 refGene humandb/
  ```

- Download the necessary reference files used to call Mutect2, those files should be put in a directory like **mutect2_resource**, and index files are needed to accelerate the speed of Seq2Neo.  The commands are following:

  ```
  mkdir mutect2_resource && cd mutect2_resource
  prefix=ftp://gsapubftp-anonymous@ftp.broadinstitute.org/bundle/Mutect2/
  wget ${prefix}af-only-gnomad.hg38.vcf.gz
  wget ${prefix}af-only-gnomad.hg38.vcf.gz.tbi
  wget ${prefix}GetPileupSummaries/small_exac_common_3.hg38.vcf.gz
  wget ${prefix}GetPileupSummaries/small_exac_common_3.hg38.vcf.gz.tbi
  
  prefix=https://storage.googleapis.com/gatk-best-practices/somatic-hg38/
  wget ${prefix}1000g_pon.hg38.vcf.gz
  wget ${prefix}1000g_pon.hg38.vcf.gz.tbi
  ```

- Download the AGFusion database and pyensembl reference genome, we select the max release of 95 to download:

  ```
  pyensembl install --species homo_sapiens --release 95
  agfusion download -g hg38 --release 95 
  ```

- Download the genome library of STAR-Fusion (1.10.1) to call gene fusions via the following commands:

  ```
  ref=GRCh38_gencode_v37_CTAT_lib_Mar012021.plug-n-play.tar.gz
  wget https://data.broadinstitute.org/Trinity/CTAT_RESOURCE_LIB/__genome_libs_StarFv1.10/${ref}
  tar -zxvf ${ref}
  ```

  The size of the compressed genome library is about 31 G, Chinese researchers can download it at a higher speed by using some useful tools like Thunder [Official Website](https://www.xunlei.com/).

- Download the human reference genome and build indexes via the following commands:

  ```
  mkdir ref_genome && cd ref_genome
  seq2neo download --build hg38 --dir .
  ```
  
  ----

### How to run

Suppose you have the following files, they are tumor RNA-seq and WES data, normal WES data, VCF and corresponding sam and sort_bam files. Then you can run Seq2Neo to obtain potential neoantigens in different situations. The following is some examples:

- Have **tumor dna, tumor rna** and **normal dna** fastq files

  ```bash
  seq2neo whole --data-type fastq --ref Homo_sapiens_assembly38.fasta --normal-dna normal_dna_1.fastq normal_dna_2.fastq --tumor-dna tumor_dna_1.fastq tumor_dna_2.fastq --tumor-rna tumor_rna_1.fastq tumor_rna_2.fastq --normal-name normal_name --tumor-name tumor_name --annovar-db-dir annovar/humandb/ --known-site-dir bqsr_resource/ --mutect2-dataset-dir mutect2_resource/ --genome-lib-dir GRCh38_gencode_v37_CTAT_lib_Mar012021.plug-n-play/ctat_genome_lib_build_dir/ --agfusion-db agfusion.homo_sapiens.95.db --pon 1000g_pon.hg38.vcf.gz --len 8 9 10 11 --threadN 15 --java-options '"-Xmx50G"' --hlahd-dir hlahd.1.4.0/ --out out/
  ```

- Have **tumor dna** and **tumor rna** fastq files

  ```bash
  seq2neo whole --data-type without-normal-dna --ref Homo_sapiens_assembly38.fasta --tumor-dna tumor_dna_1.fastq tumor_dna_2.fastq --tumor-rna tumor_rna_1.fastq tumor_rna_2.fastq --tumor-name tumor_name --annovar-db-dir annovar/humandb/ --known-site-dir bqsr_resource/ --mutect2-dataset-dir mutect2_resource/ --genome-lib-dir GRCh38_gencode_v37_CTAT_lib_Mar012021.plug-n-play/ctat_genome_lib_build_dir/ --agfusion-db agfusion.homo_sapiens.95.db --pon 1000g_pon.hg38.vcf.gz --len 8 9 --threadN 15 --java-options '"-Xmx50G"' --hlahd-dir hlahd.1.4.0/ --out out/
  ```

- Have **tumor dna** and **normal dna** fastq files

  ```bash
  seq2neo whole --data-type without-tumor-rna --ref Homo_sapiens_assembly38.fasta --normal-dna normal_dna_1.fastq normal_dna_2.fastq --tumor-dna tumor_dna_1.fastq tumor_dna_2.fastq --normal-name normal_name --tumor-name tumor_name --annovar-db-dir annovar/humandb/ --known-site-dir bqsr_resource/ --mutect2-dataset-dir mutect2_resource/ --pon 1000g_pon.hg38.vcf.gz --len 8 9 --threadN 15 --java-options '"-Xmx50G"' --hlahd-dir hlahd.1.4.0/ --out out/
  ```

- Only have **tumor dna** fastq files

  ```bash
  seq2neo whole --data-type only-tumor-dna --ref Homo_sapiens_assembly38.fasta --tumor-dna tumor_dna_1.fastq tumor_dna_2.fastq --tumor-name tumor_name --annovar-db-dir annovar/humandb/ --known-site-dir bqsr_resource/ --mutect2-dataset-dir mutect2_resource/ --pon 1000g_pon.hg38.vcf.gz --len 9 11 --threadN 15 --java-options '"-Xmx50G"' --hlahd-dir hlahd.1.4.0/ --out out/
  ```

- Only have a **vcf** file

  ```bash
  seq2neo whole --data-type vcf --ref Homo_sapiens_assembly38.fasta --tumor-name tumor_name --annovar-db-dir annovar/humandb/ --threadN 10 --hlas HLA-A01:01 HLA-B44:02 --len 8 9 --out out/ --vcf xxx.vcf
  ```

The final result of the module whole is in the folder of **final_result**, including **final_results_neo.txt** and **filtered_neo.txt**. The final_results_neo.txt includes all peptides from the detected mutation sites. After applying the criteria of TAP>0, TPM>0 (if available), immunogenicity>0.5 and IC50<=500, filtered_neo.txt is acquired (ranking by IC50).

Notice: if you don not want to use the predicted HLAs, you can specify manually through **--hlas** argument.

-----------------------

## The module of download

``` plain
usage: seq2neo download [-h] [--build {hg19,hg38}] [--dir [DIR]]

Run download module

optional arguments:
  -h, --help           show this help message and exit
  --build {hg19,hg38}  which build to download, hg38 / hg19 (default: hg38)
  --dir [DIR]          where to store (default: .)
```

This module will help users download and index human reference genome from GATK. The usage of the module is:

```
seq2neo download --build hg38 --dir .
```

-------------

## The module of immuno

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

For example, if you want to query a single peptide SVQIISCQY along with HLA-A30:02. You need to type:

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

Then you can run:

```
seq2neo immuno --mode multiple --inputfile data/test_input.csv --outdir data/
```

You will get two files, **immuno_input_file.csv** and **cnn_results.csv**. The former includes the predictions of TAP and IC50 performed by netCTLpan and netMHCpan4.1b, respectively, and the latter is the final results including immunogenicity scores.
