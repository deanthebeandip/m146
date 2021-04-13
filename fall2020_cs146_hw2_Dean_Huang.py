# -*- coding: utf-8 -*-
"""Fall2020-CS146-HW2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SYlvOENWA9dCmsfmAKIaoVAvmJ4Joqxq
"""

# This code was adapted from course material by Jenna Wiens (UMichigan).

# python libraries
import os

# numpy libraries
import numpy as np

# matplotlib libraries
import matplotlib.pyplot as plt

# To add your own Drive Run this cell.
from google.colab import drive
drive.mount('/content/drive')

######################################################################
# classes
######################################################################


class Data:
    def __init__(self, X=None, y=None):
        """
        Data class.
        
        Attributes
        --------------------
            X       -- numpy array of shape (n,d), features
            y       -- numpy array of shape (n,), targets
        """

        # n = number of examples, d = dimensionality
        self.X = X
        self.y = y

    def load(self, filename):
        """
        Load csv file into X array of features and y array of labels.
        
        Parameters
        --------------------
            filename -- string, filename
        """


        # load data
        with open(filename, "r") as fid:
            data = np.loadtxt(fid, delimiter=",")

        # separate features and labels
        self.X = data[:, :-1]
        self.y = data[:, -1]

    def plot(self, **kwargs):
        """Plot data."""

        if "color" not in kwargs:
            kwargs["color"] = "b"

        plt.scatter(self.X, self.y, **kwargs)
        plt.xlabel("x", fontsize=16)
        plt.ylabel("y", fontsize=16)
        plt.show()

# wrapper functions around Data class
def load_data(filename):
    data = Data()
    data.load(filename)
    return data


def plot_data(X, y, **kwargs):
    data = Data(X, y)
    data.plot(**kwargs)

class PolynomialRegression:
    def __init__(self, m=1, reg_param=0):
        """
        Ordinary least squares regression.
        
        Attributes
        --------------------
            coef_   -- numpy array of shape (d,)
                       estimated coefficients for the linear regression problem
            m_      -- integer
                       order for polynomial regression
            lambda_ -- float
                       regularization parameter
        """

        # self.coef_ represents the weights of the regression model
        self.coef_ = None
        self.m_ = m
        self.lambda_ = reg_param

    def generate_polynomial_features(self, X):
        """
        Maps X to an mth degree feature vector e.g. [1, X, X^2, ..., X^m].
        
        Parameters
        --------------------
            X       -- numpy array of shape (n,1), features
        
        Returns
        --------------------
            Phi     -- numpy array of shape (n,(m+1)), mapped features
        """

        n, d = X.shape

        ### ========== TODO : START ========== ###
        # part b: modify to create matrix for simple linear model
        # part g: modify to create matrix for polynomial model

        #first assign m to the value self already has inside the class
        m = self.m_
        #the idea is X is currently a [n x d] sized matrix,
        #if #columns equals to the inherent m plus one, then keep as is
        #if not, then make Phi in the form of [1 X X^2... X^m]

        if d == (m + 1):
          Phi = X    
        else:
          Phi = np.ones_like(X)
          for i in range(1, m+1):
            Phi = np.concatenate((Phi, X**(i-1)), 1)


        ### ========== TODO : END ========== ###

        return Phi

    def fit_GD(self, X, y, eta = None, eps=0, tmax=10000, verbose = True):
        """
        Finds the coefficients of a {d-1}^th degree polynomial
        that fits the data using least squares batch gradient descent.
        
        Parameters
        --------------------
            X       -- numpy array of shape (n,d), features
            y       -- numpy array of shape (n,), targets
            eta     -- float, step size
            eps     -- float, convergence criterion
            tmax    -- integer, maximum number of iterations
            verbose -- boolean, for debugging purposes
        
        Returns
        --------------------
            self    -- an instance of self
        """
        if self.lambda_ != 0:
            raise Exception("GD with regularization not implemented")

        X = self.generate_polynomial_features(X)  # map features
        n, d = X.shape
        #changed this for part f
        eta_input = eta
        self.coef_ = np.zeros(d)  # coefficients
        err_list = np.zeros((tmax, 1))  # errors per iteration

        # GD loop
        for t in range(tmax):
            ### ========== TODO : START ========== ###

            # part f: update step size
            # change the default eta in the function signature to 'eta=None'
            # and update the line below to your learning rate function
            if eta_input is None:
                #pretty straight forward
                eta = 1/ (1 + float(t))
            else:
                eta = eta_input


            ### ========== TODO : END ==========  ###

            ### ========== TODO : START ========== ###
            # part d: update w (self.coef_) using one step of GD
            # hint: you can write simultaneously update all w using vector math
            # update the weights again for each t:
            # find the error matrix, then dot product that error matrix with X^T 
            # will be the change in weights
            self.coef_ = self.coef_ - (2 * eta * np.dot(np.transpose(X), (self.predict(X) - y )) )

            # track error
            # hint: you cannot use self.predict(...) to make the predictions
            y_pred = np.dot(X, self.coef_)  # change this line
            err_list[t] = np.sum(np.power(y - y_pred, 2)) / float(n)
            ### ========== TODO : END ========== ###

            # stop?
            if t > 0 and abs(err_list[t] - err_list[t - 1]) <= eps:
                break

            # debugging
            # debugging
            if verbose :
                x = np.reshape(X[:,1], (n,1))
                cost = self.cost(x,y)
                print ("iteration: %d, cost: %f" % (t+1, cost))
                

        print("number of iterations: %d" % (t + 1))
        print(self.coef_)

        return self

    def fit(self, X, y, l2regularize=None):
        """
        Finds the coefficients of a {d-1}^th degree polynomial
        that fits the data using the closed form solution.
        
        Parameters
        --------------------
            X       -- numpy array of shape (n,d), features
            y       -- numpy array of shape (n,), targets
            l2regularize    -- set to None for no regularization. set to positive double for L2 regularization
                
        Returns
        --------------------        
            self    -- an instance of self
        """

        X = self.generate_polynomial_features(X)  # map features

        ### ========== TODO : START ========== ###
        # part e: implement closed-form solution
        # hint: use np.dot(...) and np.linalg.pinv(...)
        #       be sure to update self.coef_ with your solution
        #this should produce the closed form weight vector
        self.coef_ = np.dot( np.linalg.pinv(np.dot(np.transpose(X), X )), np.dot(np.transpose(X), y ))
        print(self.coef_)


        ### ========== TODO : END ========== ###

    def predict(self, X):
        """
        Predict output for X.
        
        Parameters
        --------------------
            X       -- numpy array of shape (n,d), features
        
        Returns
        --------------------
            y       -- numpy array of shape (n,), predictions
        """
        if self.coef_ is None:
            raise Exception("Model not initialized. Perform a fit first.")

        X = self.generate_polynomial_features(X)  # map features

        ### ========== TODO : START ========== ###
        # part c: predict y
        #given that 
        y = np.dot(X, self.coef_)
        ### ========== TODO : END ========== ###

        return y

    def cost(self, X, y):
        """
        Calculates the objective function.
        
        Parameters
        --------------------
            X       -- numpy array of shape (n,d), features
            y       -- numpy array of shape (n,), targets
        
        Returns
        --------------------
            cost    -- float, objective J(w)
        """
        ### ========== TODO : START ========== ###
        # part d: compute J(w)
        # pretty simple, just add up all the square of differences
        # between the predicted y and the actual y...
        cost = np.sum((self.predict(X) - y)**2)

        ### ========== TODO : END ========== ###
        return cost

    def rms_error(self, X, y):
        """
        Calculates the root mean square error.
        
        Parameters
        --------------------
            X       -- numpy array of shape (n,d), features
            y       -- numpy array of shape (n,), targets
        
        Returns
        --------------------
            error   -- float, RMSE
        """
        ### ========== TODO : START ========== ###
        # part h: compute RMSE
        error = np.sqrt( self.cost(X,y) / np.shape(y))
        ### ========== TODO : END ========== ###
        return error

    def plot_regression(self, xmin=0, xmax=1, n=50, **kwargs):
        """Plot regression line."""
        if "color" not in kwargs:
            kwargs["color"] = "r"
        if "linestyle" not in kwargs:
            kwargs["linestyle"] = "-"

        X = np.reshape(np.linspace(0, 1, n), (n, 1))
        y = self.predict(X)
        plot_data(X, y, **kwargs)
        plt.show()

