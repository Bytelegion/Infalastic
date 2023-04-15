# -*- coding: utf-8 -*-
import hashlib
import os
import werkzeug.wrappers
import datetime
import json

from odoo import http
from odoo.http import request
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
    @http.route('/create_user_api', auth='public',type='json',methods=['POST'], cors='*')
    def create_user(self, **kw):
        headers = request.httprequest.headers
        headers = []
        for x in request.httprequest.headers:
            headers.append(x)
        headers+=[('Content-Type','application/json')]
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        user_id = request.env['res.users'].sudo().search([('login','=',data['login'])])
        if user_id:
            responce_value = {
                'status':202,
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
                'msg':'User Created',
                'user_login':user.login,
                'user_id':user.id,
                'user_name':user.name,
                'token':token,
                }
        else:
            responce_value = {
                'status':201,
                'msg':'User Not Created',
                }
       
        return responce_value


    @http.route('/login_user_api', auth='public',type='json',methods=['POST'], cors='*')
    def login_user(self, **kw):
        headers = request.httprequest.headers
        headers = []
        for x in request.httprequest.headers:
            headers.append(x)
        headers+=[('Content-Type','application/json')]
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
                'msg':'logined sucessfully',
                'user_login':user.login,
                'user_id':user.id,
                'user_name':user.name,
                'token':token,
                }
            
        except odoo.exceptions.AccessDenied as e:
            if e.args == odoo.exceptions.AccessDenied().args:
                responce_value = {
                    'status':201,
                    'msg':'Access Denied',
                }
            else:
                responce_value = {
                    'status':202,
                    'msg':'Unknown Issue',
                }
	responce_value.headers['Access-Control-Allow-Origin'] = '*'
	responce_value.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
	responce_value.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        return responce_value


    @http.route('/reset_password_request', auth='public',type='json',methods=['POST'], cors='*')
    def email_user(self, **kw):
        headers = request.httprequest.headers
        headers = []
        for x in request.httprequest.headers:
            headers.append(x)
        headers+=[('Content-Type','application/json')]
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
                'msg':'email sent',
                'user_login':user.login,
                'user_id':user.id,
                'user_name':user.name,
                }
        return responce_value


    @http.route('/new_password_request', auth='public',type='json',methods=['POST'], cors='*')
    def change_pass_user(self, **kw):
        headers = request.httprequest.headers
        headers = []
        for x in request.httprequest.headers:
            headers.append(x)
        headers+=[('Content-Type','application/json')]
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        user = request.env['res.users'].sudo().search([('login','=',data['login'])])
        if user:
            user.password = data['new_password']
            responce_value = {
                'status':200,
                'msg':'password Changed sucessfully',
                'user_login':user.login,
                'user_id':user.id,
                'user_name':user.name,
                }

        return responce_value

    @http.route('/cors', auth='public', cors='*', type='json', methods=['GET'])
    def cors(self):
        response = Response('ok')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        return response
