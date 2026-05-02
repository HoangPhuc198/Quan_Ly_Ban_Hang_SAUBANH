"""
Tồn kho — đọc view.
"""
from typing import Any, Dict

from repositories.stock_repository import StockRepository


class StockService:
    def __init__(self):
        self.repo = StockRepository()

    def get_all_tabs(self) -> Dict[str, Any]:
        t_ok, t_err, ton = self.repo.get_ton_kho()
        s_ok, s_err, sap = self.repo.get_sap_het()
        l_ok, l_err, lau = self.repo.get_hang_ton_lau()
        errs = [e for e in (t_err, s_err, l_err) if e]
        return {
            "success": len(errs) == 0,
            "message": "; ".join(errs) if errs else None,
            "data": {
                "ton_kho": ton if t_ok else [],
                "sap_het": sap if s_ok else [],
                "hang_ton_lau": lau if l_ok else [],
            },
        }
