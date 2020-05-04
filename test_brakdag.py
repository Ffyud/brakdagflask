import pytest

from service import BronService

def testAll():
    selectall = BronService.selectAll()

    # assert selectall == 0