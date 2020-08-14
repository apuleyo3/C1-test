import flask
from flask import request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

api_key = '-------------'

app = flask.Flask(__name__)
CORS(app, support_credentials=True)
app.config["DEBUG"] = True

mysql = MySQL(app)
app.config['MYSQL_HOST'] = '172.17.0.6'
app.config['MYSQL_USER'] = '---------'
app.config['MYSQL_PASSWORD'] = '---------'
app.config['MYSQL_DB'] = '--------'


@app.route('/', methods=['GET'])
def home():
    return "<h1>API C1</h1><p>Speak friend and enter</p>"

@app.route('/api/v1/search', methods=['GET'])
def search():
    if 'key' in request.args:
        key = str(request.args['key'])
        if key == api_key:
            try:
                elem = request.args['elem']
                table = request.args['table']
                where = request.args['where']
                val = request.args['val']
            except:
                return 'Not enough elements in your key, check it out and try again'
            qr = "SELECT " + elem + " FROM " + table + " WHERE " + where + " = '" + val + "'"
            cur = mysql.connection.cursor()
            cur.execute(qr)
            data = cur.fetchall()
            mysql.connection.commit()
            cur.close()
            return jsonify(data)

        else:
            return '<p>Is this Sauron the great deceiver? (Your key is false!!)</p>'
    else:
        return '<p>You shall not pass!! (no key!!)</p>'

@app.route('/api/v1', methods=['GET', 'POST', 'PATCH'])
def users_all():
    if 'key' in request.args:
        key = str(request.args['key'])
        if key == api_key:
            if request.method == 'GET':
                try:
                    elems = request.args['elems']
                    table = request.args['table']
                except:
                    return 'Not enough elements in your key, check it out and try again'
                qr = "SELECT " + elems + " FROM " + table
                cur = mysql.connection.cursor()
                cur.execute(qr)
                data = cur.fetchall()
                mysql.connection.commit()
                cur.close()
                return jsonify(data)
            elif request.method == 'POST':
                try:
                    elems = request.args['elems']
                    table = request.args['table']
                    vals = request.args['vals']
                except:
                    return 'Not enough elements in your key, check it out and try again'
                qr = "INSERT INTO " + table + "(" + elems + ") VALUES (" + str(vals) + ")"
                cur = mysql.connection.cursor()
                cur.execute(qr)
                data = cur.fetchall()
                mysql.connection.commit()
                cur.close()
                return 'Success!'
            elif request.method == 'PATCH':
                try:
                    table = request.args['table']
                    elem = request.args['elem']
                    val = request.args['val']
                    id = request.args['id']
                except:
                    return 'Not enough elements in your key, check it out and try again'
                qr = "UPDATE " + table + " SET " + elem + "='" + val + "'" + ' WHERE id=' + id
                cur = mysql.connection.cursor()
                cur.execute(qr)
                data = cur.fetchall()
                mysql.connection.commit()
                cur.close()
                return 'Success!'
            elif request.method == 'DELETE':
                try:
                    table = request.args['table']
                    id = request.args['id']
                except:
                    return 'Not enough elements in your key, check it out and try again'
                qr = "DELETE FROM " +  table  + " WHERE id=" + id
                cur = mysql.connection.cursor()
                cur.execute(qr)
                data = cur.fetchall()
                mysql.connection.commit()
                cur.close()
                return 'Success!'

        else:
            return '<p>Is this Sauron the great deceiver? (Your key is false!!)</p>'
    else:
        return '<p>You shall not pass!! (no key!!)</p>'



app.run(host='0.0.0.0', port=80)