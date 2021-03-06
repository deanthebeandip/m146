# -*- coding: utf-8 -*-
"""Fall2020-CS146-HW3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b77itO0BZ1pauQbvVxLt5EKbBJWj2Pds
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch.utils.data import TensorDataset, DataLoader
from PIL import Image

# To add your own Drive Run this cell.
from google.colab import drive
drive.mount('/content/drive')

######################################################################
# OneLayerNetwork
######################################################################

class OneLayerNetwork(torch.nn.Module):
    def __init__(self):
        super(OneLayerNetwork, self).__init__()

        ### ========== TODO : START ========== ###
        ### part d: implement OneLayerNetwork with torch.nn.Linear
        #In: number of pixels, Out: y classes: {0, 1, 2}
        self.L1 = torch.nn.Linear(784, 3, bias = True)
        ### ========== TODO : END ========== ###

    def forward(self, x):
        # x.shape = (n_batch, n_features)

        ### ========== TODO : START ========== ###
        ### part d: implement the foward function
        outputs = self.L1(x)
        ### ========== TODO : END ========== ###
        return outputs

######################################################################
# TwoLayerNetwork
######################################################################

class TwoLayerNetwork(torch.nn.Module):
    def __init__(self):
        super(TwoLayerNetwork, self).__init__()
        ### ========== TODO : START ========== ###
        ### part g: implement TwoLayerNetwork with torch.nn.Linear

        #create two layers, one for 784->400, one for 400->3
        self.L1 = torch.nn.Linear(784, 400, bias = True)
        self.L2 = torch.nn.Linear(400, 3, bias = True)
      
        ### ========== TODO : END ========== ###

    def forward(self, x):
        # x.shape = (n_batch, n_features)

        ### ========== TODO : START ========== ###
        ### part g: implement the foward function

        #this was a little confusing, after a while I realized the weights
        #of the output of layer 1 also had to be sigmoided...
        outputs = self.L2(torch.sigmoid(self.L1(x)))
        ### ========== TODO : END ========== ###
        return outputs

# load data from csv
# X.shape = (n_examples, n_features), y.shape = (n_examples, )
def load_data(filename):
    data = np.loadtxt(filename)
    y = data[:, 0].astype(int)
    X = data[:, 1:].astype(np.float32) / 255
    return X, y

# plot one example
# x.shape = (features, )
def plot_img(x):
    x = x.reshape(28, 28)
    img = Image.fromarray(x*255)
    plt.figure()
    plt.imshow(img)
    return

def evaluate_loss(model, criterion, dataloader):
    model.eval()
    total_loss = 0.0
    for batch_X, batch_y in dataloader:
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        total_loss += loss.item()
        
    return total_loss / len(dataloader)

def evaluate_acc(model, dataloader):
    model.eval()
    total_acc = 0.0
    for batch_X, batch_y in dataloader:
        outputs = model(batch_X)
        predictions = torch.argmax(outputs, dim=1)
        total_acc += (predictions==batch_y).sum()
        
    return total_acc / len(dataloader.dataset)

def train(model, criterion, optimizer, train_loader, valid_loader):
    train_loss_list = []
    valid_loss_list = []
    train_acc_list = []
    valid_acc_list = []
    for epoch in range(1, 31):
        model.train()
        for batch_X, batch_y in train_loader:
            ### ========== TODO : START ========== ###
            ### part f: implement the training process
            #set weights to 0
            optimizer.zero_grad()
            #calculate Loss
            loss = criterion(model(batch_X), batch_y)
            #loss backwards
            loss.backward()
            #update step
            optimizer.step()
            
            ### ========== TODO : END ========== ###
            train_loss = evaluate_loss(model, criterion, train_loader)
            valid_loss = evaluate_loss(model, criterion, valid_loader)
            train_acc = evaluate_acc(model, train_loader)
            valid_acc = evaluate_acc(model, valid_loader)
            train_loss_list.append(train_loss)
            valid_loss_list.append(valid_loss)
            train_acc_list.append(train_acc)
            valid_acc_list.append(valid_acc)

        print(f"| epoch {epoch:2d} | train loss {train_loss:.6f} | train acc {train_acc:.6f} | valid loss {valid_loss:.6f} | valid acc {valid_acc:.6f} |")

    return train_loss_list, valid_loss_list, train_acc_list, valid_acc_list

######################################################################
# main
######################################################################

def main():

    # fix random seed
    np.random.seed(0)
    torch.manual_seed(0)

    # load data with correct file path

    ### ========== TODO : START ========== ###
    data_directory_path =  "/content/drive/My Drive/Colab Notebooks/"
    ### ========== TODO : END ========== ###

    # X.shape = (n_examples, n_features)
    # y.shape = (n_examples, )
    X_train, y_train = load_data(os.path.join(data_directory_path, "hw3_train.csv"))
    X_valid, y_valid = load_data(os.path.join(data_directory_path, "hw3_valid.csv"))
    X_test, y_test = load_data(os.path.join(data_directory_path, "hw3_test.csv"))

    ### ========== TODO : START ========== ###
    ### part a: print out three training images with different labels
    #plot_img(X_train[0])
    #plot_img(X_train[1])
    #plot_img(X_train[2])
    
    ### ========== TODO : END ========== ###

    print("Data preparation...")

    ### ========== TODO : START ========== ###
    ### part b: convert numpy arrays to tensors
    #just turn all of them to tensors
    X_train = torch.from_numpy(X_train)
    y_train = torch.from_numpy(y_train)
    X_valid = torch.from_numpy(X_valid)
    y_valid = torch.from_numpy(y_valid)
    X_test = torch.from_numpy(X_test)
    y_test = torch.from_numpy(y_test)



    
    ### ========== TODO : END ========== ###

    ### ========== TODO : START ========== ###
    ### part c: prepare dataloaders for training, validation, and testing
    ###         we expect to get a batch of pairs (x_n, y_n) from the dataloader
    #first put the dataset together, then load the data...
    train_loader = torch.utils.data.DataLoader(dataset=TensorDataset(X_train, y_train), batch_size = 10, shuffle=False)
    valid_loader = torch.utils.data.DataLoader(dataset=TensorDataset(X_valid, y_valid), batch_size= 10, shuffle=False)
    test_loader = torch.utils.data.DataLoader(dataset=TensorDataset(X_test, y_test), batch_size= 10, shuffle=False)

    
    ### ========== TODO : END ========== ###

    ### ========== TODO : START ========== ###
    ### part e: prepare OneLayerNetwork, criterion, and optimizer
    #just assign model one to the right model, add criterions, and then we can assign our optimizer to the right one
    model_one = OneLayerNetwork()
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model_one.parameters(), lr = .0005)
    
    ### ========== TODO : END ========== ###

    print("Start training OneLayerNetwork...")
    results_one = train(model_one, criterion, optimizer, train_loader, valid_loader)
    print("Done!")

    ### ========== TODO : START ========== ###
    ### part h: prepare TwoLayerNetwork, criterion, and optimizer
    ### model_two = ...
    ### criterion = ...
    ### optimizer = ...
    model_two = TwoLayerNetwork()
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model_two.parameters(), lr = .0005)

    ### ========== TODO : END ========== ###

    print("Start training TwoLayerNetwork...")
    results_two = train(model_two, criterion, optimizer, train_loader, valid_loader)
    print("Done!")

    one_train_loss, one_valid_loss, one_train_acc, one_valid_acc = results_one
    two_train_loss, two_valid_loss, two_train_acc, two_valid_acc = results_two

    ### ========== TODO : START ========== ###
    ### part i: generate a plot to comare one_train_loss, one_valid_loss, two_train_loss, two_valid_loss
    plt.plot(one_train_loss , 'r', label="one_train_loss")
    plt.plot(one_valid_loss , 'g', label="one_valid_loss")
    plt.plot(two_train_loss , 'b', label="two_train_loss")
    plt.plot(two_valid_loss , 'y', label="two_valid_loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    labelsh = ["one_train_loss", "one_valid_loss", "two_train_loss", "two_valid_loss" ]
    plt.legend(labelsh)
    plt.show()

    ### ========== TODO : END ========== ###

    ### ========== TODO : START ========== ###
    ### part j: generate a plot to comare one_train_acc, one_valid_acc, two_train_acc, two_valid_acc
    plt.plot(one_train_acc , 'r', label="one_train_acc")
    plt.plot(one_valid_acc , 'g', label="one_valid_acc")
    plt.plot(two_train_acc , 'b', label="two_train_acc")
    plt.plot(two_valid_acc , 'y', label="two_valid_acc")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    labelsh = ["one_train_acc", "one_valid_acc", "two_train_acc", "two_valid_acc"]
    plt.legend(labelsh)
    plt.show()
    
    ### ========== TODO : END ========== ##

    ### ========== TODO : START ========== ###
    ### part k: calculate the test accuracy

    test_acc_m1 = evaluate_acc(model_one, test_loader)
    test_acc_m2 = evaluate_acc(model_two, test_loader)

    print("Test model 1 accuracy is:",  test_acc_m1 )
    print("Test model 2 accuracy is:",  test_acc_m2 )
    



    
    ### ========== TODO : END ========== ###

    ### ========== TODO : START ========== ###
    ### part l: replace the SGD optimizer with the Adam optimizer and do the experiments again
    
    ### ========== TODO : END ========== ###



if __name__ == "__main__":
    main()