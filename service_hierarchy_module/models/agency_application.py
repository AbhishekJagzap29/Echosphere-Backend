from datetime import date
from odoo import models, fields, api

DEFAULT_AGENCY_SALES_RANKS = [
    (1, 'S.R'),
    (2, 'S.O'),
    (3, 'S.E'),
    (4, 'D.S.E'),
    (5, 'R.S.E'),
]


def _default_agency_sales_line_ids(self):
    return [
        (0, 0, {'sr_no': sr, 'rank': rank})
        for sr, rank in DEFAULT_AGENCY_SALES_RANKS
    ]


class AgencyApplication(models.Model):
    _name = 'agency.application'
    _description = 'Agency Application Form'

    unique_code = fields.Char(string='Unique Code', default='00/00/0000')
    name = fields.Char(string='Name', required=True)
    rank_applied = fields.Char(string='Rank Applied')
    dob = fields.Date(string='DOB')
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True,
        readonly=False
    )
    permanent_address = fields.Text(string='Permanent Address')
    mobile = fields.Char(string='Mobile No')
    email = fields.Char(string='Email ID')
    pan_no = fields.Char(string='PAN No')
    qualification = fields.Char(string='Qualification')
    father_husband_name = fields.Char(string="Father/Husband's Name")
    nominee_name = fields.Char(string='Nominee Name')
    relation = fields.Char(string='Relation')
    nominee_age = fields.Integer(string='Nominee Age')

    sales_line_ids = fields.One2many(
        'agency.application.sales',
        'agency_application_id',
        string='Sales Record',
        default=_default_agency_sales_line_ids
    )

    @api.depends('dob')
    def _compute_age(self):
        today = fields.Date.today()
        for rec in self:
            if rec.dob:
                rec.age = today.year - rec.dob.year - ((today.month, today.day) < (rec.dob.month, rec.dob.day))
            else:
                rec.age = 0

    @api.onchange('dob')
    def _onchange_dob(self):
        if self.dob:
            today = fields.Date.today()
            self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    @api.onchange('sales_line_ids')
    def _onchange_sales_line_ids(self):
        for index, line in enumerate(self.sales_line_ids, start=1):
            line.sr_no = index


class AgencyApplicationSales(models.Model):
    _name = 'agency.application.sales'
    _description = 'Agency Application Sales Record'

    agency_application_id = fields.Many2one(
        'agency.application',
        string='Agency Application',
        ondelete='cascade'
    )
    sr_no = fields.Integer(
        string='Sr.No',
        compute='_compute_sr_no',
        store=True
    )
    rank = fields.Char(string='Rank')
    code_no = fields.Char(string='Code No')

    @api.depends('agency_application_id.sales_line_ids')
    def _compute_sr_no(self):
        for line in self:
            if line.agency_application_id:
                siblings = line.agency_application_id.sales_line_ids
                for index, s_line in enumerate(siblings, start=1):
                    s_line.sr_no = index
            else:
                line.sr_no = 1



