"""
Sản phẩm — V_SANPHAM_TONKHO + V_GIA_HIEN_TAI (hợp nhất ở service).
View V_GIA_HIEN_TAI trong bài lọc từ BANGGIA theo NGAY_BAT_DAU / NGAY_KET_THUC
(giống chương 3), đồng bộ với trigger TRG_CHECK_GIA.
"""
from typing import Any, Dict, List, Optional, Tuple

from repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository):
    def get_ton_kho_chi_tiet(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        """V_SANPHAM_TONKHO — MASPCT, MASP, TENSP, TEN_MAU, TEN_SIZE, SL_TONKHO."""
        return self.fetch_view("V_SANPHAM_TONKHO")

    def get_gia_hien_tai(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        """V_GIA_HIEN_TAI — đơn giá đang hiệu lực (từ BANGGIA, điều kiện ngày trong view)."""
        return self.fetch_view("V_GIA_HIEN_TAI")
