
from odoo import models, fields, api, _
from datetime import datetime
import pytz
from  jdatetimext import jdatejs

class SdClinicPrescriptions(models.Model):
    _name = "sd_clinic.prescriptions"
    _description = "Prescriptions"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "visit_no"

    visit_no = fields.Char(copy=False, required=True, default=lambda self: _('New'))

    state = fields.Selection([('ongoing', 'Ongoing'),('canceled', 'Canceled'), ('closed', 'Closed'),],
                             default='ongoing', required=True, store=True, copy=False, tracking=True )
    national_id = fields.Many2one( "sd_clinic.patients", tracking=True, required=True)
    age = fields.Char(compute="_age_compute", store=True, default='')
    old_disease = fields.Boolean(related="national_id.old_disease")
    present_disease = fields.Boolean(related="national_id.present_disease")
    drug_sensitivity = fields.Boolean(related="national_id.drug_sensitivity")

    case_type = fields.Selection(selection=[('disease', 'Disease'), ('accident', 'Accident'), ],
        string='Case Type', required=True, default='disease')


    project_id = fields.Many2one("sd_projects.projects", tracking=True, required=True)
    therapy = fields.Many2one("sd_clinic.therapy_types", tracking=True, required=True,
                              default=lambda self: self.env["sd_clinic.therapy_types"].search([], order="sequence", limit=1).id)
    visit_date = fields.Date(default=lambda self: datetime.now(pytz.timezone(self._context.get('tz') or 'UTC')), tracking=True, required=True)

    description = fields.Html()

    medicines = fields.One2many("sd_clinic.medicine_prescripts", "prescript", tracking=True)

    @api.depends('national_id',)
    @api.onchange('national_id',)
    def _age_compute(self):
        for rec in self:
            if rec.national_id.birth_date:
                birth_date = rec.national_id.birth_date
                # print(f">>>>>>>>>>>>>>>\n year: {birth_date.year}  {rec.visit_date.year}")
                rec.age = rec.visit_date.year - birth_date.year
                # print(f"\n rec.age: {rec.age} ")
            else:
                rec.age = ''

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('visit_no') or vals['visit_no'] == _('New'):
                visit_no = self.env['ir.sequence'].next_by_code('sd_clinic.prescriptions') or _('New')
                # TODO: generate year
                today = datetime.now(pytz.timezone(self._context.get('tz') or 'UTC'))

                year = jdatejs(today, format="%Y")
                vals['visit_no'] = f"VISIT-{year}-{visit_no}"

        return super().create(vals_list)

    @api.onchange('medicines')
    def medicines_changed(self):
        # print(f"\n>>>>>>>>>>>>>>>\n medicines: {self.medicines}")
        pass
class SdClinicTherapyTypes(models.Model):
    _name = "sd_clinic.therapy_types"
    _description = "Therapy types"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=1000)
