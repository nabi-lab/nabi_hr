# -*- coding: utf-8 -*-
from openerp import http

# class NabiHrExtra(http.Controller):
#     @http.route('/nabi_hr_extra/nabi_hr_extra/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nabi_hr_extra/nabi_hr_extra/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nabi_hr_extra.listing', {
#             'root': '/nabi_hr_extra/nabi_hr_extra',
#             'objects': http.request.env['nabi_hr_extra.nabi_hr_extra'].search([]),
#         })

#     @http.route('/nabi_hr_extra/nabi_hr_extra/objects/<model("nabi_hr_extra.nabi_hr_extra"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nabi_hr_extra.object', {
#             'object': obj
#         })