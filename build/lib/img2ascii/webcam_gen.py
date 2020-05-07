import numpy as np
import cv2 as cv

def generate_ascii_w(color,kernel,density,cam_source):
    kernel=kernel
    density =density
    gscale = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    cam = cv.VideoCapture(cam_source)
    ret=True
    
    print('Press Esc to exit')
    while(ret):
        ret, img_c = cam.read()
        img_c = cv.flip(img_c,1)
        img = cv.cvtColor(img_c,cv.COLOR_BGR2GRAY)
        r = img.shape[0]
        c = img.shape[1]
        
        r_o = int(r/kernel)
        c_o = int(c/kernel)
        
        asci_scale= np.zeros(shape=(r_o,c_o))
        
        img_o= np.zeros_like(img)
        if color ==2:
            img_o = cv.cvtColor(img_o,cv.COLOR_GRAY2BGR)
            
        for i in range(0,r_o):
            for j in range(0,c_o):
                avg = np.mean(img[i*kernel:i*kernel+kernel,j*kernel:j*kernel+kernel])
                if color in (1,2):
                    avg_c = np.mean(np.mean(img_c[i*kernel:i*kernel+kernel,j*kernel:j*kernel+kernel],axis=0),axis=0)
                else:
                    avg_c = (255,255,255)
                #print(avg_c)
                asci_scale[i][j] = avg
                gsval = gscale[int((avg*69)/255)]
                cv.putText(img_o,gsval,(j*kernel,i*kernel),cv.FONT_HERSHEY_SIMPLEX,density,avg_c,1) 
        
        cv.imshow('IMG2ASCII',img_o)
        key = cv.waitKey(10)
        if(key==27):
            break
    cam.release()
    cv.destroyAllWindows()
        
