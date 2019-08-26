""" Spends, Earns transaction API
"""
from moneyKart.kartCal.utils import *


class SpendEarn(object):
    """ Class to maintain the spend or earn object
    """
    def __init__(self, comment, amount, date=None, id=None, type="spend", setType='personal'):
        self._comment = comment
        self._amount = float(amount)
        if date:
            self._date = convertToDate(convertFromDate(date))
        else:
            self._date = convertToDate(datetime.datetime.now())
        if self.validateType(type, types):
            self._type = type
        else:
            raise ValueError("Unable to validate the spend/earn type")
        if self.validateType(setType, seTypes):
            self._setType = setType
        else:
            raise ValueError("Unable to validate type of spend/earn")

        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def comment(self):
        return self._comment

    @property
    def amount(self):
        return self._amount

    @property
    def date(self):
        if self._date:
            date = convertFromDate(self._date)
        else:
            date = datetime.datetime.now()
        return date

    @property
    def type(self):
        return self._type

    @property
    def setType(self):
        return self._setType

    def validateType(self, type, typeList):
        result = False
        if type in typeList:
            result = True
        return result


class GetSpendEarn(object):
    """ Class to get the spends and earns data
    """
    def __init__(self):
        self.jsonFile = FILEPATH
        self.updateData()

    def getSpends(self):
        """ Definition to get all the spends data

            :return spendDetails(list): All spend data list from json file
        """
        spendDetails = []
        if self.data:
            for eachSpend in self.data['spend'].keys():
                spendData = self.data['spend'][eachSpend]
                spend = SpendEarn(
                            comment=spendData[0], amount=spendData[1],
                            date=spendData[2], id=eachSpend, type='spend',
                            setType=spendData[3]
                        )
                spendDetails.append(spend)
        return spendDetails

    def getEarns(self):
        """ Definition to get all the earns data

            :return earnDetails(list): All earn data list from json file
        """
        earnDetails = []
        if self.data:
            for eachSpend in self.data['earn'].keys():
                spendData = self.data['earn'][eachSpend]
                spend = SpendEarn(
                            comment=spendData[0], amount=spendData[1],
                            date=spendData[2], id=eachSpend, type='earn',
                            setType=spendData[3]
                        )
                earnDetails.append(spend)
        return earnDetails

    def updateData(self):
        """ Definition to update the class variables
        """
        self.data = readValues(self.jsonFile)
        self.spendEarns = self.getSpends() + self.getEarns()
        self.sortByField()

    def sortByField(self, field='date', ascend=False):
        """ Definition to sort the data collected

            :param field(str): Sort by field from the json file, default is data
            :param ascend(bool): Sort by reversed data, default False
        """
        if field == 'date':
            self.spendEarns.sort(key=lambda x:x.date, reverse=ascend)
        elif field == 'amount':
            self.spendEarns.sort(key=lambda x:x.amount, reverse=ascend)

    def addSpendEarn(self, spendEarn):
        """ Definition to add the spend or earn values to the data

            :param spendEarn(SpendEarn): SpendEarn object to get the data
            :return (bool): returns True if success or False
        """
        latest = spendEarn.id
        if not latest:
            latest = getNextEntry(self.data, spendEarn.type)
        values = [
            spendEarn.comment, spendEarn.amount,
            convertToDate(spendEarn.date),
            spendEarn.setType
        ]
        spendEarnDict = {str(latest): values}
        if not self.pushEntry(spendEarnDict, spendEarn.type):
            return False
        return True

    def pushEntry(self, spendEarnDict, type):
        """ Definition to push the entry to json file

        :param spendEarnDict(dict): Data dict to store the data to json
        :param type(str): spend or earn type will only be accepted
        :return (bool): Returns boolean if the json file is written
        """
        dictSpendEarn = self.data[type]
        dictSpendEarn.update(spendEarnDict)
        self.data[type] = dictSpendEarn
        with open(self.jsonFile, 'w') as fd:
            json.dump(self.data, fd, indent=2, sort_keys=True)
        self.updateData()
        return True

    def deleteEntry(self, id, type):
        """ Definition to delete the entry from the data

        :param id(str): Id of the data entry
        :param type(str): spend or earn type will only be accepted
        :return (bool): Returns boolean if the json file is written
        """
        self.data[type].pop(id)
        with open(self.jsonFile, 'w') as fd:
            json.dump(self.data, fd, indent=2, sort_keys=True)
        self.updateData()
        return True

    @property
    def decendSpendEarns(self):
        self.updateData()
        reverseSpendEarn = []
        for spendEarnsIndex in range(len(self.spendEarns)):
            reverseSpendEarn.append(self.spendEarns[len(self.spendEarns)-spendEarnsIndex-1])
        return reverseSpendEarn

    def sumOfSpendEarn(self, month=None, type='spend'):
        # month set to None if want to get whole total of type
        if month:
            amounts = [i.amount for i in self.spendEarns if i.date.month == month and i.type == type]
        else:
            amounts = [i.amount for i in self.spendEarns if i.type == type]
        return str(round(sum(amounts), 2))

    def spendEarnByDate(self, date, type='spend'):
        date = convertFromDate(date)
        amounts = [i.amount for i in self.spendEarns if i.date == date and i.type == type]
        if amounts:
            return round(sum(amounts), 2)
        else:
            return 0.0

    def spendEarnByList(self):
        earnData = []
        spendData = []
        today = datetime.datetime.today()
        dateFormat = "{dd}/{mm}/{yyyy}"
        for each in range(1, today.day+1):
            date = dateFormat.format(
                        dd=each, mm=today.month,
                        yyyy=today.year
                    )
            spendData.append(self.spendEarnByDate(date))
            earnData.append(self.spendEarnByDate(date, 'earn'))
        return spendData + earnData
