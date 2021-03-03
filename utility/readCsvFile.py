import csv
from .mapData import mapUser, mapResult


def openCSVFile(filename, mapUserComputerList):
    dataList = []
    with open(filename) as file:
        csvReader = csv.reader(file, delimiter=',')

        for row in csvReader:
            data = []
            #time = row[0]
            #sourceUserDomain = row[1]
            #destUserDomain = row[2]
            #sourceComputer = row[3]
            #destComputer = row[4]
            #authtype = row[5]
            #logontype = row[6]
            #authOrientation = row[7]
            #success/failure = row[8]

            #skip ? values
            if (row[3] != "?" and row[4] != "?" and row[8] != "?"):
                d, mapUserComputerList = mapUser(row[3], mapUserComputerList)
                data.append(d)#assign int to different users/computers
                d, mapUserComputerList = mapUser(row[3], mapUserComputerList)
                data.append(d)
                r, _ = mapResult(row[8])
                data.append(r)#turn success to 0 and fail to 1
                #if (row[8] != "Success"):
                #    print(row[3]+","+row[4]+","+row[8])

            dataList.append(data)

    return dataList, mapUserComputerList

import string

def readAllCSVFile(fileNamePrefix):
    data = []
    mapList = []
    #load data from authpartitionaa to authpartiitonzz files
    for firstLetter in string.ascii_lowercase:
        for secondLetter in string.ascii_lowercase:
            fullFileName = fileNamePrefix + firstLetter + secondLetter
            #print(fullFileName)
            d, mapList = openCSVFile(fullFileName, mapList)
            data.extend(d)
    return data, mapList

def readRedTeam(filename, mapUserComputerList):
    dataList = []
    with open(filename) as file:
        csvReader = csv.reader(file, delimiter=',')

        for row in csvReader:
            data = []
            #time = row[0]
            #UserDomain = row[1]
            #sourceComputer = row[2]
            #destComputer = row[3]

            #skip ? values
            if (row[1] != "?" and row[2] != "?" and row[3] != "?"):
                d, mapUserComputerList = mapUser(row[2], mapUserComputerList)
                data.append(d)#assign int to different users/computers
                d, mapUserComputerList = mapUser(row[3], mapUserComputerList)
                data.append(d)
                data.append(1)#should be failed for all red team data


            dataList.append(data)

    return dataList, mapUserComputerList
