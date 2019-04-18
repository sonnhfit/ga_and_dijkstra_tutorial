import numpy as np
import pandas as pd
import csv
import random
from random import randint

array_label = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'l', 'm', 'n','p', 'v', 'o', 'i', 'u', 'y', 't', 'r', 'e', 'w', 'q', 's', 'x', 'z']

random.seed(9001)


def choice_to(array, from_el):
    while True:
        rd = random.choice(array)
        if rd != from_el:
            return rd

solanlap = 10
ar = []
for i in range(solanlap):
    pre_choice = random.choice(array_label)
    pre2_choice = choice_to(array_label, pre_choice)
    rdint = randint(2, 90)
    sub_ar = [pre_choice, pre2_choice, rdint]
    ar.append(sub_ar)

# Creating a 2 dimensional numpy array
data= np.array(ar)

#Creating pandas dataframe from numpy array
dataset = pd.DataFrame({'from':data[:,0],'to':data[:,1], 'cost': data[:, 2]})
dataset.to_csv('data.csv', index=None, )
print('oke')
