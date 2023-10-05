from flask import Flask, request, jsonify, render_template
import sqlite3 as sql
import math

app = Flask(__name__)

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True, port=5000)