#!/usr/bin/env python
import csv
import sys

# Takes in a CSV file that starts with a header row, and returns an array of
# dictionaries, with the keys set by the names in the header.
def load_csv(filename):
  reader = csv.reader(open(filename)) or die('Couldn\'t open '+filename)
  line = 0
  output = {}
  for input_row in reader:
    line += 1
    if line == 1:
      headers = input_row
    else:
      key = input_row[0]
      value = float(input_row[1])
      output[key] = value
  return output

solution_name = sys.argv[1]
solution = load_csv(solution_name)

candidate_name = sys.argv[2]
candidate = load_csv(candidate_name)

threshold = float(sys.argv[3])

true_positives = 0
true_negatives = 0
false_positives = 0
false_negatives = 0
for key, solution_value in solution.items():
  candidate_value = candidate[key]
  solution_good = (solution_value > threshold)
  candidate_good = (candidate_value > threshold)
  if candidate_good and solution_good:
    true_positives += 1
  elif (not candidate_good) and (not solution_good):
    true_negatives += 1
  elif candidate_good:
    false_positives += 1
  else:
    false_negatives += 1

total = (true_positives + true_negatives + false_positives + false_negatives)  
true_positives_percentage = round((true_positives*1000.0)/total)/10
true_negatives_percentage = round((true_negatives*1000.0)/total)/10
false_positives_percentage = round((false_positives*1000.0)/total)/10
false_negatives_percentage = round((false_negatives*1000.0)/total)/10

print str(true_positives_percentage)+'% true positives, '+str(false_positives_percentage)+'% false positives, '+str(true_negatives_percentage)+'% true negatives, '+str(false_negatives_percentage)+'% false negatives'