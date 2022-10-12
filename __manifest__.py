{
    'name': 'Salary Slab',
    'version': '14.0.1.0.1',
    'category': 'management',
    'summary': """
        Salary Slab
        """,

    'description': """
        Salary Slab management

        Project Scope (Sales Target, Bonus and Commission Management System
        based on the Salary Slab)
    1. Option to create and Update Salary Slab
    2. Option to set and edit Sales Target to Salary Tab
    3. Option to set and edit Bonus Amount to Salary Tab
    4. Option to set and edit commission rates to Salary Tab
    5. Restrict the view and modification to only permitted users
    6. Reporting
        a. Option to enter Start and End Date of the report
        b. Option to Select Salesperson in the report
        c. Option to save as Excel and PDF Report
        d. Amount details of Sales Order, Invoiced, Payment Collected (Sample
        report below)
    """,

    'author': 'Hafiz Abbas',
    'email': 'hafizabbas9w1@gmail.com',
    'depends': ['sale', 'account', 'report_xlsx'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/salary_slab_views.xml',
        'views/sales_person_staging_views.xml',
        'report/sales_management_report.xml',
        'report/sales_management_report_template.xml',
        'wizard/sales_management_report_views.xml',
        'views/menu_items.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
