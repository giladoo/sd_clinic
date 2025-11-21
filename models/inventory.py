
from odoo import models, fields, api, _
from datetime import datetime
import pytz

from odoo.api import ValuesType, Self


# -------------------- Medicine Inventory -------------------------------
class SdClinicMedicineInventory(models.Model):
    _name = "sd_clinic.medicine_inventory"
    _description = "Medicine Inventory"

    name = fields.Many2one("sd_clinic.medicine", required=True)
    project_id = fields.Many2one("sd_projects.projects", required=True)
    # dose = fields.Char(requred=True)
    quantity = fields.Integer(requred=True)
    receive_date = fields.Date(default=lambda self: datetime.now(pytz.timezone(self._context.get('tz') or 'UTC')),)


# -------------------- Medicine Prescripts -------------------------------
class SdClinicMedicinePrescripts(models.Model):
    _name = "sd_clinic.medicine_prescripts"
    _description = "Medicine Prescripts"

    name = fields.Many2one("sd_clinic.medicine", required=True)
    on_hand = fields.Integer(compute="on_hand_calculation", store=True )
    prescript = fields.Many2one("sd_clinic.prescriptions")
    project_id = fields.Many2one("sd_projects.projects", required=True)
    quantity = fields.Integer(requred=True, tracking=True)
    description = fields.Char()

    @api.onchange('name', 'project_id')
    def on_hand_calculation(self):
        # domain = [('project_id', '=', project_id), ]
        received = self.env["sd_clinic.medicine_inventory"].search_read([], ['name', 'quantity', 'project_id'])
        prescript = self.env["sd_clinic.medicine_prescripts"].search_read([], ['name', 'quantity', 'project_id'])
        for rec in self:
            qr = sum(list(r['quantity'] for r in received if r['name'][0] == rec.name.id and r['project_id'][0] == rec.project_id.id))
            qp = sum(list(r['quantity'] for r in prescript if r['name'][0] == rec.name.id and r['project_id'][0] == rec.project_id.id))
            print(f">>>>>>>>>>>>>\nproject_id: {rec.project_id.id} {rec.id}   qr: {qr}    qp: {qp}")
            rec.on_hand = qr - qp

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            print(f"++++++++++++++++\n {vals}\n")

        return super().create(vals_list)


        # context = self.env.context
        # project_id = int(context.get('default_project_id', 0))
        #
        # print(f">>>>>>>>>>>>>\nself: {self} project: {project_id}\n ")
        # if project_id:
        #     domain = [('project_id', '=', project_id),]
        #     received = self.env["sd_clinic.medicine_inventory"].search_read(domain, ['name', 'quantity'])
        #     prescript = self.env["sd_clinic.medicine_prescripts"].search_read(domain, ['name', 'quantity'])
        #     for rec in self:
        #         qr = sum(list(r['quantity'] for r in received if r['name'][0] == rec.name.id))
        #         qp = sum(list(r['quantity'] for r in prescript if r['name'][0] == rec.name.id))
        #         print(f">>>>>>>>>>>>>\nproject_id: {project_id}    qr: {qr}    qp: {qp}")
        #         rec.on_hand = qr - qp
        # else:
        #     for rec in self:
        #         print(f">>>")
        #         rec.on_hand = 1


# -------------------- Medicine -------------------------------
class SdClinicMedicine(models.Model):
    _name = "sd_clinic.medicine"
    _description = "Medicine list"

    sequence = fields.Integer(default=1000)
    name = fields.Char(required=True, translate=True)
    medicine_type = fields.Many2one("sd_clinic.medicine_types", required=True)
    dose = fields.Char(requred=True)
    on_hand = fields.Integer(compute="medicine_quantity")

    @api.depends('name', 'medicine_type', 'dose')
    # @api.depends_context('allowed_company_ids')
    def _compute_display_name(self):
        super()._compute_display_name()
        for rec in self:
            dose = ' - ' + rec.dose if rec.dose else ''
            rec.display_name = f"{rec.name} - {rec.medicine_type.name}{dose}"

    @api.depends('name')
    def medicine_quantity(self):
        context = self.env.context
        project_id = int(context.get('default_project_id', 0))
        domain = [('project_id', '=', project_id),] if project_id else []
        received = self.env["sd_clinic.medicine_inventory"].search_read(domain, ['name', 'quantity'])
        prescript = self.env["sd_clinic.medicine_prescripts"].search_read(domain, ['name', 'quantity'])
        # print(f"<<<<<<<<<<<<< medicine_quantity >>>>>>>>>>>>>>>>\n"
        #       f"received: {received}\n"
        #       f"prescript: {prescript}\n"
        #       )
        # received: [{'id': 2, 'name': (1, 'َAxabin - قرص - 10'), 'quantity': 80},
        #            {'id': 4, 'name': (1, 'َAxabin - قرص - 10'), 'quantity': 30},
        #            {'id': 5, 'name': (3, 'Expectorant - شربت'), 'quantity': 25}]
        #
        # prescript: [{'id': 9, 'name': (3, 'Expectorant - شربت'), 'quantity': 1},
        #             {'id': 13, 'name': (2, 'Amoxicillin - کپسول - 250'), 'quantity': 0},
        #             {'id': 14, 'name': (2, 'Amoxicillin - کپسول - 250'), 'quantity': 10},
        #             {'id': 15, 'name': (3, 'Expectorant - شربت'), 'quantity': 1},
        #             {'id': 16, 'name': (2, 'Amoxicillin - کپسول - 250'), 'quantity': 0}]

        for rec in self:
            qr = sum(list(r['quantity'] for r in received if r['name'][0] == rec.id))
            qp = sum(list(r['quantity'] for r in prescript if r['name'][0] == rec.id))
            rec.on_hand = qr - qp


# -------------------- Medicine Types -------------------------------
class SdClinicMedicineTypes(models.Model):
    _name = "sd_clinic.medicine_types"
    _description = "Medicine Types"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=1000)






