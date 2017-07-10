# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 10:34:32 2017

@author: Jrahman
"""

from ManipulateData import ManipulateData

manipulate = ManipulateData();
'''
manipulate.columnSplit("pos_MIPS_complexes.txt", "positives")
manipulate.columnSplit("L_neg.txt", "negatives")

manipulate.addCommonColumn("positives.txt", "+ve")
manipulate.addCommonColumn("negatives.txt", "-ve")

manipulate.rowSplit("positives.txt", 500, 1)
manipulate.rowSplit("negatives.txt", 150000, 1)

manipulate.combineFiles("positives_500_1.txt", "negatives_150000_1.txt")

manipulate.matchLikelihoodRatio('combined_files.txt')

manipulate.predictedLikelihoodRatioVal('matched_likelihood_ratios.txt')

manipulate.matrixCalculationCol("predicted_likelihood_value_column_added_0.1.txt")#this is just for validation. Run this to validate for each file created if needed

manipulate.matrixCalculation(manipulate.getPredeictedLikelihoodFiles())

manipulate.valCol("counter_calculation.txt")

manipulate.plotlyTable("Confusion Matrix Table.txt")
'''
manipulate.rocGraph("Confusion Matrix Table.txt")
