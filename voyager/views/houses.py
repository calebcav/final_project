
from collections import namedtuple

from flask import render_template
from flask import request
from flask import escape

from voyager.db import get_db, execute


def getAllHouses(conn):
    return execute(conn, "SELECT * FROM HOUSE")


def getAllHousesByAgent(conn, name):
    pass


def getAllHousesInterested(conn, userName):
    pass


def addHouse(conn, name, price, address, aid, rent, status):
    pass


def filteredSearchForHouses(conn, name, maxPrice, address, aid, rent, status):
    pass


def addInterest(conn, userid, houseid):
    pass


def getMostPopularHouse(conn):
    pass


def views(bp):
    @bp.route("/all-houses")
    def all_houses():
        with get_db() as conn:
            rows = getAllHouses(conn)
        return render_template("table.html", name="all houses", rows=rows)

    @bp.route("/agent-houses", methods=["POST", "GET"])
    def all_agent_houses():

        return request.form["agent-name"]
