# 📘 GPU‑ML Platform (macOS)

A fully containerized machine‑learning training platform running on **Kubernetes**, with integrated **Prometheus**, **Grafana**, and **MLflow** for complete observability.

This project lets you train models, monitor system performance, track metrics, and visualize cluster health — all from your macOS environment.

---

## 🖼️ Architecture Overview

Add an image to your repo (e.g., `docs/architecture.png`) and reference it:

```md
![Architecture](docs/architecture.png)
```

If you want, I can generate a full architecture diagram for you.

---

## 📦 Project Structure

| Folder | Description |
|--------|-------------|
| `trainer/` | Python training scripts, metrics endpoints |
| `monitoring/` | Prometheus + Grafana configs |
| `k8s/` | Kubernetes manifests (Deployments, Services, ConfigMaps) |
| `docs/` | Diagrams, notes, dashboard screenshots |
| `mlruns/` | MLflow experiment tracking (ignored in Git) |
| `makefile` | Automation for port‑forwarding and cluster setup |

---

## 📊 Monitoring Dashboards

### **Trainer Metrics Dashboard**
Add an image:

```md
![Trainer Dashboard](docs/trainer-dashboard.png)
```

Shows:
- Training loss  
- Training accuracy  
- Epoch timing  
- Model performance curves  

---

### **Kubernetes Cluster Dashboard**
```md
![Cluster Dashboard](docs/cluster-dashboard.png)
```

Shows:
- Node CPU / memory  
- Pod restarts  
- Namespace usage  
- Deployment health  

---

### **System Metrics (macOS Exporter)**
```md
![System Metrics](docs/system-metrics.png)
```

Shows:
- CPU temperature  
- GPU temperature  
- Fan speed  
- Memory usage  

---

## ⚙️ How to Run the Platform

### 1. Start Kubernetes services

```bash
kubectl apply -f k8s/
```

### 2. Start Prometheus

```bash
nohup kubectl port-forward deployment/prometheus 9090:9090 > prometheus.log 2>&1 &
```

### 3. Start Grafana

```bash
nohup kubectl port-forward deployment/grafana 3000:3000 > grafana.log 2>&1 &
```

### 4. Start MLflow

```bash
nohup kubectl port-forward deployment/mlflow 5000:5000 > mlflow.log 2>&1 &
```

---

## 📡 Prometheus Scrape Targets

| Target | Purpose |
|--------|---------|
| `trainer` | Training metrics endpoint |
| `kubernetes-nodes` | Node CPU / memory |
| `kubernetes-pods` | Pod metrics |
| `kube-state-metrics` | Deployment / namespace health |
| `macos_exporter` | macOS system metrics |

---

## 🚀 Trainer API

Your trainer exposes metrics at:

```
http://localhost:8000/metrics
```

Prometheus scrapes this automatically.

---

## 🛠️ Requirements

| Component | Version |
|-----------|---------|
| Python | 3.11 |
| Kubernetes | v1.30+ |
| Prometheus | latest |
| Grafana | latest |
| MLflow | latest |
| macOS Exporter | latest |

---

## 📥 Installation

Clone the repo:

```bash
git clone https://github.com/nayeeman49/gpu-ml-platform-macos.git
cd gpu-ml-platform-macos
```

Create venv:

```bash
python3.11 -m venv gpu-ml-env
source gpu-ml-env/bin/activate
pip install -r trainer/requirements.txt
```

---

## 🧹 .gitignore (included)

Your repo is now clean and safe for GitHub.

---

## 📄 License

MIT License (or whichever you choose)

---


