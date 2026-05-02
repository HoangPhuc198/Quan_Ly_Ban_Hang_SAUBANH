"""
Cấu hình ứng dụng và SQL Server.
Chỉnh sửa biến môi trường hoặc giá trị mặc định bên dưới cho phù hợp môi trường triển khai.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env nếu có (cùng thư mục project)
_env_path = Path(__file__).resolve().parent / ".env"
if _env_path.exists():
    load_dotenv(_env_path)


class Config:
    """Flask config."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-change-in-production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # Hiển thị trên màn đăng nhập, sidebar (tên doanh nghiệp / cửa hàng)
    BUSINESS_NAME = (
        (os.environ.get("BUSINESS_NAME") or "").strip()
        or "CỬA HÀNG THỜI TRANG TRẺ EM SÁU BẢNH"
    )


class DatabaseConfig:
    """Thông tin kết nối SQL Server (pyodbc)."""

    # Tên server, ví dụ: localhost\\SQLEXPRESS hoặc 127.0.0.1,1433
    SERVER = os.environ.get("DB_SERVER") or "localhost\\SQLEXPRESS"
    DATABASE = os.environ.get("DB_NAME") or "SellerDB"
    # Trusted Connection (Windows Auth)
    TRUSTED_CONNECTION = os.environ.get("DB_TRUSTED_CONNECTION", "yes").lower() in (
        "1",
        "true",
        "yes",
    )
    DB_USER = os.environ.get("DB_USER") or ""
    DB_PASSWORD = os.environ.get("DB_PASSWORD") or ""
    # Driver ODBC — có thể cần chỉnh theo máy (ODBC Driver 17/18 for SQL Server)
    DRIVER = os.environ.get("DB_ODBC_DRIVER") or "ODBC Driver 17 for SQL Server"
    # ODBC 18: mặc định Encrypt=yes — máy local thường cần TrustServerCertificate hoặc Encrypt=no
    ENCRYPT = (os.environ.get("DB_ENCRYPT") or "").strip().lower()  # yes | no | rỗng
    TRUST_SERVER_CERT = os.environ.get("DB_TRUST_SERVER_CERTIFICATE", "yes").lower() in (
        "1",
        "true",
        "yes",
    )

    @classmethod
    def connection_string(cls) -> str:
        parts = [
            f"DRIVER={{{cls.DRIVER}}}",
            f"SERVER={cls.SERVER}",
            f"DATABASE={cls.DATABASE}",
        ]
        if cls.TRUSTED_CONNECTION:
            parts.append("Trusted_Connection=yes;")
        else:
            parts.append(f"UID={cls.DB_USER};PWD={cls.DB_PASSWORD};")
        if cls.ENCRYPT == "no":
            parts.append("Encrypt=no;")
        elif cls.ENCRYPT == "yes":
            parts.append("Encrypt=yes;")
        if cls.TRUST_SERVER_CERT:
            parts.append("TrustServerCertificate=yes;")
        return ";".join(parts)


def _safe_int_env(name: str, default: int, min_v: int, max_v: int) -> int:
    try:
        v = int(os.environ.get(name, str(default)))
    except (TypeError, ValueError):
        v = default
    return max(min_v, min(max_v, v))


# Giới hạn số dòng đọc từ View / procedure (tốc độ UI & giảm tải SQL)
QUERY_MAX_ROWS = _safe_int_env("DB_QUERY_MAX_ROWS", 200, 1, 2000)
