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
x = None
if str(options.full) != "None":
	x = 0
	def keepon(x):
		global x
		for port in range(0,49152):
			print testa(str(sys.argv[len(sys.argv)-1]),port)
			x += 1
	try:
		keepon(x)
		
	except KeyboardInterrupt:
		keepon_or_giveup = raw_input("Voce quer pausar(p)/continuar(c)/sair(s)? ")
		if keepon_or_giveup == 'p':
			avulso = raw_input("Quando quiser continuar aperte enter! Ou digite \"s\" e de enter para sair")
			if avulso != 's': keepon(x)
		elif keepon_or_giveup == 'c':
			keepon(x)
		elif keepon_or_giveup == 's':
			sys.exit(1)
		#print "\nSaindo..."
		#sys.exit()

## Se a opcao RANGE for escolhida ##
x = None
if str(options.range) != "None":
	separador = options.range.split(',')
	x = separador[0].strip()
	y = separador[1].strip()
	def keepon(x, y):
		global x
		for port in range(int(x),int(y)):
			print testa(str(sys.argv[len(sys.argv)-1]),port)
			x += 1
	try:
		keepon(x, y)
	except KeyboardInterrupt:
		keepon_or_giveup = raw_input("Voce quer pausar(p)/continuar(c)/sair(s)? ")
		if keepon_or_giveup == 'p':
			avulso = raw_input("Quando quiser continuar aperte enter! Ou digite \"s\" e de enter para sair")
			if avulso != 's': keepon(x, y)
		elif keepon_or_giveup == 'c':
			keepon(x, y)
		elif keepon_or_giveup == 's':
			sys.exit(1)
		#print "\nSaindo..."
		#sys.exit()

## Se a opcao MANUAL for escolhida ##
lista = None
if str(options.manual) != "None":
	lista = options.manual.split(',')
	def keepon(lista):
		global lista
		for port in range(len(lista)):
			print testa(str(sys.argv[len(sys.argv)-1]),int(lista[port]))
			lista.pop(port)
	try:
		keepon(lista)
	except KeyboardInterrupt:
		keepon_or_giveup = raw_input("Voce quer pausar(p)/continuar(c)/sair(s)? ")
		if keepon_or_giveup == 'p':
			avulso = raw_input("Quando quiser continuar aperte enter! Ou digite \"s\" e de enter para sair")
			if avulso != 's': keepon(lista)
		elif keepon_or_giveup == 'c':
			keepon(lista)
		elif keepon_or_giveup == 's':
			sys.exit(1)
		#print "\nSaindo..."
		#sys.exit()
