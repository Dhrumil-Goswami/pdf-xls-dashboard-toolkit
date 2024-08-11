# -*- coding: utf-8 -*-
from odoo import fields, models, _
import base64
from io import BytesIO
import xlsxwriter
from odoo.exceptions import UserError


class WizardAccountMoveReport(models.TransientModel):
    _name = 'wizard.account.move.report'
    _description = 'Invoice Report'

    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    _sql_constraints = [
        ('date_check', 'check(date_start <= date_end)',
         'Start date must be smaller than end date'),
    ]

    def print_excel_report(self):
        result = self.env['account.move'].search(
            [('move_type', '>=', 'out_invoice'),
             ('invoice_date', '>=', self.date_start),
             ('invoice_date', '<=', self.date_end)])
        if result:
            fp = BytesIO()
            workbook = xlsxwriter.Workbook(fp)
            header_format = workbook.add_format(
                {'font_name': 'Calibri', 'font_size': 12, 'bold': 1,
                 'align': 'center'})
            header_format.set_text_wrap()
            date_style = workbook.add_format(
                {'text_wrap': True, 'num_format': 'mm-dd-yyyy',
                 'align': 'center', 'bottom': 1, 'top': 1})
            row_format = workbook.add_format(
                {'font_size': 10})
            row_format.set_text_wrap()
            worksheet = workbook.add_worksheet('inv Aging')
            row_header_format = workbook.add_format(
                {'font_name': 'Calibri', 'font_size': 11, 'bold': 1,
                 'align': 'center'})
            cell_format = workbook.add_format(
                {'font_size': 10, 'align': 'center',
                 'bottom': 1, 'left': 1, 'right': 1, 'top': 1})
            cell_format_right = workbook.add_format(
                {'font_size': 10, 'align': 'right',
                 'bottom': 1, 'left': 1, 'right': 1, 'top': 1})
            header_str = [
                'Invoice number', 'Customer', 'Invoice Date', 'Total Amount']
            title_format = workbook.add_format(
                {'font_name': 'Calibri', 'font_size': 11, 'align': 'center'})
            worksheet.merge_range(
                0, 0, 0, 3, 'Invoice Excel Report', title_format)
            row = 2
            for index, header in enumerate(header_str, start=0):
                worksheet.write(row, index, header, row_header_format)
            row = 3
            col = 0
            for res in result:
                worksheet.write(row, col, res.name,
                                cell_format)
                worksheet.write(row, col + 1, res.partner_id.name,
                                cell_format)
                worksheet.write(row, col + 2, res.invoice_date,
                                date_style)
                worksheet.write(row, col + 3, '{0:,.2f}'.format(res.amount_total),
                                cell_format_right)
                row += 1

            worksheet.set_column('A:A', 20)
            worksheet.set_column('B:B', 15)
            worksheet.set_column('C:C', 12)
            worksheet.set_column('D:D', 12)
            worksheet.set_column('E:E', 12)
            worksheet.set_column('F:F', 12)
            workbook.close()
            fp.seek(0)
            result = base64.b64encode(fp.read())
            attachment_obj = self.env['ir.attachment']
            filename = 'Invoice Excel Report'
            attachment_id = attachment_obj.create(
                {'name': filename,
                 'display_name': filename,
                 'datas': result})
            download_url = '/web/content/' + \
                           str(attachment_id.id) + '?download=True'
            base_url = self.env['ir.config_parameter'].sudo(
            ).get_param('web.base.url')

            return {
                "type": "ir.actions.act_url",
                "url": str(base_url) + str(download_url),
                "target": "new",
                'nodestroy': False,
            }
        else:
            raise UserError(_('No records found'))

    def print_finance_state(self):
        fp = BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        worksheet = workbook.add_worksheet('PFS-1')
        # Tittle Formating Design.
        left_format_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'center',
             'top': 1, 'left': 1, 'right': 1, 'right_color': '51E0A5',
             'bottom': 1, 'bottom_color': 'white', 'bold': 1, 'bg_color': '51E0A5'})
        right_format_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'right',
             'top': 1, 'left': 1, 'right': 1, 'bg_color': '51E0A5',
             'right_color': '51E0A5', 'top_color': '51E0A5', 'bold': 1})
        right_format_2 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'right',
             'top': 1, 'left': 1, 'right': 1,
             'right_color': '51E0A5', 'top_color': '51E0A5', 'bg_color': '51E0A5',
             'left_color': '51E0A5', 'bold': 1})
        right_format_2_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'left',
             'top': 1, 'left': 1, 'right': 1, 'bold': 1, 'bg_color': '51E0A5',
             'right_color': '51E0A5', 'top_color': '51E0A5', 'left_color': '51E0A5'})
        right_format_3 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'right',
             'top': 1, 'left': 1, 'right': 1, 'bold': 1,
             'right_color': '51E0A5', 'left_color': '51E0A5', 'bg_color': '51E0A5'})
        right_format_4 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'right',
             'top': 1, 'left': 1, 'right': 1, 'bold': 1,
             'left_color': '51E0A5', 'bg_color': '51E0A5'})
        right_format_5 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'right',
             'top': 1, 'left': 1, 'right': 2, 'bottom': 2, 'bold': 1, })
        right_format_5_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'right',
             'top': 1, 'left': 1, 'right': 2, 'bottom': 1, 'bold': 1, })
        title_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 15,
             'align': 'center', 'right': 1, 'bg_color': '51E0A5',
             'left_color': '51E0A5', 'right_color': '51E0A5', 'bold': 1})
        worksheet.set_row(1, 20)
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 12)
        worksheet.set_column('C:C', 12)
        worksheet.set_column('D:D', 9)
        worksheet.set_column('E:E', 12)
        worksheet.set_column('F:F', 12)
        worksheet.set_column('G:G', 9)
        worksheet.set_column('H:H', 20)
        worksheet.set_column('I:I', 12)
        worksheet.set_column('J:J', 12)
        worksheet.set_column('K:K', 12)
        worksheet.write(0, 0, "OLD MISSOURI BANK", left_format_1)
        worksheet.write(0, 1, "", right_format_3)
        worksheet.write(0, 2, "", right_format_3)
        worksheet.write(1, 0, "3570 S NATIONAQL", right_format_1)
        worksheet.write(1, 1, "SPRINGFIELD,", right_format_2)
        worksheet.write(1, 2, "MO 65807", right_format_2_1)
        worksheet.merge_range(
            0, 3, 1, 7, "PERSONAL FINANCIAL STATEMENT", title_format)
        worksheet.merge_range(
            0, 8, 1, 8, "Dated:", right_format_4)
        # Created by Dhrumil.
        worksheet.merge_range(
            0, 9, 1, 10, "", right_format_5_1)
        # Content Format Design.
        format_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'center',
             'top': 1, 'left': 1, 'right': 2})
        format_2 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'center', 'right': 2})
        worksheet.merge_range(
            2, 0, 2, 10, "IMPORTANT: Read these directions before completing this Statement", format_1)
        # row 3
        worksheet.set_row(3, 25)
        format_1_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'center', })
        # Created by Dhrumil
        worksheet.write(3, 0, "", format_1_1)
        format_3 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 9, 'align': 'left', 'right': 2})
        string1 = "If you are applying for individual credit in your owname and are relyng on your own income, or assets and not the income or assets of another person as the basis for repayment of the \n credit requested, or if this statement relates to your quary of the indebtedness of other personts), firm(s), or corporation(s), complete only Sections 1, 3, and 4"
        worksheet.merge_range(
            3, 1, 3, 10, string1, format_3)
        # row 4
        worksheet.set_row(4, 40)
        worksheet.write(4, 0, "", format_1_1)
        string2 = "If you are applying for individual credit but are relying on income from alimony, child support, or separate maintenance or on the income or assets of another person as a basis for repayment \n of the credit requested, complete all Sections. Provide information in Section 2 about the person whose alimony, support, or maintenance payments or income or assets you are relying on.\n Alimony, childsupport, or separate maintenance income, need not be revealed if you do not wish to have it considered as a basis for repaying this obligation."
        worksheet.merge_range(
            4, 1, 4, 10, string2, format_3)
        # row 5
        r5_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 11, 'align': 'center',
             'top': 2, 'bottom': 2, 'left': 1, 'bg_color': 'B0A9A9',
             'right': 2, 'right_color': 'B0A9A9', 'bold': 1})
        r5_format_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 11, 'align': 'center',
             'top': 2, 'bottom': 2, 'left': 1,
             'right': 2, 'bg_color': 'B0A9A9', 'bold': 1})

        worksheet.merge_range(
            5, 0, 5, 4, "Section 1 Individual Information", r5_format)
        worksheet.merge_range(
            5, 5, 5, 10, "Section 2 - Other Party Information", r5_format_1)
        # row 6
        r6_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'left',
             'left': 1, 'right': 1, 'bottom': 1})
        r6_format_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'left',
             'left': 1, 'right': 2, 'bottom': 1})
        worksheet.write(6, 0, "Name", r6_format)
        worksheet.merge_range(
            6, 1, 6, 4, "Maberry Investments, LLC", r6_format)
        worksheet.merge_range(
            6, 5, 6, 6, "Name", r6_format)
        worksheet.merge_range(
            6, 7, 6, 10, "Maberry Investments, LLC", r6_format_1)
        # row 7
        worksheet.write(7, 0, "Address", r6_format)
        worksheet.merge_range(
            7, 1, 7, 4, "1700 Lexington", r6_format)
        worksheet.merge_range(
            7, 5, 7, 6, "Address", r6_format)
        worksheet.merge_range(
            7, 7, 7, 10, "Addres Value", r6_format_1)
        # row 8
        worksheet.write(8, 0, "", r6_format)
        worksheet.merge_range(
            8, 1, 8, 4, "", r6_format)
        worksheet.merge_range(
            8, 5, 8, 6, "", r6_format)
        worksheet.merge_range(
            8, 7, 8, 10, "", r6_format_1)
        # row 9
        worksheet.write(9, 0, "City, State, Zip", r6_format)
        worksheet.merge_range(
            9, 1, 9, 4, "Lamar, MO 64759", r6_format)
        worksheet.merge_range(
            9, 5, 9, 6, "City, State, Zip", r6_format)
        worksheet.merge_range(
            9, 7, 9, 10, "", r6_format_1)
        # row 10
        worksheet.write(10, 0, "Social Security #", r6_format)
        worksheet.merge_range(
            10, 1, 10, 4, "", r6_format)
        worksheet.merge_range(
            10, 5, 10, 6, "Social Security #", r6_format)
        worksheet.merge_range(
            10, 7, 10, 10, "", r6_format_1)
        # row 11
        worksheet.write(11, 0, "Date of Birth", r6_format)
        worksheet.merge_range(
            11, 1, 11, 4, "", r6_format)
        worksheet.merge_range(
            11, 5, 11, 6, "Date of Birth", r6_format)
        worksheet.merge_range(
            11, 7, 11, 10, "", r6_format_1)
        # row 12
        worksheet.write(12, 0, "Position/Occupation", r6_format)
        worksheet.merge_range(
            12, 1, 12, 4, "", r6_format)
        worksheet.merge_range(
            12, 5, 12, 6, "Position/Occupation", r6_format)
        worksheet.merge_range(
            12, 7, 12, 10, "", r6_format_1)
        # row 13
        worksheet.write(13, 0, "Business Name", r6_format)
        worksheet.merge_range(
            13, 1, 13, 4, "", r6_format)
        worksheet.merge_range(
            13, 5, 13, 6, "Business Name", r6_format)
        worksheet.merge_range(
            13, 7, 13, 10, "", r6_format_1)
        # row 14
        worksheet.write(14, 0, "Business Address", r6_format)
        worksheet.merge_range(
            14, 1, 14, 4, "", r6_format)
        worksheet.merge_range(
            14, 5, 14, 6, "Business Address", r6_format)
        worksheet.merge_range(
            14, 7, 14, 10, "", r6_format_1)
        # row 15
        worksheet.write(15, 0, "", r6_format)
        worksheet.merge_range(
            15, 1, 15, 4, "", r6_format)
        worksheet.merge_range(
            15, 5, 15, 6, "", r6_format)
        worksheet.merge_range(
            15, 7, 15, 10, "", r6_format_1)
        # row 16
        worksheet.write(16, 0, "City, State, Zip", r6_format)
        worksheet.merge_range(
            16, 1, 16, 4, "", r6_format)
        worksheet.merge_range(
            16, 5, 16, 6, "City, State, Zip", r6_format)
        worksheet.merge_range(
            16, 7, 16, 10, "", r6_format_1)
        # row 17
        worksheet.write(17, 0, "Length at present address", r6_format)
        worksheet.write(17, 1, "", r6_format)
        worksheet.merge_range(
            17, 2, 17, 3, "Length of employment", r6_format)
        worksheet.write(17, 4, "", r6_format)
        worksheet.merge_range(
            17, 5, 17, 6, "Length at present address", r6_format)
        worksheet.write(17, 7, "", r6_format)
        worksheet.merge_range(
            17, 8, 17, 9, "Length of employment", r6_format)
        worksheet.write(17, 10, "", r6_format_1)

        # r18_format = workbook.add_format(
        #     {'font_name': 'Calibri', 'font_size': 10, 'align': 'left',
        #      'left': 1, 'right': 1, 'bottom': 1})
        # row 18
        worksheet.write(18, 0, "Cell Phone", r6_format)
        worksheet.write(18, 1, "", r6_format)
        worksheet.merge_range(
            18, 2, 18, 3, "Business Phone", r6_format)
        worksheet.write(18, 4, "", r6_format)
        worksheet.merge_range(
            18, 5, 18, 6, "Cell Phone", r6_format)
        worksheet.write(18, 7, "", r6_format)
        worksheet.merge_range(
            18, 8, 18, 9, "Business Phone", r6_format)
        worksheet.write(18, 10, "", r6_format_1)
        # row 19
        worksheet.set_row(19, 25)
        r19_format_2 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'left',
             'left': 1, 'right': 1, 'bottom': 1, 'top': 2})
        r19_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'center',
             'left': 1, 'right': 1, 'bottom': 1, 'top': 2})
        r19_format_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'center',
             'left': 1, 'right': 2, 'bottom': 1, 'top': 2})
        stringr19_1 = "Have (either of) you or any firm in which you were a major owner ever declared bankruptcy, or settled any debts for less than the amounts owed?\n If yes, please provide details on a separate sheet.."
        worksheet.merge_range(
            19, 0, 19, 8, stringr19_1, r19_format_2)
        stringr19_2 = " Yes or No" + u"\u2192"
        worksheet.write(19, 9, stringr19_2, r19_format)
        worksheet.write(19, 10, " No ", r19_format_1)
        # row 20
        r20_format_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'center',
             'left': 1, 'right': 1, 'bottom': 1})
        r20_format_2 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'center',
             'left': 1, 'right': 2, 'bottom': 1})
        str_r20_1 = "Are (either of) you a defendant in any suit or legal action?"
        worksheet.merge_range(
            20, 0, 20, 8, str_r20_1, r6_format)
        worksheet.write(20, 9, stringr19_2, r20_format_1)
        worksheet.write(20, 10, " No ", r20_format_2)
        # row 21
        str_r21 = "Are (either of) you presently subject to any unsatisfied judgements to tax liens?"
        worksheet.merge_range(
            21, 0, 21, 8, str_r21, r6_format)
        worksheet.write(21, 9, stringr19_2, r20_format_1)
        worksheet.write(21, 10, " No ", r20_format_2)
        # row 22
        str_r22 = "When, if ever, have (either of) you been audited by IRS?"
        r22_format_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'right',
             'left': 1, 'right': 1, 'bottom': 1})
        worksheet.merge_range(
            22, 0, 22, 8, str_r22, r6_format)
        worksheet.write(22, 9, "Date" + u"\u2192", r22_format_1)
        worksheet.write(22, 10, " ", r20_format_2)
        # row 23
        r23_for = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 11, 'align': 'left',
             'top': 2, 'bottom': 2, 'left': 1,
             'right': 2, 'bg_color': 'B0A9A9', 'bold': 1})
        worksheet.merge_range(
            23, 0, 23, 10, "Section 3 - Statement of Financial Condition", r23_for)
        # row 24
        worksheet.set_row(24, 37)
        worksheet.merge_range(
            24, 0, 24, 1, "Assets", r20_format_1)
        r24_s1 = "in Dollars\n (omitcents)\nIndividual"
        r24_s2 = "Party or\n Other Party\n or Jointly"
        r24_s3 = "if joint \n with whom"
        worksheet.write(24, 2, r24_s1, r20_format_1)
        worksheet.write(24, 3, r24_s2, r20_format_1)
        worksheet.write(24, 4, r24_s3, r20_format_1)
        worksheet.merge_range(
            24, 5, 24, 7, "Liabilities", r20_format_1)
        worksheet.write(24, 8, r24_s1, r20_format_1)
        worksheet.write(24, 9, r24_s2, r20_format_1)
        worksheet.write(24, 10, r24_s3, r20_format_2)
        # row 25
        r25_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10,
             'align': 'right', 'bg_color': '51E0A5',
             'left': 1, 'right': 1, 'bottom': 1, 'top': 1})
        worksheet.merge_range(
            25, 0, 25, 1, "Cash, Checking & Savings, CD's - Sch A", r6_format)
        worksheet.write(25, 2, "$ 0.00", r25_format)
        worksheet.write(25, 3, '', r6_format)
        worksheet.write(25, 4, '', r6_format)
        worksheet.merge_range(
            25, 5, 25, 7, "Notes payable to banks & others - Sch H", r6_format)
        worksheet.write(25, 8, "$ 0.00", r25_format)
        worksheet.write(25, 9, "", r6_format)
        worksheet.write(25, 10, "", r20_format_2)

        # row 26
        worksheet.merge_range(
            26, 0, 26, 1, "U.S. Gov't & Marketable securities-Sch B", r6_format)
        worksheet.write(26, 2, "$ 0.00", r25_format)
        worksheet.write(26, 3, '', r6_format)
        worksheet.write(26, 4, '', r6_format)
        worksheet.merge_range(
            26, 5, 26, 7, "Due to brokers", r6_format)
        worksheet.write(26, 8, "", r6_format)
        worksheet.write(26, 9, "", r6_format)
        worksheet.write(26, 10, "", r20_format_2)
        # row 27
        worksheet.merge_range(
            27, 0, 27, 1, "Non-Maketable securities-Sch C", r6_format)
        worksheet.write(27, 2, "$ 0.00", r25_format)
        worksheet.write(27, 3, '', r6_format)
        worksheet.write(27, 4, '', r6_format)
        worksheet.merge_range(
            27, 5, 27, 7, "Amounts payable to others - secured", r6_format)
        worksheet.write(27, 8, "", r6_format)
        worksheet.write(27, 9, "", r6_format)
        worksheet.write(27, 10, "", r20_format_2)
        # row 28
        worksheet.merge_range(
            28, 0, 28, 1, "Securities held by broker in margin accts", r6_format)
        worksheet.write(28, 2, "", r6_format)
        worksheet.write(28, 3, '', r6_format)
        worksheet.write(28, 4, '', r6_format)
        worksheet.merge_range(
            28, 5, 28, 7, "Amounts payable to others - unsecured", r6_format)
        worksheet.write(28, 8, "", r6_format)
        worksheet.write(28, 9, "", r6_format)
        worksheet.write(28, 10, "", r20_format_2)
        # row 29
        worksheet.merge_range(
            29, 0, 29, 1, "Restricted, control or margin acct stocks", r6_format)
        worksheet.write(29, 2, "", r6_format)
        worksheet.write(29, 3, '', r6_format)
        worksheet.write(29, 4, '', r6_format)
        worksheet.merge_range(
            29, 5, 29, 7, "Accounts and bills due", r6_format)
        worksheet.write(29, 8, "", r6_format)
        worksheet.write(29, 9, "", r6_format)
        worksheet.write(29, 10, "", r20_format_2)
        # row 30
        worksheet.merge_range(
            30, 0, 30, 1, "Real estate owned-Sch D", r6_format)
        worksheet.write(30, 2, "$ 34,75,500.00", r25_format)
        worksheet.write(30, 3, '', r6_format)
        worksheet.write(30, 4, '', r6_format)
        worksheet.merge_range(
            30, 5, 30, 7, "Unpaid Income tax", r6_format)
        worksheet.write(30, 8, "", r6_format)
        worksheet.write(30, 9, "", r6_format)
        worksheet.write(30, 10, "", r20_format_2)
        # row 31
        worksheet.merge_range(
            31, 0, 31, 1, "Accts, loans, & notes receivable", r6_format)
        worksheet.write(31, 2, "", r6_format)
        worksheet.write(31, 3, '', r6_format)
        worksheet.write(31, 4, '', r6_format)
        worksheet.merge_range(
            31, 5, 31, 7, "Other unpaid taxes & interest", r6_format)
        worksheet.write(31, 8, "", r6_format)
        worksheet.write(31, 9, "", r6_format)
        worksheet.write(31, 10, "", r20_format_2)
        # row 32
        r32_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10,
             'align': 'right',
             'left': 1, 'right': 1, 'bottom': 1, 'top': 1})
        worksheet.merge_range(
            32, 0, 32, 1, "Automobiles", r6_format)
        worksheet.write(32, 2, "$ 4000.00", r32_format)
        worksheet.write(32, 3, '', r6_format)
        worksheet.write(32, 4, '', r6_format)
        worksheet.merge_range(
            32, 5, 32, 7, "Real estate mortgages payable - Sch D", r6_format)
        worksheet.write(32, 8, "$ 23,20,815.00", r25_format)
        worksheet.write(32, 9, "", r6_format)
        worksheet.write(32, 10, "", r20_format_2)
        # row 33
        worksheet.merge_range(
            33, 0, 33, 1, "Cash surrender value-life insurance - Sch E", r6_format)
        worksheet.write(33, 2, "$ 0.00", r25_format)
        worksheet.write(33, 3, '', r6_format)
        worksheet.write(33, 4, '', r6_format)
        worksheet.merge_range(
            33, 5, 33, 7, "", r6_format)
        worksheet.write(33, 8, "", r6_format)
        worksheet.write(33, 9, "", r6_format)
        worksheet.write(33, 10, "", r20_format_2)
        # row 34
        worksheet.merge_range(
            34, 0, 34, 1, "Vested interest in deferred compensation/profit- sharing plans - Sch F", r6_format)
        worksheet.write(34, 2, "$ 0.00", r25_format)
        worksheet.write(34, 3, '', r6_format)
        worksheet.write(34, 4, '', r6_format)
        worksheet.merge_range(
            34, 5, 34, 7, "", r6_format)
        worksheet.write(34, 8, "", r6_format)
        worksheet.write(34, 9, "", r6_format)
        worksheet.write(34, 10, "", r20_format_2)
        # row 35
        worksheet.merge_range(
            35, 0, 35, 1, "Business ventures - Sch G", r6_format)
        worksheet.write(35, 2, "$ 0.00", r25_format)
        worksheet.write(35, 3, '', r6_format)
        worksheet.write(35, 4, '', r6_format)
        worksheet.merge_range(
            35, 5, 35, 7, "", r6_format)
        worksheet.write(35, 8, "", r6_format)
        worksheet.write(35, 9, "", r6_format)
        worksheet.write(35, 10, "", r20_format_2)
        # row 36
        worksheet.merge_range(
            36, 0, 36, 1, "Other assets/personal property itemize - Sch G (if applicable)", r6_format)
        worksheet.write(36, 2, "$ 0.00", r25_format)
        worksheet.write(36, 3, '', r6_format)
        worksheet.write(36, 4, '', r6_format)
        worksheet.merge_range(
            36, 5, 36, 7, "", r6_format)
        worksheet.write(36, 8, "", r6_format)
        worksheet.write(36, 9, "", r6_format)
        worksheet.write(36, 10, "", r20_format_2)
        # row 37
        worksheet.merge_range(
            37, 0, 37, 1, "", r6_format)
        worksheet.write(37, 2, "", r6_format)
        worksheet.write(37, 3, '', r6_format)
        worksheet.write(37, 4, '', r6_format)
        worksheet.merge_range(
            37, 5, 37, 7, "Total Liabilities", r6_format)
        worksheet.write(37, 8, "$ 23,20,815.47", r25_format)
        worksheet.write(37, 9, "", r6_format)
        worksheet.write(37, 10, "", r20_format_2)
        # row 38
        worksheet.merge_range(
            38, 0, 38, 1, "", r6_format)
        worksheet.write(38, 2, "", r6_format)
        worksheet.write(38, 3, '', r6_format)
        worksheet.write(38, 4, '', r6_format)
        worksheet.merge_range(
            38, 5, 38, 7, "Net Worth", r6_format)
        worksheet.write(38, 8, "$ 11,58,684.53", r25_format)
        worksheet.write(38, 9, "", r6_format)
        worksheet.write(38, 10, "", r20_format_2)
        # row 39
        worksheet.merge_range(
            39, 0, 39, 1, "Total Assets", r6_format)
        worksheet.write(39, 2, "$ 34,79,500.00", r25_format)
        worksheet.write(39, 3, '', r6_format)
        worksheet.write(39, 4, '', r6_format)
        worksheet.merge_range(
            39, 5, 39, 7, "Total Liabilities and Net Worth", r6_format)
        worksheet.write(39, 8, "$ 34,79,500.00", r25_format)
        worksheet.write(39, 9, "", r6_format)
        worksheet.write(39, 10, "", r20_format_2)
        # Section 4 and row 40.
        r40_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 11, 'align': 'center',
             'top': 2, 'bottom': 2, 'left': 1, 'bg_color': 'B0A9A9',
             'right': 1, 'bold': 1})
        r40_format_2 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 11, 'align': 'center',
             'top': 2, 'bottom': 2, 'left': 1, 'bg_color': 'B0A9A9',
             'right': 2, 'bold': 1})
        r40_format_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 11, 'align': 'center',
             'top': 2, 'bottom': 2, 'left': 1,
             'right': 1, 'bold': 1})
        worksheet.merge_range(
            40, 0, 40, 2, "Section 4 - Annual Income for year ended " + u"\u2192", r40_format)
        worksheet.merge_range(
            40, 3, 40, 4, "", r40_format_1)
        worksheet.merge_range(
            40, 5, 40, 10, "", r40_format_2)
        # row 41
        worksheet.write(41, 0, "Annual Income", r20_format_1)
        worksheet.write(41, 1, "Amount", r20_format_1)
        worksheet.write(41, 2, "P / OP / J", r20_format_1)
        worksheet.merge_range(
            41, 3, 41, 4, "Annual Expenditures", r20_format_1)
        worksheet.write(41, 5, "Amount", r20_format_1)
        worksheet.write(41, 6, "P / OP / J", r20_format_1)
        worksheet.merge_range(
            41, 7, 41, 8, "Contingent Liabilities Estimated Amts", r20_format_1)
        worksheet.write(41, 9, "Amount", r20_format_1)
        worksheet.write(41, 10, "P / OP / J", r20_format_2)
        # row 42
        worksheet.write(42, 0, "Salary,bonuses,comm", r6_format)
        worksheet.write(42, 1, "", r6_format)
        worksheet.write(42, 2, "", r6_format)
        worksheet.merge_range(
            42, 3, 42, 4, "Mortgage/rental pymts", r6_format)
        worksheet.write(42, 5, "$ 1,41,154.92", r32_format)
        worksheet.write(42, 6, "", r6_format)
        worksheet.write(42, 7, "Do you have any...", r6_format)
        worksheet.write(42, 8, "Yes or No", r20_format_1)
        worksheet.write(42, 9, "", r6_format)
        worksheet.write(42, 10, "", r20_format_2)
        # row 43
        worksheet.set_row(43, 30)
        worksheet.write(43, 0, "Dividends & Interest", r6_format)
        worksheet.write(43, 1, "", r6_format)
        worksheet.write(43, 2, "", r6_format)
        worksheet.merge_range(
            43, 3, 43, 4, "RE taxes & assessments", r6_format)
        r43s = "Contingent liabilities-endorser,\n co-maker or guarantor?"
        worksheet.write(43, 5, "$ 12,000.00", r32_format)
        worksheet.write(43, 6, '', r6_format)
        worksheet.write(43, 7, r43s, r6_format)
        worksheet.write(43, 8, "N", r20_format_1)
        worksheet.write(43, 9, "", r6_format)
        worksheet.write(43, 10, "", r20_format_2)
        # row 44
        worksheet.write(44, 0, "Real Estate income", r6_format)
        worksheet.write(44, 1, "$ 3,45,078", r32_format)
        worksheet.write(44, 2, "Gross at 5% Vac", r6_format)
        worksheet.merge_range(
            44, 3, 44, 4, "Taxes-federal, state & local", r6_format)
        worksheet.write(44, 5, "", r32_format)
        worksheet.write(44, 6, "", r6_format)
        worksheet.write(44, 7, "On leases? On Contracts?", r6_format)
        worksheet.write(44, 8, "N", r20_format_1)
        worksheet.write(44, 9, "", r6_format)
        worksheet.write(44, 10, "", r20_format_2)
        # row 45
        worksheet.set_row(45, 25)
        worksheet.set_row(46, 25)
        worksheet.set_row(47, 35)
        worksheet.set_row(48, 25)
        r45_s = "Other income (alimony,\n child support, or separate\n maintenance income\n needed not be revealed if \nyou do not wish to have it\n considered as a \n basis for repaying this"
        worksheet.merge_range(
            45, 0, 48, 0, r45_s, r6_format)
        worksheet.write(45, 1, "", r32_format)
        worksheet.write(45, 2, "", r6_format)
        worksheet.merge_range(
            45, 3, 45, 4, "Insurance payments", r6_format)
        worksheet.write(45, 5, "$ 25,000.00", r32_format)
        worksheet.write(45, 6, "", r6_format)
        worksheet.write(
            45, 7, "Involvement in pending legal actions?\n actions?", r6_format)
        worksheet.write(45, 8, "N", r20_format_1)
        worksheet.write(45, 9, "", r6_format)
        worksheet.write(45, 10, "", r20_format_2)
        # row 46
        worksheet.write(46, 1, "", r32_format)
        worksheet.write(46, 2, "", r6_format)
        worksheet.merge_range(
            46, 3, 46, 4, "Other contract pymts (car pymts, charge \ncards, etc.)", r6_format)
        worksheet.write(46, 5, "", r32_format)
        worksheet.write(46, 6, "", r6_format)
        worksheet.write(46, 7, "Contested income tax liens?", r6_format)
        worksheet.write(46, 8, "N", r20_format_1)
        worksheet.write(46, 9, "", r6_format)
        worksheet.write(46, 10, "", r20_format_2)
        # row 47
        worksheet.write(47, 1, "", r32_format)
        worksheet.write(47, 2, "", r6_format)
        worksheet.merge_range(
            47, 3, 47, 4, "Alimony, child support.\n maintenance", r6_format)
        worksheet.write(47, 5, "", r32_format)
        worksheet.write(47, 6, "", r6_format)
        worksheet.write(
            47, 7, "Any estimated capital gains\n tax on the unrealized asset\n appreciation?", r6_format)
        worksheet.write(47, 8, "N", r20_format_1)
        worksheet.write(47, 9, "", r6_format)
        worksheet.write(47, 10, "", r20_format_2)
        # row 48
        worksheet.write(48, 1, "", r32_format)
        worksheet.write(48, 2, "", r6_format)
        worksheet.merge_range(
            48, 3, 48, 4, "Other expenses", r6_format)
        worksheet.write(48, 5, "", r32_format)
        worksheet.write(48, 6, "", r6_format)
        worksheet.write(
            48, 7, "Other special debt or\n circumstances?", r6_format)
        worksheet.write(48, 8, "N", r20_format_1)
        worksheet.write(48, 9, "", r6_format)
        worksheet.write(48, 10, "", r20_format_2)
        # row 49
        worksheet.write(49, 0, "Total Income", r6_format)
        worksheet.write(49, 1, "$ 3,45,078.00", r25_format)
        worksheet.write(49, 2, "", r6_format)
        worksheet.merge_range(
            49, 3, 49, 4, "Total Expenditures", r6_format)
        worksheet.write(49, 5, "$ 1,78,154.92", r25_format)
        worksheet.write(49, 6, "", r6_format)
        worksheet.merge_range(
            49, 7, 49, 8, "If yes to any question(s) describe", r6_format)
        worksheet.merge_range(
            49, 9, 49, 10, "", r20_format_2)
        # row 50
        worksheet.merge_range(
            50, 0, 52, 6, "*Party=P Other Party=OP Jointly=J", r6_format)
        worksheet.merge_range(
            50, 7, 50, 10, "", r20_format_2)
        worksheet.merge_range(
            51, 7, 51, 10, "", r20_format_2)
        worksheet.merge_range(
            52, 7, 52, 8, "Total Contingent Liabilities", r6_format)
        worksheet.write(52, 9, "$ 0.00", r25_format)
        worksheet.write(52, 10, "$ 0.00", r20_format_2)
        worksheet.merge_range(
            52, 7, 52, 8, "Total Contingent Liabilities", r6_format)
        r53_format = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 11, 'align': 'center',
             'top': 1, 'bottom': 2, 'left': 1, 'right': 2})
        worksheet.merge_range(
            53, 0, 53, 10, "COMPLETE SCHEDULES AND SIGN ON REVERSE SIDE", r53_format)

        # Sheet 2 - PFS-2 SHEET CREATE.
        worksheet_1 = workbook.add_worksheet("PFS-2")
        worksheet_1.set_column('A:A', 20)
        worksheet_1.set_column('B:B', 12)
        worksheet_1.set_column('C:C', 15)
        worksheet_1.set_column('D:D', 12)
        worksheet_1.set_column('E:E', 15)
        worksheet_1.set_column('F:F', 12)
        worksheet_1.set_column('G:G', 9)
        worksheet_1.set_column('H:H', 15)
        worksheet_1.set_column('I:I', 8)
        worksheet_1.set_column('J:J', 20)
        # Row-0
        r1_string = "SCHEDULE A - CASH, CHECKING AND SAVINGS ACCOUNTS, CERTIFICATES OF DEPOSIT, MONEY MARKET FUNDS, ETC"
        worksheet_1.merge_range(
            0, 0, 0, 9, r1_string, r23_for)
        # Row - 1
        s2_r1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'align': 'center',
             'left': 1, 'right': 1, 'bottom': 1})
        s2_r2 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'align': 'center',
             'left': 1, 'right': 2, 'bottom': 1})
        worksheet_1.write(1, 0, "Name of Financial Institution", s2_r1)
        worksheet_1.merge_range(
            1, 1, 1, 2, "Types of Account", s2_r1)
        worksheet_1.merge_range(
            1, 3, 1, 4, "Owner", s2_r1)
        worksheet_1.write(1, 5, "Joint", s2_r1)
        worksheet_1.merge_range(
            1, 6, 1, 7, "If pledged, to Whom?", s2_r1)
        worksheet_1.merge_range(
            1, 8, 1, 9, "Balance", s2_r2)
        # Row - 2
        worksheet_1.write(2, 0, "", s2_r1)
        worksheet_1.merge_range(
            2, 1, 2, 2, "", s2_r1)
        worksheet_1.merge_range(
            2, 3, 2, 4, "", s2_r1)
        worksheet_1.write(2, 5, "", s2_r1)
        worksheet_1.merge_range(
            2, 6, 2, 7, "", s2_r1)
        worksheet_1.merge_range(
            2, 8, 2, 9, "", s2_r2)
        # Row - 3
        worksheet_1.write(3, 0, "", s2_r1)
        worksheet_1.merge_range(
            3, 1, 3, 2, "", s2_r1)
        worksheet_1.merge_range(
            3, 3, 3, 4, "", s2_r1)
        worksheet_1.write(3, 5, "", s2_r1)
        worksheet_1.merge_range(
            3, 6, 3, 7, "", s2_r1)
        worksheet_1.merge_range(
            3, 8, 3, 9, "", s2_r2)
        # Row - 4
        worksheet_1.write(4, 0, "", s2_r1)
        worksheet_1.merge_range(
            4, 1, 4, 2, "", s2_r1)
        worksheet_1.merge_range(
            4, 3, 4, 4, "", s2_r1)
        worksheet_1.write(4, 5, "", s2_r1)
        worksheet_1.merge_range(
            4, 6, 4, 7, "", s2_r1)
        worksheet_1.merge_range(
            4, 8, 4, 9, "", s2_r2)
        # Row - 5
        s2r5_str = "SCHEDULE B - U.S. GOVERNMENT & MARKETABLE SECURITIES (Use additional sheet if necessary)"
        worksheet_1.merge_range(
            5, 0, 5, 9, s2r5_str, r23_for)
        # Row - 6
        worksheet_1.set_row(6, 20)
        worksheet_1.write(6, 0, "Description", s2_r1)
        worksheet_1.merge_range(
            6, 1, 6, 2, "# of Shares or Face Value of Bonds", s2_r1)
        worksheet_1.merge_range(
            6, 3, 6, 4, "In Name of", s2_r1)
        worksheet_1.merge_range(
            6, 5, 6, 6, "Registered, Pledged,\nor Held by Others?", s2_r1)
        worksheet_1.write(6, 7, "Market Value", s2_r1)
        worksheet_1.merge_range(
            6, 8, 6, 9, "Exchanges where Traded", s2_r2)
        # Row - 7
        worksheet_1.write(7, 0, "", s2_r1)
        worksheet_1.merge_range(
            7, 1, 7, 2, "", s2_r1)
        worksheet_1.merge_range(
            7, 3, 7, 4, "", s2_r1)
        worksheet_1.merge_range(
            7, 5, 7, 6, "", s2_r1)
        worksheet_1.write(7, 7, "", s2_r1)
        worksheet_1.merge_range(
            7, 8, 7, 9, "", s2_r2)
        # Row - 8
        worksheet_1.write(8, 0, "", s2_r1)
        worksheet_1.merge_range(
            8, 1, 8, 2, "", s2_r1)
        worksheet_1.merge_range(
            8, 3, 8, 4, "", s2_r1)
        worksheet_1.merge_range(
            8, 5, 8, 6, "", s2_r1)
        worksheet_1.write(8, 7, "", s2_r1)
        worksheet_1.merge_range(
            8, 8, 8, 9, "", s2_r2)
        # Row - 9
        worksheet_1.write(9, 0, "", s2_r1)
        worksheet_1.merge_range(
            9, 1, 9, 2, "", s2_r1)
        worksheet_1.merge_range(
            9, 3, 9, 4, "", s2_r1)
        worksheet_1.merge_range(
            9, 5, 9, 6, "", s2_r1)
        worksheet_1.write(9, 7, "", s2_r1)
        worksheet_1.merge_range(
            9, 8, 9, 9, "", s2_r2)
        # Row - 10
        s2r10_str = "SCHEDULE C - NON-MARKETABLE SECURITIES (Use additional sheet if necessary)"
        worksheet_1.merge_range(
            10, 0, 10, 9, s2r10_str, r23_for)
        # Row - 11
        worksheet_1.write(11, 0, "Description", s2_r1)
        worksheet_1.write(11, 1, "# of Shares", s2_r1)
        worksheet_1.merge_range(
            11, 2, 11, 3, "in Name of", s2_r1)
        worksheet_1.merge_range(
            11, 4, 11, 6, "Registered, Pledged, or Held by Others?", s2_r1)
        worksheet_1.write(11, 7, "Value", s2_r1)
        worksheet_1.merge_range(
            11, 8, 11, 9, "Method of Valuation", s2_r2)
        # Row - 12
        worksheet_1.write(12, 0, "", s2_r1)
        worksheet_1.write(12, 1, "", s2_r1)
        worksheet_1.merge_range(
            12, 2, 12, 3, "", s2_r1)
        worksheet_1.merge_range(
            12, 4, 12, 6, "", s2_r1)
        worksheet_1.write(12, 7, "", s2_r1)
        worksheet_1.merge_range(
            12, 8, 12, 9, "", s2_r2)
        # Row - 13
        worksheet_1.write(13, 0, "", s2_r1)
        worksheet_1.write(13, 1, "", s2_r1)
        worksheet_1.merge_range(
            13, 2, 13, 3, "", s2_r1)
        worksheet_1.merge_range(
            13, 4, 13, 6, "", s2_r1)
        worksheet_1.write(13, 7, "", s2_r1)
        worksheet_1.merge_range(
            13, 8, 13, 9, "", s2_r2)
        # Row - 14
        worksheet_1.write(14, 0, "", s2_r1)
        worksheet_1.write(14, 1, "", s2_r1)
        worksheet_1.merge_range(
            14, 2, 14, 3, "", s2_r1)
        worksheet_1.merge_range(
            14, 4, 14, 6, "", s2_r1)
        worksheet_1.write(14, 7, "", s2_r1)
        worksheet_1.merge_range(
            14, 8, 14, 9, "", s2_r2)
        # Row - 15
        s2r15_str = "SCHEDULE D - INVESTMENTS IN REAL ESTATE (Use additional sheet if necessary)"
        worksheet_1.merge_range(
            15, 0, 15, 9, s2r15_str, r23_for)
        # Row - 16
        worksheet_1.set_row(16, 20)
        worksheet_1.write(
            16, 0, "Description / Location of\n Real Estate Investment", s2_r1)
        worksheet_1.write(16, 1, "joint", s2_r1)
        worksheet_1.write(16, 2, "Date Original \nInvestment / $", s2_r1)
        worksheet_1.write(16, 3, "% Owned By You", s2_r1)
        worksheet_1.write(16, 4, "Market Value", s2_r1)
        worksheet_1.write(16, 5, "Present Balance", s2_r1)
        worksheet_1.write(16, 6, "Monthly /n Payment", s2_r1)
        worksheet_1.write(16, 7, "Maturity Date", s2_r1)
        worksheet_1.merge_range(
            16, 8, 16, 9, "Mortgage Owed To", s2_r2)
        # Row - 17
        s2_r17 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 8, 'align': 'right',
             'left': 1, 'right': 1, 'bottom': 1})
        worksheet_1.write(17, 0, "1803 Grand Carthage MO", s2_r1)
        worksheet_1.write(17, 1, "", s2_r1)
        worksheet_1.write(17, 2, "Sep. 2020 ", s2_r1)
        worksheet_1.write(17, 3, "100", s2_r1)
        worksheet_1.write(17, 4, "$ 12,00,000.00", s2_r17)
        worksheet_1.write(17, 5, "$ 7,73,733.99", s2_r17)
        worksheet_1.write(17, 6, "$ 3,819.21", s2_r17)
        worksheet_1.write(17, 7, "09/50", s2_r1)
        worksheet_1.merge_range(
            17, 8, 17, 9, "Richard Scott", s2_r2)
        # Row - 18
        worksheet_1.write(18, 0, "1700 Lexington", s2_r1)
        worksheet_1.write(18, 1, "", s2_r1)
        worksheet_1.write(18, 2, "02/2022", s2_r1)
        worksheet_1.write(18, 3, "100", s2_r1)
        worksheet_1.write(18, 4, "", s2_r17)
        worksheet_1.write(18, 5, "$ 6,95,945.49", s2_r17)
        worksheet_1.write(18, 6, "$ 3,341.91", s2_r17)
        worksheet_1.write(18, 7, "04/2052", s2_r1)
        worksheet_1.merge_range(
            18, 8, 18, 9, "Richard Scott", s2_r2)
        # Row - 19
        worksheet_1.write(19, 0, "Listed on attached sheet", s2_r1)
        worksheet_1.write(19, 1, "", s2_r1)
        worksheet_1.write(19, 2, "", s2_r1)
        worksheet_1.write(19, 3, "100", s2_r1)
        worksheet_1.write(19, 4, "$ 11,75,500", s2_r17)
        worksheet_1.write(19, 5, "$ 8,51,135.99", s2_r17)
        worksheet_1.write(19, 6, "$ 3,341.91", s2_r17)
        worksheet_1.write(19, 7, "04/2052", s2_r1)
        worksheet_1.merge_range(
            19, 8, 19, 9, "Richard Scott", s2_r2)
        # Row - 20
        s2r20_str = "SCHEDULE E - LIFE INSURANCE CARRIED, INCLUDING GROUP INSURANCE"
        worksheet_1.merge_range(
            20, 0, 20, 9, s2r20_str, r23_for)
        # Row - 21
        worksheet_1.write(21, 0, "Name of Financial Institution", s2_r1)
        worksheet_1.merge_range(
            21, 1, 21, 2, "Owner of Policy", s2_r1)
        worksheet_1.merge_range(
            21, 3, 21, 4, "Beneficiary & Relationship", s2_r1)
        worksheet_1.write(21, 5, "Face Amt", s2_r1)
        worksheet_1.merge_range(
            21, 6, 21, 7, "Policy Loans", s2_r1)
        worksheet_1.merge_range(
            21, 8, 21, 9, "Cash Surrender Value", s2_r2)
        # Row - 22
        worksheet_1.write(22, 0, "", s2_r1)
        worksheet_1.merge_range(
            22, 1, 22, 2, "", s2_r1)
        worksheet_1.merge_range(
            22, 3, 22, 4, "", s2_r1)
        worksheet_1.write(22, 5, "", s2_r1)
        worksheet_1.merge_range(
            22, 6, 22, 7, "", s2_r1)
        worksheet_1.merge_range(
            22, 8, 22, 9, "", s2_r2)
        # Row - 23
        worksheet_1.write(23, 0, "", s2_r1)
        worksheet_1.merge_range(
            23, 1, 23, 2, "", s2_r1)
        worksheet_1.merge_range(
            23, 3, 23, 4, "", s2_r1)
        worksheet_1.write(23, 5, "", s2_r1)
        worksheet_1.merge_range(
            23, 6, 23, 7, "", s2_r1)
        worksheet_1.merge_range(
            23, 8, 23, 9, "", s2_r2)
        # Row - 24
        worksheet_1.write(24, 0, "", s2_r1)
        worksheet_1.merge_range(
            24, 1, 24, 2, "", s2_r1)
        worksheet_1.merge_range(
            24, 3, 24, 4, "", s2_r1)
        worksheet_1.write(24, 5, "", s2_r1)
        worksheet_1.merge_range(
            24, 6, 24, 7, "", s2_r1)
        worksheet_1.merge_range(
            24, 8, 24, 9, "", s2_r2)
        # Row - 25
        s2r25_str = "SCHEDULE F - VESTED INTEREST IN DEFERRED COMPENSATION/PROFIT-SHARING PLANS"
        worksheet_1.merge_range(
            25, 0, 25, 9, s2r25_str, r23_for)
        # Row - 26
        worksheet_1.write(26, 0, "Company Name", s2_r1)
        worksheet_1.write(26, 1, "% Vested", s2_r1)
        worksheet_1.write(26, 2, "Account #", s2_r1)
        worksheet_1.merge_range(
            26, 3, 26, 4, "Manner of Payment (Annuity,Lump Sum,etc)", s2_r1)
        worksheet_1.write(26, 5, "Distribution Date", s2_r1)
        worksheet_1.merge_range(
            26, 6, 26, 7, "Beneficiary", s2_r1)
        worksheet_1.merge_range(
            26, 8, 26, 9, "Amount", s2_r2)
        # Row - 27
        worksheet_1.write(27, 0, "", s2_r1)
        worksheet_1.write(27, 1, "", s2_r1)
        worksheet_1.write(27, 2, "", s2_r1)
        worksheet_1.merge_range(
            27, 3, 27, 4, "", s2_r1)
        worksheet_1.write(27, 5, "", s2_r1)
        worksheet_1.merge_range(
            27, 6, 27, 7, "", s2_r1)
        worksheet_1.merge_range(
            27, 8, 27, 9, "", s2_r2)
        # Row - 28
        worksheet_1.write(28, 0, "", s2_r1)
        worksheet_1.write(28, 1, "", s2_r1)
        worksheet_1.write(28, 2, "", s2_r1)
        worksheet_1.merge_range(
            28, 3, 28, 4, "", s2_r1)
        worksheet_1.write(28, 5, "", s2_r1)
        worksheet_1.merge_range(
            28, 6, 28, 7, "", s2_r1)
        worksheet_1.merge_range(
            28, 8, 28, 9, "", s2_r2)
        # Row - 29
        worksheet_1.write(29, 0, "", s2_r1)
        worksheet_1.write(29, 1, "", s2_r1)
        worksheet_1.write(29, 2, "", s2_r1)
        worksheet_1.merge_range(
            29, 3, 29, 4, "", s2_r1)
        worksheet_1.write(29, 5, "", s2_r1)
        worksheet_1.merge_range(
            29, 6, 29, 7, "", s2_r1)
        worksheet_1.merge_range(
            29, 8, 29, 9, "", s2_r2)
        # Row - 30
        s2r30_str = "SCHEDULE G - BUSINESS VENTURES (Use additional sheet if necessary)"
        worksheet_1.merge_range(
            30, 0, 30, 9, s2r30_str, r23_for)
        # Row - 31
        s2r31_str1 = "list Name and Address of Any\n Business Venture in Which\n you are a Princpal or Partner"
        worksheet_1.set_row(31, 30)
        worksheet_1.write(31, 0, s2r31_str1, s2_r1)
        worksheet_1.write(31, 1, "position / Title \n in Business", s2_r1)
        worksheet_1.write(31, 2, "Line of Business", s2_r1)
        worksheet_1.write(31, 3, "Years in Business", s2_r1)
        worksheet_1.write(31, 4, "Total Assets Listed\n in Section 3", s2_r1)
        worksheet_1.write(31, 5, "% of Ownership", s2_r1)
        worksheet_1.merge_range(
            31, 6, 31, 7, "Net Worth of Business", s2_r1)
        worksheet_1.merge_range(
            31, 8, 31, 9, "Present Net Value of Your Investment", s2_r2)
        # Row - 32
        worksheet_1.write(32, 0, "", s2_r1)
        worksheet_1.write(32, 1, "", s2_r1)
        worksheet_1.write(32, 2, "", s2_r1)
        worksheet_1.write(32, 3, "", s2_r1)
        worksheet_1.write(32, 4, "", s2_r1)
        worksheet_1.write(32, 5, "", s2_r1)
        worksheet_1.merge_range(
            32, 6, 32, 7, "", s2_r1)
        worksheet_1.merge_range(
            32, 8, 32, 9, "", s2_r2)
        # Row - 33
        worksheet_1.write(33, 0, "", s2_r1)
        worksheet_1.write(33, 1, "", s2_r1)
        worksheet_1.write(33, 2, "", s2_r1)
        worksheet_1.write(33, 3, "", s2_r1)
        worksheet_1.write(33, 4, "", s2_r1)
        worksheet_1.write(33, 5, "", s2_r1)
        worksheet_1.merge_range(
            33, 6, 33, 7, "", s2_r1)
        worksheet_1.merge_range(
            33, 8, 33, 9, "", s2_r2)
        # Row - 34
        worksheet_1.write(34, 0, "", s2_r1)
        worksheet_1.write(34, 1, "", s2_r1)
        worksheet_1.write(34, 2, "", s2_r1)
        worksheet_1.write(34, 3, "", s2_r1)
        worksheet_1.write(34, 4, "", s2_r1)
        worksheet_1.write(34, 5, "", s2_r1)
        worksheet_1.merge_range(
            34, 6, 34, 7, "", s2_r1)
        worksheet_1.merge_range(
            34, 8, 34, 9, "", s2_r2)
        # Row - 35
        s2r35_str = "SCHEDULE H - LOANS OWING BANKS, BROKERS, FINANCE COMPANIES, AND OTHERS (MASTERCARD, VISA, ETC.)"
        worksheet_1.merge_range(
            35, 0, 35, 9, s2r35_str, r23_for)
        # Row - 36
        worksheet_1.write(36, 0, "Owing to (Acct #)", s2_r1)
        worksheet_1.write(36, 1, "Joint", s2_r1)
        worksheet_1.write(36, 2, "Original Loan Amount", s2_r1)
        worksheet_1.write(36, 3, "Due", s2_r1)
        worksheet_1.write(36, 4, "Present Balance", s2_r1)
        worksheet_1.write(36, 5, "Monthly Payment", s2_r1)
        worksheet_1.merge_range(
            36, 6, 36, 7, "Date of Final Pymt", s2_r1)
        worksheet_1.merge_range(
            36, 8, 36, 9, "Secured By", s2_r2)
        # Row - 37
        worksheet_1.write(37, 0, "OlD MO Bank - Line of credit", s2_r1)
        worksheet_1.write(37, 1, "", s2_r1)
        worksheet_1.write(37, 2, "$ 6,790.00", s2_r17)
        worksheet_1.write(37, 3, "", s2_r1)
        worksheet_1.write(37, 4, "", s2_r1)
        worksheet_1.write(37, 5, "$ 26.40", s2_r17)
        worksheet_1.merge_range(
            37, 6, 37, 7, "", s2_r1)
        worksheet_1.merge_range(
            37, 8, 37, 9, "", s2_r2)
        # Row - 38
        worksheet_1.write(38, 0, "", s2_r1)
        worksheet_1.write(38, 1, "", s2_r1)
        worksheet_1.write(38, 2, "", s2_r17)
        worksheet_1.write(38, 3, "", s2_r1)
        worksheet_1.write(38, 4, "", s2_r1)
        worksheet_1.write(38, 5, "", s2_r17)
        worksheet_1.merge_range(
            38, 6, 38, 7, "", s2_r1)
        worksheet_1.merge_range(
            38, 8, 38, 9, "", s2_r2)
        # Row - 39
        worksheet_1.write(39, 0, "", s2_r1)
        worksheet_1.write(39, 1, "", s2_r1)
        worksheet_1.write(39, 2, "", s2_r17)
        worksheet_1.write(39, 3, "", s2_r1)
        worksheet_1.write(39, 4, "", s2_r1)
        worksheet_1.write(39, 5, "", s2_r17)
        worksheet_1.merge_range(
            39, 6, 39, 7, "", s2_r1)
        worksheet_1.merge_range(
            39, 8, 39, 9, "", s2_r2)
        # Row - 40
        s2_r40 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 7, 'align': 'top',
             'left': 1, 'right': 2})
        worksheet_1.set_row(40, 100)
        s2r40_text = "The information contained in this statement is provided"\
            "to induce you to extend or to continue the extension of credit to the"\
            "undersigned or to others upon the guaranty of the undersigned.  The "\
            "undersigned acknowledges and understands that"\
            "\nyou are relying on the information provided herein in deciding to "\
            "grant or continue credit or to accept a guaranty thereof.  Each of "\
            "the undersigned represents, warrants, and certifies that (1) the"\
            "information provided herein is true,\n correct and complete and gives"\
            "a correct and complete showing of the financial condition of the "\
            "undersigned, (2) the undersigned has no liabilities direct, indirect"\
            "or contingent except as set forth in this statement, and (3) legal and"\
            "equitable\n title to all assets listed herein is in the undersigned's"\
            "sole name, except as may be herein otherwise noted.  Each of the undersigned"\
            "agrees to notify you immediately and in writing of any change in name, address,"\
            "or \nemployment and of any material adverse change (1) in any of the information "\
            "contained in this statement or (2) in the financial condition of any of the "\
            "undersigned or (3) in the ability of any of the undersigned to perform its "\
            "(or their) obligations to you.\n In the absence of such notice or a new and"\
            "full written statement, this should be considered as a continuing statement"\
            "and substantially correct.  You are authorized to make all inquiries you deem"\
            "necessary to verify the accuracy of the information\n contained herein, "\
            "and to determine the credit-worthiness of the undersigned and the "\
            "undersigned hereby authorizes all persons of whom you make such inquiries"\
            "to respond thereto in full.\n  Each of the undersigned authorizes you to "\
            "answer questions about your credit experience with the undersigned."
        worksheet_1.merge_range(
            40, 0, 40, 9, s2r40_text, s2_r40)
        # Row - 41-42
        s2_r41 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 9, 'align': 'left'})
        s2_r41_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 9,
             'align': 'left', 'right': 2})
        worksheet_1.merge_range(
            41, 0, 42, 2, "Date signed___________", s2_r41)
        worksheet_1.merge_range(
            41, 3, 42, 9, "Signature__________________________________", s2_r41_1)
        # Row - 43-47
        worksheet_1.set_row(43, 20)
        worksheet_1.set_row(44, 20)
        s2_r44 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 9, 'align': 'left',
             'bottom': 1, 'bottom_color': 'white'})
        s2_r44_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 9,
             'align': 'left', 'right': 2, 'bottom': 1, 'bottom_color': 'white'})
        s2_r44_2 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 9,
             'align': 'left', 'right': 2, 'bottom': 2})
        s2_r44_3 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 9, 'align': 'left',
             'bottom': 2})
        worksheet_1.merge_range(
            43, 0, 44, 2, "Date signed___________", s2_r44)
        worksheet_1.merge_range(
            43, 3, 44, 9, "Signature__________________________________", s2_r44_1)
        worksheet_1.merge_range(
            45, 0, 47, 2, "", s2_r44_3)
        worksheet_1.merge_range(
            45, 3, 47, 9, "", s2_r44_2)
        # Sheet - 3 PFS-3
        worksheet_2 = workbook.add_worksheet("PFS-3")
        worksheet_2.set_column('A:A', 8)
        worksheet_2.set_column('B:B', 15)
        worksheet_2.set_column('C:C', 8)
        worksheet_2.set_column('D:D', 15)
        worksheet_2.set_column('E:E', 8)
        worksheet_2.set_column('F:F', 15)
        worksheet_2.set_column('G:G', 8)
        worksheet_2.set_column('H:H', 15)
        worksheet_2.set_column('I:I', 8)
        worksheet_2.set_column('J:J', 15)
        # Row - s3-0
        worksheet_2.merge_range(
            0, 0, 0, 9, "PERSONAL FINANCIAL STATEMENT – ADDITIONAL SHEET", r5_format_1)
        # Row - s3-1
        worksheet_2.merge_range(
            1, 0, 1, 1, "Name:", r20_format_1)
        worksheet_2.merge_range(
            1, 2, 1, 9, "", r20_format_2)
        # Row - s3-2
        worksheet_1.write(2, 0, "", format_1_1)
        worksheet_1.write(2, 1, "", format_1_1)
        worksheet_2.merge_range(
            2, 2, 2, 3, "Value", r20_format_1)
        worksheet_2.merge_range(
            2, 4, 2, 5, "Current Balance", r20_format_1)
        worksheet_2.merge_range(
            2, 6, 2, 7, "Monthly Payment", r20_format_1)
        worksheet_2.merge_range(
            2, 8, 2, 9, "Lien", r20_format_2)

        # Row - s3-3
        worksheet_2.merge_range(
            3, 0, 3, 1, "210 E Yale Street Liberal", r20_format_1)
        worksheet_2.merge_range(
            3, 2, 3, 3, "$ 3,20,500", r20_format_1)
        worksheet_2.merge_range(
            3, 4, 3, 5, "$ 2,72,032.5", r20_format_1)
        worksheet_2.merge_range(
            3, 6, 3, 7, "$ 1,485.98", r20_format_1)
        worksheet_2.merge_range(
            3, 8, 3, 9, "OLD MO", r20_format_2)
        for i in range(4, 48):
            worksheet_2.merge_range(
                i, 0, i, 1, "", r20_format_1)
            worksheet_2.merge_range(
                i, 2, i, 3, "", r20_format_1)
            worksheet_2.merge_range(
                i, 4, i, 5, "", r20_format_1)
            worksheet_2.merge_range(
                i, 6, i, 7, "", r20_format_1)
            worksheet_2.merge_range(
                i, 8, i, 9, "", r20_format_2)
        s3_r48_1 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'center',
             'bottom': 2, 'right': 1})
        s3_r48_2 = workbook.add_format(
            {'font_name': 'Calibri', 'font_size': 10, 'align': 'center',
             'bottom': 2, 'right': 2})
        worksheet_2.merge_range(
            48, 0, 48, 1, "", s3_r48_1)
        worksheet_2.merge_range(
            48, 2, 48, 3, "", s3_r48_1)
        worksheet_2.merge_range(
            48, 4, 48, 5, "", s3_r48_1)
        worksheet_2.merge_range(
            48, 6, 48, 7, "", s3_r48_1)
        worksheet_2.merge_range(
            48, 8, 48, 9, "", s3_r48_2)
        workbook.close()
        fp.seek(0)
        result = base64.b64encode(fp.read())
        attachment_obj = self.env['ir.attachment']
        filename = 'Report'
        attachment_id = attachment_obj.create(
            {'name': filename,
             'display_name': filename,
             'datas': result})
        download_url = '/web/content/' + \
                       str(attachment_id.id) + '?download=True'
        base_url = self.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')

        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
            'nodestroy': False,
        }
