from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SalarySlab(models.Model):
    _name = 'salary.slab'
    _description = 'Salary Slab'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        tracking=True,
    )

    salary = fields.Float(
        string='Salary',
        required=True,
        tracking=True,
    )

    sales_target = fields.Float(
        string='Sales Target',
        required=True,
        tracking=True,
    )

    bonus = fields.Float(
        string='Bonus',
        required=True,
        tracking=True,
    )

    commission_percentage = fields.Float(
        string='Commission Percentage',
        required=True,
        tracking=True,
    )

    active = fields.Boolean('Active', default=True)

    @api.model
    def create(self, vals):
        """
        Prevent zero values on creation
        """
        res = super().create(vals)
        if vals.get('salary') == 0.00:
            raise ValidationError(
                _('Salary cannot be zero'),
            )
        elif vals.get('sales_target') == 0.00:
            raise ValidationError(
                _('Sales Target cannot be zero'),
            )
        elif vals.get('bonus') == 0.00:
            raise ValidationError(
                _('Bonus cannot be zero'),
            )
        elif vals.get('commission_percentage') == 0.00:
            raise ValidationError(
                _('Commission Percentage cannot be zero'),
            )
        return res

    def write(self, vals):
        """
        Prevent zero values on edit
        """
        res = super().write(vals)
        if vals.get('salary') == 0.00:
            raise ValidationError(
                _('Salary cannot be zero'),
            )
        elif vals.get('sales_target') == 0.00:
            raise ValidationError(
                _('Sales Target cannot be zero'),
            )
        elif vals.get('bonus') == 0.00:
            raise ValidationError(
                _('Bonus cannot be zero'),
            )
        elif vals.get('commission_percentage') == 0.00:
            raise ValidationError(
                _('Commission Percentage cannot be zero'),
            )
        return res
