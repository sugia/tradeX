from os import listdir
from hashlib import md5

if __name__ == '__main__':
  dir_path = '/Users/steve/Desktop/tradeX/data/cash_flow_statement/'
  files = listdir(dir_path)

  md5_file = {}
  for file in files:
    file_path = dir_path + file
    with open(file_path, 'rb') as f:
      content = f.read()
      key = md5(content)
      if key not in md5_file:
        md5_file[key] = []
      md5_file[key] = file

