
from flask import Blueprint, render_template, redirect, url_for, session
from db import get_db_connection

cart = Blueprint("cart", __name__)


@cart.route("/cart")
def view_cart():
    cart_ids = session.get("cart", [])
    pcs = []

    if cart_ids:
        connection = get_db_connection()

        if connection is None:
            return "<h1>Database connection failed!</h1>"

        cursor = connection.cursor(dictionary=True)

        placeholders = ", ".join(["%s"] * len(cart_ids))

        cursor.execute(f"""
            SELECT pc_ID, model_name, price, specs, image
            FROM PC
            WHERE pc_ID IN ({placeholders})
        """, tuple(cart_ids))

        pcs = cursor.fetchall()

        cursor.close()
        connection.close()

        # Keep items in the order they were added
        pcs.sort(key=lambda pc: cart_ids.index(pc["pc_ID"]))

    subtotal = sum(pc["price"] for pc in pcs)

    return render_template("cart.html", pcs=pcs, subtotal=subtotal)


@cart.route("/cart/add/<int:pc_id>", methods=["POST"])
def add_to_cart(pc_id):
    cart_ids = session.get("cart", [])

    if pc_id not in cart_ids:
        session["cart"] = cart_ids + [pc_id]

    return redirect(url_for("cart.view_cart"))


@cart.route("/cart/remove/<int:pc_id>", methods=["POST"])
def remove_from_cart(pc_id):
    cart_ids = session.get("cart", [])

    session["cart"] = [i for i in cart_ids if i != pc_id]

    return redirect(url_for("cart.view_cart"))
