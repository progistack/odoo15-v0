# -*- coding: utf-8 -*-
import json
import logging
from odoo import fields, http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import boto3

_logger = logging.getLogger(__name__)


class WebsiteSaleInherite(WebsiteSale):
    number_list = []

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        if kw:
            if kw['email'] == '':
                kw.update({'email': 'kissi@gmail.com'})
            print('data receved ----------------', kw['email'])
            self.number_list.append(kw['phone'])
        res = super(WebsiteSaleInherite, self).address(**kw)
        print("context ----------------", res.qcontext)
        order = request.website.sale_get_order()
        if order:
            print('555555555555555', order.total_amount)
        return res

    @http.route('/shop/payment/validate', type='http', auth="public", website=True, sitemap=False)
    def shop_payment_validate(self, transaction_id=None, sale_order_id=None, **post):

        res = super(WebsiteSaleInherite, self).shop_payment_validate(transaction_id=None, sale_order_id=None, **post)
        phone = self.number_list[-1]
        print('liste -1-----------------', phone)
        self.amazon_sns_sms(phone)
        return res

    def test(self):
        print('*******************7885544788-----------------')

    def amazon_sns_sms(self, phone):
        try:
            client = boto3.client('sns',
                                  aws_access_key_id='AKIAYL3DDQROVCJACPGV',
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


        except Exception as e:
            raise AssertionError("verifier votre connexion internet : " + e.args[0])

