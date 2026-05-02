"""
Luồng bán hàng: tạo HĐ — thêm chi tiết (procedure tự kiểm tồn/UPDLOCK) — thanh toán.
"""
from typing import Any, Dict, Optional

from repositories.sales_repository import SalesRepository


class SalesService:
    def __init__(self):
        self.repo = SalesRepository()

    def create_invoice(
        self,
        ma_hdb: str,
        ma_nv: str,
        ma_kh: str,
        chiet_khau: float,
    ) -> Dict[str, Any]:
        ma_hdb = (ma_hdb or "").strip()
        if not ma_hdb:
            return {"success": False, "message": "Mã hóa đơn không được để trống.", "data": None}
        ma_nv = (ma_nv or "").strip()
        if not ma_nv:
            return {"success": False, "message": "Mã nhân viên không được để trống.", "data": None}
        mk = (ma_kh or "").strip()
        makh_sql = None if not mk else mk
        ck = float(chiet_khau or 0)
        if ck < 0:
            return {"success": False, "message": "Chiết khấu không hợp lệ.", "data": None}

        ok, err, _ = self.repo.tao_hoa_don_ban(ma_hdb, makh_sql, ma_nv, ck)
        if not ok:
            return {"success": False, "message": err or "Không tạo được hóa đơn.", "data": None}
        return {"success": True, "message": "Đã tạo hóa đơn.", "data": {"ma_hdb": ma_hdb}}

    def add_item(
        self,
        ma_hdb: Optional[str],
        ma_spct: str,
        so_luong: int,
    ) -> Dict[str, Any]:
        ma_hdb = (ma_hdb or "").strip()
        ma_spct = (ma_spct or "").strip()
        if not ma_hdb:
            return {"success": False, "message": "Chưa có mã hóa đơn — hãy tạo hóa đơn trước.", "data": None}
        if not ma_spct:
            return {"success": False, "message": "Chưa nhập mã sản phẩm chi tiết.", "data": None}
        try:
            sl = int(so_luong)
        except (TypeError, ValueError):
            return {"success": False, "message": "Số lượng không hợp lệ.", "data": None}
        if sl <= 0:
            return {"success": False, "message": "Số lượng phải lớn hơn 0.", "data": None}

        ok, err, _ = self.repo.them_cthdb(ma_hdb, ma_spct, sl)
        if not ok:
            return {
                "success": False,
                "message": err or "Không thêm được vào hóa đơn (kiểm tra tồn kho / giá).",
                "data": None,
            }
        return {"success": True, "message": "Đã thêm sản phẩm vào hóa đơn.", "data": None}

    def checkout(self, ma_hdb: Optional[str], tien_khach_dua: float) -> Dict[str, Any]:
        ma_hdb = (ma_hdb or "").strip()
        if not ma_hdb:
            return {"success": False, "message": "Chưa có mã hóa đơn.", "data": None}
        try:
            t = float(tien_khach_dua)
        except (TypeError, ValueError):
            return {"success": False, "message": "Số tiền không hợp lệ.", "data": None}
        if t <= 0:
            return {"success": False, "message": "Tiền khách đưa phải lớn hơn 0.", "data": None}

        ok, err, _ = self.repo.thanh_toan_hoa_don_ban(ma_hdb, t)
        if not ok:
            return {"success": False, "message": err or "Thanh toán thất bại.", "data": None}
        return {"success": True, "message": "Thanh toán thành công.", "data": None}
