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
   - Bowtie2 == 2.3.5  [Bowtie 2: fast and sensitive read alignment (sourceforge.net)](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)
   - GATK == 4.2.5  [gatk resource](https://gatk.broadinstitute.org)
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
```

Then, you should also install packages mentioned in the Conda section.

## Usage

stand by
