import sys
import numpy
import pandas
import matplotlib


#Todo : scatter plot

def aligned_pair_percentage(n_total,n_align):
	return (n_align/n_total)*100

file1 = sys.argv[1]
file2 = sys.argv[2]

f1 = open(file1)
f2 = open(file2)

lines1 = f1.readlines()
lines2 = f2.readlines()

n_align = len(lines1)
n_total = len(lines2)

perc = aligned_pair_percentage(n_total,n_align)

filterpoint = sys.argv[3]

print("Analysis for filtering based on similairty score: "+str(filterpoint))
print("Total langauge pairs : " + str(n_total))
print("Aligned langauge pairs : " + str(n_align))
print("Percentage of aligned langauge pairs : " + str(perc) +" %")