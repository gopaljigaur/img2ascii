import numpy as np
import cv2 as cv
import os, os.path
from random import random

def generate_ascii_v(inputfile,outputfile,color=0,kernel=7,density=0.3,fancy=False):
    kernel=kernel
    density =density
    inputfile = inputfile
    outputfile = outputfile
    gscale = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    vid = cv.VideoCapture(inputfile)

    ret, frame = vid.read()
    
    fancy_dir = './fancy'
    fancy_num = len([name for name in os.listdir(fancy_dir) if os.path.isfile(os.path.join(fancy_dir, name))])
    #print(fancy_num)
    
    FrameSize=(frame.shape[1], frame.shape[0])
    fourcc = cv.VideoWriter_fourcc(*'MJPG')
    fps = float(vid.get(cv.CAP_PROP_FPS))
    frames = int(vid.get(cv.CAP_PROP_FRAME_COUNT))
    print('Total frames to process : ',frames)
    
    output = cv.VideoWriter(outputfile, fourcc, fps, FrameSize,1)

    #print(fps)
    print('Converting video...')
    print('Press q to stop')
    print('')
    print('Percentage complete :')

    if(fancy):
        img_fancy = cv.imread(os.path.join(fancy_dir,str(int((random()*fancy_num)+1))+'.jpg'))
        img_fancy = cv.resize(img_fancy,FrameSize)
        color=2

    col_mode=""
    if(color==0):
        col_mode = "B/W"
    if(color==1):
        col_mode = "Gray"
    if(color==2):
        col_mode = "RGB"
    
    frame_title = outputfile+" | Color - "+col_mode+" | kernel_size - "+str(kernel)+"x"+str(kernel)+" | text_density - "+str(density)
    
    
    n_frames = 0
    prev_per=0
    while(vid.isOpened()):
        ret, frame = vid.read()
        n_frames=n_frames+1
        per = int((n_frames/frames)*100)
        if(per!=prev_per):
            print(str(int((n_frames/frames)*100)),end='%\n')
            prev_per=per
        if not ret: break
        img = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        r = img.shape[0]
        c = img.shape[1]
        
        r_o = int(r/kernel)
        c_o = int(c/kernel)
        
        asci_scale= np.zeros(shape=(r_o,c_o))
        img_o= np.zeros_like(frame)
        #if color ==2:
        #    img_o = cv.cvtColor(img_o,cv.COLOR_GRAY2BGR)
            
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
        #if color==1:
        #    img_o = cv.cvtColor(img_o,cv.COLOR_BGR2GRAY)
        output.write(img_o)
        cv.imshow(frame_title,img_o)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    print('')
    print('Video saved to : ',outputfile)
    vid.release()
    output.release()
    cv.destroyAllWindows()
