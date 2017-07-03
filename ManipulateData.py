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
