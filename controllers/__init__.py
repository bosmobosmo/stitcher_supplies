import json
from logging import getLogger

from odoo import exceptions, http

CONTROLLER_PATH = "/bosmobosmo"
logger = getLogger(__name__)


class KedaController(http.Controller):

    @http.route(
        f'{CONTROLLER_PATH}/auth',
        auth='none',
        methods=['POST'],
        csrf=False, type='json',
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

    @http.route(
        f'{CONTROLLER_PATH}/list-materials',
        auth='user',
        methods=['GET']
    )
    def list_materials(self, *args, **params):
        material_type = params.get("type", None)
        material_model = http.request.env['keda.material']
        material_objects = material_model.search([])
        materials = []
        for material_object in material_objects:
            if material_type is not None:
                if getattr(material_object, 'type', None) != material_type:
                    continue
            materials.append({
                'Code': material_object.code,
                'Name': getattr(material_object, 'name', ""),
                'Type': getattr(material_object, 'type', ""),
                'Buy Price': getattr(material_object, 'buy_price'),
                'Supplier Name': material_object.supplier_id.name
            })
        return json.dumps(materials)

    # get specific material
    def get_material(self): ...

    # get list of suppliers
    def list_suppliers(self): ...

    # delete a material
    def delete_material(self): ...

    # update a material
    def update_material(self, *args, **post): ...
