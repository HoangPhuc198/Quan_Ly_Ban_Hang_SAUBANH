"""
Đăng nhập / phiên — xử lý kết quả usp_DANG_NHAP (username, role, full_name / TEN_NV).
"""
from typing import Any, Dict, List, Optional

from repositories.auth_repository import AuthRepository


def _get_col(row: Dict[str, Any], *candidates: str) -> Optional[Any]:
    """Lấy giá trị cột bất kể hoa thường tên cột."""
    lower_map = {k.lower(): v for k, v in row.items()}
    for c in candidates:
        if c.lower() in lower_map:
            return lower_map[c.lower()]
    return None


def _normalize_role(raw: Optional[str]) -> str:
    if not raw:
        return "SALE"
    r = str(raw).strip().upper().replace(" ", "_")
    aliases = {
        "QUẢN_LÝ": "ADMIN",
        "QUAN_LY": "ADMIN",
        "CHỦ": "OWNER",
        "CHU": "OWNER",
        "THU_NGÂN": "CASHIER",
        "THU_NGAN": "CASHIER",
        "BÁN_HÀNG": "SALE",
        "BAN_HANG": "SALE",
        "KHO": "WAREHOUSE",
        "NHÂN_VIÊN_KHO": "WAREHOUSE",
        "ADMIN_ROLE": "ADMIN",
        "ADMIN": "ADMIN",
        "BANHANG_ROLE": "SALE",
        "BANHANG": "SALE",
        "KHO_ROLE": "WAREHOUSE",
        "SELLER": "SALE",
        "CASHIER": "CASHIER",
    }
    if r in aliases:
        return aliases[r]
    return r if r in (
        "OWNER", "ADMIN", "CASHIER", "SALE", "WAREHOUSE"
    ) else "SALE"


def _row_indicates_login_failure(row: Dict[str, Any]) -> bool:
    """Heuristic: cột thông báo lỗi / không thành công từ procedure."""
    for key in row.keys():
        lk = key.lower()
        if lk in ("success", "thanhcong", "ok", "ketqua"):
            val = row[key]
            if val in (0, "0", False, "false", "FAIL", "fail"):
                return True
        if lk in ("loi", "error", "errormessage") and row[key]:
            return True
    return False


class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def login(self, username: str, password: str) -> Dict[str, Any]:
        if not username or not password:
            return {"success": False, "message": "Nhập đủ tên đăng nhập và mật khẩu.", "data": None}

        ok, err, rows = self.repo.dang_nhap(username.strip(), password)
        if not ok:
            return {"success": False, "message": err or "Đăng nhập thất bại.", "data": None}

        if not rows:
            return {"success": False, "message": "Sai tên đăng nhập hoặc mật khẩu.", "data": None}

        first = rows[0]
        if _row_indicates_login_failure(first):
            return {"success": False, "message": "Sai tên đăng nhập hoặc mật khẩu.", "data": None}

        role_raw = _get_col(first, "role", "ROLE_NAME", "ChucVu", "VaiTro", "Role")
        user_payload = {
            "username": _get_col(first, "username", "USERNAME") or username.strip(),
            "ma_nv": _get_col(first, "MANV", "MaNV"),
            "ten": _get_col(first, "full_name", "TEN_NV", "TenNV", "Ten", "HoTen"),
            "raw": first,
            "role": _normalize_role(str(role_raw) if role_raw else "SALE"),
        }

        return {"success": True, "message": "Đăng nhập thành công.", "data": user_payload}
