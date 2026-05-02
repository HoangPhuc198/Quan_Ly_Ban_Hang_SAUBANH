"""
Nhập hàng.
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from controllers.decorators import login_required, role_required, PURCHASE_ROLES
from services.purchase_service import PurchaseService

purchase_bp = Blueprint("purchase", __name__)
_purchase_service = PurchaseService()


@purchase_bp.route("/purchase", methods=["GET"])
@login_required
@role_required(PURCHASE_ROLES)
def purchase():
    ma_nv = (session.get("user") or {}).get("ma_nv") or ""
    return render_template("purchase.html", default_ma_nv=ma_nv)


@purchase_bp.route("/purchase/create", methods=["POST"])
@login_required
@role_required(PURCHASE_ROLES)
def purchase_create():
    ma_hdn = request.form.get("ma_hdn")
    ma_ncc = request.form.get("ma_ncc", "")
    ma_nv = request.form.get("ma_nv", "")
    result = _purchase_service.create_purchase(ma_hdn, ma_ncc, ma_nv)
    flash(result["message"], "success" if result["success"] else "danger")
    return redirect(url_for("purchase.purchase"))


@purchase_bp.route("/purchase/add-item", methods=["POST"])
@login_required
@role_required(PURCHASE_ROLES)
def purchase_add_item():
    ma_hdn = request.form.get("ma_hdn")
    ma_spct = request.form.get("ma_spct")
    try:
        sl = int(request.form.get("so_luong") or 0)
    except ValueError:
        sl = 0
    result = _purchase_service.add_item(ma_hdn, ma_spct, sl)
    flash(result["message"], "success" if result["success"] else "danger")
    return redirect(url_for("purchase.purchase"))
