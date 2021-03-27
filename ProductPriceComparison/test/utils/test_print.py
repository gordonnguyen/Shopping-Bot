import datetime


def test_print():
    print('SUCCESS')

def printCurrentDateTime():
    print(datetime.datetime.now().strftime('< %m/%d/%Y - %H:%M:%S >'))

printCurrentDateTime()