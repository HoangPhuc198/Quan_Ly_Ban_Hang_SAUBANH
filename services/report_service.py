"""
Báo cáo tổng hợp (view + procedure).
"""
from typing import Any, Dict

from repositories.report_repository import ReportRepository


class ReportService:
    def __init__(self):
        self.repo = ReportRepository()

    def get_report_bundle(self) -> Dict[str, Any]:
        r_ok, r_err, revenue = self.repo.get_doanh_thu_theo_thang()
        t_ok, t_err, top = self.repo.get_top_san_pham()
        s_ok, s_err, sap = self.repo.get_sap_het()
        l_ok, l_err, lau = self.repo.get_hang_ton_lau()
        c_ok, c_err, cong_no = self.repo.get_bao_cao_cong_no()
        errs = [e for e in (r_err, t_err, s_err, l_err, c_err) if e]
        return {
            "success": len(errs) == 0,
            "message": "; ".join(errs) if errs else None,
            "data": {
                "doanh_thu": revenue if r_ok else [],
                "top": top if t_ok else [],
                "sap_het": sap if s_ok else [],
                "hang_ton_lau": lau if l_ok else [],
                "cong_no": cong_no if c_ok else [],
            },
        }
