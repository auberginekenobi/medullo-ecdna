import argparse
import os
import functools

# Parse input params
parser = argparse.ArgumentParser('Convert a bedpe file to my weird circos format where each contig is a different chromosome.')
parser.add_argument('bedpe',help='bedpe file, eg of loops called by HiCCUPS')
parser.add_argument('contigs',help='.bed file containing the SORTED regions in the ecDNA.')
parser.add_argument('outfile', help='outfile.circos.bedpe')
args = parser.parse_args()

def _parse_contigs(bed_file):
	'''
	Parse each line of a bed file
	chr1	1000	2000
	to
	[(chr1,1000,2000)]
	'''
	contigs = []
	with open(bed_file,'r') as f:
		for line in f:
			line = line.strip().split()
			contigs.append((line[0],int(line[1]),int(line[2])))
	return contigs

def _circosize_line(line, contigs):
	'''
	Takes a pgl line of the format:
		chr start end chr start end
	and alters chromosomes based on my weird circos format
	'''
	line=line.strip().split()
	line[1] = int(line[1])
	line[2] = int(line[2])
	line[4] = int(line[4])
	line[5] = int(line[5])
	seg1=[];seg2=[]
	for i in range(len(contigs)):
		c = contigs[i]
		if line[0]==c[0] and line[1]>=c[1] and line[2]<=c[2]:
			seg1.append(str(i+1))
		if line[3]==c[0] and line[4]>=c[1] and line[5]<=c[2]:
			seg2.append(str(i+1))
	bezier=1.5**(1-abs(line[1]-line[4])/(3*10000))*.4
	lines = []
	for s1 in seg1:
		for s2 in seg2:
			out_line = [s1]+line[1:3]+[s2]+line[4:6]
			out_line = '\t'.join(map(str,out_line))+"\tbezier_radius="+str(bezier)+"r"'\n'
			lines.append(out_line)
	return lines

def circosize(bedpe_file,contigs_file,output_file):
	contigs = _parse_contigs(contigs_file)
	with open(bedpe_file,'r') as r:
		with open(output_file,'w') as w:
			for line in r.readlines():
				if line.startswith('#'):
					continue
				lines = _circosize_line(line,contigs)
				for out in lines:
					w.write(out)

circosize(args.bedpe,args.contigs,args.outfile)