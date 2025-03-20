import csv

class spreadsheet():
    def __init__(self,file, titled = None):
        self.data = [[]]
        self.titles = []
        if titled == True:
            self.read_csv(file,titled = True)
        else:
            self.titled = False
            self.read_csv(file)

    def read_csv(self,file_path,titled = None):
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                self.data.append([])
                for i in row:
                    self.data[line_count].append(i) 
                line_count += 1
        self.data.pop(int(len(self.data)-1))
        if titled  == True:
            self.titles = self.data[0]
            self.data.pop(0)
    
    def col_2_list(self,column):
        col_data = []*1
        for i in self.data:
            col_data.append(i[column])
        return col_data