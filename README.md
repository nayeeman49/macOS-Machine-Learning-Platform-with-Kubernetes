
# 📘 macOS Machine Learning Platform with Kubernetes

A fully containerized machine‑learning training platform built on **Kubernetes**, featuring **Prometheus**, **Grafana**, and **MLflow** for complete observability.  
The system provides an end‑to‑end workflow for training models, tracking experiments, and monitoring both application and system‑level metrics — all running locally on macOS. It is being hosted locally and eligible for any Arm based MacOS device, in my case my m1 max macbook pro

---

## 🖼️ Architecture Overview

### **Platform Architecture**

This diagram outlines the core components of the platform:
Main tree concept:
<img width="618" height="720" alt="image" src="https://github.com/user-attachments/assets/f2be2eb1-0f32-4e0a-b350-2c9f1cb0de81" />

- Kubernetes workloads (Trainer, Prometheus, Grafana, MLflow)  
- macOS system metrics via node‑exporter  
- Prometheus scraping pipeline  
- Grafana dashboards  
- MLflow experiment tracking  

---

This grafana dashboard references each trainer run:
<img width="1275" height="664" alt="image" src="https://github.com/user-attachments/assets/2e9166bb-6679-4669-b89a-b9f85e9be499" />

It feeds off data from metrics running the trainer:
<img width="402" height="86" alt="image" src="https://github.com/user-attachments/assets/ddab7e47-87d6-4c8c-98ef-972837e9c9aa" />

This is all being run by my local kubernetes cluster:
<img width="958" height="228" alt="image" src="https://github.com/user-attachments/assets/e4410966-4c14-48a7-ae9b-7108a190056f" />

The device being used is my M1 Max Macbook pro which has sufficient power to enable some GPU autoscaling:
<img width="4000" height="1848" alt="image" src="https://github.com/user-attachments/assets/552e9828-0fd8-4a95-b3c9-e53c5e20ab38" />


## 📁 Repository Structure Diagram

### **Repo Tree**

A visual overview of the repository layout, showing how training code, Kubernetes manifests, monitoring configurations, and documentation fit together.

---

## 📦 Project Structure

| Folder | Description |
|--------|-------------|
| `trainer/` | Model training code, Dockerfile, MLflow integration |
| `monitoring/` | Prometheus rules, Grafana dashboards |
| `k8s/` | Kubernetes manifests for all platform components |
| `docs/` | Architecture diagrams, setup notes, dashboard screenshots |
| `mlruns/` | MLflow experiment artifacts (local only) |
| `makefile` | Automation for port‑forwarding and cluster startup |

---

## 📊 Monitoring Dashboards

### **Trainer Metrics Dashboard**
`[Looks like the result wasn't safe to show. Let's switch things up and try something else!]`

Includes:

- Training loss  
- Accuracy  
- Epoch timing  
- Model performance curves  

---

### **Kubernetes Cluster Dashboard**

Visualizes:

- Node CPU / memory  
- Pod restarts  
- Namespace usage  
- Deployment health  

---

### **System Metrics (macOS Exporter)**

Tracks:

- CPU temperature  
- GPU temperature  
- Fan speed  
- Memory usage  

---

## ⚙️ Running the Platform

### 1. Deploy all Kubernetes workloads

```bash
kubectl apply -f k8s/
```

### 2. Start Prometheus (background)

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

The trainer exposes Prometheus metrics at:

```
http://localhost:8000/metrics
```

These metrics are scraped automatically by Prometheus and visualized in Grafana.

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

Clone the repository:

```bash
git clone https://github.com/nayeeman49/gpu-ml-platform-macos.git
cd gpu-ml-platform-macos
```

Create a Python environment:

```bash
python3.11 -m venv gpu-ml-env
source gpu-ml-env/bin/activate
pip install -r trainer/requirements.txt
```

---

## 🧹 .gitignore

The repository includes a `.gitignore` to keep logs, datasets, MLflow artifacts, and runtime files out of version control.

---

## 📄 License

MIT License (or another license of your choice).

---
