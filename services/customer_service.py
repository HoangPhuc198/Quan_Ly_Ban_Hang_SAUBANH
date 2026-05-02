"""
Khách hàng — thêm KH, tích điểm, sử dụng điểm; đọc V_DIEM_KHACHHANG.
"""
import re
from typing import Any, Dict

from repositories.customer_repository import CustomerRepository


class CustomerService:
    def __init__(self):
        self.repo = CustomerRepository()

    def list_customers_points(self) -> Dict[str, Any]:
        ok, err, rows = self.repo.list_diem_khach_hang()
        if not ok:
            return {"success": False, "message": err or "Không tải được danh sách điểm.", "data": []}
        return {"success": True, "message": None, "data": rows}

    def create_customer(
        self,
        ma_kh: str,
        ten_kh: str,
        sdt: str,
    ) -> Dict[str, Any]:
        ma_kh = (ma_kh or "").strip()
        ten = (ten_kh or "").strip()
        sdt = (sdt or "").strip()

        if not ma_kh:
            return {"success": False, "message": "Mã khách hàng không được để trống.", "data": None}
        if not ten:
            return {"success": False, "message": "Tên khách hàng không được để trống.", "data": None}
        if not re.fullmatch(r"0\d{9}", sdt):
            return {
                "success": False,
                "message": "Số điện thoại phải có 10 chữ số và bắt đầu bằng 0.",
                "data": None,
            }

        ok, err, _ = self.repo.them_khach_hang(ma_kh, ten, sdt)
        if not ok:
            return {"success": False, "message": err or "Không thêm được khách hàng.", "data": None}
        return {"success": True, "message": "Đã thêm khách hàng.", "data": None}

    def tich_diem(self, id_bd: str, ma_kh: str, ma_hdb: str) -> Dict[str, Any]:
        id_bd = (id_bd or "").strip()
        ma_kh = (ma_kh or "").strip()
        ma_hdb = (ma_hdb or "").strip()
        if not id_bd or not ma_kh or not ma_hdb:
            return {"success": False, "message": "Nhập đủ mã biến động, mã khách và mã hóa đơn.", "data": None}

        ok, err, _ = self.repo.tich_diem(id_bd, ma_kh, ma_hdb)
        if not ok:
            return {"success": False, "message": err or "Không ghi nhận tích điểm.", "data": None}
        return {"success": True, "message": "Đã xử lý tích điểm (nếu đủ điều kiện nghiệp vụ).", "data": None}

    def su_dung_diem(self, id_bd: str, ma_kh: str, ma_hdb: str) -> Dict[str, Any]:
        id_bd = (id_bd or "").strip()
        ma_kh = (ma_kh or "").strip()
        ma_hdb = (ma_hdb or "").strip()
        if not id_bd or not ma_kh or not ma_hdb:
            return {"success": False, "message": "Nhập đủ mã biến động, mã khách và mã hóa đơn.", "data": None}

        ok, err, _ = self.repo.su_dung_diem(id_bd, ma_kh, ma_hdb)
        if not ok:
            return {"success": False, "message": err or "Không áp dụng được đổi điểm.", "data": None}
        return {"success": True, "message": "Đã áp dụng sử dụng điểm (nếu đủ điều kiện).", "data": None}
