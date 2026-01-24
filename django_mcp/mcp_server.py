#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Odoo MCP Server
===============

Model Context Protocol server for complete Odoo ERP access.
Allows AI agents to interact with Odoo via standardized MCP tools.
"""
import json
import sys
import os
from typing import Any, Dict, List, Optional

# Add django_mcp to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from services.odoo_client import OdooClient

odoo = OdooClient()


def handle_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Route tool calls to appropriate handlers."""

    handlers = {
        # Universal CRUD
        'odoo_search': handle_odoo_search,
        'odoo_create': handle_odoo_create,
        'odoo_write': handle_odoo_write,
        'odoo_delete': handle_odoo_delete,
        'odoo_execute': handle_odoo_execute,
        'odoo_inspect': handle_odoo_inspect,

        # SRI Ecuador
        'sri_sign_invoice': handle_sri_sign,
        'sri_check_authorization': handle_sri_check,
        'sri_consult_ruc': handle_sri_ruc,

        # Ecuador-specific
        'ecuador_onboarding': handle_ecuador_onboarding,
        'create_withholding': handle_create_withholding,
        'get_tax_deadlines': handle_tax_deadlines,
        'get_payroll_rates': handle_payroll_rates,
        'create_payslip': handle_create_payslip,

        # Core business
        'create_invoice': handle_create_invoice,
        'post_invoice': handle_post_invoice,
        'create_partner': handle_create_partner,
        'search_partner': handle_search_partner,
        'create_sale_order': handle_create_sale_order,
        'confirm_sale_order': handle_confirm_sale_order,
        'create_purchase_order': handle_create_purchase_order,
        'get_stock_levels': handle_stock_levels,
        'validate_picking': handle_validate_picking,
        'create_payment': handle_create_payment,

        # HR & Project
        'get_employees': handle_get_employees,
        'create_crm_lead': handle_create_lead,
        'create_project_task': handle_create_task,
        'log_timesheet': handle_log_timesheet,

        # Config
        'get_config': handle_get_config,
        'set_config': handle_set_config,
    }

    handler = handlers.get(tool_name)
    if not handler:
        return {"error": f"Unknown tool: {tool_name}"}

    try:
        return handler(arguments)
    except Exception as e:
        return {"error": str(e)}


# =============================================================================
# UNIVERSAL CRUD HANDLERS
# =============================================================================

def handle_odoo_search(args: Dict) -> Any:
    return odoo.execute_kw(
        args['model'],
        'search_read',
        [args.get('domain', [])],
        {
            'fields': args.get('fields'),
            'limit': args.get('limit', 80),
            'offset': args.get('offset', 0),
        }
    )


def handle_odoo_create(args: Dict) -> Dict:
    record_id = odoo.execute_kw(args['model'], 'create', [args['values']])
    return {"id": record_id}


def handle_odoo_write(args: Dict) -> Dict:
    odoo.execute_kw(args['model'], 'write', [args['ids'], args['values']])
    return {"status": "updated", "ids": args['ids']}


def handle_odoo_delete(args: Dict) -> Dict:
    odoo.execute_kw(args['model'], 'unlink', [args['ids']])
    return {"status": "deleted", "ids": args['ids']}


def handle_odoo_execute(args: Dict) -> Any:
    call_args = [args['ids']] + args.get('args', [])
    return odoo.execute_kw(
        args['model'],
        args['method'],
        call_args,
        args.get('kwargs', {})
    )


def handle_odoo_inspect(args: Dict) -> Any:
    return odoo.execute_kw(
        args['model'],
        'fields_get',
        [],
        {'attributes': ['string', 'help', 'type', 'selection', 'required']}
    )


# =============================================================================
# SRI ECUADOR HANDLERS
# =============================================================================

def handle_sri_sign(args: Dict) -> Any:
    odoo.execute_kw('account.move', 'action_send_sri', [[args['invoice_id']]])
    return odoo.execute_kw(
        'account.move',
        'search_read',
        [[['id', '=', args['invoice_id']]]],
        {'fields': ['l10n_ec_sri_status', 'l10n_ec_sri_access_key', 'l10n_ec_sri_error']}
    )[0]


def handle_sri_check(args: Dict) -> Any:
    odoo.execute_kw('account.move', 'action_check_sri', [[args['invoice_id']]])
    return odoo.execute_kw(
        'account.move',
        'search_read',
        [[['id', '=', args['invoice_id']]]],
        {'fields': ['l10n_ec_sri_status', 'l10n_ec_authorization_date']}
    )[0]


def handle_sri_ruc(args: Dict) -> Any:
    return odoo.execute_kw('l10n_ec.sri.ruc.service', 'consult_ruc', [args['ruc']])


# =============================================================================
# ECUADOR HANDLERS
# =============================================================================

