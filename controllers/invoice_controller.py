"""
Truy vết chi tiết hóa đơn bán — V_HOADON_BAN_CHITIET.
"""
from flask import Blueprint, flash, render_template

from controllers.decorators import login_required, role_required
from services.invoice_service import InvoiceService

# Ai bán hàng / quản lý đều cần tra cứu chứng từ
INVOICE_VIEW_ROLES = frozenset({"OWNER", "ADMIN", "CASHIER", "SALE"})

invoice_bp = Blueprint("invoice", __name__)
_invoice_service = InvoiceService()


@invoice_bp.route("/invoices")
@login_required
@role_required(INVOICE_VIEW_ROLES)
def invoices():
    result = _invoice_service.list_invoice_lines()
    if not result["success"]:
        flash(result.get("message") or "Không tải được hóa đơn.", "warning")
    return render_template("invoices.html", rows=result.get("data") or [])
