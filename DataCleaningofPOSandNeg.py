# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 10:34:32 2017

@author: Jrahman
"""

def pos_column_split(file):
    newFile = open("Positives.txt", "w")
    with open(file, "r") as curr_file:
        for columns in curr_file:
            splited_columns = columns.split("\t")
            input_data = ("\t".join((splited_columns[0], splited_columns[1])))
            newFile.write(input_data + "\n")

    newFile.close()
    
    print("Done")
pos_column_split("pos_MIPS_complexes.txt")

#" ".join(splited_columns[0:2]+".txt")