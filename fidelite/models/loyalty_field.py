
from odoo import fields,models, api

class LoyaltyField(models.Model):
    _inherit = 'res.partner'
    loyalty = fields.Float(string="point", default=0)

    @api.model
    def save_user(self, user_id, loyalty):
        user = self.env['res.partner'].search([('id', '=', user_id)])
        user.write({'loyalty': float(loyalty)})