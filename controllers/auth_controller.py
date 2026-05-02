"""
Đăng nhập / đăng xuất.
"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)
_auth_service = AuthService()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        result = _auth_service.login(username, password)
        if result["success"] and result["data"]:
            data = result["data"]
            session["user"] = {
                "username": data.get("username"),
                "ma_nv": data.get("ma_nv"),
                "ten": data.get("ten"),
            }
            session["role"] = data.get("role", "SALE")
            flash(result["message"], "success")
            return redirect(url_for("dashboard.dashboard"))
        flash(result.get("message") or "Đăng nhập thất bại.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Đã đăng xuất.", "info")
    return redirect(url_for("auth.login"))
