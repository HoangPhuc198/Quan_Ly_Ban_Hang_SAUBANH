"""
Nhập hàng — usp_TAO_HOADON_NHAP(@MAHDN,@MA_NCC,@MANV); usp_THEM_CTHDN.
"""
from typing import Any, Dict, List, Optional, Tuple

from repositories.base_repository import BaseRepository


class PurchaseRepository(BaseRepository):
    def tao_hoa_don_nhap(
        self,
        ma_hdn: str,
        ma_ncc: str,
        ma_nv: str,
    ) -> Tuple[bool, Optional[str], Optional[List[Dict[str, Any]]]]:
        return self.execute_procedure(
            "usp_TAO_HOADON_NHAP",
            (ma_hdn, ma_ncc, ma_nv),
            fetch_result=False,
        )

    def them_cthdn(
        self,
        ma_hdn: str,
        ma_spct: str,
        so_luong: int,
    ) -> Tuple[bool, Optional[str], Optional[List[Dict[str, Any]]]]:
        return self.execute_procedure(
            "usp_THEM_CTHDN",
            (ma_hdn, ma_spct, so_luong),
            fetch_result=False,
        )
