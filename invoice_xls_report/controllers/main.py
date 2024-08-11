from odoo import http
import werkzeug
from datetime import datetime
from odoo import http
from odoo.http import request


class RegisterContact(http.Controller):
    @http.route('/booking', type='http', auth="public", website=True)
    def booking_form(self):
        ctx = {'booking': 'booking'}
        return request.render('invoice_xls_report.routemanager', ctx)

    @http.route('/check/group', type='json', auth="public", website=True)
    def check_group(self, **kw):
        if request.env.user.has_group('invoice_xls_report.group_web_url'):
            return 'Y'
        else:
            return 'N'


    @http.route('/fetch/products', type='json', auth="public", website=True, methods=['POST'])
    def product_data(self, **kw):
        ctx = []
        products = request.env['product.product'].sudo().search([('type', 'in', ['consu', 'service'])])
        for product in products:
            ctx.append({'id': product.id, 'name': product.name})
        return ctx

    @http.route('/fetch/def-cost', type='json', auth="public", website=True, methods=['POST'])
    def fetch_product_data(self, **kw):
        product = request.env['product.product'].sudo().search(
            [('id', '=', int(kw.get('product_id')))])
        ctx = {'id': product.id, 'def': product.product_tmpl_id.display_name,
               'cost': product.product_tmpl_id.list_price, 'name': product.product_tmpl_id.name}
        return ctx

    @http.route('/route-manager/order-now', type='http', auth="public", website=True, methods=['POST'])
    def booking_confirm(self, **arg):
        row = int(arg.get('row'))
        if row > 0:
            line_obj = request.env['account.move.line']
            move_obj = request.env['account.move']
            product_obj = request.env['product.product']
            account = request.env['account.account'].sudo().search(
                [('reconcile', '=', True)], limit=1)
            name = arg.get('Company')
            street1 = arg.get('Contact')
            street2 = arg.get('address2')
            street2 = arg.get('address2')
            city = arg.get('city')
            zip_code = arg.get('zip')
            company_phone = arg.get('company_phone')
            company_web_site = arg.get('company_web_site')
            vals = {
                'name': name,
                'street': street1,
                'street2': street2,
                'city': city,
                'zip': zip_code or False,
                'phone': company_phone or False,
                'website': company_web_site
            }
            partner = request.env['res.partner'].sudo().create(vals)
            move_vals = {
                # 'journal_id': journal_id.id,
                'partner_id': partner.id,
                'move_type': 'out_invoice',
            }
            move = move_obj.sudo().create(move_vals)
            if move:
                for r in range(1, row):
                    str1 = 'A' + str(r)
                    product_id = arg.get(str1)
                    product = product_obj.sudo().browse(int(product_id))
                    if product.product_tmpl_id.property_account_income_id:
                        account = product.product_tmpl_id.property_account_income_id
                    acc = product.product_tmpl_id.get_product_accounts(
                        fiscal_pos=move.fiscal_position_id)
                    line_rec = {
                        'product_id': int(product_id),
                        'move_id': move.id,
                        'account_id': acc['income'].id or account.id

                    }
                    ctx = {'active_model': 'account.move',
                           'check_move_validity': False}
                    line = line_obj.with_context(ctx).create(line_rec)
                    if line:
                        line._onchange_product_id()
                return request.redirect('/booking')
