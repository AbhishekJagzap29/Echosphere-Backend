from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    website = fields.Char(default="https://dreamwarez.in")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("website"):
                vals["website"] = "https://dreamwarez.in"
        return super().create(vals_list)