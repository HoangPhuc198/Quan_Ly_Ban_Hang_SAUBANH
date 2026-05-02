"""
Quản lý kết nối SQL Server qua pyodbc.
"""
from contextlib import contextmanager
from typing import Generator, Optional

import pyodbc

from config import DatabaseConfig


class Database:
    """Wrapper kết nối — dùng get_connection() hoặc connection context."""

    def __init__(self, connection_string: Optional[str] = None):
        self._connection_string = connection_string or DatabaseConfig.connection_string()

    def get_connection(self) -> pyodbc.Connection:
        """Trả về connection mới; caller chịu trách nhiệm đóng."""
        return pyodbc.connect(self._connection_string)

    @contextmanager
    def connection(self) -> Generator[pyodbc.Connection, None, None]:
        """Context manager: đảm bảo đóng connection."""
        conn = self.get_connection()
        try:
            yield conn
        finally:
            try:
                conn.close()
            except Exception:
                pass


# Singleton mặc định cho app
db = Database()
