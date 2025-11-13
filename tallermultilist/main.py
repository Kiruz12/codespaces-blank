from flask import Flask, render_template, jsonify
from multilista import LinkedList
import csv

app = Flask(__name__)

def parse_coord(value):
    return float(value.replace(',', '.')) if value else None

def cargar_divipola(ruta_csv):
    pais = LinkedList()
    pais_node = pais.add("CO", "Colombia")
    pais_node.sub_list = LinkedList()
    with open(ruta_csv, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            dep_id, dep_name, mun_id, mun_name, tipo, lon, lat = row
            lat = parse_coord(lat)
            lon = parse_coord(lon)
            dep_node = pais_node.sub_list.find(dep_id)
            if not dep_node:
                dep_node = pais_node.sub_list.add(dep_id, dep_name)
                dep_node.sub_list = LinkedList()
            dep_node.sub_list.add(mun_id, mun_name, lat, lon)
    return pais

divipola = cargar_divipola("/workspaces/codespaces-blank/tallermultilist/divipola.csv")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/divipola")
def api_divipola():
    return jsonify(divipola.to_dict())

if __name__ == "__main__":
    app.run(debug=True, port=8080)
