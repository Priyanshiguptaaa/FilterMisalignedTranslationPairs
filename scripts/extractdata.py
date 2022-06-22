import xml.etree.ElementTree as ET
import subprocess
import sys

#reading the directory where the tmx file is stored

## python extract.py --tmx-file file.tmx --output “./myfolder/output”

DIR = sys.argv[1]

tree = ET.parse(DIR)

#get the whole file tree structure in root

root = tree.getroot()

#get content from the body
child = root[1]

lang1 = "de"
lang2 = "fr"

out1 = sys.argv[2]
out2 = sys.argv[3]

file1 = open(out1,"w")
file2 = open(out2,"w")


#parsing through the elements/nodes of the tree

for element in child.iter("tu"):

	#getting the language pair segments from the element
	lang1seg = element[4][0].text
	lang2seg = element[5][0].text


	#skipping the language pair for the empty segments
	if lang1seg!=None or lang2seg!=None:
		
		#storing the langauge pairs in parallel files
		file1.write(lang1seg+"\n")
		file2.write(lang2seg+"\n")

file1.close()
file2.close()


