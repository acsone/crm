# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CrmTeam(models.Model):

    _inherit = "crm.team"
    parent_id = fields.Many2one("crm.team", string="Parent Team")

    @api.constrains("parent_id")
    def _constrains_parent_id(self):
        def _check_for_loop(new_child, current):
            if current.parent_id:
                if current.parent_id == new_child:
                    raise ValidationError(
                        _(
                            "Wrong Parent Team : No loop allowed in the teams' hierarchy."
                        )
                    )
                else:
                    _check_for_loop(new_child, current.parent_id)

        _check_for_loop(self, self)

