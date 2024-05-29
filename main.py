# api.py
from flask import Flask, request, jsonify
import pyodbc
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
conx = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=Admin\SQLEXPRESS;DATABASE=QUANLYKHOHANG; UID=minhngoc; PWD=luandz123')
cursor = conx.cursor()


@app.route('/', methods=['GET'])
def home():
    return "Welcome to my API!"

@app.route('/tables', methods=['GET'])
def get_tables():
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    tables = [row.TABLE_NAME for row in cursor.fetchall()]
    return jsonify(tables)

@app.route('/table/<table_name>', methods=['GET'])
def get_table_data(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    data = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    return jsonify(data)

@app.route('/table/<table_name>', methods=['POST'])
def add_data(table_name):
    data = request.json
    columns = ', '.join(data.keys())
    placeholders = ', '.join('?' * len(data))
    values = list(data.values())
    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
    conx.commit()
    return '', 204

@app.route('/table/<table_name>/<id>', methods=['PUT'])
def edit_data(table_name, id):
    data = request.json
    set_clause = ', '.join(f"{column} = ?" for column in data.keys())
    values = list(data.values())
    cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE id = ?", *values, id)
    conx.commit()
    return '', 204








if __name__ == '__main__':
    app.run(debug=True, port=5000)