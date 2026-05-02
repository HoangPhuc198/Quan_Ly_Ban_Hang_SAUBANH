"""
Bán hàng — procedure đúng chữ ký: usp_TAO_HOADON_BAN(@MAHDB,@MAKH,@MANV,@CHIETKHAU), usp_THEM_CTHDB, usp_THANH_TOAN_HOADON_BAN.
Kiểm tra tồn kho được xử lý trong usp_THEM_CTHDB (UPDLOCK + logic kho).
"""
from typing import Any, Dict, List, Optional, Tuple

from repositories.base_repository import BaseRepository


class SalesRepository(BaseRepository):
    def tao_hoa_don_ban(
        self,
        ma_hdb: str,
        ma_kh: Optional[str],
        ma_nv: str,
        chiet_khau: float,
    ) -> Tuple[bool, Optional[str], Optional[List[Dict[str, Any]]]]:
        """
        usp_TAO_HOADON_BAN @MAHDB, @MAKH, @MANV, @CHIETKHAU
        Khách vãng lai: @MAKH = NULL (truyền None).
        """
        return self.execute_procedure(
            "usp_TAO_HOADON_BAN",
            (ma_hdb, ma_kh, ma_nv, chiet_khau),
            fetch_result=False,
        )

    def them_cthdb(
        self,
        ma_hdb: str,
        ma_spct: str,
        so_luong: int,
    ) -> Tuple[bool, Optional[str], Optional[List[Dict[str, Any]]]]:
        """usp_THEM_CTHDB @MAHDB, @MASPCT, @SOLUONG"""
        return self.execute_procedure(
            "usp_THEM_CTHDB",
            (ma_hdb, ma_spct, so_luong),
            fetch_result=False,
        )

    def thanh_toan_hoa_don_ban(
        self, ma_hdb: str, tien_khach_dua: float
    ) -> Tuple[bool, Optional[str], Optional[List[Dict[str, Any]]]]:
        """usp_THANH_TOAN_HOADON_BAN @MAHDB, @TIENKHACHDUA"""
        return self.execute_procedure(
            "usp_THANH_TOAN_HOADON_BAN",
            (ma_hdb, tien_khach_dua),
            fetch_result=False,
        )
