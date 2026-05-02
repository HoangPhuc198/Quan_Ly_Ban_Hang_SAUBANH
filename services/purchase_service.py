"""
Nhập hàng.
"""
from typing import Any, Dict, Optional

from repositories.purchase_repository import PurchaseRepository


class PurchaseService:
    def __init__(self):
        self.repo = PurchaseRepository()

    def create_purchase(
        self,
        ma_hdn: str,
        ma_ncc: str,
        ma_nv: str,
    ) -> Dict[str, Any]:
        ma_hdn = (ma_hdn or "").strip()
        if not ma_hdn:
            return {"success": False, "message": "Mã hóa đơn nhập không được để trống.", "data": None}
        ma_nv = (ma_nv or "").strip()
        if not ma_nv:
            return {"success": False, "message": "Mã nhân viên không được để trống.", "data": None}

        ok, err, _ = self.repo.tao_hoa_don_nhap(ma_hdn, (ma_ncc or "").strip(), ma_nv)
        if not ok:
            return {"success": False, "message": err or "Không tạo được phiếu nhập.", "data": None}
        return {"success": True, "message": "Đã tạo phiếu nhập.", "data": {"ma_hdn": ma_hdn}}

    def add_item(
        self,
        ma_hdn: Optional[str],
        ma_spct: str,
        so_luong: int,
    ) -> Dict[str, Any]:
        ma_hdn = (ma_hdn or "").strip()
        ma_spct = (ma_spct or "").strip()
        if not ma_hdn:
            return {"success": False, "message": "Mã hóa đơn nhập không được để trống.", "data": None}
        if not ma_spct:
            return {"success": False, "message": "Chưa nhập mã sản phẩm chi tiết.", "data": None}
        try:
            sl = int(so_luong)
        except (TypeError, ValueError):
            return {"success": False, "message": "Số lượng không hợp lệ.", "data": None}
        if sl <= 0:
            return {"success": False, "message": "Số lượng nhập phải lớn hơn 0.", "data": None}

        ok, err, _ = self.repo.them_cthdn(ma_hdn, ma_spct, sl)
        if not ok:
            return {"success": False, "message": err or "Không thêm được chi tiết nhập.", "data": None}
        return {"success": True, "message": "Đã thêm chi tiết nhập.", "data": None}
