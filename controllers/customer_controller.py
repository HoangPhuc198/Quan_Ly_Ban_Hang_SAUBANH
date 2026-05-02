"""
Khách hàng.
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from controllers.decorators import login_required, role_required, CUSTOMER_ROLES
from services.customer_service import CustomerService

customer_bp = Blueprint("customer", __name__)
_customer_service = CustomerService()


@customer_bp.route("/customers", methods=["GET"])
@login_required
@role_required(CUSTOMER_ROLES)
def customers():
    pts = _customer_service.list_customers_points()
    if not pts["success"]:
        flash(pts.get("message") or "Không tải được điểm khách hàng.", "warning")
    return render_template(
        "customers.html",
        customer_points=pts.get("data") or [],
    )


@customer_bp.route("/customers/create", methods=["POST"])
@login_required
@role_required(CUSTOMER_ROLES)
def customers_create():
    result = _customer_service.create_customer(
        request.form.get("ma_kh", ""),
        request.form.get("ten_kh", ""),
        request.form.get("sdt", ""),
    )
    flash(result["message"], "success" if result["success"] else "danger")
    return redirect(url_for("customer.customers"))


@customer_bp.route("/customers/tich-diem", methods=["POST"])
@login_required
@role_required(CUSTOMER_ROLES)
def customers_tich_diem():
    result = _customer_service.tich_diem(
        request.form.get("id_bd", ""),
        request.form.get("ma_kh", ""),
        request.form.get("ma_hdb", ""),
    )
    flash(result["message"], "success" if result["success"] else "danger")
    return redirect(url_for("customer.customers"))


@customer_bp.route("/customers/su-dung-diem", methods=["POST"])
@login_required
@role_required(CUSTOMER_ROLES)
def customers_su_dung_diem():
    result = _customer_service.su_dung_diem(
        request.form.get("id_bd", ""),
        request.form.get("ma_kh", ""),
        request.form.get("ma_hdb", ""),
    )
    flash(result["message"], "success" if result["success"] else "danger")
    return redirect(url_for("customer.customers"))
