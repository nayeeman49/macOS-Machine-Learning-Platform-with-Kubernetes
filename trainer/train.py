import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import mlflow
import mlflow.pytorch

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64, shuffle=True)

model = torchvision.models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, 10)
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

mlflow.set_experiment("macos-mps-training")
mlflow.start_run()

epochs = 5
for epoch in range(epochs):
    running_loss = 0.0
    for i, (inputs, labels) in enumerate(trainloader):
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    avg_loss = running_loss / len(trainloader)
    mlflow.log_metric("loss", avg_loss, step=epoch)
    print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")

mlflow.pytorch.log_model(model, "model")
mlflow.end_run()
print("Training complete.")
