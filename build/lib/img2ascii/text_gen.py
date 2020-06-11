##
##img2ascii
##
##Authors:
## Gopalji Gaur <gopaljigaur@gmail.com>
##
##Copyright (c) 2020 Gopalji Gaur
##
##Permission is hereby granted, free of charge, to any person obtaining a copy
##of this software and associated documentation files (the "Software"), to deal
##in the Software without restriction, including without limitation the rights
##to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##copies of the Software, and to permit persons to whom the Software is
##furnished to do so, subject to the following conditions:
##
##The above copyright notice and this permission notice shall be included in all
##copies or substantial portions of the Software.
##
##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##SOFTWARE.
##

import os, os.path
import cv2 as cv
import numpy as np

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
