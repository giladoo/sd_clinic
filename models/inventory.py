
from odoo import models, fields, api, _
from datetime import datetime
import pytz

class SdClinicMedicineInventory(models.Model):
    _name = "sd_clinic.medicine_inventory"
    _description = "Medicine Inventory"

    name = fields.Many2one("sd_clinic.medicine", required=True)
    medicine_type = fields.Many2one("sd_clinic.medicine_types", required=True)
    dose = fields.Char(requred=True)
    quantity = fields.Integer(requred=True)
    receive_date = fields.Date(default=lambda self: datetime.now(pytz.timezone(self._context.get('tz') or 'UTC')),)



class SdClinicMedicine(models.Model):
    _name = "sd_clinic.medicine"
    _description = "Medicine list"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1000)


class SdClinicMedicineTypes(models.Model):
    _name = "sd_clinic.medicine_types"
    _description = "Medicine Types"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1000)






