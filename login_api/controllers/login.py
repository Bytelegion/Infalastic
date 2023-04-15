# -*- coding: utf-8 -*-
import hashlib
import os
import werkzeug.wrappers
import datetime
import json

from odoo import http
from odoo.http import request, Response
from odoo.http import route
from odoo.exceptions import AccessError, UserError, AccessDenied



import odoo

def nonce(length=40, prefix=""):
    rbytes = os.urandom(length)
    return "{}{}".format(prefix,str(hashlib.sha1(rbytes).hexdigest()))

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, bytes):
        return str(o)

class LoginUserApi(http.Controller):
    @http.route('/create_user_api', auth='public',type='json',methods=['POST'],csrf=False,cors="*")
    def create_user(self, **kw):
        # headers = request.httprequest.headers
        # headers = []
        # for x in request.httprequest.headers:
        #     headers.append(x)
        # headers+=[('Content-Type','application/json')]
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        user_id = request.env['res.users'].sudo().search([('login','=',data['login'])])
        if user_id:
            responce_value = {
                'status':202,
                'success':False,
                'msg':'User already exits with this login',
                'user_login':user_id.login,
                'user_id':user_id.id,
                'user_name':user_id.name,
                }
            return responce_value

        user = request.env['res.users'].sudo().create({
            'name':data['name'],
            'login':data['login'],
            'password':data['password'],
            })
        if user:
            token = nonce(50)
            responce_value = {
                'status':200,
                'success':True,
                'msg':'User Created',
                'user_login':user.login,
                'user_id':user.id,
                'user_name':user.name,
                'token':token,
                }
        else:
            responce_value = {
                'status':201,
                'success':False,
                'msg':'User Not Created',
                }
       
        return responce_value


    @http.route('/login_user_api', auth='public',type='json',methods=['POST'],csrf=False, cors="")
    def login_user(self, **kw):
        # headers = request.httprequest.headers
        # headers = []
        # for x in request.httprequest.headers:
        #     headers.append(x)
        # headers+=[('Content-Type','application/json')]
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        try:
            uid = request.session.authenticate(request.session.db, data['login'], data['password'])
            responce_value = "200"
            token = nonce(50)
            status = 200
            user = request.env['res.users'].sudo().search([('id','=',uid)])
            # responce_value = []
            responce_value = {
                'status':200,
                'success':True,
                'msg':'logined successfuly',
                'user_login':user.login,
                'user_id':user.id,
                'user_name':user.name,
                'token':token,
                }
            
        except odoo.exceptions.AccessDenied as e:
            if e.args == odoo.exceptions.AccessDenied().args:
                responce_value = {
                    'status':201,
                    'success':False,
                    'msg':'Access Denied',
                }
            else:
                responce_value = {
                    'status':202,
                    'success':False,
                    'msg':'Unknown Issue',
                }

        return responce_value


    @http.route('/reset_password_request', auth='public',type='json',methods=['POST'],csrf=False, cors="*")
    def email_user(self, **kw):
        # headers = request.httprequest.headers
        # headers = []
        # for x in request.httprequest.headers:
        #     headers.append(x)
        # headers+=[('Content-Type','application/json')]
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        user = request.env['res.users'].sudo().search([('login','=',data['login'])])
        if user:
            # mail_template_id = user.mail_template_id()
            link = data['link']
            link = '"'+str(link)+'"'
            email_to = [data['login']]
            emails = ','.join(email_to)
            # mail_template = request.env['mail.template'].sudo().search([('id','=',mail_template_id)])
            mail_template = request.env.ref('login_api.template_request_password_change_id')
            mail_template.sudo().email_to = emails
            mail_template.sudo().body_html = '<p>Dear '+user.name+',</p><p>You can find link below to chnage your login password. Thanks</p><a href='+link+'>Reset Password Link</a>'
            mail_template.sudo().send_mail(user.id, force_send=True)
            responce_value = {
                'status':200,
                'success':True,
                'msg':'email sent',
                'user_login':user.login,
                'user_id':user.id,
                'user_name':user.name,
                }
        else:
            responce_value = {
                'status':201,
                'success':False,
                'msg':'User not found with this login email',
                }

        return responce_value


    @http.route('/new_password_request', auth='public',type='json',methods=['POST'],csrf=False, cors="*")
    def change_pass_user(self, **kw):
        # headers = request.httprequest.headers
        # headers = []
        # for x in request.httprequest.headers:
        #     headers.append(x)
        # headers+=[('Content-Type','application/json')]
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        user = request.env['res.users'].sudo().search([('login','=',data['login'])])
        if user:
            user.password = data['new_password']
            responce_value = {
                'status':200,
                'success':True,
                'msg':'password Changed successfuly',
                'user_login':user.login,
                'user_id':user.id,
                'user_name':user.name,
                }
        else:
            responce_value = {
                'status':201,
                'success':False,
                'msg':'User not found with this login email',
                }

        return responce_value

    @http.route("/get_partner_api", auth='none', type='json', methods=['POST','GET'], csrf=False, cors='*')
    def get_partner_api(self, **kw):
        partners = request.env['res.partner'].sudo().search([])

        partners_list = []
        for partner in partners:
            partners_list.append({
                'name':partner.name
                })

        # (partners_list)

        headers = {'Content-Type': 'application/json','Access-Control-Allow-Origin':'*'}
        body = { 'results': { 'code': 200, 'message': partners_list } }

        return Response(json.dumps(body), headers=headers)