def handle_ecuador_onboarding(args: Dict) -> Dict:
    """Super simple onboarding - just RUC."""
    ruc = args['ruc']

    # 1. Consult SRI
    sri_data = odoo.execute_kw('l10n_ec.sri.ruc.service', 'consult_ruc', [ruc])
    if not sri_data or sri_data.get('error'):
        return {"error": "RUC no encontrado en SRI", "ruc": ruc}

    # 2. Update company
    company_id = odoo.execute_kw('res.company', 'search', [[]], {'limit': 1})[0]
    odoo.execute_kw('res.company', 'write', [[company_id], {
        'name': sri_data.get('razonSocial', ''),
        'vat': ruc,
        'street': sri_data.get('direccionMatriz', ''),
        'l10n_ec_special_contributor': sri_data.get('contribuyenteEspecial') == 'SI',
        'l10n_ec_retention_agent': sri_data.get('agenteRetencion') == 'SI',
        'l10n_ec_obligated_accounting': sri_data.get('obligadoContabilidad') == 'SI',
    }])

    return {"status": "success", "company_id": company_id, "sri_data": sri_data}


def handle_create_withholding(args: Dict) -> Dict:
    invoice = odoo.execute_kw(
        'account.move', 'search_read',
        [[['id', '=', args['invoice_id']]]],
        {'fields': ['partner_id', 'amount_untaxed', 'amount_tax']}
    )[0]

    lines = []
    if args.get('ir_tax_id'):
        lines.append((0, 0, {'tax_id': args['ir_tax_id'], 'base': invoice['amount_untaxed']}))
    if args.get('iva_tax_id'):
        lines.append((0, 0, {'tax_id': args['iva_tax_id'], 'base': invoice['amount_tax']}))

    ret_id = odoo.execute_kw('l10n_ec.withholding', 'create', [{
        'partner_id': invoice['partner_id'][0],
        'invoice_id': args['invoice_id'],
        'line_ids': lines,
    }])
    return {"withholding_id": ret_id}


def handle_tax_deadlines(args: Dict) -> Any:
    return odoo.execute_kw('l10n_ec.tax.calendar', 'get_upcoming_deadlines', [args.get('days_ahead', 30)])


def handle_payroll_rates(args: Dict) -> Dict:
    def get_param(key, default):
        return odoo.execute_kw('ir.config_parameter', 'get_param', [key]) or default

    return {
        "sbu": float(get_param('l10n_ec.sbu', '482')),
        "iess_personal": float(get_param('l10n_ec.iess_aporte_personal', '9.45')),
        "iess_employer": float(get_param('l10n_ec.iess_aporte_patronal', '12.15')),
    }


def handle_create_payslip(args: Dict) -> Dict:
    payslip_id = odoo.execute_kw('l10n_ec.payslip', 'create', [{
        'employee_id': args['employee_id'],
        'date_start': args['date_start'],
        'date_end': args['date_end'],
    }])
    return {"payslip_id": payslip_id}


# =============================================================================
# CORE BUSINESS HANDLERS
# =============================================================================

def handle_create_invoice(args: Dict) -> Dict:
    lines = [(0, 0, {
        'product_id': l.get('product_id'),
        'quantity': l.get('quantity', 1),
        'price_unit': l.get('price_unit', 0),
    }) for l in args['lines']]

    invoice_id = odoo.execute_kw('account.move', 'create', [{
        'move_type': 'out_invoice',
        'partner_id': args['partner_id'],
        'invoice_line_ids': lines,
    }])
    return {"invoice_id": invoice_id}


def handle_post_invoice(args: Dict) -> Any:
    odoo.execute_kw('account.move', 'action_post', [[args['invoice_id']]])
    return odoo.execute_kw(
        'account.move', 'search_read',
        [[['id', '=', args['invoice_id']]]],
        {'fields': ['name', 'state', 'l10n_ec_sri_status', 'l10n_ec_sri_access_key']}
    )[0]


def handle_create_partner(args: Dict) -> Dict:
    vals = {'is_company': args.get('is_company', True)}

    if args.get('ruc') and len(args['ruc']) == 13:
        sri_data = odoo.execute_kw('l10n_ec.sri.ruc.service', 'consult_ruc', [args['ruc']])
        if sri_data and not sri_data.get('error'):
            vals.update({
                'name': sri_data.get('razonSocial', args.get('name', '')),
                'vat': args['ruc'],
                'street': sri_data.get('direccionMatriz', ''),
                'l10n_ec_identifier_type': 'ruc',
            })
    else:
        vals['name'] = args.get('name', 'Cliente')
        if args.get('ruc'):
            vals['vat'] = args['ruc']

    if args.get('email'):
        vals['email'] = args['email']
    if args.get('phone'):
        vals['phone'] = args['phone']

    partner_id = odoo.execute_kw('res.partner', 'create', [vals])
    return {"partner_id": partner_id, "name": vals.get('name')}


def handle_search_partner(args: Dict) -> Any:
    domain = ['|', '|',
        ('vat', 'ilike', args['query']),
        ('name', 'ilike', args['query']),
        ('ref', 'ilike', args['query'])
    ]
    return odoo.execute_kw('res.partner', 'search_read', [domain],
                          {'fields': ['id', 'name', 'vat', 'email'], 'limit': 10})


