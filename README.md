# Seller Management System

Ứng dụng web quản lý bán lẻ (Flask + SQL Server + Bootstrap 5), kiến trúc 3 lớp: Controller → Service → Repository. Repository chỉ gọi **Stored Procedure** và đọc **View** — không truy vấn trực tiếp bảng nghiệp vụ.

## Yêu cầu môi trường

- Python 3.10+ (khuyến nghị 3.11/3.12)
- SQL Server (Express hoặc bản đầy đủ) và ODBC Driver 17/18 for SQL Server
- Database đã có đủ procedure/view theo đặc tả dự án (`usp_*`, `V_*`)

## Cài đặt

```powershell
cd seller_system
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Cấu hình SQL Server

Tạo file `.env` (hoặc chỉnh `config.py`) trong thư mục `seller_system`:

```env
SECRET_KEY=chuoi-bi-mat-cua-ban
DB_SERVER=localhost\SQLEXPRESS
DB_NAME=TenDatabaseCuaBan
DB_TRUSTED_CONNECTION=yes
# Hoặc SQL login:
# DB_TRUSTED_CONNECTION=no
# DB_USER=sa
# DB_PASSWORD=matkhau
# DB_ODBC_DRIVER=ODBC Driver 17 for SQL Server
```

Đảm bảo tài khoản Windows hoặc SQL có quyền `EXEC` các procedure và `SELECT` các view đã nêu.

## Chạy ứng dụng

```powershell
cd seller_system
.\.venv\Scripts\Activate.ps1
py -3 app.py
```

Hoặc:

```powershell
set FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

Mở trình duyệt: `http://127.0.0.1:5000`

## Đối chiếu tham số Stored Procedure

Trong repository, thứ tự tham số `EXEC` được ghi rõ bằng comment. Nếu chữ ký thực tế trong SQL Server khác, chỉnh **một chỗ** tại file repository tương ứng:

| Procedure | File |
|-----------|------|
| `usp_DANG_NHAP` | `repositories/auth_repository.py` |
| `usp_TAO_HOADON_BAN`, `usp_THEM_CTHDB`, `usp_KiemTraTonKho`, `usp_THANH_TOAN_HOADON_BAN` | `repositories/sales_repository.py` |
| `usp_TAO_HOADON_NHAP`, `usp_THEM_CTHDN` | `repositories/purchase_repository.py` |
| `usp_THEM_KHACHHANG`, `usp_TICH_DIEM` | `repositories/customer_repository.py` |
| `usp_TOP_SANPHAM` | `repositories/dashboard_repository.py`, `repositories/report_repository.py` |

**`usp_TOP_SANPHAM`:** mặc định gọi không tham số `()`. Nếu DB yêu cầu `@TopN`, sửa thành `(top_n,)` trong hai file trên.

## Phân quyền (session `role`)

Chuẩn hóa trong `auth_service`: `OWNER`, `ADMIN`, `CASHIER`, `SALE`, `WAREHOUSE`. Cột vai trò trả về từ `usp_DANG_NHAP` có thể được map qua bảng alias trong `auth_service._normalize_role`.

- **OWNER / ADMIN:** đầy đủ menu, dashboard doanh thu, báo cáo.
- **CASHIER / SALE:** bán hàng, sản phẩm, tồn kho (xem), khách hàng — không nhập hàng, không báo cáo tài chính.
- **WAREHOUSE:** tồn kho, nhập hàng, sản phẩm — không POS, không khách hàng, không báo cáo doanh thu.

## Tài khoản demo

Phụ thuộc dữ liệu trong SQL Server (bảng nhân viên / người dùng mà `usp_DANG_NHAP` tham chiếu). Không có user cố định trong code — tạo user trong DB theo quy ước của stored procedure.

## Kiểm tra chức năng (checklist)

1. Đăng nhập (`/login`).
2. Dashboard (`/dashboard`).
3. Sản phẩm (`/products`).
4. POS (`/sales`): tạo HĐ → thêm dòng (kiểm tra tồn qua `usp_KiemTraTonKho`) → thanh toán.
5. Tồn kho (`/stock`): ba tab view.
6. Nhập hàng (`/purchase`): tạo phiếu → thêm chi tiết.
7. Khách hàng (`/customers`): thêm KH; tích điểm (chỉnh tham số `usp_TICH_DIEM` nếu cần).
8. Báo cáo (`/reports`): chỉ OWNER/ADMIN.

## TODO đã ghi trong code

- **Danh sách khách hàng:** không có view/procedure trong danh sách được phép — `customers.html` hiển thị TODO.
- **Danh sách hóa đơn:** `invoices.html` / `invoice_detail.html` dự phòng — chưa có route (cần view/procedure từ DBA).

## Ghi chú package Python

Thư mục package dùng `__init__.py` (chuẩn Python). Nếu tài liệu nội bộ ghi `_init_.py`, đổi tên thành `__init__.py`.

## API kiểm tra nhanh

- `GET /health` — trạng thái process.
# Quan_Ly_Ban_Hang_SAUBANH
