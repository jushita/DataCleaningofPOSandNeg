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

                if os.path.isfile(file_protein1):
                    with open(file_protein1) as file:
                        for line in file:
                            other_protein = line.split("\t")[0]
                            if split_line[1] == other_protein:
                                lpip = line.split('\t')[5]
                                split_line.append(lpip.rstrip('\n'))
                elif os.path.isfile(file_protein2):
                    with open(file_protein2) as file:
                        for line in file:
                            other_protein = line.split("\t")[0]
                            if split_line[0] == other_protein:
                                lpip = line.split('\t')[5]
                                split_line.append(lpip.rstrip('\n'))
                else:
                    split_line.append("0.00")

                new_file.write("\t".join(split_line) + "\n")

    print ("Done")

    def predictedLikelihoodRatioVal(self, _file, val):

        predicted_likelihoo_value_column_added = open("pr_lr_file" + ".txt", "w")

        with open(_file, "r") as file:
            for i, line in enumerate(file):
                if (i==5):
                    break
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
                predicted_likelihoo_value_column_added.write(lr_prLrval + "\n")
