# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrDepartment(models.Model):
	_inherit = 'hr.department'

	image_url = fields.Char('Image Url')
	


