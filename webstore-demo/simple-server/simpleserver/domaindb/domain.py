import csv
from typing import Dict, Any

from simpleserver.util.consts import ENTER, EXIT
from simpleserver.util.logger import SSLogger


# Run this in Console to refresh module in console:
# runfile('/mnt/edata/aw/kari/github/python/webstore-demo/simple-server/simpleserver/domaindb/domain.py',
#     wdir='/mnt/edata/aw/kari/github/python/webstore-demo/simple-server')

class Domain:
    """Domain class."""

    myLogger = SSLogger(__name__).get_logger()

    def __read_product_groups(self):
        """Read product groups from csv and returns a dictionary of product groups."""
        self.myLogger.debug(ENTER)
        ret = {}
        with open('resources/product-groups.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            rows = []
            for row in csv_reader:
                rows.append(row)
        for row in rows:
            key = row[0]
            value = row[1]
            ret[key] = value
        self.myLogger.debug(EXIT)
        return ret

    def __read_raw_products_for_pg(self, pg_id):
        """Read raw products for a product group id."""
        self.myLogger.debug(ENTER)
        ret = []
        with open('resources/pg-' + str(pg_id) + '-products.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for row in csv_reader:
                ret.append(row)
        self.myLogger.debug(EXIT)
        return ret

    def __transform_to_products(self, raw_products):
        """Returns the first four elements of every product."""
        self.myLogger.debug(ENTER)
        ret = list(map((lambda x: x[:4]), raw_products))
        self.myLogger.debug(EXIT)
        return ret

    def __read_raw_products(self):
        """Read raw products for all product groups."""
        self.myLogger.debug(ENTER)
        ret = {}
        pg_ids = list(self.__read_product_groups().keys())
        for pg_id in pg_ids:
            raw_products = self.__read_raw_products_for_pg(pg_id)
            ret['pg-' + str(pg_id) + '-raw-products'] = raw_products
            ret['pg-' + str(pg_id) + '-products'] = self.__transform_to_products(raw_products)
        self.myLogger.debug(EXIT)
        return ret

    def __init_product_db(self):
        """Initializes the product db (reads data from csv files)."""
        self.myLogger.debug(ENTER)
        ret = {}
        product_groups = self.__read_product_groups()
        ret['product-groups'] = product_groups
        raw_products: Dict[str, Any] = self.__read_raw_products()
        ret.update(raw_products)
        self.myLogger.debug(EXIT)
        return ret

    def get_product_groups(self):
        """Return product groups dictionary."""
        self.myLogger.debug(ENTER)
        self.myLogger.debug(EXIT)
        return self.product_db['product-groups']

    def get_raw_products(self, pg_id):
        """Returns raw products for a product group id,
        or None if product group id not found."""
        self.myLogger.debug(ENTER)
        key = 'pg-' + str(pg_id) + '-raw-products'
        try:
            ret = self.product_db[key]
        except KeyError:
            ret = None
        self.myLogger.debug(EXIT)
        return ret

    def get_products(self, pg_id):
        """Returns products for a product group id,
        or None if product group id not found."""
        self.myLogger.debug(ENTER)
        key = 'pg-' + str(pg_id) + '-products'
        try:
            ret = self.product_db[key]
        except KeyError:
            ret = None
        self.myLogger.debug(EXIT)
        return ret

    def get_product(self, pg_id, p_id):
        """Returns the product of given product group id and product id
        or None if product not found."""
        self.myLogger.debug(ENTER)
        key = 'pg-' + str(pg_id) + '-raw-products'
        try:
            raw_products = self.product_db[key]
        except KeyError:
            raw_products = None
        if not raw_products:
            ret = None
        else:
            product = list(filter((lambda x: x[0] == str(p_id)), raw_products))
            ret = product[0] if (len(product) > 0) else None
        self.myLogger.debug(EXIT)
        return ret

    def __init__(self):
        self.product_db = self.__init_product_db()
