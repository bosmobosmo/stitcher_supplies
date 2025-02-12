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
