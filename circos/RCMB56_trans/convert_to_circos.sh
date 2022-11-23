#!/bin/bash
awk 'BEGIN {OFS="\t"} {print "hs"$1,$2,$3,"hs"$4,$5,$6};' ../../../2022-08-18_fithic/out/RCMB56_ecDNA1_trans_contacts.bedpe > RCMB56_ecDNA1_trans_contacts.bedpe
