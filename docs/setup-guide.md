# Setup Guide
1. Install Docker Desktop and enable Kubernetes.
2. Install Python, kind, kubectl, and GitHub CLI via Homebrew.
3. Create cluster: `kind create cluster --name gpu-ml`
4. Deploy MLflow, Prometheus, Grafana: `kubectl apply -f k8s/`
5. Run training: 
