from scipy import*
from matplotlib import pyplot as plt
from imageio import*
import numpy as np


class ImageRestoration:
    
    def __init__(self, img, mask):
        
        self.image=self.loadimage(img)
        self.original=self.image.copy()
        self.mask=self.loadmask(mask)
                
    
    def loadimage(self, img, gs=0):
        #add grayscale conversion in if
        return imread(img, as_gray=1)
    
    def loadmask(self, img):
        #add mask conditions
        return imread(img, pilmode='F')
    
    def showimage(self):
        plt.figure()
        plt.imshow(self.image, cmap='gray')
    
    def showmask(self):
        plt.figure()
        plt.imshow(self.mask, cmap='gray')
        
    def showoriginal(self):
        plt.figure()
        plt.imshow(self.original, cmap='gray')
        
    def __analyzemask(self, m):
        D_ind=[]
        for i in range(shape(m)[0]):
            for j in range(shape(m)[1]):
                if m[i, j]!=255:
                    D_ind.append([i, j])
        return array(D_ind)

    def __EulerStep(self,D_ind, u, D, h, a=1):
        #Problem with mask-points at the border of the frame 
        for ind in D_ind:

            u[ind[0], ind[1]]+=D*h/a**2*(u[ind[0]-1, ind[1]]+u[ind[0]+1, ind[1]]+u[ind[0], ind[1]-1]+u[ind[0], ind[1]+1]-4*u[ind[0], ind[1]])
        return u
    def restore(self):
        D_ind=self.__analyzemask(self.mask)
        u=self.image
        u_p=u.copy()

        u=self.__EulerStep(D_ind, u, 1, 0.1)
        while any(u!=u_p):
            print(1)
            u_p=u.copy()
            u=self.__EulerStep( D_ind, u, 1, 0.1)
        plt.figure()
        plt.imshow(u, cmap='gray')
        
imgres=ImageRestoration('flower_destroyed.jpg','Mask1.jpg')
imgres.restore()
    