'''
This file combines data from balance sheet, income statement, cash flow statement
to get intersections, and stores those intersections into
../data/processed_data/combined_filtered_data_intersection.txt
'''
def getMapAndHeaderFromFile(file_path):
  # key: (Symbol,Period Ending), value: the rest
  res = {}
  res_header = []
  with open(file_path, 'r') as f:
    content = f.read().split('\n')
    res_header = content[0].split(',')
    content.pop(0)
    for row in content:
      tokens = row.split(',')
      key = tokens[:2]
      value = tokens[2:]
      res[tuple(key)] = value

  return res, res_header

if __name__ == '__main__':
  balance_sheet_filtered_data_path = '../data/processed_data/balance_sheet_filtered_data.txt'
  income_statement_filtered_data_path = '../data/processed_data/income_statement_filtered_data.txt'
  cash_flow_statement_filtered_data_path = '../data/processed_data/cash_flow_statement_filtered_data.txt'


  balance_sheet, balance_sheet_header = getMapAndHeaderFromFile(balance_sheet_filtered_data_path)
  print(len(balance_sheet))
  print(balance_sheet_header)

  income_statement, income_statement_header = getMapAndHeaderFromFile(income_statement_filtered_data_path)
  print(len(income_statement))
  print(income_statement_header)

  cash_flow_statement, cash_flow_statement_header = getMapAndHeaderFromFile(cash_flow_statement_filtered_data_path)
  print(len(cash_flow_statement))
  print(cash_flow_statement_header)


  output_path = '../data/processed_data/combined_filtered_data_intersection.txt'
  with open(output_path, 'w') as f:
    f.write(','.join(balance_sheet_header) + ',' +
      ','.join(income_statement_header[2:]) + ',' +
      ','.join(cash_flow_statement_header[2:]) +
      '\n')
    for k in balance_sheet:
      if k not in income_statement:
        continue
      if k not in cash_flow_statement:
        continue

      f.write(','.join(k) + ',' +
        ','.join(balance_sheet[k]) + ',' +
        ','.join(income_statement[k]) + ',' +
        ','.join(cash_flow_statement[k]) +
        '\n')