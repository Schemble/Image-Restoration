from scipy import*
from matplotlib import pyplot as plt
from imageio import*
import numpy as np
import time

class ImageRestoration:
    
    def __init__(self, org, img, mask):
        
        self.image=self.loadimage(img)
        self.destroyed=self.image.copy()
        self.mask=self.loadmask(mask)
        self.original=self.loadimage(org)
    
    def loadimage(self, img, gs=0):
        #add grayscale conversion in if
        return imread(img, as_gray=1)
    
    def loadoriginal(self, img, gs=0):
        #add grayscale conversion in if
        return imread(img, as_gray=1)
    
    def loadmask(self, img):
        #add mask conditions
        return imread(img, as_gray=1)
    
    def showimage(self):
        plt.figure()
        plt.imshow(self.image, cmap='gray')
        
    
    def showmask(self):
        plt.figure()
        plt.imshow(self.mask, cmap='gray')
        
    def showoriginal(self):
        plt.figure()
        plt.imshow(self.original, cmap='gray')
        
    def __analyzemask(self, m, S):
        if S==True:
            
            '''
            Work in process
            '''
            t1=time.process_time()
            s=where(m!=255)
            
            s=array(s).T
            t2=time.process_time()-t1

            #sM=repeat(s[:, newaxis], len(s), axis=1)
            #print(sM)
            '''
            '''
#            s=[]
#            for i in range(shape(m)[0]):
#                for j in range(shape(m)[1]):
#                    if m[i, j]!=255:
#                        s.append([i, j])
#                    
#                    k+=1
            print(time.process_time()-t2)
            A=zeros([len(s), len(s)])
            b=zeros([len(s)])
            '''
            '''
            
#            #diff=sM-s[:,None]
#            print(diff)
#            #A[where(sum(diff*diff, axis=1)==1)]=1
#            print('woohoo')
##            for n, i in enumerate(s):
##                A[n, n]=-4
##                A[n,where(sum((s-s[n])*((s-s[n])), axis=1)==1)]=1
##                #print(n)

            '''
            '''
            for n, i in enumerate(s):
                A[n, n]=-4
                if ((s==i+[1,0]).all(axis=1)).any():
                    A[n, where((s==i+[1,0]).all(axis=1))]=1
                else:
                    b[n]-=self.image[i[0]+1, i[1]]
                if ((s==i-[1,0]).all(axis=1)).any():
                    A[n, where((s==i-[1,0]).all(axis=1))]=1
                else:
                    b[n]-=self.image[i[0]-1, i[1]]
                if ((s==i+[0,1]).all(axis=1)).any():
                    A[n, where((s==i+[0,1]).all(axis=1))]=1
                else:
                    b[n]-=self.image[i[0],i[1]+1]
                if ((s==i-[0,1]).all(axis=1)).any():
                    A[n, where((s==i-[0,1]).all(axis=1))]=1
                else:
                    b[n]-=self.image[i[0], i[1]-1]
            print('A done:', time.process_time()-t0)
            return s, matrix(A), b
        else:
            D_ind=[]
            for i in range(shape(m)[0]):
                for j in range(shape(m)[1]):
                    if m[i, j]!=255:
                        D_ind.append([i, j])
            return array(D_ind)

    def __EulerStep(self,D_ind, u, D, h, a=1):
        #Problem with mask-points at the border of the frame 
        u_next=u.copy()
        for ind in D_ind:
            u_next[ind[0], ind[1]]+=D*h/a**2*(u[ind[0]-1, ind[1]]+u[ind[0]+1, ind[1]]+u[ind[0], ind[1]-1]+u[ind[0], ind[1]+1]-4*u[ind[0], ind[1]])
        return u_next
    def Restore(self, method):
        if method=='Euler':
            D_ind=self.__analyzemask(self.mask, S=0)
            u=self.image
            u_p=u.copy()
    
            u=self.__EulerStep(D_ind, u, 1, 0.1)
            while any(u!=u_p):
                u_p=u.copy()
                u=self.__EulerStep( D_ind, u, 1, 0.1)

            plt.figure()
            plt.imshow(u, cmap='gray')
            self.__chi2(D_ind)
        if method=='CN':
            s, A, b=self.__analyzemask(self.mask, S=1)
            u=array([self.image[i, j] for i, j in s])
            
            C=1     #C=D*h/a**2

            M=identity(len(u))+C/2*A
            invM=(identity(len(u))-C/2*A).I
            print('Matrices done:', time.process_time()-t0)
            u_p=u.copy()
            u=self.__CNStep(u,invM, M, b, C)
            print(shape(u))
            while any(abs(u-u_p)>1e-3):
                u_p=u.copy()
                u=self.__CNStep(u, invM, M, b, C)
            n=0
            for i, j in s:                   
                self.image[i, j]=u[n] 
                n+=1
            plt.figure()
            plt.imshow(self.image, cmap='gray')
            self.__chi2(s)
    def __CNStep(self, u, invM, M, b, C):
        return (dot(invM, (dot(M, u)-C*b).T)).A1
        
    
    def __chi2(self, D_ind):
        n=len(D_ind)
        sum1=sum((self.image-self.original)**2)
        mean=0
        for ind in D_ind:
            mean+=self.original[ind[0], ind[1]]/n
        sum2=sum((self.original-mean)**2)
        chi2=(1/n*sum1)/(1/(n-1)*sum2)
        print(chi2)
        
        
t0=time.process_time()
imgres=ImageRestoration('bird_original.jpg', 'bird_broad.jpg','bird_maskbroad.jpg')

#imgres=ImageRestoration('flower_original.jpg', 'flower_destroyed.jpg','flower_mask1.jpg')
#imgres.showimage()
imgres.Restore('CN')
print('All done:',time.process_time()-t0)
#CN=imgres.image
#imgres=ImageRestoration('bird_original.jpg', 'bird_broad.jpg','bird_maskbroad.jpg')
#imgres.Restore('Euler')
#euler=imgres.image