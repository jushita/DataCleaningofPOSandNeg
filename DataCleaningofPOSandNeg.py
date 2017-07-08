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

manipulate.predictedLikelihoodRatioVal('matched_likelihood_ratios.txt', [0.1,1,10,20,30,40,50,60,70,80,90,100, 200,
300,400,500,600,700,800,900,1000,10000,20000,30000,40000,50000])

#manipulate.matrixCalculationCol("predicted_likelihood_value_column_added_0.1.txt")#this is just for validation. Run this to validate for each file created if needed

manipulate.matrixCalculation(manipulate.getPredeictedLikelihoodFiles())

'''
manipulate.plotlyTable("counter_calculation.txt")
