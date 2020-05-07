import numpy as np
import cv2 as cv

def generate_ascii_i(color,kernel,density,inputfile,outputfile):
    print('')
    print('Generating ASCII image...')
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
        
    img_o= np.zeros_like(img_c)
            
    for i in range(0,r_o):
        for j in range(0,c_o):
            avg = np.mean(img[i*kernel:i*kernel+kernel,j*kernel:j*kernel+kernel])
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
            gsval = gscale[int((avg*69)/255)]
            cv.putText(img_o,gsval,(j*kernel,i*kernel),cv.FONT_HERSHEY_SIMPLEX,density,avg_c,1) 
    
    cv.imshow('IMG2ASCII',img_o)
    cv.imwrite(outputfile,img_o)
    print('Ouput file saved : ',outputfile)
    print('')
    print('Press any key to close the window')
    key = cv.waitKey(0)
    if(key==27):
        cv.destroyAllWindows()
