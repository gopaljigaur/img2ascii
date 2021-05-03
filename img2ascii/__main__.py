#!/usr/bin/env python
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

import sys, getopt, os, os.path, cv2, re, filetype
from .text_gen import generate_ascii_t
from .image_gen import generate_ascii_i
from .video_gen import generate_ascii_v
from .webcam_gen import generate_ascii_w
from .pygrabber.dshow_graph import FilterGraph

def disphelp():
   print('')
   print('img2ascii')
   print('')
   print('Authors:')
   print(' Gopalji Gaur <gopaljigaur@gmail.com>')
   print('')
   print('img2ascii is a library written in python which can convert image or video files to ASCII')
   print('')
   print('Option list:')
   print('')
   print('-h or --help       : To generate this help text')
   print('-m or --mode       : Select the mode of operation -- `t` for text, `i` for image, `v` for video and `w` for webcam input')
   print('-c or --color      : Optional parameter to select color mode. 0 - binary, 1 - Grayscale and 2 - RGB. Default color mode is binary')
   print('--fcolor           : Optional parameter to set the text color in binary color mode. Default = white')
   print('--bcolor           : Optional parameter to set the background color in binary color mode. Default = black')
   print('                     for --fcolor and --bcolor, you can use color names - [white, black, red, green, blue, yellow, cyan, magenta]')
   print('                     For all other colors hex color codes must be supplied')
   print('-k or --kernel     : Optional parameter to set the kernel size, default is 7px')
   print('-d or --density    : Optional parameter to set the ASCII text density on image, default is 0.3 units; Range - (0,1) (exclusive)')
   print('-i or --ifile      : Path to the input file for image and video modes')
   print('-o or --ofile      : Path to the output file for image and video modes')
   print('-s or --cam_source : Camera to be used for webcam mode. Use 0,1,2,3... to select cameras connected to the PC. Default value is 0')
   print('-f or --fancy      : Fancy color mode :) [Color mode will default to RGB]')
   print('')
   print('Usage : ')
   print('')
   print('For text   : img2ascii.py -m <mode>[t=text] -i <inputfile> -o <outputfile> -k <kernel_size>[optional] -d <text_density>[optional]')
   print('For image  : img2ascii.py -m <mode>[i=image] -c[color mode (optional)] -i <inputfile> -o <outputfile> -k <kernel_size>[optional] -d <text_density>[optional]')
   print('For video  : img2ascii.py -m <mode>[v=video] -c[color mode (optional)] -i <inputfile> -o <outputfile> -k <kernel_size>[optional] -d <text_density>[optional]')
   print('For webcam : img2ascii.py -m <mode>[w=webcam] -c[color mode (optional)] -k <kernel_size>[optional] -d <text_density>[optional -s <source_camera (0,1,2...)>[optional]')
   print('')
   
