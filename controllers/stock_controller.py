"""
Tồn kho.
"""
from flask import Blueprint, flash, render_template

from controllers.decorators import login_required, role_required, STOCK_ROLES
from services.stock_service import StockService

stock_bp = Blueprint("stock", __name__)
_stock_service = StockService()


@stock_bp.route("/stock")
@login_required
@role_required(STOCK_ROLES)
def stock():
    result = _stock_service.get_all_tabs()
    if not result["success"] and result.get("message"):
        flash(result["message"], "warning")
    data = result.get("data") or {}
    return render_template(
        "stock.html",
        ton_kho=data.get("ton_kho") or [],
        sap_het=data.get("sap_het") or [],
        hang_ton_lau=data.get("hang_ton_lau") or [],
    )
