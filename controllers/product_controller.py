"""
Sản phẩm — danh sách bán.
"""
from flask import Blueprint, flash, render_template

from controllers.decorators import login_required, role_required, PRODUCT_VIEW_ROLES
from services.product_service import ProductService

product_bp = Blueprint("product", __name__)
_product_service = ProductService()


@product_bp.route("/products")
@login_required
@role_required(PRODUCT_VIEW_ROLES)
def products():
    result = _product_service.list_products()
    if not result["success"]:
        flash(result.get("message") or "Không tải được sản phẩm.", "danger")
    return render_template("products.html", products=result.get("data") or [])
