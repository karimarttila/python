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
    # A raw product should have 8 items.
    assert (len(raw_products_1[0])) == 8
    # What a coincidence - it is the national book of Finland.
    assert raw_products_1[0][2] == 'Kalevala'
    # What a coincidence! The chosen movie is the best western of all times!
    assert raw_products_2[48][2] == 'Once Upon a Time in the West'
    raw_products_3 = myDomain.get_raw_products(3)  # No such product group id.
    assert raw_products_3 is None
    myLogger.debug(EXIT)


def test_get_products():
    myLogger.debug(ENTER)
    products_1 = myDomain.get_products(1)
    products_2 = myDomain.get_products(2)
    assert len(products_1) == 35
    assert len(products_2) == 169
    # A product should have 4 items.
    assert (len(products_1[0])) == 4
    # What a coincidence - it is the national book of Finland.
    assert products_1[0][2] == 'Kalevala'
    # What a coincidence! The chosen movie is the best western of all times!
    assert products_2[48][2] == 'Once Upon a Time in the West'
    products_3 = myDomain.get_products(3)  # No such product group id.
    assert products_3 is None
    myLogger.debug(EXIT)


def test_get_product():
    myLogger.debug(ENTER)
    product = myDomain.get_product(2, 49)
    assert len(product) == 8
    # What a coincidence! The chosen movie is the best western of all times!
    assert product[2] == 'Once Upon a Time in the West'
    product = myDomain.get_product(2, 10000)  # No such product id.
    assert product is None
    product = myDomain.get_product(3, 10000)  # No such product group id.
    assert product is None
    myLogger.debug(EXIT)

