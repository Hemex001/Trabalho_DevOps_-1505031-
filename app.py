from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Inicializa métricas e loga uma mensagem para confirmar
try:
    metrics = PrometheusMetrics(app)
    print("PrometheusMetrics initialized successfully.")
except Exception as e:
    print(f"Error initializing PrometheusMetrics: {e}")

@app.route('/')
def index():
    return "Hello, Prometheus!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
