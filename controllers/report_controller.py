"""
Báo cáo — chỉ Owner/Admin.
"""
from flask import Blueprint, flash, render_template

from controllers.decorators import login_required, role_required, REPORT_FINANCE_ROLES
from services.report_service import ReportService

report_bp = Blueprint("report", __name__)
_report_service = ReportService()


@report_bp.route("/reports")
@login_required
@role_required(REPORT_FINANCE_ROLES)
def reports():
    result = _report_service.get_report_bundle()
    if not result["success"] and result.get("message"):
        flash(result["message"], "warning")
    return render_template("reports.html", report=result.get("data") or {})
