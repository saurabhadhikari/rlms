# -*- coding: utf-8 -*-
from odoo import http

# class Stream(http.Controller):
#     @http.route('/stream/stream/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stream/stream/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stream.listing', {
#             'root': '/stream/stream',
#             'objects': http.request.env['stream.stream'].search([]),
#         })

#     @http.route('/stream/stream/objects/<model("stream.stream"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stream.object', {
#             'object': obj
#         })