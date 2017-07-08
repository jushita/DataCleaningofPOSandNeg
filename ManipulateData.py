import os, glob
import plotly
import plotly.figure_factory as ff
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *

plotly.offline.init_notebook_mode(connected=True)


class ManipulateData():
    def columnSplit(self, file, new_file):
        newFile = open(new_file + ".txt", "w")

        with open(file, "r") as curr_file:
            for columns in curr_file:
                splited_columns = columns.split("\t")
                input_data = ("\t".join((splited_columns[0], splited_columns[1])))
                newFile.write(input_data + "\n")

        newFile.close()

        print("Done")

    def rowSplit(self, _file, num_row, num_files):
        file_counter = 0;
         #open file
        with open(_file, "r") as file:
            #loop throught each line of file
            for i, line in enumerate(file):

                #check if we're at a 500,000 mark
                if i%num_row == 0:
                    if (file_counter >= num_files) and i != 0:
                        break

                    #create open new file to write to
                    new_file = open(os.path.basename(_file).split(".")[0] + "_" + str(num_row) + "_" + str(file_counter + 1) + ".txt", "w")
                    file_counter += 1

                #write current line to new file
                new_file.write(line)

        print("Done!")

    def addCommonColumn(self, _file, col_data):
        with open(_file, "r") as file:
            data = file.readlines();

        for i, line in enumerate(data):
            data[i] = line.rstrip('\n') + "\t" + col_data + "\n"

        with open(_file, "w") as file:
            file.writelines(data)

    def combineFiles(self, posFile, negFile):
        with open(posFile, "r") as posNewFile:
            data1 = posNewFile.readlines()

        with open(negFile, "r") as negNewFile:
            data2 = negNewFile.readlines()

        with open("combined_files.txt", "w") as file:
            file.writelines(data1)
            file.writelines(data2)

    def matchLikelihoodRatio(self, _file):
        new_file = open("matched_likelihood_ratios.txt", "w")

        #read lines of file to list
        with open(_file, "r") as file:
            for i, line in enumerate(file):

                line = line.rstrip("\n")
                split_line = line.split('\t')

                file_protein1 = "L_PIP/" + split_line[0] + ".txt"
                file_protein2 = "L_PIP/" + split_line[1] + ".txt"

                lpip_found = False

                if os.path.isfile(file_protein1):
                    with open(file_protein1) as file:
                        for i, line in enumerate(file):
                            other_protein = line.split("\t")[0]
                            if split_line[1] == other_protein:
                                lpip = line.split('\t')[5]
                                split_line.append(lpip.rstrip('\n'))
                                lpip_found = True
                                break

                if not lpip_found and os.path.isfile(file_protein2):
                    with open(file_protein2) as file:
                        for line in file:
                            other_protein = line.split("\t")[0]
                            if split_line[0] == other_protein:
                                lpip = line.split('\t')[5]
                                split_line.append(lpip.rstrip('\n'))
                                lpip_found = True
                                break

                if lpip_found:
                    new_file.write("\t".join(split_line) + "\n")

        print ("Done")

    def predictedLikelihoodRatioVal(self, _file, values):
        for val in values:
            newFile = open("predicted_likelihood_value_column_added_" + str(val) + ".txt", "w")

            with open(_file, "r") as file:

                for i, line in enumerate(file):

                #storing each line of the file in a list then isolating 4th column
                    line = line.rstrip("\n")
                    split_line = line.split('\t')[3]
                    #converting the 4th column value from str to float
                    split_line = float(split_line)
                    #comparing the actual likelihood value with a threshold and writing the predicted pos or neg value
                    if (split_line >= val):
                        prLrval = "+ve"
                        #converting float into str again
                        split_line = str(split_line)
                        #adding the value to the previous list with all 4 columns
                        lr_prLrval = line + "\t" + prLrval
                    else:
                        prLrval = "-ve"
                        split_line = str(split_line)
                        lr_prLrval = line + "\t" + prLrval
                    #writing in a new file
                    newFile.write(lr_prLrval + "\n")

        print("Done")

    def getPredeictedLikelihoodFiles(self):
        files = list()

        for file in glob.glob("predicted_likelihood_value_column_added_*.txt"):
            files.append(file)

        return files

    def matrixCalculationCol(self, _file):
        newFile = open("matrix_clc_col_added.txt" , "w")
        newFile_1 = open("counter_calculation.txt" , "w")
        tp_counter = 0
        fn_counter = 0
        fp_counter = 0
        tn_counter = 0

        #storing each line of the file in a list then isolating 3rd and 5th column
        with open(_file, "r") as file:
            for i, line in enumerate(file):

                line = line.rstrip("\n")
                    #isolating actual labels
                actual = line.split('\t')[2]
                    #isolating predicted labels
                predicted = line.split('\t')[4]
                #checking which one is tp/fp/tn/fn
                if (actual == "+ve" and predicted == "+ve"):
                    tp = "TP"
                    tp_counter += 1
                    newLine = line + "\t" + tp
                elif (actual == "+ve" and predicted == "-ve"):
                    fn = "FN"
                    fn_counter += 1
                    newLine = line + "\t" + fn
                elif (actual == "-ve" and predicted == "+ve"):
                    fp = "FP"
                    fp_counter += 1
                    newLine = line + "\t" + fp
                else:
                    tn = "TN"
                    tn_counter += 1
                    newLine = line + "\t" + tn   #adding tp/fp/tn/fn to the previous line

                #writing the final list
                newFile.write(newLine + "\n")

            #storing value of each in a list

            print (tp_counter)
            print (tn_counter)
            print (fn_counter)
            print(fp_counter)

        print("Done!")

    def matrixCalculation(self, _files):
        #newFile = open("matrix_clc_col_added.txt" , "w")
        newFile_1 = open("counter_calculation.txt" , "w")
        tp = 0
        fn = 0
        fp = 0
        tn = 0
        actual_yes = 0
        actual_no = 0
        tpr = 0
        fpr = 0
        cm_lists = list()*len(_files)

        #storing each line of the file in a list then isolating 3rd and 5th column
        for _file in _files:
            with open(_file, "r") as file:
                for i, line in enumerate(file):

                    line = line.rstrip("\n")
                    #isolating actual labels
                    actual = line.split('\t')[2]
                    #isolating predicted labels
                    predicted = line.split('\t')[4]
                #checking which one is tp/fp/tn/fn
                    if (actual == "+ve" and predicted == "+ve"):
                        #tp = "TP"
                        tp += 1
                        #newLine = line + "\t" + tp
                    elif (actual == "+ve" and predicted == "-ve"):
                        #fn = "FN"
                        fn += 1
                        #newLine = line + "\t" + fn
                    elif (actual == "-ve" and predicted == "+ve"):
                        #fp = "FP"
                        fp += 1
                        #newLine = line + "\t" + fp
                    else:
                        #tn = "TN"
                        tn += 1
                        #newLine = line + "\t" + tn   #adding tp/fp/tn/fn to the previous line

                #writing the final list
                #newFile.write(newLine + "\n")

            #storing value of each in a list
            actual_yes=tp+fn
            actual_no=fp+tn
            tpr = tp/actual_yes
            fpr = fp/actual_no

            cm_lists.append([str(tp), str(fn), str(fp), str(tn), str(actual_yes), str(actual_no), str(tpr),str(fpr)])

        for cm_list in cm_lists:
            newFile_1.write("\t".join(cm_list) + "\n")

        print("Done!")

    def plotlyTable(self, _file):

        with open(_file, "r") as file:
            for i, line in enumerate(file):
                line = line.rstrip("\n")
                if (i==0):
                    data_matrix = [['True Positive (TP)','False Negative (FN)','False Positive (FP)', 'True Negative (TN)', 'Actual Yes', 'Actual No', 'True Posive Rate (TPR)', 'False Positive Rate (FPR)'],
                    line.split("\t")]

        table = ff.create_table(data_matrix)
        plotly.offline.plot(table, filename='simple_table')
        print ("Done")
'''

    data_matrix = [['Country', 'Year', 'Population'],
               ['United States', 2000, 282200000],
               ['Canada', 2000, 27790000],
               ['United States', 2005, 295500000],
               ['Canada', 2005, 32310000],
               ['United States', 2010, 309000000],
               ['Canada', 2010, 34000000]]

    table = ff.create_table(data_matrix)
    plotly.offline.plot(table, filename='simple_table')

    print("done")
'''
