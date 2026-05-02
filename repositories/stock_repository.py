"""
Tồn kho — các View được phép.
"""
from typing import Any, Dict, List, Optional, Tuple

from repositories.base_repository import BaseRepository


class StockRepository(BaseRepository):
    def get_ton_kho(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        return self.fetch_view("V_SANPHAM_TONKHO")

    def get_sap_het(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        return self.fetch_view("V_SANPHAM_SAP_HET")

    def get_hang_ton_lau(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        return self.fetch_view("V_HANG_TON_LAU")
