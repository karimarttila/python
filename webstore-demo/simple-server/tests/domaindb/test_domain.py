import pytest
from simpleserver.util.consts import ENTER, EXIT
from simpleserver.util.logger import SSLogger
from simpleserver.domaindb.domain import Domain

myLogger = SSLogger(__name__).get_logger()
myDomain = Domain()

def test_get_product_groups():
    myLogger.debug(ENTER)
    product_groups = myDomain.get_product_groups()
    assert product_groups['1'] == 'Books'
    assert product_groups['2'] == 'Movies'
    myLogger.debug(EXIT)

def test_get_raw_products():
    myLogger.debug(ENTER)
    raw_products_1 = myDomain.get_raw_products(1)
    raw_products_2 = myDomain.get_raw_products(2)
    assert len(raw_products_1) == 35
    assert len(raw_products_2) == 169
    # What a coincidence - it is the national book of Finland.
    assert raw_products_1[0][2] == 'Kalevala'
    # What a coincidence! The chosen movie is the best western of all times!
    assert raw_products_2[48][2] == 'Once Upon a Time in the West'
    myLogger.debug(EXIT)

