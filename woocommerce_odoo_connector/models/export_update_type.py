#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api,fields,models
from odoo.tools.translate import _
from datetime import datetime,timedelta
from odoo.exceptions import UserError
import logging
_logger	 = logging.getLogger(__name__)
try:
	from woocommerce import API
except ImportError:
	_logger.info('**Please Install Woocommerce Python Api=>(cmd: pip3 install woocommerce)')
class MultiChannelSale(models.Model):
	_inherit = "multi.channel.sale"

	# 
	# def action_export_update_woocommerce_categories(self):
	# 	if self._context['active_ids']:
	# 		count = 0
	# 		store_category_id = 0
	# 		message = self.export_woocommerce_categories(0)
	# 		category_ids = self._context['active_ids']
	# 		for category_id in category_ids:
	# 			category_mapping_record = self.env['channel.category.mappings'].search([('odoo_category_id','=',category_id),('channel_id.id','=',self.id)])
	# 			if category_mapping_record:
	# 				category = category_mapping_record.category_name
	# 				if category_mapping_record.need_sync == 'yes':
	# 					count += 1
	# 					if category.parent_id:
	# 						parent_category_id = self.env['channel.category.mappings'].search([('odoo_category_id','=',category.parent_id.id),('channel_id.id','=',self.id)])
	# 						store_category_id = parent_category_id.store_category_id
	# 					category_dict = {
	# 						'name' 		: category.name,
	# 						'parent_id'	: store_category_id,
	# 					}
	# 					woocommerce = self.get_woocommerce_connection()
	# 					woocommerce.put('products/categories/'+category_mapping_record.store_category_id,category_dict)
	# 					category_mapping_record.need_sync = 'no'
	# 		message = str(message)+" Categories have been exported"+", "+str(count)+" Categories have been Updated"
	# 		return self.display_message(message)

	
	def export_update_woocommerce_type(self):
		count = 0
		store_type_id = 0
		category_update = self.env['channel.type.mappings'].search([('need_sync','=','yes'),('channel_id.id','=',self.id)])
		for category_map in category_update:
				category = category_map.category_name
				count += 1
				if category.parent_id:
					parent_category = self.env['channel.type.mappings'].search([('odoo_type_id','=',category.parent_id.id),('channel_id.id','=',self.id)])
					if not parent_category:
						self.export_woocommerce_types(0)
						parent_category = self.env['channel.type.mappings'].search([('odoo_type_id','=',category.parent_id.id),('channel_id.id','=',self.id)])
						store_type_id = parent_category.store_type_id
				category_dict = {
					'name' 		: category.name,
					'parent_id'	: store_type_id,
				}
				woocommerce = self.get_woocommerce_connection()
				return_dict = woocommerce.put('products/product types/'+category_map.store_type_id,category_dict).json()
				if 'message' in return_dict:
					raise UserError(_('Error in Updating Types : '+str(return_dict['message'])))
				category_map.need_sync = 'no'
		return self.display_message(str(count)+" Types Updated  ")
