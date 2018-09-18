from scipy import*
from matplotlib import pyplot as plt
from imageio import*

pic=imread('flower_original.jpg')


class ImageResoration:
    
    def __init__(self, img, mask):
        
        self.image=self.loadimage(img)
        self.mask=self.loadmask(mask)
                
    def load(self, img):
        img=imread(img)
        return img
    
    def loadimage(self, img, gs=0):
        #add grayscale conversion in if
        return imread(img)
    
    def loadmask(self, img):
        #add mask conditions
        return imread(img)
    
    def showimage(self):
        plt.imshow(img)
    
    def showmask(self):
        plt.imshow(mask)