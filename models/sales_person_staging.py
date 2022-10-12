from odoo import api, fields, models


class SalesPersonStaging(models.Model):
    _name = 'sales.person.staging'
    _description = 'Sales Person Staging'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(related='user_id.partner_id.name')

    date_from = fields.Date(
        string='Date From',
        required=True,
        tracking=True,
    )

    date_to = fields.Date(
        string='Date to',
        required=True,
        tracking=True,
    )

    user_id = fields.Many2one(
        'res.users',
        string='Sales Person',
        required=True,
        tracking=True,
    )

    salary_slab_id = fields.Many2one(
        'salary.slab',
        string='Salary Slab',
        required=True,
        tracking=True,
    )

    salary = fields.Float(
        string='Salary',
        related='salary_slab_id.salary',
    )

    sales_target = fields.Float(
        string='Sales Target',
        related='salary_slab_id.sales_target',
    )

    bonus = fields.Float(
        string='Bonus',
        related='salary_slab_id.bonus',
    )

    commission_percentage = fields.Float(
        string='Commission Percentage',
        related='salary_slab_id.commission_percentage',
    )

    sales_order_total = fields.Float(
        compute='_compute_sales_order_total',
        string='Sales Order',
        tracking=True,
    )

    account_move_total = fields.Float(
        compute='_compute_account_move_total',
        string='Invoiced',
        tracking=True,
    )

    account_payment_total = fields.Float(
        compute='_compute_account_payment_total',
        string='Paid',
        required=True,
        tracking=True,
    )

    commission = fields.Float(
        compute='_compute_commission',
        string='Commission',
        required=True,
        tracking=True,
    )

    total_earnings = fields.Float(
        compute='_compute_total_earnings',
        string='Total Earnings',
        tracking=True,
    )

    active = fields.Boolean('Active', default=True)

    @api.depends('user_id', 'date_from', 'date_to')
    def _compute_sales_order_total(self):
        """
        Compute total confirmed sales order for sales person within
        selected date
        """
        for rec in self:
            sales_order_ids = self.env['sale.order'].search(
                [
                    ('user_id', '=', rec.user_id.id),
                    ('state', '=', 'sale'),
                    '&',
                    ('create_date', '>=', rec.date_from),
                    ('create_date', '<=', rec.date_to),
                ]).mapped('amount_untaxed')

            total_sales = 0
            for line in sales_order_ids:
                total_sales += line
            rec.sales_order_total = total_sales

    @api.depends('user_id', 'date_from', 'date_to')
    def _compute_account_move_total(self):
        """
        Compute total invoiced sales order for sales person within
        selected date
        """
        for rec in self:
            sales_order_ids = self.env['sale.order'].search(
                [
                    ('user_id', '=', rec.user_id.id),
                    ('state', '=', 'sale'),
                    '&',
                    ('create_date', '>=', rec.date_from),
                    ('create_date', '<=', rec.date_to),
                ]).mapped('name')

            account_move_ids = self.env['account.move'].search(
                [('invoice_origin', 'in', sales_order_ids)],
            ).mapped('amount_untaxed')

            total_invoiced = 0
            for line in account_move_ids:
                total_invoiced += line
            rec.account_move_total = total_invoiced

    @api.depends('user_id', 'date_from', 'date_to')
    def _compute_account_payment_total(self):
        """
        Compute total invoiced payment sales order for sales person within
        selected date
        """
        for rec in self:
            sales_order_ids = self.env['sale.order'].search(
                [
                    ('user_id', '=', rec.user_id.id),
                    ('state', '=', 'sale'),
                    '&',
                    ('create_date', '>=', rec.date_from),
                    ('create_date', '<=', rec.date_to),
                ]).mapped('name')

            account_amount_total = self.env['account.move'].search(
                [('invoice_origin', 'in', sales_order_ids)],
            ).mapped('amount_total')

            account_amount_residual = self.env['account.move'].search(
                [('invoice_origin', 'in', sales_order_ids)],
            ).mapped('amount_residual')

            amount_total = 0
            for line in account_amount_total:
                amount_total += line

            amount_residual = 0
            for line in account_amount_residual:
                amount_residual += line

            rec.account_payment_total = amount_total - amount_residual

    @api.depends('sales_order_total', 'sales_target', 'commission_percentage')
    def _compute_commission(self):
        """
        Compute commission on excess volume
        """
        for rec in self:
            if rec.sales_order_total < rec.sales_target:
                rec.commission = 0
            else:
                if rec.sales_order_total >= rec.sales_target:
                    rec.commission = (
                        rec.sales_order_total - rec.sales_target
                    ) * (rec.commission_percentage / 100)

    @api.depends(
        'sales_order_total',
        'sales_target',
        'commission_percentage',
        'bonus',
    )
    def _compute_total_earnings(self):
        """
        Compute total earnings
        """
        for rec in self:
            if rec.sales_order_total < rec.sales_target:
                rec.total_earnings = 0 + rec.bonus
            else:
                if rec.sales_order_total >= rec.sales_target:
                    rec.total_earnings = (
                        (
                            rec.sales_order_total - rec.sales_target
                        ) * (rec.commission_percentage / 100)) + rec.bonus
