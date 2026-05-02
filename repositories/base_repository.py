"""
Base repository: EXEC procedure và SELECT view — không truy vấn trực tiếp bảng nghiệp vụ.
Đọc tối đa QUERY_MAX_ROWS dòng (mặc định 200) để giảm tải và tăng tốc hiển thị.
"""
from typing import Any, Dict, List, Optional, Sequence, Tuple

import pyodbc

from config import QUERY_MAX_ROWS
from database import db


class BaseRepository:
    """Hàm dùng chung cho mọi repository."""

    def __init__(self):
        self._db = db

    @property
    def max_rows(self) -> int:
        return QUERY_MAX_ROWS

    @staticmethod
    def rows_to_dicts(cursor: pyodbc.Cursor) -> List[Dict[str, Any]]:
        """Chuyển toàn bộ kết quả fetchall() thành list[dict] (tên cột từ description)."""
        if cursor.description is None:
            return []
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def first_row_to_dict(cursor: pyodbc.Cursor) -> Optional[Dict[str, Any]]:
        """Một dòng đầu tiên hoặc None."""
        rows = BaseRepository.rows_to_dicts(cursor)
        return rows[0] if rows else None

    def execute_procedure(
        self,
        procedure_name: str,
        parameters: Sequence[Any],
        *,
        fetch_result: bool = False,
    ) -> Tuple[bool, Optional[str], Optional[List[Dict[str, Any]]]]:
        """
        EXEC stored procedure với tham số theo thứ tự.
        fetch_result=True: giới hạn số dòng trả về bằng SET ROWCOUNT (SQL Server).
        """
        placeholders = ", ".join(["?"] * len(parameters))
        sql = f"EXEC {procedure_name} {placeholders}"
        conn = self._db.get_connection()
        try:
            cursor = conn.cursor()
            if fetch_result:
                cursor.execute(f"SET ROWCOUNT {self.max_rows}")
            try:
                cursor.execute(sql, parameters)
                data: Optional[List[Dict[str, Any]]] = None
                if fetch_result:
                    data = (
                        self.rows_to_dicts(cursor)
                        if cursor.description
                        else []
                    )
                else:
                    while True:
                        if cursor.description:
                            cursor.fetchall()
                        if not cursor.nextset():
                            break
            finally:
                if fetch_result:
                    cursor.execute("SET ROWCOUNT 0")
            conn.commit()
            return True, None, data
        except pyodbc.Error as e:
            try:
                conn.rollback()
            except Exception:
                pass
            return False, self._safe_db_message(e), None
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def fetch_procedure(
        self,
        procedure_name: str,
        parameters: Sequence[Any],
    ) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        """EXEC procedure và luôn lấy result set đầu tiên (tối đa QUERY_MAX_ROWS dòng)."""
        ok, err, data = self.execute_procedure(
            procedure_name, parameters, fetch_result=True
        )
        return ok, err, data or []

    def fetch_view(self, view_name: str) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        """
        SELECT TOP (n) * FROM view — chỉ view được phép gọi từ repository.
        """
        n = self.max_rows
        sql = f"SELECT TOP ({n}) * FROM {view_name}"
        conn = self._db.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            data = self.rows_to_dicts(cursor)
            return True, None, data
        except pyodbc.Error as e:
            return False, self._safe_db_message(e), []
        finally:
            try:
                conn.close()
            except Exception:
                pass

    @staticmethod
    def _safe_db_message(exc: pyodbc.Error) -> str:
        """Không lộ chi tiết kỹ thuật cho người dùng cuối — log nội bộ có thể mở rộng."""
        return "Lỗi kết nối hoặc xử lý dữ liệu. Vui lòng thử lại hoặc liên hệ quản trị."
