# -*- coding: utf-8 -*-
from odoo import fields, models, api


class OfficeManager(models.Model):
    _name = 'office.manager'

    create_date = fields.Date(string='Date')
    libele = fields.Text(string='Libellé')
    num_facture = fields.Char(string="Numéro facture")
    nature_payment = fields.Selection([('espece', 'Espèce'), ('autre', 'Autre')], default='espece')
    payment_with = fields.Selection([('employee', 'Employé'), ('client', 'Client'), ('fournisseur', 'Fournisseur')],
                                    "Par l’intermédiaire de", default='employee')
    payment_with_employee = fields.Many2one('hr.employee', string='Employé')
    payment_with_other = fields.Many2one('res.partner', string='Client/Fournisseur')
    beneficiaire = fields.Many2one('hr.employee', string='Bénéficiaire finale')
    check_in_out = fields.Selection([('entrer', 'Entrer'), ('sortie', 'Sortie')], 'Entrée/Sortie')
    somme = fields.Float(string='Somme')
    update = fields.Datetime(string='Mise à jour')
    update_by = fields.Many2one('res.users', string='Mise à jour par')
    visibility = fields.Selection([('0', 'Oui'), ('1', 'Non')],
                                  "à ne pas déclarer ?", default='1')
    name = fields.Char(string="N° de bon")
    chantier_id = fields.Many2one('agentis.chantier', string="Chantier") #, 'agentis_office_id'
    etat = fields.Boolean(string='etat')

    @api.model
    def create(self, vals):
        print("vals", vals)
        vals['name'] = self.env['ir.sequence'].next_by_code('office.sequence')
        vals['etat'] = True
        result = super(OfficeManager, self).create(vals)
        return result

    def create_enter(self):
        print("iiiiiiiiiiii")

    def create_out(self):
        print("iiiiiiiiiiii", self)

    def return_list(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'agentis.dga',
            'target': 'main'
        }
