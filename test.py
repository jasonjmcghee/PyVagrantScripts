from __future__ import print_function
import vagrant
from fabric.api import run, execute
import logging
from logging import warn, error, info
import fileinput, os, sys
from subprocess import Popen, PIPE, STDOUT
import subprocess

def start(provider=None):
	"""Starts the specified machine using vagrant"""
	info("Creating new Vagrant cell...")

	v = vagrant.Vagrant()
	info("Initializing Vagrant cell...")
	v.init("raring64")
	info("Modifying Vagrantfile...")
	if provider == "kvm": 
		for line in fileinput.FileInput("Vagrantfile",inplace=1):
			line = line.replace("# config.vm.network :pri","config.vm.network :pri")
			print (line, end='')
	info("Booting up cell...")
	v.up(provider)
	info("Finalizing new cell...")
	if provider is not "kvm":
		with settings(host_string= v.user_hostname_port(),
			key_filename = v.keyfile(),
			disable_known_hosts = True):
			run('echo hello')

l = logging.getLogger()
l.setLevel('DEBUG')

def finish():
   shell_command = "vagrant status | tail -6 | head -1 | awk '{ print $2 }'"
   event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
   output = event.communicate()
   if output[0].find("running") != -1: info("Successfully created new cell!")
   else: warn("Something went horribly wrong.")
   print()

try:
   execute(start("kvm"))
except subprocess.CalledProcessError:
   print()
   error('Some bad things are happening...')

finish()
