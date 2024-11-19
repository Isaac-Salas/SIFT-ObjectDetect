# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 17:48:52 2024

@author: Isok
"""

#import numpy as np
import cv2
from matplotlib import pyplot as plt



def training(objnum,view,trainpath):
    trainpath = path + (str(objnum))+'__'
    keypoints = []
    descriptors = []
    images = []
    for i in range(iterations):
        strview = str(view)
        newpath = trainpath + strview + ".png"
        #print(newpath)
        img = cv2.imread(newpath,0)
        kp1, des1 = orb.detectAndCompute(img,None)
        keypoints.append(kp1)
        descriptors.append(des1)
        images.append(img)
        view += 5
    return keypoints, descriptors, images


def compare(descriptorlist, descriptor):
    allmatches = []
    for i in descriptorlist:
        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        # Match descriptors.
        matches = bf.match(i,descriptor)
        # Sort them in the order of their distance.
        matches = sorted(matches, key = lambda x:x.distance)
        allmatches.append(matches)
    return allmatches

def drawMatches(imagelist, keypointlist, image, keypoints, matchlist, lable):
    newimages = []
    allpoints = 0
    allmatches = 0
    counter = 1
    
    for i, k, m in zip(imagelist,keypointlist, matchlist):
        #print('La imagen numero', counter, 'tiene', len(m), 'coincidencias de', len(k), 'Puntos')
        allmatches += len(m)
        allpoints += len(k)
        counter += 1
        newimg = cv2.drawMatches(i,k,image,keypoints, m, None, flags=2)
        newimages.append(newimg)
        
    #print('Todos los puntos:',allpoints,'//','Todas las coincidencias:', allmatches)
    percentage = (allmatches*100)/allpoints
    print('Esto es una', lable, 'con un', percentage, 'de seguridad')
    return newimages,percentage
        
def showMatches(imagelist):
    for i in imagelist:
        plt.imshow(i),plt.show()
        
def automate(comparenum,view, trainkey, traindes, trainimg, lable, show):
    comparepath = path + (str(comparenum))+'__'+str(view)+'.png'
    img1 = cv2.imread(comparepath,0)
    kp1, des1 = orb.detectAndCompute(img1,None)
    trmatch = compare(traindes,des1)
    FINALIMG, percentage = drawMatches(trainimg, trainkey, img1, kp1, trmatch, lable)
    if show == True:
        showMatches(FINALIMG)
    else:
        plt.imshow(img1),plt.show()
    return percentage,lable

def sortDict(dict1):
    sorted_values = sorted(dict1.values()) # Sort the values
    sorted_dict = {}
    for i in sorted_values:
        for k in dict1.keys():
            if dict1[k] == i:
                sorted_dict[k] = dict1[k]
    return sorted_dict
   
    
   
#Variables que componen el path
path = 'coil-100/obj'



#Numero de vista (Entrenar)
view : int = 0


#Numero en str de vista (Entrenar)
strview : str

#Path de entrenamiento y path de comparacion
trainpath = ''
comparepath = ''



# Initiate SIFT detector
orb = cv2.ORB_create()


#Variable para numero de imagenes usadas para entrenamiento
iterations = 10

# Entrenamos para 10 objetos: 
# 3 Barquitp Amarillo
# 7 Arizona
# 14 Gato de la suerte
# 17 Gato de hule
# 21 Objeto de cocina
# 28 Rana de hule
# 22 Desodorante
# 75 Fresa
# 74 Patito de hule
# 91 Carro amarillo

tomkey, tomdes, tomimg = training(3,view,trainpath)
arikey, arides, ariimg = training(7,view,trainpath)
gaskey, gasdes, gasimg = training(14,view,trainpath)
gahkey, gahdes, gahimg = training(17,view,trainpath)
cockey, cocdes, cocimg = training(21,view,trainpath)
rankey, randes, ranimg = training(28,view,trainpath)
sankey, sandes, sanimg = training(22,view,trainpath)
frekey, fredes, freimg = training(75,view,trainpath)
patkey, patdes, patimg = training(74,view,trainpath)
carkey, cardes, carimg = training(91,view,trainpath)
showimg = False


itlist = [[tomkey, tomdes, tomimg, 'Barquito Amarillo', showimg], 
          [arikey, arides, ariimg,'Arizona', showimg], 
          [gaskey, gasdes, gasimg,'Gato de la suerte', showimg], 
          [gahkey, gahdes, gahimg,'Gato de hule', showimg], 
          [cockey, cocdes, cocimg,'Objeto de cocina', showimg],
          [rankey, randes, ranimg,'Rana de hule', showimg],
          [sankey, sandes, sanimg,'Desodorante', showimg],
          [frekey, fredes, freimg,'Fresa', showimg],
          [patkey, patdes, patimg,'Patito de Hule', showimg],
          [carkey, cardes, carimg,'Carrito Amarillo', showimg],]


#Numero en str de vista (Comparar)
numview = 0
numobj = 28


porcentajes = {}
for i in itlist:
    porcentaje, nombre = automate(numobj, numview, *i)
    porcentajes[nombre] = porcentaje
    
porcentajesord = sortDict(porcentajes)

print('\n---------------------------------------\n\nEsto es un', list(porcentajesord)[9])



