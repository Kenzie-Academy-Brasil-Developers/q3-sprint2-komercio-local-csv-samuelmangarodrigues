import csv
import os

file_test=os.getenv('FILE_PATH')
print(file_test)
prod=[]
def base():
  files =open(file_test, "r")
  data_prod = csv.DictReader(files)
  for file in data_prod:
    prod.append(file)
  
  files.close()
  return prod


