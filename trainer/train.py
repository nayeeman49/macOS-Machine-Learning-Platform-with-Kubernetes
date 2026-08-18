import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import mlflow
import mlflow.pytorch
from prometheus_client import Gauge, start_http_server
import socket

# -------------------------------
# Start Prometheus metrics server
# -------------------------------
start_http_server(8000, addr="0.0.0.0")
print(f"✅ Prometheus metrics server started on {socket.gethostbyname(socket.gethostname())}:8000")

training_loss_gauge = Gauge('training_loss', 'Training loss per epoch')
training_accuracy_gauge = Gauge('training_accuracy', 'Training accuracy per epoch')

# -------------------------------
# Device setup (Apple MPS or CPU)
# -------------------------------
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")

# -------------------------------
# Data preparation (CIFAR-10)
# -------------------------------
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

trainset = torchvision.datasets.CIFAR10(
    root='./data',
    train=True,
    download=True,
    transform=transform
)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)

# -------------------------------
# Model setup (ResNet18)
# -------------------------------
model = torchvision.models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 10)
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# -------------------------------
# MLflow experiment setup
# -------------------------------
mlflow.set_experiment("macos-mps-training")
mlflow.start_run()

# -------------------------------
# Training loop
# -------------------------------
epochs = 5
for epoch in range(epochs):
    running_loss = 0.0
    correct = 0
    total = 0

    for i, (inputs, labels) in enumerate(trainloader):
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    avg_loss = running_loss / len(trainloader)
    accuracy = 100 * correct / total

    # Log to MLflow
    mlflow.log_metric("loss", avg_loss, step=epoch)
    mlflow.log_metric("accuracy", accuracy, step=epoch)

    # Update Prometheus metrics
    training_loss_gauge.set(avg_loss)
    training_accuracy_gauge.set(accuracy)

    print(f"Epoch {epoch+1}/{epochs} | Loss: {avg_loss:.4f} | Accuracy: {accuracy:.2f}%")

# -------------------------------
# Save model to MLflow
# -------------------------------
# Use 'pickle' format for compatibility with PyTorch 2.x and MLflow 2.14+
mlflow.pytorch.log_model(
    model,
    name="model",
    serialization_format="pickle"
)

mlflow.end_run()
print("Training complete.")

