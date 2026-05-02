"""
Khách hàng — usp_THEM_KHACHHANG(@MAKH,@TENKH,@SDT); usp_TICH_DIEM(@ID,@MAKH,@MAHDB); V_DIEM_KHACHHANG.
"""
from typing import Any, Dict, List, Optional, Tuple

from repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):
    def list_diem_khach_hang(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        return self.fetch_view("V_DIEM_KHACHHANG")

    def them_khach_hang(
        self,
        ma_kh: str,
        ten_kh: str,
        sdt: str,
    ) -> Tuple[bool, Optional[str], Optional[List[Dict[str, Any]]]]:
        return self.execute_procedure(
            "usp_THEM_KHACHHANG",
            (ma_kh, ten_kh, sdt),
            fetch_result=False,
        )

    def tich_diem(
        self,
        id_bien_dong: str,
        ma_kh: str,
        ma_hdb: str,
    ) -> Tuple[bool, Optional[str], Optional[List[Dict[str, Any]]]]:
        """usp_TICH_DIEM @ID, @MAKH, @MAHDB"""
        return self.execute_procedure(
            "usp_TICH_DIEM",
            (id_bien_dong, ma_kh, ma_hdb),
            fetch_result=False,
        )

    def su_dung_diem(
        self,
        id_bien_dong: str,
        ma_kh: str,
        ma_hdb: str,
    ) -> Tuple[bool, Optional[str], Optional[List[Dict[str, Any]]]]:
        """usp_SUDUNG_DIEM @ID, @MAKH, @MAHDB"""
        return self.execute_procedure(
            "usp_SUDUNG_DIEM",
            (id_bien_dong, ma_kh, ma_hdb),
            fetch_result=False,
        )
