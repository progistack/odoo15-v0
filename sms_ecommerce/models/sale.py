# -*- coding: utf-8 -*-
import boto3

from odoo import models, api


class SaleOrderLine(models.Model):

    _inherit = 'sale.order'

    def amazon_sns_sms(self, phone):
        #AKIAYL3DDQROVCJACPGV
        #1Yr6ri2pcH0BpDhtAGygyVQY6oc5CZRxQif1A/hK
        client = boto3.client('sns',
                              aws_access_key_id='AKIAYL3DDQRO65DRYBNU',
                              aws_secret_access_key='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',
                              region_name='us-east-1'
                              )
        message = "Bonjour,Votre commande S00058 d'un montant de $ 6,47 est en attente. Elle sera confirmée une " \
                  "fois le paiement reçu. La référence de votre paiement est S00058.N'hésitez pas à nous " \
                  "contacter si vous avez des questions. "
        client.publish(
            PhoneNumber=phone,
            Message='bonjour ecommerce test'
        )
        print("sms envoyé --------------------")


    @api.model
    def action_confirm(self):
        res = super(SaleOrderLine, self).action_confirm()
        phone = self.partner_id.phone
        self.amazon_sns_sms(phone)
        print('888888888888888',phone)
