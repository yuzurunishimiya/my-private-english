from flask import Blueprint
from flask import request, redirect, render_template
from itertools import groupby
from operator import itemgetter

from connection import db_vocabulary

vocab_bp = Blueprint("vocab", __name__, template_folder="./templates")


def proccess_vocabulary(data):
    result = sorted(data, key=lambda i: i["group"])
    final_res = {}
    for group, items in groupby(result, itemgetter("group")):
        final_res[group] = list(items)
    return final_res


@vocab_bp.route("/vocabulary/simple")
def vocabulary_func():
    language = request.args.get("language")
    if not language:
        return redirect("/vocabulary/simple?language=en-id")

    data = list(db_vocabulary.aggregate([
        {"$project": {
            "_id": 0,
            "english": 1,
            "bahasa": 1,
            "group": 1,
            "code": 1
        }}
    ]))

    data = proccess_vocabulary(data)
    return render_template("vocabulary.html", data=data)
