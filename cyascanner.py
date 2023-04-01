#!/bin/python3

#Required libraries
import re
from socket import gethostbyname, setdefaulttimeout, AF_INET, SOCK_STREAM, gaierror, error, socket
from optparse import OptionParser
from ipaddress import IPv4Address, AddressValueError
from datetime import datetime
from pyfiglet import Figlet
from termcolor import colored
from getmac import get_mac_address




def define_target(target_ip,target_port):
	#Define our target

	if target_ip != None:
		try:
			IPv4Address(target_ip)
			target = gethostbyname(target_ip) #Translate hostname to IPv4

		except AddressValueError:
			print('—' * 50)
			print('[!] Error: Invalid ip address.')
			print('—' * 50)
			exit()
		#print('Invalid amount of arguments. \nSyntax: python3 cya_scanner.py -i <target_ip>')
	else:
		print('—'*70)
		print('[!] Error: Invalid amount of arguments. \nSyntax: python3 cya_scanner.py -i <target_ip>')
		#print('Syntax: python3 cya_scanner.py -i <target_ip>')
		print('—'*70)
		exit()
	add_banner(target_ipaddr=target_ip)

def add_banner(target_ipaddr):
	#Add a banner
	custom_fig1 = Figlet(font='rectangles')
	custom_fig2 = Figlet(font='threepoint')

	print('\n')
	cya_text = custom_fig1.renderText('CYA').strip() #YOU CAN CHANGE BANNER TEXT
	cya_text_col = colored(cya_text, "light_cyan")  #YOU CAN CHANGE BANNER COLOR

	scanner_text = custom_fig2.renderText('scanner') #YOU CAN CHANGE BANNER TEXT
	scanner_text_col = colored(scanner_text, "light_red") #YOU CAN CHANGE BANNER COLOR

	target_text_col = colored('Target:','red')
	time_start_col = colored('Time started:', 'light_yellow')
	print(cya_text_col)
	print(scanner_text_col)

	
	try:
		print(target_text_col+' '+target_ipaddr)
	except NameError:
		print('Invalid amount of arguments. \nSyntax: python3 cya_scanner.py -i <target_ip>\n')
		exit()
	start_time = datetime.now()
	print(time_start_col, start_time)
	print('—' * 50)

	scan(target=target_ipaddr,start=start_time,target_port=options.target_port)


def scan(target,start,target_port):
	#Variables
	open_str = colored('Open ⇢ ', "green", attrs=["reverse", "bold"])
	
	min_port = 0
	max_port = 1000
	try:
		if target_port != None:
			port_model = re.compile("([0-9]+)-([0-9]+)")
			port_range_valid = port_model.search(target_port.replace("",""))

			min_port = int(port_range_valid.group(1))
			max_port = int(port_range_valid.group(2))
	except AttributeError:
		print('Inlavid Port number.\n')
		exit()

	try:
		for port in range(min_port,max_port):
			s = socket(AF_INET, SOCK_STREAM)
			setdefaulttimeout(1)
		
			result = s.connect_ex((target,port))
			target_col = colored(target, 'light_red')
			port_col = colored(port,'light_red')
			symbol = colored(':','light_red')
			output = open_str+' '+target_col+symbol+port_col
			if result == 0:
				print(str(output).strip())

			s.close

		get_mac(target=target,start=start)


	except KeyboardInterrupt:
		print('\nNooo! Dont\'t leave me alone :((')
		exit()

	except gaierror:
		print('Hostname could not be resolved.')
		exit()

	except error:
		print('Could not connect to server.')
		exit()


def get_mac(target,start):
	ip_mac = get_mac_address(ip=target)

	mac_text_col = colored(ip_mac, "light_cyan")
	mac_text = colored('MAC ⇢', 'red')
	elapsed_col = colored('Elapsed time: ', 'light_yellow')


	print(f'\n {mac_text}  {mac_text_col}')

	stop = datetime.now()

	print('—' * 50)
	print(f'{elapsed_col} {stop-start}\n')

#Arguments
parser = OptionParser()
parser.add_option("-i", "--ipaddress", dest="target_ip",
                  help="Target ip address.")
parser.add_option("-p", "--port", dest="target_port",
		  			help="Port range (example: 1-100)")
(options, args) = parser.parse_args()
