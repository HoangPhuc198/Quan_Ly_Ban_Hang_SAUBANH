"""
Dashboard — chủ cửa hàng / quản lý (mọi role đăng nhập đều vào được; số liệu nhạy cảm ẩn theo role trong template).
"""
from flask import Blueprint, flash, redirect, render_template, session, url_for

from controllers.decorators import login_required
from services.dashboard_service import DashboardService

dashboard_bp = Blueprint("dashboard", __name__)
_dashboard_service = DashboardService()


@dashboard_bp.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("auth.login"))
    return redirect(url_for("dashboard.dashboard"))


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    result = _dashboard_service.get_dashboard_data()
    if not result["success"] and result.get("message"):
        flash(result["message"], "warning")
    data = result.get("data") or {}
    role = (session.get("role") or "").upper()
    show_finance = role in ("OWNER", "ADMIN")
    return render_template(
        "dashboard.html",
        dashboard=data,
        show_finance_charts=show_finance,
    )
