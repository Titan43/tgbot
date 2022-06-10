import json
import random
from datetime import datetime

def write_json(new_data, filename):

    flag = True
    with open(filename+'.json','r+') as file:
        file_data = json.load(file)
        if new_data not in file_data[filename]:
            file_data[filename].append(new_data)
        else:
            flag = False
        file.seek(0)
        json.dump(file_data, file)
        
    return flag

def getime(loginfo):
	with open('log.txt', 'a') as file:
		file.write(loginfo+str(datetime.now()))
		file.write('\n')

def addtotxtfile(msgtxt, filename):
	with open('srcfiles/'+filename, 'a') as file:
		file.write(msgtxt)
		file.write('\n')

def cljson(filename='predicted.json'):
    with open(filename,'r+') as file:
        file.seek(0)
        file.truncate()
        file_data = {"predicted": []}
        json.dump(file_data, file, indent = 4)


def get_data(filename):
    with open(filename+'.json','r+') as file:
        file_data = json.load(file)
        return file_data


def advis(filename):
    with open('srcfiles/'+filename, 'r+', encoding='utf-8-sig') as file:
        dataf = file.readlines()
        random.seed(datetime.now())
        return dataf[random.randint(0, len(dataf) - 1)]

