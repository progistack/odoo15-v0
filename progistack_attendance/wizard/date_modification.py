from odoo import api, models, fields

class DateModification(models.TransientModel):
    _name = "date.modification"

    date_change = fields.Float(string="Départ réel")

    def add_date_sortie(self):
        self.env['hr.attendance'].browse(self.env.context.get('active_id')).write({
            'heure_sortie': self.date_change, 'visible': False
        })
