import json

from odoo import exceptions, http


class KedaController(http.Controller):

    @http.route(
        '/auth', auth='none', methods=['POST'], csrf=False, type='json',
    )
    def authenticate(self, *args, **post):
        try:
            login = post['login']
            password = post['password']
            db = post['db']
        except KeyError:
            raise exceptions.AccessDenied(
                "Please provide a login, a password, and a db name"
            )

        http.request.session.authenticate(db, login, password)
        res = http.request.env['ir.http'].session_info()
        return res

    @http.route('/list-materials', auth='user', methods=['GET'])
    def list_materials(self):
        material_model = http.request.env['keda.material']
        material_objects = material_model.search([])
        materials = []
        for material_object in material_objects:
            materials.append({
                'Code': material_object.code,
                'Name': getattr(material_object, 'name', ""),
                'Type': getattr(material_object, 'type', ""),
                'Buy Price': getattr(material_object, 'buy_price'),
                'Supplier Name': material_object.supplier_id.name
            })
        return json.dumps(materials)
