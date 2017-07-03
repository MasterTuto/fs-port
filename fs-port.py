#!/usr/bin/python
# -*- coding: utf8 -*-

import socket
import sys
import subprocess
from optparse import OptionParser

__author__ = "Rodrigo Lp (Apoc), SEU_NOME/NICK"
__version__ = "1.0.0"
__email__ = "contato@fsocietybrasil.org"

subprocess.call('clear', shell=True)

## Construindo o HELP ##
usage = "%prog [opcao1] [opcap2]... [IP_ALVO]"
parser = OptionParser(usage=usage)
parser.add_option("-f", "--full", dest="full", help="Varredura em todas as portas de 0 a 49151.")
parser.add_option("-r", "--range", dest="range", help="Varredura de porta X a Y (separado por virgula). Exemplo: -r/--range 10,20")
parser.add_option("-m", "--manual", dest="manual", help="Varredura de lista de portas (separado por virgula). Exemplo: -m/--manual 80,22,8080,443")
(options, args) = parser.parse_args()


## Funcao para testar as portas ##
def testa(ip,porta):
	try:
		abre_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		abre_sock.settimeout(2) ## Define tempo de espera para TimeOut na porta.
		resultado = abre_sock.connect_ex((ip,porta))
		if resultado == 0:
			return "Port {}: Open".format(porta)
		else:
			return "Port {}: Close".format(porta)
		abre_sock.close()

	except socket.error as err:
		print "Port {}: Error (%s)".format(porta) % str(err)


## Se a opcao FULL for escolhida ##
if str(options.full) != "None":
	try:
		for port in range(0,49152):
			print testa(str(sys.argv[len(sys.argv)-1]),port)

	except KeyboardInterrupt:
		print "\nSaindo..."
		sys.exit()

## Se a opcao RANGE for escolhida ##
if str(options.range) != "None":
	separador = options.range.split(',')
	x = separador[0].strip()
	y = separador[1].strip()
	try:
		for port in range(int(x),int(y)+1):
			print testa(str(sys.argv[len(sys.argv)-1]),port)

	except KeyboardInterrupt:
		print "\nSaindo..."
		sys.exit()

## Se a opcao MANUAL for escolhida ##
if str(options.manual) != "None":
	lista = options.manual.split(',')
	try:
		for port in lista:
			print testa(str(sys.argv[len(sys.argv)-1]),int(port))

	except KeyboardInterrupt:
		print "\nSaindo..."
		sys.exit()
