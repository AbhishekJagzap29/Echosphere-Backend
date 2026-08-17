from datetime import date
from odoo import models, fields, api

DEFAULT_SALES_RANKS = [
    (1, 'S.R'),
    (2, 'S.O'),
    (3, 'S.E'),
    (4, 'D.S.E'),
    (5, 'R.S.E'),
]


def _default_sales_line_ids(self):
    return [
        (0, 0, {'sr_no': sr, 'rank': rank})
        for sr, rank in DEFAULT_SALES_RANKS
    ]


class DiscountCard(models.Model):
    _name = 'discount.card'
    _description = 'Discount Card Form'

    unique_code = fields.Char(
        string='Number',
        default='New',
        copy=False,
        readonly=True
    )
    name = fields.Char(string='Name', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)
    address = fields.Text(string='Address')
    pin_code = fields.Char(string='Pin Code')
    mobile = fields.Char(string='Mobile No')

    @api.model
    def _default_unique_code(self):
        return 'New'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('unique_code') or vals.get('unique_code') == 'New':
                seq = self.env['ir.sequence'].sudo().search([('code', '=', 'discount.card.unique.code')], limit=1)
                if seq and seq.number_increment != 1:
                    seq.sudo().write({'number_increment': 1})
                seq_code = self.env['ir.sequence'].next_by_code('discount.card.unique.code')
                if not seq_code:
                    last_rec = self.search([('unique_code', '!=', False), ('unique_code', '!=', 'New')], order='id desc', limit=1)
                    if last_rec and last_rec.unique_code:
                        try:
                            seq_code = str(int(last_rec.unique_code) + 1)
                        except ValueError:
                            seq_code = '16000'
                    else:
                        seq_code = '16000'
                vals['unique_code'] = seq_code
        return super().create(vals_list)

    family_line_ids = fields.One2many(
        'discount.card.family',
        'discount_card_id',
        string='Family Details'
    )
    sales_line_ids = fields.One2many(
        'discount.card.sales',
        'discount_card_id',
        string='Sales Record',
        default=_default_sales_line_ids
    )

    rank = fields.Char(
        string='Rank',
        compute='_compute_rank_and_code',
        store=True
    )
    code_no = fields.Char(
        string='Code No',
        compute='_compute_rank_and_code',
        store=True
    )

    @api.depends('sales_line_ids.code_no', 'sales_line_ids.rank')
    def _compute_rank_and_code(self):
        for rec in self:
            filled_lines = rec.sales_line_ids.filtered(lambda l: l.code_no)
            if filled_lines:
                rec.rank = ", ".join(line.rank for line in filled_lines if line.rank)
                rec.code_no = ", ".join(line.code_no for line in filled_lines if line.code_no)
            else:
                rec.rank = False
                rec.code_no = False

    @api.onchange('family_line_ids')
    def _onchange_family_line_ids(self):
        for index, line in enumerate(self.family_line_ids, start=1):
            line.sr_no = index

    @api.onchange('sales_line_ids')
    def _onchange_sales_line_ids(self):
        for index, line in enumerate(self.sales_line_ids, start=1):
            line.sr_no = index


class DiscountCardFamily(models.Model):
    _name = 'discount.card.family'
    _description = 'Discount Card Family Details'

    discount_card_id = fields.Many2one(
        'discount.card',
        string='Discount Card',
        ondelete='cascade'
    )
    sr_no = fields.Integer(
        string='Sr.No',
        compute='_compute_sr_no',
        store=True
    )
    full_name = fields.Char(string='Full Name', required=True)
    age = fields.Integer(string='Age')
    dob = fields.Date(string='DOB')
    relationship = fields.Char(string='Relationship')

    @api.depends('discount_card_id.family_line_ids')
    def _compute_sr_no(self):
        for line in self:
            if line.discount_card_id:
                siblings = line.discount_card_id.family_line_ids
                for index, s_line in enumerate(siblings, start=1):
                    s_line.sr_no = index
            else:
                line.sr_no = 1

    @api.onchange('dob')
    def _onchange_dob(self):
        if self.dob:
            today = fields.Date.today()
            self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))


class DiscountCardSales(models.Model):
    _name = 'discount.card.sales'
    _description = 'Discount Card Sales Record'

    discount_card_id = fields.Many2one(
        'discount.card',
        string='Discount Card',
        ondelete='cascade'
    )
    sr_no = fields.Integer(
        string='Sr.No',
        compute='_compute_sr_no',
        store=True
    )
    rank = fields.Char(string='Rank')
    code_no = fields.Char(string='Code No')

    @api.depends('discount_card_id.sales_line_ids')
    def _compute_sr_no(self):
        for line in self:
            if line.discount_card_id:
                siblings = line.discount_card_id.sales_line_ids
                for index, s_line in enumerate(siblings, start=1):
                    s_line.sr_no = index
            else:
                line.sr_no = 1





