# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ParentLoopError(ValidationError):
    pass


class CrmTeam(models.Model):

    _inherit = "crm.team"
    _parent_store = True
    parent_path = fields.Char(index=True)
    parent_id = fields.Many2one(comodel_name="crm.team", string="Parent Team")

    @api.constrains("parent_id")
    def _constrains_parent_id(self):
        def _check_for_loop(new_child, current):
            if current.parent_id:
                if current.parent_id == new_child:
                    raise ParentLoopError(
                        _(
                            "Wrong Parent Team : No loop allowed in the teams' hierarchy."
                        )
                    )
                else:
                    _check_for_loop(new_child, current.parent_id)

        _check_for_loop(self, self)
