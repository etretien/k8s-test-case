from flask import Flask, request
import psycopg2
import os

app = Flask(__name__)

def insert_client_ip(ip):
    conn = psycopg2.connect(
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO client_ips (client_ip) VALUES (%s)", (ip,))
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def index():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.remote_addr

    insert_client_ip(client_ip)
    return f"Client IP: {client_ip}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

