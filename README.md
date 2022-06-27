# Seq2Neo: a comprehensive pipeline for cancer neoantigen immunogenicity prediction

## Overview
Neoantigens derived from somatic DNA alterations are ideal cancer specific targets. However, not all somatic DNA mutations can cause immunogenicity to cancer cell, and efficient tools for predicting the immunogenicity of neo-peptide is still urgently needed. Here we present the **Seq2Neo** pipeline, which provides a one-stop solution for neo-peptide features prediction with HLA class I from raw sequencing data, and neoantigens derived from different types of genome DNA alterations, including point mutations, insertion deletions, and gene fusions are supported. Importantly a convolutional neural networks (CNN) based model has been trained to predict the immunogenicity of neoepitope. And this model shows improved performance compared with currently available tools in immunogenicity prediction in independent datasets.

## Installation:
### Conda



### Docker

### Pip (not recommended)

You can install the stable release of **Seq2Neo** with:

> pip install Seq2Neo

However, you should install all of dependencies manually. It includes the following softwares and packages that should be installed in advance:

``` plain
- python=3.7
- protobuf <3.20
- biopython=1.77
- keras=2.4.3
- tensorflow=2.3.0
- agfusion=1.252
- bamtools=2.5.1
- bwa=0.7.17
- fastp=0.23.2
- perl=5.26.2=h470a237_0
- pyensembl=1.9.4
- samtools=1.15.1
- star=2.7.8a
- tpmcalculator=0.0.4
- vcftools=0.1.16
```



## Usage
