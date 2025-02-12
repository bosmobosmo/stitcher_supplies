from logging import getLogger

from psycopg2 import errors
from odoo.tests import tagged
from odoo.tests.common import SavepointCase

logger = getLogger(__name__)


@tagged('post_install', '-at_install', 'stitcher_supplies')
class MaterialTestCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(MaterialTestCase, cls).setUpClass()
        cls.materials = cls.env['stitcher_supplies.material']
        cls.suppliers = cls.env['stitcher_supplies.supplier']

    def test_invalid_buy_price(self):
        with self.assertRaises(errors.CheckViolation):
            self.materials.create([
                {
                    'code': '2532',
                    'buy_price': 50,
                    'supplier_id': 1
                }
            ])

    def test_invalid_supplier(self):
        suppliers = self.suppliers.search([], order='id')
        max_supplier_id = suppliers[-1].id
        with self.assertRaises(errors.ForeignKeyViolation):
            self.materials.create([
                {
                    'code': '4082',
                    'buy_price': 100,
                    'supplier_id': max_supplier_id + 1
                }
            ])
