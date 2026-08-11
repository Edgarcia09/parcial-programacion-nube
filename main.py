from flask import Flask, jsonify
import os
import pymysql

app = Flask(__name__)


def get_connection():
    return pymysql.connect(
        unix_socket=f"/cloudsql/{os.environ['INSTANCE_CONNECTION_NAME']}",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route("/")
def inicio():
    return jsonify({
        "mensaje": "Aplicación desplegada correctamente en Google Cloud",
        "estado": "funcionando mediante CI/CD",
        "servicio": "Cloud Run"
    })


@app.route("/saludo")
def saludo():
    return jsonify({
        "mensaje": "Hola, esta es nuestra API en la nube"
    })


@app.route("/productos")
def productos():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, nombre, precio FROM productos"
            )
            resultados = cursor.fetchall()

        return jsonify(resultados)

    finally:
        connection.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
