# -*- coding: utf-8 -*-

from odoo import models, fields, _, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    state = fields.Selection([
        ('draft', 'Draft Quotation'),
        ('sent', 'Quotation Sent'),
        ('pending_approval', 'Pending Approval'),
        ('sale', 'Sales Order'),
        ('done', 'Sales Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True)

    def pending_approval_action(self):
        print("\n\n\n::::::pendig::::")
        self.write({'state': 'pending_approval'})

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if vals.get("order_line"):
            for line in self.order_line:
                tax = 0
                extra_cost_tax = 0
                print("\n\n\n::::;line::::::", res)
                for t in line.tax_id:
                    tax += t.amount
                extra_cost = line.pnf_charge + line.exe_charge
                line.price_subtotal += extra_cost
                if tax > 0:
                    extra_cost_tax = (extra_cost * tax) / 100
                    line.price_tax += extra_cost_tax
                    line.price_total += line.price_tax
                line.price_total += line.price_subtotal
        return res

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        if vals.get("order_line"):
            for line in res.order_line:
                tax = 0
                print("\n\n\n::::;line::::::", res)
                for t in line.tax_id:
                    tax += t.amount
                extra_cost = line.pnf_charge + line.exe_charge
                line.price_subtotal += extra_cost
                if tax > 0:
                    extra_cost_tax = (extra_cost * tax) / 100
                    line.price_tax += extra_cost_tax
                    line.price_total += line.price_tax
                line.price_total += line.price_subtotal
        return res


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        res = super(AccountMove, self.with_context(
            check_move_validity=False)).create(vals)
        if vals.get("invoice_line"):
            for line in res.invoice_line_ids:
                tax = 0
                for t in line.tax_id:
                    tax += t.amount
                extra_cost = line.pnf_charge + line.exe_charge
                line.price_subtotal += extra_cost
                if tax > 0:
                    extra_cost_tax = (extra_cost * tax) / 100
                    line.price_tax += extra_cost_tax
                    line.price_total += line.price_tax
                line.price_total += line.price_subtotal
        return res

    @api.depends(
        'line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
        'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state',
        'line_ids.full_reconcile_id',
        'line_ids.exe_charge',
        'line_ids.pnf_charge')
    def _compute_amount(self):
        for move in self:

            if move.payment_state == 'invoicing_legacy':
                # invoicing_legacy state is set via SQL when setting setting field
                # invoicing_switch_threshold (defined in account_accountant).
                # The only way of going out of this state is through this setting,
                # so we don't recompute it here.
                move.payment_state = move.payment_state
                continue
            cus_total = 0
            cus_untax_total = 0
            cus_tax = 0

            total_untaxed = 0.0
            total_untaxed_currency = 0.0
            total_tax = 0.0
            total_tax_currency = 0.0
            total_to_pay = 0.0
            total_residual = 0.0
            total_residual_currency = 0.0
            total = 0.0
            total_currency = 0.0
            currencies = move._get_lines_onchange_currency().currency_id

            for line in move.line_ids:
                if move.is_invoice(include_receipts=True):
                    # === Invoices ===

                    if not line.exclude_from_invoice_tab:
                        # Untaxed amount.
                        total_untaxed += line.balance
                        total_untaxed_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.tax_line_id:
                        # Tax amount.
                        total_tax += line.balance
                        total_tax_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.account_id.user_type_id.type in ('receivable', 'payable'):
                        # Residual amount.
                        total_to_pay += line.balance
                        total_residual += line.amount_residual
                        total_residual_currency += line.amount_residual_currency
                    else:
                        # === Miscellaneous journal entry ===
                        if line.debit:
                            total += line.balance
                            total_currency += line.amount_currency
                    if line.pnf_charge or line.exe_charge:
                        tax = 0
                        extra_cost = 0
                        price_tax = 0
                        for t in line.tax_ids:
                            tax += t.amount
                            extra_cost = line.pnf_charge + line.exe_charge
                            print("\n\n\n:::;extra_cost:::", extra_cost)
                            line.price_subtotal = line.price_subtotal + extra_cost
                            cus_untax_total += extra_cost
                            if tax > 0:
                                extra_cost_tax = (extra_cost * tax) / 100
                                print("\n\n\n::extra_cost_tax:", extra_cost_tax)
                                price_tax += (line.price_total -
                                              line.price_subtotal) + extra_cost_tax
                                line.price_total = line.price_subtotal + price_tax
                                cus_tax += extra_cost_tax
                            line.price_total = line.price_subtotal
                            cus_total += extra_cost + extra_cost_tax

            if move.move_type == 'entry' or move.is_outbound():
                sign = 1
            else:
                sign = -1
            print("\n\n\n:::::cus_untax_total::::", cus_untax_total)
            print("\n\n\n:::::cus_tax::::", cus_tax)
            print("\n\n\n:::::cus_total::::", cus_total)
            move.amount_untaxed = cus_untax_total + sign * \
                (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
            move.amount_tax = cus_tax + sign * \
                (total_tax_currency if len(currencies) == 1 else total_tax)
            move.amount_total = cus_total + sign * \
                (total_currency if len(currencies) == 1 else total)
            move.amount_residual = -sign * \
                (total_residual_currency if len(currencies) == 1 else total_residual)
            move.amount_untaxed_signed = -total_untaxed
            move.amount_tax_signed = -total_tax + cus_tax
            move.amount_total_signed = abs(
                total) if move.move_type == 'entry' else -total
            move.amount_residual_signed = total_residual
            print("\n\n\n:::::amount_untaxed::::", move.amount_untaxed)
            print("\n\n\n:::::amount_tax::::", move.amount_tax)
            print("\n\n\n:::::move.amount_total::::", move.amount_total)
            print("\n\n\n:::::move.amount_tax_signed::::", move.amount_tax_signed)

            currency = len(
                currencies) == 1 and currencies or move.company_id.currency_id

            # Compute 'payment_state'.
            new_pmt_state = 'not_paid' if move.move_type != 'entry' else False

            if move.is_invoice(include_receipts=True) and move.state == 'posted':

                if currency.is_zero(move.amount_residual):
                    reconciled_payments = move._get_reconciled_payments()
                    if not reconciled_payments or all(payment.is_matched for payment in reconciled_payments):
                        new_pmt_state = 'paid'
                    else:
                        new_pmt_state = move._get_invoice_in_payment_state()
                elif currency.compare_amounts(total_to_pay, total_residual) != 0:
                    new_pmt_state = 'partial'

            if new_pmt_state == 'paid' and move.move_type in ('in_invoice', 'out_invoice', 'entry'):
                reverse_type = move.move_type == 'in_invoice' and 'in_refund' or move.move_type == 'out_invoice' and 'out_refund' or 'entry'
                reverse_moves = self.env['account.move'].search(
                    [('reversed_entry_id', '=', move.id), ('state', '=', 'posted'), ('move_type', '=', reverse_type)])

                # We only set 'reversed' state in cas of 1 to 1 full reconciliation with a reverse entry; otherwise, we use the regular 'paid' state
                reverse_moves_full_recs = reverse_moves.mapped(
                    'line_ids.full_reconcile_id')
                if reverse_moves_full_recs.mapped('reconciled_line_ids.move_id').filtered(lambda x: x not in (reverse_moves + reverse_moves_full_recs.mapped('exchange_move_id'))) == move:
                    new_pmt_state = 'reversed'

            move.payment_state = new_pmt_state


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    pnf_charge = fields.Float("PNF Charge")
    exe_charge = fields.Float("Extra Charge")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pnf_charge = fields.Float("PNF Charge")
    exe_charge = fields.Float("Extra Charge")

    def _prepare_invoice_line(self, **optional_values):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        :param optional_values: any parameter that should be added to the returned invoice line
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'pnf_charge': self.pnf_charge,
            'exe_charge': self.exe_charge,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
        }
        if optional_values:
            res.update(optional_values)
        if self.display_type:
            res['account_id'] = False
        return res