def handle_create_sale_order(args: Dict) -> Dict:
    lines = [(0, 0, {
        'product_id': l.get('product_id'),
        'product_uom_qty': l.get('quantity', 1),
        'price_unit': l.get('price_unit'),
    }) for l in args['lines']]

    order_id = odoo.execute_kw('sale.order', 'create', [{
        'partner_id': args['partner_id'],
        'order_line': lines,
    }])
    return {"order_id": order_id}


def handle_confirm_sale_order(args: Dict) -> Dict:
    odoo.execute_kw('sale.order', 'action_confirm', [[args['order_id']]])
    return {"status": "confirmed", "order_id": args['order_id']}


def handle_create_purchase_order(args: Dict) -> Dict:
    lines = [(0, 0, l) for l in args['lines']]
    order_id = odoo.execute_kw('purchase.order', 'create', [{
        'partner_id': args['partner_id'],
        'order_line': lines,
    }])
    return {"order_id": order_id}


def handle_stock_levels(args: Dict) -> Any:
    return odoo.execute_kw('stock.quant', 'search_read',
                          [[['product_id', '=', args['product_id']]]],
                          {'fields': ['location_id', 'quantity', 'available_quantity']})


def handle_validate_picking(args: Dict) -> Dict:
    odoo.execute_kw('stock.picking', 'button_validate', [[args['picking_id']]])
    return {"status": "validated", "picking_id": args['picking_id']}


def handle_create_payment(args: Dict) -> Dict:
    payment_id = odoo.execute_kw('account.payment', 'create', [{
        'partner_id': args['partner_id'],
        'amount': args['amount'],
        'journal_id': args['journal_id'],
        'payment_type': args.get('payment_type', 'inbound'),
    }])
    return {"payment_id": payment_id}


# =============================================================================
# HR & PROJECT HANDLERS
# =============================================================================

def handle_get_employees(args: Dict) -> Any:
    return odoo.execute_kw('hr.employee', 'search_read', [[]],
                          {'fields': ['id', 'name', 'job_title', 'department_id'], 'limit': 100})


def handle_create_lead(args: Dict) -> Dict:
    lead_id = odoo.execute_kw('crm.lead', 'create', [{
        'name': args['name'],
        'email_from': args.get('email_from'),
        'phone': args.get('phone'),
        'expected_revenue': args.get('expected_revenue', 0),
    }])
    return {"lead_id": lead_id}


def handle_create_task(args: Dict) -> Dict:
    task_id = odoo.execute_kw('project.task', 'create', [{
        'name': args['name'],
        'project_id': args['project_id'],
        'user_ids': [(6, 0, args.get('user_ids', []))],
        'date_deadline': args.get('date_deadline'),
    }])
    return {"task_id": task_id}


def handle_log_timesheet(args: Dict) -> Dict:
    line_id = odoo.execute_kw('account.analytic.line', 'create', [{
        'project_id': args['project_id'],
        'task_id': args['task_id'],
        'unit_amount': args['hours'],
        'name': args['description'],
    }])
    return {"timesheet_id": line_id}


# =============================================================================
# CONFIG HANDLERS
# =============================================================================

def handle_get_config(args: Dict) -> Dict:
    params = odoo.execute_kw('ir.config_parameter', 'search_read',
                            [[['key', 'like', 'l10n_ec.%']]],
                            {'fields': ['key', 'value']})
    return {p['key']: p['value'] for p in params}


def handle_set_config(args: Dict) -> Dict:
    odoo.execute_kw('ir.config_parameter', 'set_param', [args['key'], args['value']])
    return {"status": "success", "key": args['key'], "value": args['value']}


# =============================================================================
# MCP PROTOCOL IMPLEMENTATION
# =============================================================================

def read_message() -> Optional[Dict]:
    """Read JSON-RPC message from stdin."""
    line = sys.stdin.readline()
    if not line:
        return None
    return json.loads(line)


def write_message(msg: Dict) -> None:
    """Write JSON-RPC message to stdout."""
    sys.stdout.write(json.dumps(msg) + '\n')
    sys.stdout.flush()


def handle_request(request: Dict) -> Dict:
    """Handle incoming MCP request."""
    method = request.get('method', '')
    params = request.get('params', {})
    req_id = request.get('id')

    if method == 'initialize':
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "odoo-erp-mcp", "version": "1.0.0"}
            }
        }

    elif method == 'tools/list':
        with open('mcp.json', 'r') as f:
            manifest = json.load(f)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": manifest.get('tools', [])}
        }

    elif method == 'tools/call':
        tool_name = params.get('name')
        arguments = params.get('arguments', {})
        result = handle_tool_call(tool_name, arguments)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
        }

    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"}
        }


def main():
    """Main MCP server loop."""
    while True:
        try:
            request = read_message()
            if request is None:
                break
            response = handle_request(request)
            write_message(response)
        except Exception as e:
            write_message({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            })


if __name__ == '__main__':
    main()
