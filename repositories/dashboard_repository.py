"""
Dashboard: View và procedure được phép.
"""
from typing import Any, Dict, List, Optional, Tuple

from repositories.base_repository import BaseRepository


class DashboardRepository(BaseRepository):
    def get_doanh_thu_theo_thang(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        return self.fetch_view("V_DOANH_THU_THEO_THANG")

    def get_top_san_pham(
        self,
        top_n: int = 10,
    ) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        """
        usp_TOP_SANPHAM — đối chiếu chữ ký trong SQL Server.
        - Nếu procedure không có tham số: dùng tuple ().
        - Nếu có @TopN: dùng (top_n,) và bỏ comment dòng tương ứng.
        """
        try:
            tn = int(top_n)
        except (TypeError, ValueError):
            tn = 10
        n = max(1, min(tn, self.max_rows))
        return self.fetch_procedure("usp_TOP_SANPHAM", (n,))

    def get_san_pham_sap_het(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        return self.fetch_view("V_SANPHAM_SAP_HET")

    def get_ton_kho_summary(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        """Đếm dòng tồn kho — dùng view V_SANPHAM_TONKHO."""
        return self.fetch_view("V_SANPHAM_TONKHO")

    def get_hang_ton_lau(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        return self.fetch_view("V_HANG_TON_LAU")
