"""
Hóa đơn bán — V_HOADON_BAN_CHITIET (truy vết, không SELECT trực tiếp bảng).
"""
from typing import Any, Dict, List, Optional, Tuple

from repositories.base_repository import BaseRepository


class InvoiceRepository(BaseRepository):
    def list_hoa_don_ban_chi_tiet(self) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        return self.fetch_view("V_HOADON_BAN_CHITIET")
