# -*- coding: utf-8 -*-

from odoo import models, api, fields


class AgentisChantier(models.Model):
    _name = 'agentis.chantier'

    name = fields.Char(string='Nom du chantier')
    agentis_pga_id = fields.One2many('agentis.dga', 'chantier_id', string='DGA')
    agentis_office_id = fields.One2many('office.manager', 'chantier_id', string='Office manager')
    description = fields.Text(string='Description')


