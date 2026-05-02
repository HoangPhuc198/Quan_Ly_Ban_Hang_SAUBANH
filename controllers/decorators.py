"""
Decorators: đăng nhập và phân quyền theo vai trò (session).
"""
from functools import wraps
from typing import Callable, FrozenSet, Iterable, Union

from flask import flash, redirect, session, url_for


def login_required(f: Callable) -> Callable:
    """Yêu cầu đã đăng nhập (session có user)."""

    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user"):
            flash("Vui lòng đăng nhập.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


# Nhóm quyền — so khớp không phân biệt hoa thường
RoleStr = str

FULL_ADMIN_ROLES: FrozenSet[str] = frozenset({"OWNER", "ADMIN"})
SALES_ROLES: FrozenSet[str] = frozenset({"OWNER", "ADMIN", "CASHIER", "SALE"})
PURCHASE_ROLES: FrozenSet[str] = frozenset({"OWNER", "ADMIN", "WAREHOUSE"})
STOCK_ROLES: FrozenSet[str] = frozenset({"OWNER", "ADMIN", "WAREHOUSE", "CASHIER", "SALE"})
PRODUCT_VIEW_ROLES: FrozenSet[str] = frozenset(
    {"OWNER", "ADMIN", "CASHIER", "SALE", "WAREHOUSE"}
)
CUSTOMER_ROLES: FrozenSet[str] = frozenset({"OWNER", "ADMIN", "CASHIER", "SALE"})
REPORT_FINANCE_ROLES: FrozenSet[str] = frozenset({"OWNER", "ADMIN"})


def _current_role() -> str:
    return (session.get("role") or "").upper()


def role_required(
    allowed: Union[Iterable[str], FrozenSet[str]],
    *,
    redirect_endpoint: str = "dashboard.dashboard",
) -> Callable:
    """
    Chỉ cho phép các role trong allowed (không phân biệt hoa thường).
    Nếu không đủ quyền: flash + redirect.
    """

    allowed_set = frozenset(x.upper() for x in allowed)

    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not session.get("user"):
                flash("Vui lòng đăng nhập.", "warning")
                return redirect(url_for("auth.login"))
            role = _current_role()
            if role not in allowed_set:
                flash("Bạn không có quyền truy cập chức năng này.", "danger")
                return redirect(url_for(redirect_endpoint))
            return f(*args, **kwargs)

        return wrapped

    return decorator
