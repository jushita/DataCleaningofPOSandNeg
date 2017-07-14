from __future__ import print_function
import os, glob
import plotly
import plotly.figure_factory as ff
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *
import plotly.graph_objs as go
from operator import itemgetter
import numpy as np
from scipy.integrate import simps
from numpy import trapz
import collections

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

    def predictedLikelihoodRatioVal(self, _file):
        values = [0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,10,20,30,40,50,60,70,80,90,100,200,
        300,400,500,600,700,800,900,1000,10000,20000,30000,40000,50000,79000]

        for val in values:
            newFile = open("PL_" + str(val) + ".txt", "w")

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
                        lr_prLrval =line + "\t" + prLrval
                    else:
                        prLrval = "-ve"
                        split_line = str(split_line)
                        lr_prLrval =line + "\t" + prLrval
                    #writing in a new file
                    newFile.write(lr_prLrval + "\n")

        print("Done")

    def getPredeictedLikelihoodFiles(self):
        files = list()

        for file in glob.glob("PL_*.txt"):
            files.append(file)
            files=sorted(files)

        return files
        #print(files)

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
            print(tp_counter,fn_counter,fp_counter,tn_counter)

        print("Done!")

    def matrixCalculation(self, _files):
        #newFile = open("matrix_clc_col_added.txt" , "w")
        newFile_1 = open("counter_calculation.txt" , "w")

        cm_lists = list()*len(_files)
        #opening one file for each loop and re-initializing the counters
        for _file in _files:
            tp = 0
            fn = 0
            fp = 0
            tn = 0
            actual_yes = 0
            actual_no = 0
            tpr = 0
            fpr = 0
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
                        tp += 1
                    elif (actual == "+ve" and predicted == "-ve"):
                        fn += 1
                    elif (actual == "-ve" and predicted == "+ve"):
                        fp += 1
                    else:
                        tn += 1
                        #newLine = line + "\t" + tn   #adding tp/fp/tn/fn to the previous line
            actual_yes=tp+fn
            actual_no=fp+tn
            tpr = tp/actual_yes
            fpr = fp/actual_no

            cm_lists.append([str(tp), str(fn), str(fp), str(tn), str(actual_yes), str(actual_no), str(tpr),str(fpr)])

        for cm_list in cm_lists:
            newFile_1.write("\t".join(cm_list) + "\n")

        print("Done!")

    def valCol(self, _file):
        '''THIS FUNCTION ADDS THE LIKELIHOOD COLUMN TO THE FINAL OUTPUT FILE'''
        #creating a new file
        newFile=open("Confusion Matrix Table.txt","w")
        values = ['0.01','0.02','0.03','0.04','0.05','0.06','0.07','0.08','0.09','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','0','1','10','100',
        '1000','10000','20','200','20000','30','300','30000','40', '400','40000','50','500','50000','60','600','70','700','79000','80','800','90','900']
        #opening the file where we want the values to be added as the first column
        with open(_file, "r") as file:
            for i, line in enumerate(file):
                #taking off \n from each line
                line = line.rstrip("\n")
                #splitting each lines into a list of elements where they are finding \t
                split_line = line.split("\t")
                #inserting the first column as values
                split_line.insert(0, values[i])
                #saving it into a separate list
                saved=split_line
                #joining the list and inserting "\t" between each element
                newSaved="\t".join(saved)
                #wriing the new variable with each line and entering new line at the end of each line
                newFile.write(newSaved+"\n")
        print("DONE")

    def sortConfusionMatrices(self,_file):
        newFile=open("Confusion Matrix Table (Sorted).txt","w")
        listofMatrix=list()*45
        with open(_file, "r") as file:
            for i, line in enumerate(file):
                #taking off \n from each line
                line = line.rstrip("\n")
                #splitting each lines into a list of elements where they are finding \t
                split_line = line.split("\t")
                split_line[0] = float(split_line[0])
                listofMatrix.append(split_line)

            l=sorted(listofMatrix, key=itemgetter(0))
            for each in l:
                each[0] = str(each[0])
                newSaved="\t".join(each)
                newFile.write(newSaved+ "\n")


    def plotlyTable(self, _file):
        '''THIS FUNCTION CREATES THE PLOTLY TABLE'''
        new_list= list()*len(_file)
        print(len(_file))
        first_line ='Likelihood\t'  'True Positive (TP)\t'   'False Negative (FN)\t'   'False Positive (FP)\t'   'True Negative (TN)\t'    'Actual Yes\t'    'Actual No\t' 'True Posive Rate (TPR)\t'    'False Positive Rate (FPR)\n'
        first_line = first_line.rstrip("\n")
        first_line=first_line.split("\t")

        new_list.append(first_line)
        with open(_file, "r") as file:
            for i, line in enumerate(file):
                #print (line)
                line = line.rstrip("\n")
                line = line.split("\t")
                new_list.append(line)
            data_matrix=new_list

        table = ff.create_table(data_matrix)
        plotly.offline.plot(table, filename='Confusion Matrix Values')
        print ("Done")

    def rocGraph(self, _file):
        with open (_file, "r") as file:
            xList=list()*27
            yList=list()*27
            for i, line in enumerate(file):
                line = line.rstrip("\n")
                tpr = line.split('\t')[7]
                fpr = line.split('\t')[8]
                xList.append(fpr)
                yList.append(tpr)
            trace1 = go.Scatter(
            x=xList,
            y=yList,
            line=dict(color="navy"),name='ROC curve'
            )
            trace2= go.Scatter(
            x=[0,1],
            y=[0,1],
            line=dict(color="orange", dash="dash"),
            showlegend=False
            )
            data = [trace1,trace2]
            layout = go.Layout(title="Receiver Operating Characteristic (ROC)",
            xaxis=dict(type='linear',title="False Positive Rate",autorange=True),
            yaxis=dict(type='linear',title="True Positive Rate", autorange=True))

            fig=go.Figure(data=data, layout=layout)
            plotly.offline.plot(fig)

    def auc(self,_file):
        x=list()*45
        y=list()*45
        new_dict=dict()
        with open(_file, "r") as file:
            for i, line in enumerate(file):
                #taking off \n from each line
                line = line.rstrip("\n")
                #splitting each lines into a list of elements where they are finding \t
                split_line = line.split("\t")
                fpr = float(split_line[8])
                tpr = float(split_line[7])
                new_dict[fpr]=tpr
            new_dict= collections.OrderedDict(sorted(new_dict.items()))
            for key, value in new_dict.items():
                x.append(key)
                y.append(value)
            area = trapz(y, x)
            print("area =", area)
