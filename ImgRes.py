from scipy import*
from matplotlib import pyplot as plt
from imageio import*
import numpy as np


class ImageRestoration:
    
    def __init__(self, img, mask):
        
        self.image=self.loadimage(img)
        self.mask=self.loadmask(mask)
                
    
    def loadimage(self, img, gs=0):
        #add grayscale conversion in if
        return imread(img, pilmode='F')
    
    def loadmask(self, img):
        #add mask conditions
        return imread(img, pilmode='F')
    
    def showimage(self):
        plt.imshow(img)
    
    def showmask(self):
        plt.imshow(mask)
        
    def analyzemask(self, m):
        D_ind=[]
        for i in range(shape(m)[0]):
            for j in range(shape(m)[1]):
                if m[i, j]!=0:
                    Dind.append([i, j])
        return D_ind

#    def __Euler(self, u, D, h, a):
#        
#        for i in range(shape(u)[0]):
#            for j in range(shape(u)[1]):
#                u[i, j]+=D*h/a**2*(u[i-1, j]+u[i+1, j]+u[i, j-1]+u[i, j+1]-(4-B)*u[i,j])
# 
#       return u