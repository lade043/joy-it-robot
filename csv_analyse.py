import time
import csv

file = "sequence.csv"
with open(file) as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        if "delay" in row[0]:
            print("sleep " + row[0].split(" ")[1])
            time.sleep(int(row[0].split(" ")[1]))
        else:
            for count, i in enumerate(row):
                print(i)
                print(count)
