# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
class ProgrammeFidelite(models.Model):
    _name = "programme.loyalty"

    name_programme = fields.Char(string="Nom du programme de fidélité")
    point_franc = fields.Integer(struct="Point par franc")
    loyalty_reward_id = fields.One2many("loyalty.reward", "loyalty_programme_id",
                                        string="récompense de fidelité", copy=False, readonly=False)


class LoyaltyReward(models.Model):
    _name = "loyalty.reward"
    name = fields.Char(string="Nom")
    type_reward = fields.Selection([('remise','Remise'),('article','Produit gratuit')])
    cost_reward = fields.Float(string="coût de la récompense")
    minimum_point = fields.Float(string="Point minimum")
    discount_product_id = fields.Many2one('product.product', 'Article de remise')
    discount_type = fields.Selection([('percentage', 'Pourcentage'), ('fixed_amount', 'montant fixe')], default='fixed_amount')
    loyalty_programme_id = fields.Many2one("programme.loyalty", ondelete='cascade', string='programme de fidélité')
    amount_fexed = fields.Float(string="Montant fixe")
    minimal_amount = fields.Float(string='Montant minimal')
