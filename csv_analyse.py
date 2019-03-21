import time
import csv

file = "/home/lars/Schreibtisch/sequence.csv"
with open(file) as f:
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        if "delay" in row[0]:
            print("sleep " + row[0].split(" ")[1])
            time.sleep(int(row[0].split(" ")[1]))
        else:
            f = 0
            for i in row:
                print(i)
                print(str(f))
                f += 1
