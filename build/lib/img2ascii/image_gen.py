import numpy as np
import cv2 as cv
from random import random
import os, os.path

def generate_ascii_i(inputfile,outputfile,color=0,kernel=7,density=0.3,fancy=False):
    print('Generating ASCII image...')
    kernel=kernel
    density =density
    gscale = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
      
    fancy_dir = './fancy'
    fancy_num = len([name for name in os.listdir(fancy_dir) if os.path.isfile(os.path.join(fancy_dir, name))])
    #print(fancy_num)
    img_c = cv.imread(inputfile)
    img = cv.cvtColor(img_c,cv.COLOR_BGR2GRAY)
    r = img.shape[0]
    c = img.shape[1]
        
    r_o = int(r/kernel)
    c_o = int(c/kernel)
    
    if(fancy):
        img_fancy = cv.imread(os.path.join(fancy_dir,str(int((random()*fancy_num)+1))+'.jpg'))
        img_fancy = cv.resize(img_fancy,(c,r))
        color=2

    col_mode=""
    if(color==0):
        col_mode = "B/W"
    if(color==1):
        col_mode = "Gray"
    if(color==2):
        col_mode = "RGB"
    
    frame_title = outputfile+" | Color - "+col_mode+" | kernel_size - "+str(kernel)+"x"+str(kernel)+" | text_density - "+str(density)
        
    asci_scale= np.zeros(shape=(r_o,c_o))
        
    img_o= np.zeros_like(img_c)
            
    for i in range(0,r_o):
        for j in range(0,c_o):
            avg = np.mean(img[i*kernel:i*kernel+kernel,j*kernel:j*kernel+kernel])
            if(fancy):
                avg_c = np.mean(np.mean(img_fancy[i*kernel:i*kernel+kernel,j*kernel:j*kernel+kernel],axis=0),axis=0)
            else:
                avg_c = np.mean(np.mean(img_c[i*kernel:i*kernel+kernel,j*kernel:j*kernel+kernel],axis=0),axis=0)
            if color==0:
                avg_c = (255,255,255)
            elif color==1:
                #print(avg_c)
                avg_c = np.uint8([[[avg_c[0],avg_c[1],avg_c[2]]]])
                avg_c = cv.cvtColor(avg_c,cv.COLOR_BGR2GRAY)
                avg_c = (float(avg_c[0][0]),float(avg_c[0][0]),float(avg_c[0][0]))
                #print(avg_c)
            asci_scale[i][j] = avg
            gsval = gscale[int((avg*(len(gscale)-1))/255)]
            cv.putText(img_o,gsval,(j*kernel,i*kernel),cv.FONT_HERSHEY_SIMPLEX,density,avg_c,1) 
    
    cv.imshow(frame_title,img_o)
    cv.imwrite(outputfile,img_o)
    print('Ouput file saved : ',outputfile)
    print('')
    print('Press any key to close the window')
    key = cv.waitKey(0)
    if(key==27):
        cv.destroyAllWindows()
