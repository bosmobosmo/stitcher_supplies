import json
from logging import getLogger

from odoo import exceptions, http, tools

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
        search_params = []
        if material_type is not None:
            search_params.append(('type', '=', material_type))
        material_objects = material_model.search(search_params)
        return json.dumps(
            material_objects.read(),
            default=tools.date_utils.json_default
        )

    @http.route(
        f'{CONTROLLER_PATH}/get-material',
        auth='user',
        methods=['GET']
    )
    def get_material(self, *args, **params):
        material_model = http.request.env['keda.material']
        try:
            material_id = int(params["id"])
        except (KeyError, ValueError, TypeError):
            http.Response.status = '400'
            return "Please provide a valid material id"
        material = material_model.browse([material_id])
        if not (material.exists()):
            return f"Material with id {material_id} does not exist"
        return json.dumps(
            material.read(),
            default=tools.date_utils.json_default
        )

    @http.route(
        f'{CONTROLLER_PATH}/list-suppliers',
        auth='user',
        methods=['GET']
    )
    def list_suppliers(self):
        supplier_model = http.request.env['keda.supplier']
        suppliers = supplier_model.search([])
        return json.dumps(
            suppliers.read(),
            default=tools.date_utils.json_default
        )

    @http.route(
        f'{CONTROLLER_PATH}/delete-material',
        auth='user',
        methods=['GET']
    )
    def delete_material(self, *args, **params):
        material_model = http.request.env['keda.material']
        try:
            material_id = int(params["id"])
        except (KeyError, ValueError, TypeError):
            http.Response.status = '400'
            return "Please provide a valid material id"
        material_object = material_model.browse([material_id])
        if not (material_object.exists()):
            return f"Material with id {material_id} does not exist"
        material_object.unlink()
        return f"Material with id {material_id} removed"

    @http.route(
        f'{CONTROLLER_PATH}/update-material',
        auth='user',
        csrf=False,
        methods=['POST']
    )
    def update_material(self, *args, **post):
        material_model = http.request.env['keda.material']
        try:
            material_id = int(post["id"])
        except (KeyError, ValueError, TypeError):
            http.Response.status = '400'
            return "Please provide a valid material id"
        material = material_model.browse([material_id])
        if not (material.exists()):
            return f"Material with id {material_id} does not exist"
        try:
            material.write(post)
        except Exception as e:
            logger.exception(e)
            http.Response.status = '400'
            return "Error when trying to update the material"

        return "Material updated successfully"
