# -*- coding: utf-8

import sys
import socket
import subprocess
import argparse
import time
import os
import requests


os.system("cls") if os.name == 'nt' else os.system('reset')
_name_ = "FS-Port"
_version_ = '2.0.0'
_author_ = 'Rodrigo Lp (Apoc) / Breno Carvalho (Lord13)'


'''
 _______  _______         _______  _______  ______    _______ 
|       ||       |       |       ||       ||    _ |  |       |
|    ___||  _____| ____  |    _  ||   _   ||   | ||  |_     _|
|   |___ | |_____ |____| |   |_| ||  | |  ||   |_||_   |   |  
|    ___||_____  |       |    ___||  |_|  ||    __  |  |   |  
|   |     _____| |       |   |    |       ||   |  | |  |   |  
|___|    |_______|       |___|    |_______||___|  |_|  |___|  
								Official Fsociety Port Scanner


COMO USAR (pt-br):

Pretendo adicionar as seguintes funções:
   [+] Salvar em arquivo
   [+] Pausa
   [+] Autoscanner
   [+] E TALVEZ MAIS

Para usar faça assim:

Para usar range:

>> python %SCRIPTNAME% -r 1-78 --server example.com
>> python %SCRIPTNAME% --range 60-80 --server example.com

Para usar a manual:

>> python %SCRIPTNAME% -m 1,2,3,9-13,89-90 --server example.com
>> python %SCRIPTNAME% --manual 80,21,69,70,22,30-40 --server example.com

Para usar a exception com qualquer outra funcao:

>> python %SCRIPTNAME% --except 12-90 -f --server example.com
>> python %SCRIPTNAME% --except 80-100 -r 1-110 --server example.com
>> python %SCRIPTNAME% --manual 1,2,3-120 --except "1, 2, 3-80" --server example.com

+=========================================================================================+
+ NÃO precisa se preocupar com espaços, desde que estejam entre aspas... o programa subs- +
+  titui por uma string vazia com ".replace(" ", "")"									  +
+=========================================================================================+

Além disso há outros argumentos de se pode usar. Temos por exemplo:

O argumento "output", que quando dado, diz ao programa para salvar o resultado num log
onde segue o seguinte padrão no nome do arquivo:

DD.MM.AAAA - HH.MM.txt

Para usar fazemos o seguinte:

>> python %SCRIPTNAME% --manual 80 --server example.com -o

ou

>> python %SCRIPTNAME% --manual 80 --server example.com --output

O argument "backwards" quando dado faz o programa fazer a análise ao contrário, só
válido para inputs "não arquivos", por enquanto. Para usar:

>> python %SCRIPTNAME% --manual 80 --server example.com -b

ou:

>> python %SCRIPTNAME% --manual 80 --server example.com --backwards

E os três últimos argumentos "servers", 'ports', 'both'. Os três fazem basicamente
a mesma coisa, exceto o último. Os dois primeiros exprimem uma wordlist que conte-
nha servidores ou portas (nem precisa especificar qual é qual). E a última, "both",
lê arquivos que contenham tanto portas como servidores, especificados intrisecamente
entre si. O arquivo seria assim:


google.com:80
example.com:23
example.net:587
facebook.com:23

'''


# Global log variable
string  = ''


def analyse_arguments():
	'''
	@function
	:return A parser containing the necessary data
	'''
	parser = argparse.ArgumentParser(description="Official FSociety Port Analyser")

	parser.add_argument('-e', "--except", dest='exceptions', help="EXCLUI a análise dessas portas\n")
	parser.add_argument('-f', '--full', dest='full', action='store_true', help="Varre todas as portas de 1 a 49151")
	parser.add_argument('-r', '--range', dest='range', help="Varre as portas especificadas num range")
	parser.add_argument('-m', '--manual', dest='manual', help="Varre somente as portas especificadas")
	parser.add_argument('-s', '--server', dest="server", help="Explicita o servidor a ser analisado")
	parser.add_argument('-o', '--output', dest="save", action='store_true', help="Salva em um arquivo de log, NÃO insira nome de arquivo")
	parser.add_argument('-b', '--backwards', dest="reverse", action='store_true', help="Inverte a ordem de escanear")
	parser.add_argument("-os", '--servers', dest="servers_file", help="Abre uma wordlist de servidores")
	parser.add_argument("-op", '--ports', dest="ports_file", help="Abre uma wordlist de portas")
	parser.add_argument('-ob', '--both', dest='both_file', help="Abre uma wordlist de servidores E portas")

	parser2 = parser.parse_args()

	return parser2


def _name_port(port):
	try:
		return "Port {} ({}):".format(port, socket.getservbyport(port))
	except:
		return "Port {} (unknown):".format(port)


def check_port(serv, port):
	try:
		abre_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
		abre_sock.settimeout(2)
		resultado = abre_sock.connect_ex((serv,port))

		if resultado == 0:
			return "\033[032m[+] {} Open\033[0;0m".format(_name_port(port))
		else:
			return "\033[031m[-] {} Closed\033[0;0m".format(_name_port(port))

		abre_sock.close()

	except Exception as err:
		return "\033[033m[!] {} Error ({})\033[0;0m".format(_name_port(port), str(err))


