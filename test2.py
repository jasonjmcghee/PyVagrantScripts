import re
import fileinput
import commands

def test():
   o = open("output","w")
   data = open("/home/elvis/pythonVagrant/Vagrantfile").read()
   o.write( re.sub('#\ config.vm.network\ :pri','config.vm.network\ :pri',data))
   o.close()

def test2():
   commands.getoutput('cat Vagrantfile | sed \'s/# config.vm.network :pri/config.vm.network :pri/\' > Vagrantfile')

def test3():
    for line in fileinput.FileInput("Vagrantfile",inplace=1):
    	line = line.replace("# config.vm.network :pri","config.vm.network :pri")
    	print line
