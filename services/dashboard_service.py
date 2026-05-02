"""
Tổng hợp dữ liệu dashboard từ View và procedure.
"""
from typing import Any, Dict

from repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self):
        self.repo = DashboardRepository()

    def get_dashboard_data(self) -> Dict[str, Any]:
        try:
            return self._load_dashboard()
        except Exception:
            return {
                "success": False,
                "message": "Không tải được dữ liệu tổng quan.",
                "data": {
                    "doanh_thu_thang": [],
                    "top_san_pham": [],
                    "san_pham_sap_het": [],
                    "ton_kho_rows": [],
                    "hang_ton_lau": [],
                    "count_ton_lines": 0,
                    "count_sap_het": 0,
                    "count_ton_lau": 0,
                },
            }

    def _load_dashboard(self) -> Dict[str, Any]:
        revenue_ok, revenue_err, revenue_rows = self.repo.get_doanh_thu_theo_thang()
        top_ok, top_err, top_rows = self.repo.get_top_san_pham()
        # Nếu usp_TOP_SANPHAM không nhận tham số TopN, repository có thể lỗi — README hướng dẫn chỉnh.

        sap_ok, sap_err, sap_rows = self.repo.get_san_pham_sap_het()
        ton_ok, ton_err, ton_rows = self.repo.get_ton_kho_summary()
        lau_ok, lau_err, lau_rows = self.repo.get_hang_ton_lau()

        errors = [x for x in [revenue_err, top_err, sap_err, ton_err, lau_err] if x]

        return {
            "success": len(errors) == 0,
            "message": "; ".join(errors) if errors else None,
            "data": {
                "doanh_thu_thang": revenue_rows if revenue_ok else [],
                "top_san_pham": top_rows if top_ok else [],
                "san_pham_sap_het": sap_rows if sap_ok else [],
                "ton_kho_rows": ton_rows if ton_ok else [],
                "hang_ton_lau": lau_rows if lau_ok else [],
                "count_ton_lines": len(ton_rows) if ton_ok else 0,
                "count_sap_het": len(sap_rows) if sap_ok else 0,
                "count_ton_lau": len(lau_rows) if lau_ok else 0,
            },
        }

