Circos notes

##################################
hg38:
	D458, MB106, MB248, MB268, MB275, RCMB56
hg19:
	PT_FN4GEEFR

2/18/2020

Hello world
http://circos.ca/documentation/tutorials/quick_start/hello_world/lesson

circos -conf hello_world.conf

##################################
Making a karyotype

formatted as:
chr - ID LABEL START END COLOR

##################################
Adding genes
See tutorial on "Tiles"
http://circos.ca/documentation/tutorials/2d_tracks/tiles/lesson
Used gene tracks for hg19 from HOMER
http://homer.ucsd.edu/homer/interactions/circos.html

Genes, take 2:
wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_33/gencode.v33.basic.annotation.gff3.gz \
gunzip the above
awk '$3 == "gene"' file \
    | convert2bed -i gff - \
    > genes.bed

##################################
Adding histogram (ATAC)

Getting real hacky now. Since I've had to redefine each of my segments as its own chromosome,
it takes some work to convert into histogram. Below, my steps.

Get bed file of each region in my ecDNA
Split bed file into n bed files, one for each line.
for i in n:
	# chop into kilobase windows:
	bedops --chop 1000 circos_k$n.bed > circos_k$n.chop.bed
	
	# map mean bedgraph value onto each windows
	bedtools intersect -a $ATAC/macs2_hg38/MB268_treat_pileup.bdg -b circos_k$n.chop.bed -wa > MB268_k$n.bdg
	bedtools map -a circos_k$n.chop.bed -b MB268_filterdup.pileup.bdg -c 4 -o mean > MB268_k$n.bdg
	
	# revise each chromosome name to match my altered karyotype file:
	awk -v n=$n '{print n "\t" $2 "\t" $3 "\t" $4};' MB268_k$n.bdg > circos_k$n.bdg	
	
	# cat them all into the same bedgraph

###################################
Adding histogram (RNAseq)

Ged bed file in hg19 of my region
Split into n bed files
	# chop into kilobase windows
	bedops --chop 1000 circos_k$n.bed > circos_k$n.chop.bed
	
	# bedtools coverage
	samtools view -F 0x100 -u -L [bed file] /broad/medullo/dkfz.transfer201610/RNAseq_FireCloud_BAMs/MB106.Aligned.sortedByCoord.out.bam \
	| samtools sort -o MB106.Aligned.sortedByCoord.out.bam - 
	bedtools coverage -a $n.chop.bed -b MB106.Aligned.sortedByCoord.out.bam -split -counts -sorted -g $ATAC/genomes/human.b37.genome \
	> $n.bdg
	
	# crossmap each
	CrossMap.py bed $ATAC/genomes/GRCh37_to_GRCh38.chain.gz $n.bdg $n.grch38.bdg
	
	# revise each chromosome name to match my altered karyotype file:
	awk -v n=$n '{print n "\t" $2 "\t" $3 "\t" $4};' $n.grch38.bdg > MB106_rnaseq.circos.bdg	
	
	# cat them all into the same bedgraph	



###################################
Adding links (HiC)

HiCCUPS CPU:
java -Xms512m -Xmx2048m -Djava.librarylpath=$CLASSPATH -jar $JUICERTOOLS hiccups --cpu --threads 0 --ignore-sparsity -c 8 -k KR /dtn/juicebox/MB106/rawdata.allValidPairs.hic .

HiCCUPS:
java -Xms512m -Xmx14g -jar $JUICERTOOLS hiccups --threads 0 --ignore-sparsity -k KR -f .2 -r 5000,10000,25000 -p 4,2,1 -i 7,5,3 -t 0.02,1.5,1.75,2 -d 20000,20000,50000 /dtn/juicebox/MB268/rawdata.allValidPairs.hic .

Using pgltools:
tail -n +2 merged_loops_CURATED.bedpe | cut -f1-6 | pgltools formatbedpe > MB106_hiccups.pgl
tail -n +2 MB268.spline_pass2.res5000.significances.pval_0.01.bedpe | cut -f1-6 | pgltools formatbedpe > MB268_fithic.pgl

###################################
Adding exons

Generated genes files for hg19, hg38
See scripts/Gene_annotation_parsers.ipynb

