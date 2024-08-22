from csv import reader
from os import walk
import pygame

def csv_tolist(path):
    with open(path) as csv_file:
        floor = list()
        file = reader(csv_file, delimiter=',')
        for row in file:
            floor.append(list(row))
        return floor
    
def import_folder(path):
    fol_list = []
    for _, _, folder in walk(path):
        for p in folder:
            img = pygame.image.load(path + "/" + p).convert_alpha()
            fol_list.append(img)
    return fol_list