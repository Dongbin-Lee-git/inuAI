# ## Dataset과 DataLoader를 이용한 Digit classifier 학습

# ### 손글씨 숫자 데이터 분류

import torch
from torch import nn, optim
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt

digits = load_digits()

X = digits.data
print(type(X))
print(X.shape)

y = digits.target
print(type(y))
print(y.shape)
print(y)

# ### 학습과 테스트 데이터 분류

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=True)

print('Type: x_train, y_train, x_test, y_test')
print(type(x_train), type(y_train), type(x_test), type(y_test))

print('Shape: x_train, y_train, x_test, y_test')
print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

# #### Tensor로 변환

x_train = torch.tensor(x_train, dtype=torch.float).to('cuda')
y_train = torch.tensor(y_train, dtype=torch.long).to('cuda')
x_test = torch.tensor(x_test, dtype=torch.float).to('cuda')
y_test = torch.tensor(y_test, dtype=torch.long).to('cuda')

# ### TensorDataset과 Dataloader를 이용

# #### Dataset을 만든다. (비유: 약수물을 정수기 통에 담는다.)

from torch.utils.data import TensorDataset, DataLoader

train_dataset = TensorDataset(x_train, y_train)
test_dataset = TensorDataset(x_test, y_test)

print(train_dataset)
print(test_dataset)

# #### Dataloader를 만든다. (비유: 정수기 물통에 냉수 파이프와 온수 파이프를 설치한다)

train_dataloader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=10000, shuffle=True)

print(train_dataloader)
print(test_dataloader)

# #### 학습을 위한 모델, Loss, Optimizer 설정

net = nn.Linear(64, 10)
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.01)

# #### 학습 시작

losses = []
net.train()
net.to('cuda')

for epoc in range(200):

  batch_loss = 0.0

  for x_train, y_train in train_dataloader:
    
    optimizer.zero_grad()

    y_pred = net(x_train)
    # print('y_pred size: ', y_pred.size())
    loss = loss_fn(y_pred, y_train)
    loss.backward()

    optimizer.step()
    batch_loss += loss.item()
  losses.append(batch_loss)
  print(epoc, ' Loss: ', batch_loss)

# #### 학습 과정 중의 loss visualization

plt.plot(losses)

# #### 테스트 시작

net.eval()

with torch.no_grad():

  for x_test, y_test in test_dataloader:
    test_result = net(x_test)
    pred = torch.argmax(test_result, dim=1)

    num_correct = (pred == y_test).sum().item()
    print('Accuracy: ', num_correct*100.0/len(y_test), '%')

