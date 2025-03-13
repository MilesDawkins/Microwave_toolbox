import csv

class spreadsheet():
    def __init__(self,file):
        self.data = [[]]
        self.read_csv(file)

    def read_csv(self,file_path):
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                for i in row:
                    self.data[line_count].append(i) 
                self.data.append([])
                line_count += 1
    
    
    def col_2_list(self,column):
        col_data = []*1
        for i in self.data:
            col_data.append(i[column])
        return col_data