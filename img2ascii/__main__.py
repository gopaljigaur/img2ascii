#!/usr/bin/python

import sys, getopt, os.path, cv2, filetype
from image_gen import image_gen
from video_gen import video_gen
from webcam_gen import webcam_gen


def main(argv):
   kernel = 7
   density = 0.3
   color = 0
   mode = ''
   inputfile = ''
   outputfile = ''
   cam_source = 0
   try:
      # modes - image, video, webcam
      # color - colored mode
      # kernel - kernel size
      # density - text density
      # ifile - input image or video file
      # ofile - output image or video file
      # cam_source - camera source for webcam mode
      opts, args = getopt.getopt(argv,"hm:c:k:d:i:o:s",["help","color=","mode=","kernel=","density=","ifile=","ofile=","cam_source="])
   except getopt.GetoptError:
      print('For image  : img2ascii.py -m <mode>[i=image] -c[color mode (optional)] -i <inputfile> -o <outputfile> -k <kernel_size>[optional] -d <text_density>[optional]')
      print('For video  : img2ascii.py -m <mode>[v=video] -c[color mode (optional)] -i <inputfile> -o <outputfile> -k <kernel_size>[optional] -d <text_density>[optional]')
      print('For webcam : img2ascii.py -m <mode>[w=webcam] -c[color mode (optional)] -k <kernel_size>[optional] -d <text_density>[optional] -s <source_camera (0,1,2...)>[optional]')
      print('To get help on usage : img2ascii.py -h <or> img2ascii.py --help')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('')
         print('img2ascii is a library written in python which can convert image or video files to ASCII')
         print('')
         print('Option list:')
         print('')
         print('-h or --help       : To generate this help text')
         print('-m or --mode       : Select the mode of operation -- `i` for image, `v` for video and `w` for webcam input')
         print('-c or --color      : Optional parameter to select color mode. 0 - B/W, 1 - Grayscale and 2 - RGB. Default color mode is B/W')
         print('-k or --kernel     : Optional parameter to set the kernel size, default is 7px')
         print('-d or --density    : Optional parameter to set the ASCII text density on image, default is 0.3 units; Range - (0,1) (exclusive)')
         print('-i or --ifile      : Path to the input file for image and video modes')
         print('-o or --ofile      : Path to the output file for image and video modes')
         print('-s or --cam_source : Camera to be used for webcam mode. Use 0,1,2,3... to select cameras connected to the PC. Default value is 0')
         print('')
         print('Usage : ')
         print('')
         print('For image  : img2ascii.py -m <mode>[i=image] -c[color mode (optional)] -i <inputfile> -o <outputfile> -k <kernel_size>[optional] -d <text_density>[optional]')
         print('For video  : img2ascii.py -m <mode>[v=video] -c[color mode (optional)] -i <inputfile> -o <outputfile> -k <kernel_size>[optional] -d <text_density>[optional]')
         print('For webcam : img2ascii.py -m <mode>[w=webcam] -c[color mode (optional)] -k <kernel_size>[optional] -d <text_density>[optional -s <source_camera (0,1,2...)>[optional]')
         print('')
         sys.exit()
      elif opt in ("-m", "--mode"):
         mode = arg
         if mode not in ("i","v","w"):
            print('Please select one of the following modes : \'i\', \'v\' or \'w\' ')
            print('To get help on usage : img2ascii.py -h <or> img2ascii.py --help')
            sys.exit()
      elif opt in ("-c", "--color"):
         color = int(arg)
         if not color in (0,1,2):
            print('Please select one of the following color modes : 0 - B/W, 1 - Grayscale and 2 - RGB')
            print('To get help on usage : img2ascii.py -h <or> img2ascii.py --help')
            sys.exit()
      elif opt in ("-k", "--kernel"):
         kernel = arg
         if not kernel.isnumeric() or kernel=='0':
            print('Kernel size must be an integer greater than or equal to 1')
            print('To get help on usage : img2ascii.py -h <or> img2ascii.py --help')
            sys.exit()
         kernel = int(kernel)
      elif opt in ("-d", "--density"):
         try:
            density = float(arg)
         except:
            print('Density must be a floating point value in the range (0,1)  (exclusive)')
            print('To get help on usage : img2ascii.py -h <or> img2ascii.py --help')
            sys.exit()
         if not 0<density<1:
            print('Density must be a floating point value in the range (0,1) (exclusive)')
            print('To get help on usage : img2ascii.py -h <or> img2ascii.py --help')
            sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
         try:
            f = open(inputfile)
            f.close()
         except IOError:
            print('No such file exists')
            sys.exit()
         kind = filetype.guess(inputfile)
         if mode=='i' and (kind==None or kind.mime[:kind.mime.index('/')]!='image'):
            print('Image mode selected but input file is not an image.')
            sys.exit()
         if mode=='v' and (kind==None or kind.mime[:kind.mime.index('/')]!='video'):
            print('Video mode selected but input file is not a video.')
            sys.exit()
      elif opt in ("-o", "--ofile"):
         outputfile = os.path.abspath(arg)
         if not os.path.exists(outputfile[:len(outputfile)-outputfile[::-1].index('\\')]):
            print(outputfile[:len(outputfile)-outputfile[::-1].index('\\')])
            print('Output path is inaccessible')
            sys.exit()
   print('') 
   if(mode=='i'):
      print('Image Mode')
      if(color==0):
         print('Selected color mode : B/W')
      elif(color==1):
         print('Selected color mode : Grayscale')
      elif(color==2):
         print('Selected color mode : RGB')
      print('')
      print('Kernel size  : ',kernel)
      print('Text density : ',density)
      print('')
      print('Input file   : ', inputfile)
      print('Output file  : ', outputfile)
      image_gen(color,kernel,density,inputfile,outputfile)
   elif(mode=='v'):
      print('Video Mode')
      if(color==0):
         print('Selected color mode : B/W')
      elif(color==1):
         print('Selected color mode : Grayscale')
      elif(color==2):
         print('Selected color mode : RGB')
      print('')
      print('Kernel size  : ',kernel)
      print('Text density : ',density)
      print('')
      print('Input file   : ', inputfile)
      print('Output file  : ', outputfile)
      
      video_gen(color,kernel,density,inputfile,outputfile)
   elif(mode=='w'):
      print('Webcam Mode')
      #testing cam availability
      cap = cv2.VideoCapture(cam_source)
      if cap is None or not cap.isOpened():
         print('Error: Unable to open video source: ', cam_source)
         print('Please select other video source and try again.')
         sys.exit()
      else:
         cap.release()
      if(color==0):
         print('Selected color mode : B/W')
      elif(color==1):
         print('Selected color mode : Grayscale')
      elif(color==2):
         print('Selected color mode : RGB')
      print('')
      print('Kernel size  : ',kernel)
      print('Text density : ',density)
      print('')
      print('Video source : ',cam_source)
      print('')
      webcam_gen(color,kernel,density,cam_source)
   
if __name__ == "__main__":
   main(sys.argv[1:])
