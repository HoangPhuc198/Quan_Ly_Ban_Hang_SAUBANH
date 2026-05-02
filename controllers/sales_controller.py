"""
Màn hình bán hàng POS.
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from controllers.decorators import login_required, role_required, SALES_ROLES
from services.sales_service import SalesService
from services.product_service import ProductService

sales_bp = Blueprint("sales", __name__)
_sales_service = SalesService()
_product_service = ProductService()


@sales_bp.route("/sales", methods=["GET"])
@login_required
@role_required(SALES_ROLES)
def sales():
    plist = _product_service.list_products()
    products = plist.get("data") or [] if plist.get("success") else []
    if not plist.get("success"):
        flash(plist.get("message") or "Không tải được danh sách sản phẩm.", "warning")
    ma_nv = (session.get("user") or {}).get("ma_nv") or ""
    return render_template("sales.html", products=products, default_ma_nv=ma_nv)


@sales_bp.route("/sales/create-invoice", methods=["POST"])
@login_required
@role_required(SALES_ROLES)
def create_invoice():
    ma_hdb = request.form.get("ma_hdb")
    ma_nv = request.form.get("ma_nv") or (session.get("user") or {}).get("ma_nv")
    ma_kh = request.form.get("ma_kh", "")
    try:
        ck = float(request.form.get("chiet_khau") or 0)
    except ValueError:
        ck = 0.0
    result = _sales_service.create_invoice(ma_hdb, ma_nv, ma_kh, ck)
    flash(result["message"], "success" if result["success"] else "danger")
    return redirect(url_for("sales.sales"))


@sales_bp.route("/sales/add-item", methods=["POST"])
@login_required
@role_required(SALES_ROLES)
def add_item():
    ma_hdb = request.form.get("ma_hdb")
    ma_spct = request.form.get("ma_spct")
    try:
        sl = int(request.form.get("so_luong") or 0)
    except ValueError:
        sl = 0
    result = _sales_service.add_item(ma_hdb, ma_spct, sl)
    flash(result["message"], "success" if result["success"] else "danger")
    return redirect(url_for("sales.sales"))


@sales_bp.route("/sales/checkout", methods=["POST"])
@login_required
@role_required(SALES_ROLES)
def checkout():
    ma_hdb = request.form.get("ma_hdb")
    try:
        t = float(request.form.get("tien_khach_dua") or 0)
    except ValueError:
        t = 0.0
    result = _sales_service.checkout(ma_hdb, t)
    flash(result["message"], "success" if result["success"] else "danger")
    return redirect(url_for("sales.sales"))