def main(argv):
   kernel = 7    #default
   density = 0.3 #default
   color = 0     #default
   mode = ''
   inputfile = ''
   outputfile = ''
   cam_source = ''
   hex_code = '^(?:[0-9a-fA-F]{3}){1,2}$'
   colors = ['black','blue','green','cyan','red','magenta','yellow','white']
   fcolor = (255,255,255)
   bcolor = (0,0,0)
   no_device=False
   fancy = False #default

   #get attached cameras
   try:
      device_list = getCamera() 
   except:
      no_device=True
      
   try:
      # modes - text, image, video, webcam
      # color - colored mode
      # kernel - kernel size
      # density - text density
      # ifile - input image or video file
      # ofile - output image or video file
      # cam_source - camera source for webcam mode
      # fancy - fancy mode
      # fcolor, bcolor - front and background colors for binary color mode (to be used only in case of binary mode)
      opts, args = getopt.getopt(argv,"hm:c:k:d:i:o:s:f",["help","color=","fcolor=","bcolor=","mode=","kernel=","density=","ifile=","ofile=","cam_source=","fancy"])
   except getopt.GetoptError:
      print('For text   : img2ascii.py -m <mode>[t=text] -i <inputfile> -o <outputfile> -k <kernel_size>[optional] -d <text_density>[optional]')
      print('For image  : img2ascii.py -m <mode>[i=image] -c[color mode (optional)] --fcolor <text_color_hex>[optional] --bcolor <background_color_hex>[optional] -i <inputfile> -o <outputfile> -k <kernel_size>[optional] -d <text_density>[optional] -f [fancy mode (optional)]')
      print('For video  : img2ascii.py -m <mode>[v=video] -c[color mode (optional)] --fcolor <text_color_hex>[optional] --bcolor <background_color_hex>[optional] -i <inputfile> -o <outputfile> -k <kernel_size>[optional] -d <text_density>[optional]  -f [fancy mode (optional)]')
      print('For webcam : img2ascii.py -m <mode>[w=webcam] -c[color mode (optional)] --fcolor <text_color_hex>[optional] --bcolor <background_color_hex>[optional] -k <kernel_size>[optional] -d <text_density>[optional] -s <source_camera (0,1,2...)>[optional]  -f [fancy mode (optional)]')
      print('To get help on usage : img2ascii.py -h <or> img2ascii.py --help')
      sys.exit(2)
   if not opts:
      disphelp()
      sys.exit()
   for opt, arg in opts:

      if opt == '-h':
         disphelp()
         sys.exit()

      elif opt in ("-m", "--mode"):
         mode = arg
         if mode not in ("t","i","v","w"):
            print('Please select one of the following modes : \'t\', \'i\', \'v\' or \'w\' ')
            print('To get help on usage : img2ascii.py -h <or> img2ascii.py --help')
            sys.exit()

      elif opt in ("-c", "--color"):
         color = int(arg)
         if not color in (0,1,2):
            print('Please select one of the following color modes : 0 - binary, 1 - Grayscale and 2 - RGB')
            print('To get help on usage : img2ascii.py -h <or> img2ascii.py --help')
            sys.exit()

      elif opt in ("-f","--fancy"):
         fancy = True
         color=2
         
      elif opt in ("--fcolor"):
         fcolor = arg
         if fcolor in colors:
            fcolor = "{0:b}".format(colors.index(fcolor))
            while(len(fcolor)<3):
               fcolor="0"+fcolor
            fcolor = list(fcolor)
            fcolor = tuple(int(i)*255 for i in fcolor)
            
         elif(re.match(hex_code,fcolor)):
            fcolor = (int(fcolor[0:2],16),int(fcolor[2:4],16),int(fcolor[4:6],16))
         else:
            print('Please give a valid value for fcolor')
            sys.exit()

      elif opt in ("--bcolor"):
         bcolor = arg
         if bcolor in colors:
            bcolor = "{0:b}".format(colors.index(bcolor))
            while(len(bcolor)<3):
               bcolor="0"+bcolor
            bcolor=list(bcolor)
            bcolor = tuple(int(i)*255 for i in bcolor)
            
         elif(re.match(hex_code,bcolor)):
            bcolor = (int(bcolor[0:2],16),int(bcolor[2:4],16),int(bcolor[4:6],16))
         else:
            print('Please give a valid value for bcolor')
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
         if mode=='t' and (output[-4:]!='.txt'):
            print('Output file must be a .txt file for text mode.')
            sys.exit()

      elif opt in ("-s", "--cam_source"):
         cam_source = int(arg)
         if(no_device):
            print("No camera input available. Please check your camera or use text, image or video mode.")
            sys.exit()

         
   print('') 

   if(mode=='t'):
      print('//////////////////////')
      print('///////Text Mode//////')
      print('//////////////////////')
      print('')
      print(' -------------------- ')
      print('|     Parameters     |')
      print(' -------------------- ')
      print('Kernel size  : ',kernel)
      print('Text density : ',density)
      print('Input file   : ', inputfile)
      print('Output file  : ', outputfile)
      print('')
      generate_ascii_t(inputfile,outputfile,kernel,density)
      
   if(mode=='i'):
      print('//////////////////////')
      print('//////Image Mode//////')
      print('//////////////////////')
      if fancy:
         print('')
         print('------Fancy Mode------')
      print('')
      print(' -------------------- ')
      print('|     Parameters     |')
      print(' -------------------- ')
      if(color==0):
         print('Selected color mode : binary')
      elif(color==1):
         print('Selected color mode : Grayscale')
      elif(color==2):
         print('Selected color mode : RGB')
      print('Kernel size  : ',kernel)
      print('Text density : ',density)
      print('Input file   : ', inputfile)
      print('Output file  : ', outputfile)
      if(color==0):
         print('Text color       : ',fcolor)
         print('Background color : ',bcolor)
      print('')
      generate_ascii_i(inputfile,outputfile,color,kernel,density,fancy,fcolor,bcolor)

   elif(mode=='v'):
      print('//////////////////////')
      print('//////Video Mode//////')
      print('//////////////////////')
      if fancy:
         print('')
         print('------Fancy Mode------')
      print('')
      print(' -------------------- ')
      print('|     Parameters     |')
      print(' -------------------- ')
      if(color==0):
         print('Selected color mode : binary')
      elif(color==1):
         print('Selected color mode : Grayscale')
      elif(color==2):
         print('Selected color mode : RGB')
      print('Kernel size  : ',kernel)
      print('Text density : ',density)
      print('Input file   : ', inputfile)
      print('Output file  : ', outputfile)
      if(color==0):
         print('Text color       : ',fcolor)
         print('Background color : ',bcolor)
      print('')
      generate_ascii_v(inputfile,outputfile,color,kernel,density,fancy,fcolor,bcolor)

   elif(mode=='w'):
      if(no_device):
         print("No camera input available. Please check your camera or use text, image or video mode.")
         sys.exit()
      print('///////////////////////')
      print('//////Webcam Mode//////')
      print('///////////////////////')
      if fancy:
         print('')
         print('------Fancy Mode------')
      print('')
      #testing cam availability
      while(True):
         if cam_source not in device_list.keys():
            print('Please select one of the following camera(s) : ')
            print('')
            for i,j in device_list.items():
               print(i," : ",j)
            print('')
            print("Your choice [0] : ",end='')
            cam_source=input()
            if(cam_source==''):
               cam_source=0
            cam_source = int(cam_source)
         else:
            break
      cap = cv2.VideoCapture(cam_source,cv2.CAP_DSHOW)
      if cap is None or not cap.isOpened():
         print('Error: Unable to open video source: ', device_list.get(cam_source))
         print('Please select other video source and try again.')
         sys.exit()
      else:
         cap.release()
         cv2.destroyAllWindows()
      print('')
      print(' -------------------- ')
      print('|     Parameters     |')
      print(' -------------------- ')
      if(color==0):
         print('Selected color mode : binary')
      elif(color==1):
         print('Selected color mode : Grayscale')
      elif(color==2):
         print('Selected color mode : RGB')
      print('Kernel size  : ',kernel)
      print('Text density : ',density)
      print('Video source : ',device_list.get(cam_source))
      if(color==0):
         print('Text color       : ',fcolor)
         print('Background color : ',bcolor)
      print('')
      generate_ascii_w(color,kernel,density,cam_source,device_list.get(cam_source),fancy,fcolor,bcolor)

def getCamera():
   graph = FilterGraph()
   devices = graph.get_input_devices()
   num_devices = len(devices)
   dev = {}
   for i in range(0,num_devices):
      dev[i] = devices[i]
   return dev

if __name__ == "__main__":
   main(sys.argv[1:])
