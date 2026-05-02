"""
Truy vết hóa đơn bán qua view.
"""
from typing import Any, Dict

from repositories.invoice_repository import InvoiceRepository


class InvoiceService:
    def __init__(self):
        self.repo = InvoiceRepository()

    def list_invoice_lines(self) -> Dict[str, Any]:
        ok, err, rows = self.repo.list_hoa_don_ban_chi_tiet()
        if not ok:
            return {"success": False, "message": err or "Không tải được dữ liệu hóa đơn.", "data": []}
        return {"success": True, "message": None, "data": rows}