######################################################################
# main
######################################################################

def main():
    # load data with correct file path

    ### ========== TODO : START ========== ###
    data_directory_path =  "/content/drive/My Drive/Colab Notebooks/"
    ### ========== TODO : END ========== ###

    train_data = load_data(os.path.join(data_directory_path, "train.csv"))
    test_data = load_data(os.path.join(data_directory_path,"test.csv"))

    ### ========== TODO : START ========== ###
    # part a: main code for visualizations
    print("Visualizing data...")
    #plot_data(train_data, test_data, **kwargs)
    #plot_data(train_data.X, train_data.y)
    #plot_data(test_data.X, test_data.y)

    ### ========== TODO : END ========== ###

    ### ========== TODO : START ========== ###
    # parts b-f: main code for linear regression
    print("Investigating linear regression...")

    # part d, use what the question gave me...
    model = PolynomialRegression(1)
    model.coef_ = np.zeros(2)
    c = model.cost (train_data.X, train_data.y)
    print(f'model_cost:{c}')

    #part e and f:
    #model.fit(train_data.X, train_data.y)
    #model.fit_GD(train_data.X, train_data.y,  .001, 0, 10000, True )

    ### ========== TODO : END ========== ###

    ### ========== TODO : START ========== ###
    # parts g-i: main code for polynomial regression
    print("Investigating polynomial regression...")
    
    #part h
    #print("Model Error: ", model.rms_error(train_data.X, train_data.y))


    #part i
    # for m = 0 - 10, used closed form to find best model
    # on training data. then calculate RSME on training and testing
    # Plot both arrays on the axis
    
    #declare the empty arrays that we will populate soon
    index = []
    train_error = []
    test_error =  []

    for i in range(0,11):
        #We will populate the index first
        index.append(i)

        #Fit the model with Closed Form fit...
        model = PolynomialRegression(m = i)
        model.coef_ = np.zeros(2)
        model.fit(train_data.X, train_data.y)
        train_error.append(model.rms_error(train_data.X, train_data.y) )
        test_error.append(model.rms_error(test_data.X, test_data.y) )
        
        
    #graph all four arrays on the same plot with different colors with a legend
    plt.plot(index, train_error , 'r', label="Training Error")
    plt.plot(index, test_error  , 'g', label="Testing Error")
    plt.xlabel("M value")
    plt.ylabel("RMSE")
    labelsh = ["Training Error", "Testing Error" ]
    plt.legend(labelsh)
    plt.show()




    ### ========== TODO : END ========== ###

    print("Done!")

if __name__ == "__main__":
    main()