def except_(ports, exceptions_):
	return list(set(ports)^set(exceptions_))


def range_(port_string):
	global string
	print "[!] Using range mode"
	string += "[!] Using range mode\n"
	splitted_port_string = port_string.replace(" ", '').split("-")
	return range(int(splitted_port_string[0]), int(splitted_port_string[1])+1)


def manual(port_string):
	global string
	print "[!] Using manual mode"
	string += "[!] Using manual mode\n"
	splitted_port_string = port_string.replace(' ', '').split(',')
	total_ports = []

	for i in splitted_port_string:
		if '-' in i:
			splitted_i = i.split("-")
			total_ports.extend(range(int(splitted_i[0]), int(splitted_i[1])+1))
		else:
			total_ports.append(int(i))

	return sorted(total_ports)


def full():
	global string
	print "[!] Using full mode"
	string += "[!] Using full mode"
	return range(1, 49151)


# NOT FINISHED!!!
def autoscan():
	ip = requests.get("http://httpbin.org/ip")
	ip_ = ip.json()['origin']

def write_to_file(log):
	global string
	times = time.localtime()

	filename = "%02d.%02d.%d - %02d.%02d.txt" % (times.tm_mday,
		times.tm_mon,
		times.tm_year,
		times.tm_hour,
		times.tm_min)

	print "[*] Saving to file \"{}\"...".format(filename)
	string += "[*] Saving to file \"{}\"...\n".format(filename)
	with open(filename, 'wb') as f:
		f.write(log)
	print "[+] Succesfully saved!"
	string += "[+] Succesfully saved!\n"


def main():
	global string
	arguments = analyse_arguments()
	list_of_ports = []
	servers = []

	if not(arguments.ports_file):

		dict_for_args = {
			'range': arguments.range,
			'manual': arguments.manual,
			'full': arguments.full
		}

		functions = {
			'range': range_,
			'manual': manual,
			'full': full
		}

		# Filtering "None" values on dict
		dict_for_args = {v: dict_for_args[v] for v in dict_for_args if dict_for_args[v]}
		if len(dict_for_args) > 1:
			print "[!]Insira somente uma das opções (--range, --manual, --full)!"
			string += "[!]Insira somente uma das opções (--range, --manual, --full)!\n"
			exit(1)
		

		# Converting the given string in a list
		for i in dict_for_args:
			result_list = functions[i](dict_for_args[i]) if i != 'full' else full()
			list_of_ports.extend(result_list)
	else:
		port_file = open(arguments.ports_file, 'rb')
		print "[*] File of ports succesfully opened"
		string += "[*] File of ports succesfully opened\n"
		list_of_ports = [int(c.strip("\n")) for c in port_file.readlines()]
		port_file.close()

	# Servers from file
	servers = [arguments.server]
	if arguments.servers_file:
		server_file = open(arguments.servers_file, 'rb')
		print "[*] File of servers succesfully opened"
		string += "[*] File of servers succesfully opened\n"
		servers = [c.strip() for c in server_file.readlines()]
		server_file.close()
	
	if arguments.both_file:
		both = []
		both_file_ = open(arguments.both_file, 'rb')
		print "[*] File of servers and ports succesfully opened"
		string += "[*] File of servers and ports succesfully opened\n"

		for line in both_file_.readlines():
			splitted = line.strip().split(':')
			both.append(splitted)

		for each in both:
			print "Working with %s on port %s..." % (each[0], each[1])
			string += "Working with %s on port %s...\n" % (each[0], each[1])
			open_or_closed = check_port(each[0], int(each[1]))
			print open_or_closed
			string += open_or_closed+'\n' # Writes to a log
		string += "\n"+"==="*10

		both_file_.close()

	if arguments.save and string != '':
		write_to_file(string) # Writes the log to a file

	# Removes the ports given in "except"
	if arguments.exceptions:
		prepared_exceptions = manual(arguments.exceptions)
		list_of_ports = except_(list_of_ports, prepared_exceptions)

	if arguments.reverse:
		print "[!] Order reversed"
		string += "[!] Order reversed\n"
		list_of_ports = reversed(list_of_ports)

	for server in servers:
		print "[*] Working with: %s" % server
		string += "[*] Working with: %s\n" % server
		for port in list_of_ports:
			open_or_closed = check_port(server, port)
			print open_or_closed
			string += open_or_closed+'\n' # Writes to a log
		string += "\n"+"==="*10
		print "\n"+"==="*10

	if arguments.save and string != '':
		write_to_file(string) # Writes the log to a file


if __name__ == '__main__':
	print """
[+]===========================================[+]
[+]{}[+]
[+]{}[+]
[+]                                           [+]
[+]{}[+]
[+]                                           [+]
[+]{}[+]
[+]===========================================[+]
	""".format("FS-PORT".center(43),
		"Scanner de portas da FSociety Brasil".center(43),
		"Coded by Apoc e Lord13".center(43),
		"FSOCIETYBRASIL.ORG".center(43)
		)
	main()