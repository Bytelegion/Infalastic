# -*- coding: utf-8 -*-
import hashlib
import os
import werkzeug.wrappers
import datetime
import json

from odoo import http
from odoo.http import request, Response , JsonRequest
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

class LoginEmployeeApi(http.Controller):
    @http.route('/create_department_api', auth='none',type='json',methods=['POST','GET'],csrf=False, cors="*")
    def create_department(self, **kw):
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        department_id = request.env['hr.department'].sudo().search([('name','=',data['department_name'])])
        manager_id = request.env['hr.employee'].sudo().search([('id','=',data['manager_id'])])
        if department_id:
            responce_value = {
                'status':202,
                'success':False,
                'msg':'Department already exits with this name',
                'department_id':department_id.id,
                'department_name':department_id.name,
                'image_url':department_id.image_url,
                'manager_id':department_id.manager_id.id,
                'manager_image':department_id.manager_id.image_url,
                'manager_name':department_id.manager_id.name,
                }
            return responce_value

        department_id = request.env['hr.department'].sudo().create({
            'name':data['department_name'],
            'image_url':data['image_url'],
            'manager_id':manager_id.id,
            })

        if department_id:
            responce_value = {
                'status':200,
                'success':True,
                'msg':'Department Created',
                'department_id':department_id.id,
                'department_name':department_id.name,
                'image_url':department_id.image_url,
                'manager_id':department_id.manager_id.id,
                'manager_image':department_id.manager_id.image_url,
                'manager_name':department_id.manager_id.name,

                }
        else:
            responce_value = {
                'status':201,
                'success':False,
                'msg':'Department Not Created',
                }
       
        return responce_value



    @http.route('/get_department_api', auth='none',type='json',methods=['POST','GET'],csrf=False, cors="*")
    def get_all_departments(self, **kw):
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        dept_ids = request.env['hr.department'].sudo().search([])
        if dept_ids:
            dept_id = []
            for dept in dept_ids:
                dept_id.append({
                    'department_id':dept.id,
                    'department_name':dept.name,
                    'image_url':dept.image_url,
                    'manager_id':dept.manager_id.id,
                    'manager_image':dept.manager_id.image_url,
                    'manager_name':dept.manager_id.name,
                    })

            responce_value = {
                'status':200,
                'success':True,
                'msg':'All Departments',
                'departments_details':dept_id,
                }
            return responce_value
       
        return responce_value



    @http.route('/get_department_employee', auth='none',type='json',methods=['POST','GET'],csrf=False, cors="*")
    def get_department_employees(self, **kw):
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        empolyee_ids = request.env['hr.employee'].sudo().search([('department_id','=',data['department_id'])])
        if empolyee_ids:
            empolyee_id = []
            for emp in empolyee_ids:
                empolyee_id.append({
                    'employee_id':emp.id,
                    'employee_name':emp.name,
                    'first_name':emp.first_name,
                    'last_name':emp.last_name,
                    'job_title':emp.job_title,
                    'email':emp.work_email,
                    'phone':emp.work_phone,
                    'image_url':emp.image_url,
                    'manager_id':emp.parent_id.id,
                    'manager_name':emp.parent_id.name,
                    'department_id':emp.department_id.id,
                    'department_name':emp.department_id.name,
                    'employee_status':emp.employee_status,

                    })

            responce_value = {
                'status':200,
                'success':True,
                'msg':'Empolyees against requested department',
                'empolyee_details':empolyee_id,
                }
            return responce_value
        
        else:
            responce_value = {
                'status':201,
                'success':False,
                'msg':'Empolyees Not Found',
                }
       
        return responce_value
