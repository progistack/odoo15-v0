# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo.exceptions import UserError, ValidationError


class AgentisDGA(models.Model):
    _name = 'agentis.dga'

    create_date = fields.Date(string='Date')
    libele = fields.Text(string='Libellé')
    name = fields.Char(string="Numéro facture")
    nature_payment = fields.Selection([('espece', 'Espèce'), ('autre', 'Autre')], default='espece')
    payment_with = fields.Selection([('employee', 'Employé'), ('client', 'Client'), ('fournisseur', 'Fournisseur')],"Par l’intermédiaire de", default='employee')
    payment_with_employee = fields.Many2one('hr.employee', string='Employé')
    payment_with_other = fields.Many2one('res.partner', string='Client/Fournisseur')
    beneficiaire = fields.Many2one('hr.employee', string='Bénéficiaire finale')
    check_in_out = fields.Selection([('entrer', 'Entrée'), ('sortie', 'Sortie')], 'Entrée/Sortie')
    somme = fields.Float(string='Somme')
    update = fields.Datetime(string='Mise à jour')
    update_by = fields.Many2one('res.users', string='Mise à jour par')
    visibility = fields.Selection([('0', 'Oui'), ('1', 'Non')],
                                  "à ne pas déclarer ?", default='1')
    chantier_id = fields.Many2one('agentis.chantier', string="Chantier") #'agentis_pga_id'
    etat = fields.Boolean(string='etat')
    solde = fields.Float(string='Solde', compute='get_solde')

    def create_enter(self):
        enter_out = self.check_in_out
        if enter_out == 'entrer':
            """
            vals = {
                'create_date': self.create_date,
                'libele': self.libele,
                'name': self.name,
                'nature_payment': self.nature_payment,
                'payment_with': self.payment_with,
                'payment_with_employee': self.payment_with_employee.id,
                'payment_with_other': self.payment_with_other.id,
                'beneficiaire': self.beneficiaire.id,
                'check_in_out': self.check_in_out,
                'somme': self.somme,
                'update': self.update,
                'update_by': self.update_by.id,
                'visibility': self.visibility,
                'chantier_id': self.chantier_id.id,
                'etat': self.etat,

            }
            self.env['agentis.dga'].create(vals)"""
        else:
            raise ValidationError("l'entrée/sortie n'est pas une entrée")
        return {
            'type': 'ir.actions.act_window',
            'name': '',
            'view_mode': 'tree',
            'res_model': 'agentis.dga'
        }

    def create_out(self):
        print("iiiiiiiiiiii", self)

    def get_solde(self):
        print()

    def return_list(self):
        return {
            'type': 'ir.actions.act_window',
            'name': '',
            'view_mode': 'tree',
            'res_model': 'agentis.dga',
        }




