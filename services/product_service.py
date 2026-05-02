"""
Danh sách sản phẩm bán — ghép V_SANPHAM_TONKHO với V_GIA_HIEN_TAI theo MASPCT.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime, date

from repositories.product_repository import ProductRepository


def _norm_key(row: Dict[str, Any], *names: str) -> Optional[str]:
    lower = {str(k).lower(): v for k, v in row.items()}
    for n in names:
        v = lower.get(n.lower())
        if v is not None:
            return str(v).strip()
    return None


def _safe_date_value(val: Any) -> date:
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, date):
        return val
    if isinstance(val, str):
        try:
            return datetime.fromisoformat(val.replace("Z", "")).date()
        except ValueError:
            return date.min
    return date.min


def _merge_ton_and_gia(
    ton_rows: List[Dict[str, Any]],
    gia_rows: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    gia_by_ct: Dict[str, Dict[str, Any]] = {}
    for g in gia_rows:
        k = _norm_key(g, "MASPCT", "maspct")
        if k:
            ku = k.upper()
            cur = gia_by_ct.get(ku)
            if not cur:
                gia_by_ct[ku] = g
                continue
            cur_start = _safe_date_value(cur.get("NGAY_BAT_DAU"))
            new_start = _safe_date_value(g.get("NGAY_BAT_DAU"))
            if new_start >= cur_start:
                gia_by_ct[ku] = g

    merged: List[Dict[str, Any]] = []
    for t in ton_rows:
        k = _norm_key(t, "MASPCT", "maspct")
        out = dict(t)
        out["HAS_ACTIVE_PRICE"] = False
        if k:
            g = gia_by_ct.get(k.upper())
            if g:
                out["HAS_ACTIVE_PRICE"] = True
                for col in (
                    "DONGIA_BAN",
                    "DONGIA_NHAP",
                    "NGAY_BAT_DAU",
                    "NGAY_KET_THUC",
                ):
                    if col in g:
                        out[col] = g[col]
        merged.append(out)
    return merged


class ProductService:
    def __init__(self):
        self.repo = ProductRepository()

    def list_products(self) -> Dict[str, Any]:
        t_ok, t_err, ton = self.repo.get_ton_kho_chi_tiet()
        g_ok, g_err, gia = self.repo.get_gia_hien_tai()
        errs = [e for e in (t_err, g_err) if e]
        if not t_ok and not g_ok:
            return {
                "success": False,
                "message": "; ".join(errs) or "Không tải được dữ liệu sản phẩm.",
                "data": [],
            }
        ton = ton if t_ok else []
        gia = gia if g_ok else []
        data = _merge_ton_and_gia(ton, gia)
        return {
            "success": len(errs) == 0,
            "message": "; ".join(errs) if errs else None,
            "data": data,
        }
