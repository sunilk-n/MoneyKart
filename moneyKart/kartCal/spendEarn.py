from moneyKart.kartCal.utils import *


class SpendEarn(object):
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
    def __init__(self):
        self.jsonFile = FILEPATH
        self.updateData()

    def getSpends(self):
        spendDetails = []
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
        spendDetails = []
        for eachSpend in self.data['earn'].keys():
            spendData = self.data['earn'][eachSpend]
            spend = SpendEarn(
                        comment=spendData[0], amount=spendData[1],
                        date=spendData[2], id=eachSpend, type='earn',
                        setType=spendData[3]
                    )
            spendDetails.append(spend)
        return spendDetails

    def updateData(self):
        self.data = readValues(self.jsonFile)
        self.spendEarns = self.getSpends() + self.getEarns()
        self.sortByField()

    def sortByField(self, field='date', ascend=False):
        if field == 'date':
            self.spendEarns.sort(key=lambda x:x.date, reverse=ascend)
        elif field == 'amount':
            self.spendEarns.sort(key=lambda x:x.amount, reverse=ascend)

    def addSpendEarn(self, spendEarn):
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
        dictSpendEarn = self.data[type]
        dictSpendEarn.update(spendEarnDict)
        self.data[type] = dictSpendEarn
        with open(self.jsonFile, 'w') as fd:
            json.dump(self.data, fd, indent=2, sort_keys=True)
        self.updateData()
        return True

    def deleteEntry(self, id, type):
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

if __name__ == '__main__':
    a = GetSpendEarn()
    # b = SpendEarn(comment="Rent", amount=11500,
    #               date="01-07-2019", type="spend", setType="bill")
    # a.addSpendEarn(b)
    print(a.spendEarns)

