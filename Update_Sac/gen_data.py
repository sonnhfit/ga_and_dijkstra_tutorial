import csv
import random
from random import randint

array_label = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'l', 'm', 'n','p', 'v', 'o', 'i', 'u', 'y', 't', 'r', 'e', 'w', 'q', 's', 'x', 'z']


def choice_to(array, from_el):
    while True:
        if random.choice(array_label) != from_el:
            return from_el

solanlap = 10

with open('data.csv', mode='w') as csv_file:
    fieldnames = ['from', 'to', 'cost']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for i in range(solanlap):
        pre_choice = random.choice(array_label)
        writer.writerow({'from': pre_choice, 'to': choice_to(array_label, pre_choice), 'cost': randint(2, 90)})
