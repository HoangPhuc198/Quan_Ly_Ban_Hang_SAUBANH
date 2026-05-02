"""
Seller Management System — Flask application factory / entry.
"""
import re

from flask import Flask, session

from config import Config, QUERY_MAX_ROWS


def hide_sql_object_names(value) -> str:
    """Loại bỏ tên view / stored procedure / trigger kiểu SQL Server khỏi chuỗi hiển thị cho người dùng."""
    if value is None:
        return ""
    s = str(value)
    s = re.sub(
        r"\b(?:V_|v_|usp_|USP_|trg_|TRG_)[A-Za-z0-9_]+\b",
        "",
        s,
        flags=re.UNICODE,
    )
    s = re.sub(r"\s{2,}", " ", s).strip()
    return s


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # Blueprints
    from controllers.auth_controller import auth_bp
    from controllers.dashboard_controller import dashboard_bp
    from controllers.product_controller import product_bp
    from controllers.sales_controller import sales_bp
    from controllers.stock_controller import stock_bp
    from controllers.purchase_controller import purchase_bp
    from controllers.customer_controller import customer_bp
    from controllers.report_controller import report_bp
    from controllers.invoice_controller import invoice_bp
    from controllers.system_controller import system_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(purchase_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(system_bp)

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    @app.route("/health/db")
    def health_db():
        """Kiểm tra kết nối SQL Server (pyodbc). Mở trong trình duyệt để xem lỗi kết nối cụ thể."""
        try:
            from config import DatabaseConfig
            from database import db

            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.fetchone()
            cur.close()
            conn.close()
            return {
                "database": "connected",
                "server": DatabaseConfig.SERVER,
                "database_name": DatabaseConfig.DATABASE,
            }, 200
        except Exception as e:
            return {"database": "error", "detail": str(e)}, 503

    @app.context_processor
    def inject_user():
        user = session.get("user")
        role = (session.get("role") or "").upper()
        return dict(
            current_user=user,
            current_role=role,
            query_max_rows=QUERY_MAX_ROWS,
            business_name=Config.BUSINESS_NAME,
        )

    @app.template_filter("to_float")
    def to_float_filter(val, default=0.0):
        if val is None:
            return default
        try:
            return float(val)
        except (TypeError, ValueError):
            return default

    @app.template_filter("field")
    def field_lookup(row, *names):
        """Lấy giá trị từ dict row theo danh sách tên cột có thể có (không phân biệt hoa thường)."""
        if not row or not names:
            return ""
        lower_map = {str(k).lower(): v for k, v in row.items()}
        for n in names:
            v = lower_map.get(str(n).lower())
            if v is not None:
                return v
        return ""

    @app.template_filter("hide_sql_names")
    def hide_sql_names_filter(val):
        return hide_sql_object_names(val)

    @app.errorhandler(404)
    def not_found(_e):
        from flask import render_template

        return render_template("error.html", code=404, message="Không tìm thấy trang."), 404

    @app.errorhandler(500)
    def server_error(_e):
        from flask import render_template

        return render_template("error.html", code=500, message="Lỗi hệ thống. Vui lòng thử lại sau."), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
