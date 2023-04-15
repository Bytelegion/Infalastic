# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmployee(models.Model):
	_inherit = 'hr.employee'

	first_name = fields.Char('First Name')
	last_name = fields.Char('Last Name')
	image_url = fields.Char('Image Url')
	resource_id = fields.Many2one('resource.resource',required=False)
	employee_status = fields.Selection([
		('active', 'active'),
		('not_active', 'Not Active')], string='Status')


class ResourceResource(models.Model):
	_inherit = 'resource.resource'

	calendar_id = fields.Many2one("resource.calendar", string="Resource's Calendar", required=False, ondelete='cascade')



