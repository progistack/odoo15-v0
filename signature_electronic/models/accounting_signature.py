import os
from datetime import datetime
import pytz

from odoo import models, fields, api


class Users(models.Model):
    _inherit = "account.payment"

    @api.model
    def _default_time_utc(self):
        locale_time = datetime.now()
        dt_utc = locale_time.astimezone(pytz.UTC)
        return dt_utc

    digital_signature = fields.Binary(string="Signature")
    date_signature = fields.Date(string="date de signature", default=_default_time_utc)

class HrExpense(models.Model):

    _inherit = "hr.expense"

    @api.model
    def _default_time_utc(self):
        locale_time = datetime.now()
        dt_utc = locale_time.astimezone(pytz.UTC)
        return dt_utc

    digital_signature = fields.Binary(string="Signature")
    date_signature = fields.Date(string="date de signature", default=_default_time_utc)
