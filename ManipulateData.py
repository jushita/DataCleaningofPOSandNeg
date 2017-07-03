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
