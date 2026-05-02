"""
Trang tĩnh mô tả liên kết View — Procedure — Trigger (khối nghiệp vụ thống nhất).
"""
from flask import Blueprint

from controllers.decorators import login_required

system_bp = Blueprint("system", __name__)


@system_bp.route("/he-thong-du-lieu")
@login_required
def system_map():
    # Mục "Sơ đồ CSDL" đã được gỡ khỏi UI theo yêu cầu báo cáo.
    # Giữ route để tránh lỗi 404 nếu còn link cũ trong bookmark.
    from flask import redirect, url_for

    return redirect(url_for("dashboard.dashboard"))
