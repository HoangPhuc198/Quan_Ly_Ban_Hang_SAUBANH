"""
Đăng nhập qua usp_DANG_NHAP — không truy vấn bảng người dùng trực tiếp.
"""
from typing import Any, Dict, List, Optional, Tuple

from repositories.base_repository import BaseRepository


class AuthRepository(BaseRepository):
    def dang_nhap(
        self, username: str, password: str
    ) -> Tuple[bool, Optional[str], List[Dict[str, Any]]]:
        """
        EXEC usp_DANG_NHAP @username, @password
        Đối chiếu thứ tự tham số trong SQL Server nếu khác.
        """
        return self.fetch_procedure("usp_DANG_NHAP", (username, password))
