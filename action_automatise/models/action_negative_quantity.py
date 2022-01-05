# -*- coding: utf-8 -*-
from odoo import fields, api, _ , models
from odoo.exceptions import UserError

class NegativeQuantityProduct(models.Model):
    _name = "negative.quantity"

    product_id = fields.Many2one('product.product', string='Articles')
    location_id = fields.Many2one('stock.location', string='Articles')
    quantity = fields.Char(string='Quantité')

    @api.model
    def action_negative_quantity(self):
        all_variant = self.env['product.product'].search([])
        print("------------------",all_variant)
        for val in all_variant:
            quant = self.env['stock.quant'].search([('product_id', '=', val.id)])
            if len(quant) > 1:
                for ln in quant:
                    print("-----------quantity------", ln.quantity)
                    if ln.quantity < 0:
                        self.env['negative.quantity'].write({'product_id': ln.product_id.id,
                                                              'quantity': ln.quantity, 'location_id': ln.location_id.id})
            else:
                print("-----------quantity------", quant.quantity)
                if quant.quantity < 0:
                    self.env['negative.quantity'].write({'product_id': quant.product_id.id,
                                                          'quantity': quant.quantity, 'location_id': quant.location_id.id})
