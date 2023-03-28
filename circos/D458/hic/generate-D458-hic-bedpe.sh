#!/bin/bash

cat manual_loops.pgl D458_hiccups.pgl | pgltools sort > D458_ecDNA_loops.pgl
#cat D458_hiccups.pgl | pgltools sort > D458_ecDNA_loops.pgl

cb=../../circosize_bedpe.py
python $cb D458_ecDNA_loops.pgl D458_bionano.hg38.bed /home/ochapman/Documents/Mesirov/medullo_ecDNA/src/circos/D458/hic/D458_ecDNA_loops.circos.bedpe
