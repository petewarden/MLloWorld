import csv
import numpy as np
import scipy.sparse as sp

# Takes our Kaggle data sets, where some of the columns are lists of space-separated
# numbers representing words, and expands them into a flat array containing a binary
# value for each possible word, indicating if it was present
def expand_to_vectors(filename, code_headers, target_header=None):
  code_headers_map = {}
  for index, header in enumerate(code_headers):
    code_headers_map[header] = index
  reader = csv.reader(open(filename))
  max_code = 0
  max_index = 0
  max_i = 0
  for i, input_row in enumerate(reader):
    max_i = max(max_i, i)
    if i == 0:
      continue # Skip header row
    for index, value in enumerate(input_row):
      max_index = max(max_index, index)
      if index in code_headers_map:
        codes = value.split(' ')
        for code_string in codes:
          if code_string == '':
            continue
          code = int(code_string)
          max_code = max(max_code, code)
  max_j = max_index+(len(code_headers)*max_code)
  reader = csv.reader(open(filename))
  i_indices = []
  j_indices = []
  values = []
  target = []
  for i, input_row in enumerate(reader):
    if i == 0:
      continue # Skip header row
    for index, value in enumerate(input_row):
      if index == target_header:
        target.append(int(value))
      elif index in code_headers_map:
        code_offset = max_index+(code_headers_map[index]*max_code)
        codes = value.split(' ')
        for code_string in codes:
          if code_string == '':
            continue
          code = int(code_string)
          i_indices.append(i-1)
          j_indices.append(code_offset+code)
          values.append(1.0)
      elif index != 0:
        i_indices.append(i-1)
        j_indices.append(index)
        values.append(int(value))
  shape = (max_i+1, max_j+1)
  output = sp.coo_matrix((values, (i_indices, j_indices)), shape=shape, dtype=np.dtype(float))
  return (output, target)
