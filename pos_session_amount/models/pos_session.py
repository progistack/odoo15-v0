from odoo import fields, models, api


class PosSession(models.Model):
    _inherit = 'pos.session'

    total = fields.Float(string='Total', compute='get_total')

    def get_total(self):
        for session in self:
            amount = 0
            payment = self.env['pos.payment'].search([('session_id', '=', session.id)])
            for pay in payment:
                amount = amount + pay.amount
            session.total = amount
