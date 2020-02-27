from collections import namedtuple

from flask import render_template
from flask import request

from voyager.db import get_db, execute


def voyages(conn):
    return execute(conn, "SELECT v.sid, v.bid, v.date_of_voyage FROM Voyages as v")

def add_voyage(conn, sid, bid, date):
    return execute(conn, f"INSERT INTO Voyages (sid, bid, date_of_voyage) VALUES ({sid}, {bid}, '{date}')")

def views(bp):
    @bp.route("/voyages")
    def _voyages():
        with get_db() as conn:
            rows = voyages(conn)
        return render_template("table.html", name="voyages", rows=rows)


    @bp.route("/voyages/add")
    def addvoyagespage():
        return render_template("addvoyages.html")

    @bp.route("/voyages/add", methods=["POST", "GET"])
    def _add_voyage():

        if request.method == "POST":
            with get_db() as conn:
                voyage_sid = request.form["voyage-sid"]
                voyage_bid = request.form["voyage-bid"]
                voyage_date = request.form["voyage-date"]
                add_voyage(conn, voyage_sid, voyage_bid, voyage_date)
                return "SUCCESS"
        else:
            return "FAILURE"
    