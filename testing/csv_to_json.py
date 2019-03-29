import csv
import json

#Read the input.csv and convert it to output.json
csvfile = open('input.csv', 'r')
jsonfile = open('output.json', 'w')

#Sort each row with cooresponding attribute to json format
fieldnames = ("")
csvReader = csv.DictReader(csvfile, fieldnames)
for csvRow in csvReader:
    json.dump(csvRow, jsonfile)
    jsonfile.write('\n')
