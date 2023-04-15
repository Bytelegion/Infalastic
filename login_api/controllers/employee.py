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
    @http.route('/create_employee_api', auth='none',type='json',methods=['POST','GET'],csrf=False, cors="*")
    def create_employee(self, **kw):
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        emp_name = data['first_name']+' '+data['last_name']
        empolyee_id = request.env['hr.employee'].sudo().search([('first_name','=',data['first_name']),('last_name','=',data['last_name'])])
        job_id = request.env['hr.job'].sudo().search([('name','=',data['job_title'])])
        if not job_id:
            job_id = request.env['hr.job'].sudo().create({
                'name':data['job_title'],
                })
        department_id = request.env['hr.department'].sudo().search([('id','=',data['department_id'])])
        company_id = request.env['res.company'].sudo().search([('id','=',data['company_id'])])
        manager_id = request.env['hr.employee'].sudo().search([('id','=',data['manager_id'])])
        employee_status = None
        if data['employee_status'] == True:
            employee_status = 'active'
        if data['employee_status'] == False:
            employee_status = 'not_active'

        if empolyee_id:
            responce_value = {
                'status':202,
                'success':False,
                'msg':'Empolyee already exits with this name',
                'employee_id':empolyee_id.id,
                'employee_name':empolyee_id.name,
                'first_name':empolyee_id.first_name,
                'last_name':empolyee_id.last_name,
                'job_title':empolyee_id.job_title,
                'email':empolyee_id.work_email,
                'phone':empolyee_id.work_phone,
                'image_url':empolyee_id.image_url,
                'manager_id':empolyee_id.parent_id.id,
                'manager_name':empolyee_id.parent_id.name,
                'department_id':empolyee_id.department_id.id,
                'department_name':empolyee_id.department_id.name,
                'employee_status':empolyee_id.employee_status,
                }
            return responce_value

        empolyee_id = request.env['hr.employee'].sudo().create({
            'name':emp_name,
            'first_name':data['first_name'],
            'last_name':data['last_name'],
            'work_email':data['email'],
            'work_phone':data['phone'],
            'job_title':data['job_title'],
            'image_url':data['image_url'],
            'job_id':job_id.id,
            'parent_id':manager_id.id,
            'company_id':company_id.id,
            'department_id':department_id.id,
            'employee_status':employee_status,
            })

        if empolyee_id:
            responce_value = {
                'status':200,
                'success':True,
                'msg':'Empolyee Created',
                'employee_id':empolyee_id.id,
                'employee_name':empolyee_id.name,
                'first_name':empolyee_id.first_name,
                'last_name':empolyee_id.last_name,
                'job_title':empolyee_id.job_title,
                'email':empolyee_id.work_email,
                'phone':empolyee_id.work_phone,
                'image_url':empolyee_id.image_url,
                'manager_id':empolyee_id.parent_id.id,
                'manager_name':empolyee_id.parent_id.name,
                'department_id':empolyee_id.department_id.id,
                'department_name':empolyee_id.department_id.name,
                'employee_status':empolyee_id.employee_status,

                }
        else:
            responce_value = {
                'status':201,
                'success':False,
                'msg':'Empolyee Not Created',
                }
       
        return responce_value


    @http.route('/get_employee_api', auth='none',type='json',methods=['POST','GET'],csrf=False, cors="*")
    def get_employee(self, **kw):
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        empolyee_id = request.env['hr.employee'].sudo().search([('id','=',data['empolyee_id'])])
        if empolyee_id:
            responce_value = {
                'status':200,
                'success':True,
                'msg':'Empolyee details',
                'employee_id':empolyee_id.id,
                'employee_name':empolyee_id.name,
                'first_name':empolyee_id.first_name,
                'last_name':empolyee_id.last_name,
                'job_title':empolyee_id.job_title,
                'email':empolyee_id.work_email,
                'phone':empolyee_id.work_phone,
                'image_url':empolyee_id.image_url,
                'manager_id':empolyee_id.parent_id.id,
                'manager_name':empolyee_id.parent_id.name,
                'department_id':empolyee_id.department_id.id,
                'department_name':empolyee_id.department_id.name,
                'employee_status':empolyee_id.employee_status,

                }
            return responce_value
        
        else:
            responce_value = {
                'status':201,
                'success':False,
                'msg':'Empolyee Not Found',
                }
       
        return responce_value


    @http.route('/get_manager_api', auth='none',type='json',methods=['POST','GET'],csrf=False, cors="*")
    def get_manager_employees(self, **kw):
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        empolyee_ids = request.env['hr.employee'].sudo().search([('parent_id','=',data['empolyee_id'])])
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
                'msg':'Empolyees against requested manager',
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


    @http.route('/get_company_employee', auth='none',type='json',methods=['POST','GET'],csrf=False, cors="*")
    def get_company_employees(self, **kw):
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        empolyee_ids = request.env['hr.employee'].sudo().search([('company_id','=',data['company_id'])])
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
                'msg':'Empolyees against requested company',
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


    @http.route('/get_all_employee_api', auth='none',type='json',methods=['POST','GET'],csrf=False, cors="*")
    def get_all_employee(self, **kw):
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        empolyee_ids = request.env['hr.employee'].sudo().search([])
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
                'msg':'All Empolyees',
                'empolyee_details':empolyee_id,
                }
            return responce_value
       
        return responce_value


    @http.route('/get_company_api', auth='none',type='json',methods=['POST','GET'],csrf=False, cors="*")
    def get_all_companies(self, **kw):
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        company_ids = request.env['res.company'].sudo().search([])
        if company_ids:
            company_id = []
            for comp in company_ids:
                company_id.append({
                    'company_id':comp.id,
                    'company_name':comp.name,
                    })

            responce_value = {
                'status':200,
                'success':True,
                'msg':'All Companies',
                'company_details':company_id,
                }
            return responce_value
       
        return responce_value



    @http.route('/get_location_api', auth='none',type='json',methods=['POST','GET'],csrf=False, cors="*")
    def get_all_location(self, **kw):
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        country_ids = request.env['res.country'].sudo().search([])
        if country_ids:
            country_id = []
            for country in country_ids:
                country_id.append({
                    'location_id':country.id,
                    'location_name':country.name,
                    })

            responce_value = {
                'status':200,
                'success':True,
                'msg':'All Locations',
                'location_details':country_id,
                }
            return responce_value
       
        return responce_value


    @http.route('/get_job_api', auth='none',type='json',methods=['POST','GET'],csrf=False, cors="*")
    def get_all_job(self, **kw):
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        job_ids = request.env['hr.job'].sudo().search([])
        if job_ids:
            job_id = []
            for job in job_ids:
                job_id.append({
                    'job_id':job.id,
                    'job_name':job.name,
                    })

            responce_value = {
                'status':200,
                'success':True,
                'msg':'All Jobs',
                'job_details':job_id,
                }
            return responce_value
       
        return responce_value


    @http.route('/test_department_api', auth='none',type='json',methods=['POST','GET'],csrf=False, cors="*")
    def get_test_departments(self, **kw):
        # headers = {'Content-type': 'application/json','Access-Control-Allow-Origin': '*'}
        headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Max-Age': '3600',
                'Access-Control-Allow-Headers': 'Content-Type, application/json',
            }
        data = request.httprequest.data
        data = json.loads(data)
        response_data = {"result": "success", "message": "User created successfully"}
        status_code = 200

        dept_ids = request.env['hr.department'].sudo().search([])
        if dept_ids:
            dept_id = []
            for dept in dept_ids:
                dept_id.append({
                    'company_id':dept.id,
                    'company_name':dept.name,
                    })

        return Response(response=dept_id, headers=headers, status=status_code)


    @http.route('/get_company_manager', auth='none',type='json',methods=['POST','GET'],csrf=False, cors="*")
    def get_company_manager(self, **kw):
        headers = {'Content-type': 'application/json'}
        data = request.httprequest.data
        data = json.loads(data)
        responce_value = {}
        empolyee_ids = request.env['hr.employee'].sudo().search([('company_id','=',data['company_id']),('parent_id','=',False)])
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
                'msg':'Managers against requested company',
                'empolyee_details':empolyee_id,
                }
            return responce_value
        
        else:
            responce_value = {
                'status':201,
                'success':False,
                'msg':'Managers Not Found',
                }
       
        return responce_value






   