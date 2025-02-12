from odoo import fields, models


class Material(models.Model):
    _name = 'keda.material'
    _description = 'Material details'
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Codes must be unique'),
        (
            'buy_price_min',
            'CHECK(buy_price >= 100)',
            'Buy price must be at least 100'
        )
    ]

    code = fields.Integer(required=True, copy=False)
    name = fields.Char()
    type = fields.Selection(
        string='Material Type',
        selection=[
            ('fabric', 'Fabric'),
            ('jeans', 'Jeans'),
            ('cotton', 'Cotton'),
        ]
    )
    buy_price = fields.Float(required=True)
    supplier_id = fields.Many2one('keda.supplier', string='Supplier', required=True)


class Supplier(models.Model):
    _name = 'keda.supplier'
    _description = 'Material suppliers'

    name = fields.Char(required=True)
