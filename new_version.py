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

import os
import subprocess
import shutil
from getpass import getpass
file = open("setup.py","r+")
file_temp = open("setup_tmp.py","w")
content = file.read()
file_temp.write(content)
file.close()
file_temp.close()
try:
    file = open("setup.py","w+")

    version = content[content.find("version")+9:content.find("author")-7]
    start = content[:content.find("version")+9]
    end = content[content.find("author")-7:]

    print("Current Version : ",version)
    print("New version name : ",end="")
    version_name= input()
    new = start+version_name+end
    print("Specify the changes : ",end='')
    msg=input()
    print("Username : ",end="")
    login = input()
    passw = getpass(prompt="Password : ",stream=None)
    file.seek(0)
    file.write(new)
    file.close()
except:
    sys.exit()
try:
    shutil.rmtree("build")
except OSError as e:
    print("Warn: %s : %s" % ("build", e.strerror))
try:
    shutil.rmtree("dist")
except OSError as e:
    print("Warn: %s : %s" % ("dist", e.strerror))
try:
    shutil.rmtree("img2ascii.egg-info")
except OSError as e:
    print("Warn: %s : %s" % ("img2ascii.egg-info", e.strerror))

try:
    subprocess.call(["python","-m","setup.py","sdist","bdist_wheel"])
    subprocess.call(["python","-m","twine","upload","dist/*","-u",login,"-p",passw])
    subprocess.call(["git","pull"])
    subprocess.call(["git","add","."])
    subprocess.call(["git","commit","-a","-m",msg])
    subprocess.call(["git","push"])
except subprocess.CalledProcessError:
    print('error')
    sys.exit()
if(os.path.exists("setup_tmp.py")):
    os.remove("setup_tmp.py")
