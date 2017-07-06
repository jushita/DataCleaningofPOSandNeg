import os

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

    def predictedLikelihoodRatioVal(self, _file, val):

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

    def matrixCalculationCol(self, _file):
        newFile = open("matrix_clc_col_added.txt" , "w")
        newFile_1 = open("counter_calculation.txt" , "w")
        tp_counter = 0
        fn_counter = 0
        fp_counter = 0
        tn_counter = 0


        with open(_file, "r") as file:
            for i, line in enumerate(file):

                line = line.rstrip("\n")
                actual = line.split('\t')[2]
                predicted = line.split('\t')[4]

                if (actual == "+ve" and predicted == "+ve"):
                    tp = "TP"
                    tp_counter += 1
                    newCol = line + "\t" + tp
                if (actual == "+ve" and predicted == "-ve"):
                    fn = "FN"
                    fn_counter += 1
                    newCol = line + "\t" + fn
                if (actual == "-ve" and predicted == "+ve"):
                    fp = "FP"
                    fp_counter += 1
                    newCol = line + "\t" + fp
                if (actual == "-ve" and predicted == "-ve"):
                    tn = "TN"
                    tn_counter += 1
                    newCol = line + "\t" + tn

                newFile.write(newCol+ "\n")

            cmList= [tp_counter, fn_counter, fp_counter, tn_counter]
            cmList = str(cmList)
            print (tp_counter)
            #print("\n")
            print (fn_counter)
            #print("\n")
            print (fp_counter)
            #print("\n")
            print (tn_counter)
            #print("\n")
            newFile_1.write(cmList)
