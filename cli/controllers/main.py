from odoo import http
from odoo.http import request

class Main(http.Controller):

    @http.route('/api/items', auth='public', website=True)
    def index(self, **kw):
        items = request.env['api.item'].sudo().search([])
        return request.render('cli.index', {
            'items': items,
        })