# ============================
# GPU ML Platform Makefile
# ============================

# Ports
MLFLOW_PORT=5000
GRAFANA_PORT=3000
PROM_PORT=9090

# ============================
# ENVIRONMENT
# ============================

env:
    python3.11 -m venv gpu-ml-env
    ./gpu-ml-env/bin/pip install --upgrade pip
    ./gpu-ml-env/bin/pip install -r trainer/requirements.txt

activate:
    @echo "Run: source gpu-ml-env/bin/activate"

# ============================
# TRAINING
# ============================

train:
    source gpu-ml-env/bin/activate && python trainer/train.py

# ============================
# PORT-FORWARD START
# ============================

start:
    @echo "Starting MLflow..."
    nohup kubectl port-forward deployment/mlflow $(MLFLOW_PORT):5000 > mlflow.log 2>&1 &
    @echo "Starting Grafana..."
    nohup kubectl port-forward deployment/grafana $(GRAFANA_PORT):3000 > grafana.log 2>&1 &
    @echo "Starting Prometheus..."
    nohup kubectl port-forward deployment/prometheus $(PROM_PORT):9090 > prometheus.log 2>&1 &
    @echo "All services started."

# ============================
# PORT-FORWARD STOP
# ============================

stop:
    @echo "Stopping all kubectl port-forward processes..."
    -pkill -f "kubectl port-forward"
    @echo "All services stopped."

# ============================
# STATUS
# ============================

status:
    @echo "Active port-forward processes:"
    ps aux | grep "kubectl port-forward" | grep -v grep || echo "No active port-forwards."

# ============================
# CLEAN LOGS
# ============================

clean:
    rm -f mlflow.log grafana.log prometheus.log
    @echo "Logs cleaned."

