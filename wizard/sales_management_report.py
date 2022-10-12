from odoo import fields, models


class SalesManagementReport(models.TransientModel):
    _name = 'sales.management.report'
    _description = 'Sales Management Report'

    sales_person_staging_ids = fields.Many2many(
        'sales.person.staging',
        string='Sales Person',
        required=True,
    )

    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')

    def action_sales_management_pdf_download(self):
        """
        Sales management report action for PDF
        """
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'sales_person_staging_ids': self.sales_person_staging_ids.ids,
        }
        return self.env.ref(
            'salary_slab.action_sales_management_pdf_report').report_action(
                self, data=data)

    def action_sales_management_excel_download(self):
        """
        Sales management report action for Excel
        """
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'sales_person_staging_ids': self.sales_person_staging_ids.ids,
        }
        return self.env.ref(
            'salary_slab.action_sales_management_excel_report').report_action(
                self, data=data)


class SalarySlabReportPDF(models.AbstractModel):
    _name = 'report.salary_slab.sales_management_report'

    def _get_report_values(self, docids, data=None):
        """
        Get values for Sales management report for PDF
        """
        domain = []
        if data.get('date_from'):
            domain.append(('date_from', '>=', data.get('date_from')))
        if data.get('date_to'):
            domain.append(('date_to', '<=', data.get('date_to')))
        if data.get('sales_person_staging_ids'):
            domain.append(('user_id', 'in', data.get(
                'sales_person_staging_ids')))
        docs = self.env['sales.person.staging'].search(domain)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'sales.person.staging',
            'docs': docs,
            'datas': data,
        }


class SalarySlabReportExcel(models.AbstractModel):
    _name = 'report.salary_slab.sales_management_excel_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        """
        Get values for Sales management report for Excel
        """
        domain = []
        if data.get('date_from'):
            domain.append(('date_from', '>=', data.get('date_from')))
        if data.get('date_to'):
            domain.append(('date_to', '<=', data.get('date_to')))
        if data.get('sales_person_staging_ids'):
            domain.append(('user_id', 'in', data.get(
                'sales_person_staging_ids')))

        sheet = workbook.add_worksheet('Sales Management Report')
        title = workbook.add_format(
            {'bold': True,
             'align': 'center',
             'font_size': 20, 'bg_color': '#f2eee4', 'border': True})
        header_row_style = workbook.add_format(
            {'bold': True, 'align': 'center', 'border': True})

        sheet.merge_range('A1:F1', 'Sales Management Report', title)

        stages = self.env['sales.person.staging'].search(domain)
        row = 3
        col = 0

        sheet.set_column(0, 5, 18)
        sheet.write(row, col, 'Sales Person', header_row_style)
        sheet.write(row, col+1, 'Salary', header_row_style)
        sheet.write(row, col+2, 'Sales Target', header_row_style)
        sheet.write(row, col+3, 'Sales Order', header_row_style)
        sheet.write(row, col+4, 'Invoiced', header_row_style)
        sheet.write(row, col+5, 'Paid', header_row_style)
        sheet.write(row, col+6, 'Bonus', header_row_style)
        sheet.write(row, col+7, 'Commission', header_row_style)
        sheet.write(row, col+8, 'Total', header_row_style)
        row += 2
        for stage in stages:
            sheet.write(row, col, stage.user_id.name)
            sheet.write(row, col+1, stage.salary)
            sheet.write(row, col+2, stage.sales_target)
            sheet.write(row, col+3, stage.sales_order_total)
            sheet.write(row, col+4, stage.account_move_total)
            sheet.write(row, col+5, stage.account_payment_total)
            sheet.write(row, col+6, stage.bonus)
            sheet.write(row, col+7, stage.commission)
            sheet.write(row, col+8, stage.total_earnings)
            row += 1
