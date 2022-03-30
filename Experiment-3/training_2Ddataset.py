import torch
import torch.nn as nn
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import logging
import numpy as np
import warnings
warnings.filterwarnings('always')
import dataset_2D_generator
from collections import OrderedDict
from torch.nn import functional as F

class Model2D(torch.nn.Module):
    def __init__(self):
        super(Model2D, self).__init__()
        weight = torch.randn(1, 3, 100, 100)
        self.weight = torch.nn.Parameter(weight)
        torch.nn.init.kaiming_normal_(self.weight)

    def forward(self, x):
        # img = torch.randn(3, 3, 10, 10)
        # conv = F.conv2d(self.weight, img, stride=10)
        # sum = torch.sum(conv, dim=[0, 2, 3]).reshape(1, 3)
        # prediction = torch.sigmoid(sum)
        # print(prediction)
        # return prediction

        x = x[0].view(1, 1, 10, 10).repeat(3, 3, 1, 1) #one image. how to get the kernel to (3, 3, 10, 10)
        output = F.conv2d(self.weight, x, stride=10)
        print(output.shape)
        sum = torch.sum(output, dim=[0, 2, 3]).reshape(1, 3)
        prediction = torch.sigmoid(sum)
        print(prediction)
        return prediction

def load_dataset():
    samples, targets = dataset_2D_generator.main()
    shuffled_indices = np.random.permutation(samples.shape[0])
    shuffled_samples = samples[shuffled_indices]
    shuffled_targets = targets[shuffled_indices]

    train_size = int(0.7 * len(shuffled_samples))
    validation_size = train_size + int(0.2 * len(shuffled_samples))

    X_train, y_train = shuffled_samples[:train_size], shuffled_targets[:train_size]
    X_validation, y_validation = shuffled_samples[train_size:validation_size], shuffled_targets[train_size:validation_size]
    X_test, y_test = shuffled_samples[validation_size:], shuffled_targets[validation_size:]

    return {"train": dict(X=torch.Tensor(X_train), y=torch.Tensor(y_train)),
            "test": dict(X=torch.Tensor(X_test), y=torch.Tensor(y_test)),
            "validation": dict(X=torch.Tensor(X_validation), y=torch.Tensor(y_validation))}


def train(model,criterion,optimizer,X,y):
    model.train()
    y_pred = model(X)
    loss = criterion(y_pred, y)
    loss.backward()  # backprop (compute gradients)
    optimizer.step()  # update weights (gradient descent step)
    optimizer.zero_grad()  # reset gradients
    return loss


def test(model,criterion,X,y,validation):
    model.eval()
    with torch.no_grad():
        y_pred = model(X)  # forward step
        if validation:
            eval_metric = criterion(y_pred, y)  # compute loss
            return eval_metric
        else:
            y_pred = torch.argmax(y_pred,dim=1)
            return y_pred

def main():
    torch.manual_seed(696)
    data = load_dataset()

    X_train, y_train = data['train']['X'], data['train']['y'].type(torch.LongTensor)
    X_validation, y_validation = data['validation']['X'], data['validation']['y'].type(torch.LongTensor)
    X_test, y_test = data['test']['X'], data['test']['y'].type(torch.LongTensor)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    lr = 5e-2  # Learning rate

    model = Model2D().to(device)

    criterion = torch.nn.CrossEntropyLoss()  # loss function
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)  # optimizer

    # training the model for 1000 epochs
    optimum_training_loss = float('inf')
    optimum_validation_loss = float('inf')

    for epoch in range(100):
        training_loss = train(model,criterion,optimizer,X_train,y_train)
        validation_loss = test(model,criterion,X_validation,y_validation,validation=True)
        print(f'training loss: {training_loss}, validation loss:{validation_loss}')
        if training_loss < optimum_training_loss and validation_loss < optimum_validation_loss:
            optimum_validation_loss = validation_loss
            optimum_training_loss = training_loss
            torch.save(model.state_dict(), "./models/2D_model" + ".pt")

    model.load_state_dict(torch.load("./models/2D_model" + ".pt"))
    preds = test(model,criterion,X_test,y_test,validation=False)
    print(f'Test accuracy: {accuracy_score(y_test,preds)}')

if __name__ == '__main__':
    main()