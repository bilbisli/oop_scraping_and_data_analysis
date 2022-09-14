import os
import glob

path = 'c:\\'
extension = 'csv'
os.chdir(path)
result = glob.glob('*.{}'.format(extension))
print(result)