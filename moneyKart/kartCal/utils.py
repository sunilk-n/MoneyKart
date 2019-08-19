import datetime
import re
import json
import os

try:
    from moneyKart import lib
except:
    modulePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    libPath = os.path.join(modulePath, 'lib')
    os.mkdir(libPath)
    with open(os.path.join(libPath, '__init__.py'), 'w') as libModule:
        libModule.write('""" Data storing module\n"""')
    from moneyKart import lib


types = ['spend', 'earn']
seTypes = ['personal', 'grocery', 'bill', 'salary', 'weekend', 'other']

fileName = "spendEarnTable.json"
libPath = lib.__path__[0]
FILEPATH = os.path.join(libPath, fileName)


def getNextEntry(data, type):
    latest = 1
    if data[type]:
        latest = max([int(i) for i in data[type].keys()]) + 1
    return latest


def convertFromDate(date):
    """ Must have date format as 'dd-mm-yyyy'
    """
    pattern = r"([0-3]?[0-9])[-/.]([0-3]?[0-9])[-/.]((?:[0-9]{2})?[0-9]{2})"
    matchObj = re.match(pattern, date)
    if matchObj:
        dater = datetime.datetime(
            int(matchObj.group(3)),
            int(matchObj.group(2)),
            int(matchObj.group(1))
        )
    else:
        raise ValueError("Invalid date format, Please maintain dd-mm-yyy or dd/mm/yyyy or dd.mm.yyyy")
    return dater


def convertToDate(dateTime):
    if isinstance(dateTime, datetime.datetime):
        date = "{DATE}-{MONTH}-{YEAR}".format(
            DATE=str(dateTime.day).zfill(2),
            MONTH=str(dateTime.month).zfill(2),
            YEAR=dateTime.year
        )
    else:
        raise ValueError("Invalid datetime. Please follow datetime instance")
    return date


def buildSpendEarnTable():

    defaultValues = {}
    for value in types:
        defaultValues.update({value: {}})

    if not os.path.exists(FILEPATH):
        addDefaultValues(defaultValues)
    else:
        data = open(FILEPATH)
        if not len(data.read()):
            addDefaultValues(defaultValues)


def addDefaultValues(values):
    with open(FILEPATH, 'w') as fd:
        json.dump(values, fd, indent=2, sort_keys=True)


def readValues(filePath):
    with open(filePath, 'r') as fd:
        data = json.load(fd)
    return data

if not os.path.exists(FILEPATH):
    buildSpendEarnTable()

if __name__ == '__main__':
    buildSpendEarnTable()
