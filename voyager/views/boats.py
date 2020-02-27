
from collections import namedtuple

from flask import render_template
from flask import request
from flask import escape

from voyager.db import get_db, execute

def boats(conn):
    return execute(conn, "SELECT b.bid, b.name, b.color FROM Boats AS b")

def sailed_by(conn, sailor_name):
    return execute(conn, f"SELECT Boats.name FROM Boats INNER JOIN Voyages ON Boats.bid = Voyages.bid INNER JOIN Sailors ON Sailors.sid = Voyages.sid WHERE Sailors.name = '{sailor_name}'")

def boats_pop(conn):
    return execute(conn, "SELECT Boats.name, count(*) FROM Boats INNER JOIN Voyages on Boats.bid = Voyages.bid GROUP BY Boats.name ORDER BY count(*) DESC")

def add_boat(conn, name, color):
    return execute(conn, f"INSERT INTO Boats(name, color) VALUES ('{name}', '{color}')")

def views(bp):
    @bp.route("/boats")
    def _boats():
        with get_db() as conn:
            rows = boats(conn)
        return render_template("table.html", name="boats", rows=rows)


    @bp.route("/boats/sailed-by", methods=["POST", "GET"])

    def _sailed_by():

        if request.method == "POST":
            with get_db() as conn:
                sailor_name = request.form["sailor-name"]
                rows = sailed_by(conn, sailor_name)
            return render_template("table.html", name=sailor_name, rows=rows)
        else:
            return "Hello"
    
    @bp.route("/boats/by-popularity", methods=["POST", "GET"])

    def _boats_popularity():

        if request.method == "GET":
            with get_db() as conn:
                rows = boats_pop(conn)
            return render_template("table.html", name="Popular Boats", rows=rows)
        else:
            return "Hello"
    
    @bp.route("/boats/add")
    def addboatspage():
        return render_template("addboats.html")
    
    @bp.route("/boats/add", methods=["POST", "GET"])
    def _add_boats():

        if request.method == "POST":
            with get_db() as conn:
                boat_name = request.form["boats-name"]
                boat_color = request.form["boats-color"]
                add_boat(conn, boat_name, boat_color)
                return "SUCCESS"
        else:
            return "FAILURE"
