# Computation of Confusion Matrices for Likelihood Values of protein pairs.
# Computation of ROC and corresponding AUC from the calculated Confusion Matrices

This program:
1. Cleans data obtained from Gold Standard Dataset by Jansen and Co-workers
2. Calculates Likelihood ratio for a set of positive and negative Dataset
3. Predicts which protein would be positive and negative based on a certain threshold
4. Computes Confusion Matrix for each case
5. Constructs the Confusion Matrix Table using plot.ly API
6. Computes the ROC curve using plot.ly API
7. Computes AUC (Area Under Curve) using numpy
The data set used here is the Gold Standard Dataset by Jansen and Co-workers  
