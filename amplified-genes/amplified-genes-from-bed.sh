#!/bin/bash

# Gene coordinates from gencode
hg19genes=/home/ochapman/Documents/circos/genes/gencode.v34lift37.annotation_genes.bed
hg38genes=/home/ochapman/Documents/circos/genes/gencode.v33.basic.annotation_genes.bed

for filepath in ./cohort/*.hg19.bed; do
	echo "Processing $filepath ..."
	filename=$(basename $filepath)
	bedtools intersect -wa -a $hg19genes -b $filepath | sort | uniq > cohort-genes/$filename
done

for filepath in ./cohort/*.hg38.bed; do
	echo "Processing $filepath ..."
	filename=$(basename $filepath)
	bedtools intersect -wa -a $hg38genes -b $filepath | sort | uniq > cohort-genes/$filename
done
