"""
Báo cáo — view + usp_TOP_SANPHAM + usp_BAOCAO_CONGNO.
"""
from typing import Any, Dict, List, Optional, Tuple

from repositories.base_repository import BaseRepository


class ReportRepository(BaseRepository):
    def get_doanh_thu_theo_thang(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        return self.fetch_view("V_DOANH_THU_THEO_THANG")

    def get_top_san_pham(self, top_n: int = 10) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        try:
            tn = int(top_n)
        except (TypeError, ValueError):
            tn = 10
        n = max(1, min(tn, self.max_rows))
        return self.fetch_procedure("usp_TOP_SANPHAM", (n,))

    def get_sap_het(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        return self.fetch_view("V_SANPHAM_SAP_HET")

    def get_hang_ton_lau(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        return self.fetch_view("V_HANG_TON_LAU")

    def get_bao_cao_cong_no(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        """usp_BAOCAO_CONGNO — danh sách công nợ hóa đơn (CON_NO > 0)."""
        return self.fetch_procedure("usp_BAOCAO_CONGNO", ())
