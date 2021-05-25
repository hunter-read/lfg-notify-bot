from flask import Flask, jsonify, request
from model import Database, Post

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/statistics', methods=['GET'])
def api_all():
    args = request.args

    with Database() as db:
        if 'date' in args:
            return jsonify(Post.statistics(db, date=args.get("date")))
        else:
            return jsonify(Post.statistics(db))


app.run()
