import numpy as np
import cv2 as cv
import os, os.path

def generate_ascii_t(inputfile,outputfile,kernel=7,density=0.3):
    print('Generating ASCII text...')
    kernel=kernel
    density =density
    gscale = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    
    img_c = cv.imread(inputfile)
    img = cv.cvtColor(img_c,cv.COLOR_BGR2GRAY)
    r = img.shape[0]
    c = img.shape[1]
        
    r_o = int(r/kernel)
    c_o = int(c/kernel)
        
    asci_scale= np.zeros(shape=(r_o,c_o))
    w=""
    
    for i in range(0,r_o):
        for j in range(0,c_o):
            avg = np.mean(img[i*kernel:i*kernel+kernel,j*kernel:j*kernel+kernel])
            asci_scale[i][j] = avg
            gsval = gscale[int((avg*(len(gscale)-1))/255)]
            w=w+gsval
        w=w+"\n"

    file = open(outputfile,'w')
    file.write(w)
    file.close()
    print('Ouput file saved : ',outputfile)
