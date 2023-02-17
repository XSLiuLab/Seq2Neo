FROM liuxslab/seq2neo:v1.1

LABEL maintainer="diaokx" email="diaokx@shanghaitech.edu.cn"

ARG prefix=/home/seq2neo/miniconda3/envs/Seq2Neo/lib/
ENV PATH /home/seq2neo/miniconda3/bin:$PATH
RUN conda config --remove-key channels && conda config --set show_channel_urls yes \
    && conda config --add channels simpleitk \
    && conda config --add channels pytorch-lts \
    && conda config --add channels pytorch \
    && conda config --add channels msys2 \
    && conda config --add channels r \
    && conda config --add channels main \
    && conda config --add channels menpo \
    && conda config --add channels bioconda \
    && conda config --add channels conda-forge
RUN conda remove -n Seq2Neo --all -y && conda create -n Seq2Neo \
    && source activate Seq2Neo && conda install -c liuxslab seq2neo=2.1 -y
RUN ln -s ${prefix}libcrypto.so.1.1 ${prefix}libcrypto.so.1.0.0

ENV Seq2Neo_Version 2.1
WORKDIR /home/seq2neo/

CMD [ "/bin/bash" ]