import csv

def readCSV(file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        csv_return=[[]*1]*1
        for row in csv_reader:
            for i in row:
                csv_return[line_count].append(i) 
            csv_return.append([])
            line_count += 1
    return csv_return