# Python3 program to find the missing 
# and additional elements 
  
# examples of lists

f = open("pdb-an.txt", "r")
HST = set(f)


f = open("ZY-files-Newcards-dir2.txt", "r")
ZY = set(f)

diff = list(set(ZY).difference(HST))

print(diff)

#print("Accession Numbers in ZY-DB not found in HST Photo DB:",(set(ZY).difference(HST)))
  


