# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
# # must build python 2.5
# WARNING! All changes made in this file will be lost!

import sys,os
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import requests
from xml.dom import minidom
import argparse
from pyVies import api
from easyxsd import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import json
from datetime import date
import time
import ctypes







try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

tabela_pdf = []
wynik = []
walidacja =[]

parser = argparse.ArgumentParser()
parser.add_argument('parametr1', help='Description')
parser.add_argument('parametr2', help='Description')

args = parser.parse_args()

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin
	


def connectVies_k(nip):

		try:
			vies = api.Vies()
			result = vies.request(nip)

			# works as well
			# result = vies.request('RO2785503')
			# result = vies.request('RO2785503', 'RO')

		except api.ViesValidationError as e:
			print (e)
		except api.ViesHTTPError as e:
			print (e)
			
		except api.ViesError as e:
			print (e)
		
		else:
			value_vies = str(result.valid)
			return value_vies
##obsługa w programie rejestracja dokumentów -->sprawdzenie VAT 
def konsola(NIP_konsola):
       
		
		NIP_konsola = args.parametr2
		node2 = NIP_konsola
		NIP = (node2)
		NIP_x = NIP.replace("-", "")
		
		payload = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.mf.gov.pl/uslugiBiznesowe/uslugiDomenowe/AP/WeryfikacjaVAT/2018/03/01"><soapenv:Header/><soapenv:Body><ns:NIP>'''+str(NIP_x)+'''</ns:NIP></soapenv:Body></soapenv:Envelope>
									'''
		try:
			r = requests.post('https://sprawdz-status-vat.mf.gov.pl',
				headers = {
					'SOAPAction'  : 'http://www.mf.gov.pl/uslugiBiznesowe/uslugiDomenowe/AP/WeryfikacjaVAT/2018/03/01/WeryfikacjaVAT/SprawdzNIP',
					'Content-type': 'text/xml;charset=UTF-8'
				},
							
				data = payload,
			)
					
		except requests.exceptions.HTTPError as errh:
			print ("Http Error:",errh)
							
		except requests.exceptions.ConnectionError as errc:
			print ("Error Connecting:",errc)
			
		except requests.exceptions.Timeout as errt:
			print ("Timeout Error:",errt)
			
						
		except requests.exceptions.RequestException as err:
						
			print ("OOps: Something Else",err)
		
		
		NIP_len = len(NIP_x)
		payload1 = str(r.content)
		
		NIP_len = len(NIP_x)
		payload1 = str(payload1)
		result = payload1.find('<Kod>') 
		NIP_status = payload1[result+5]
		NIP_status_N = 'Podmiot  o  podanym  identyfikatorze  podatkowym  NIP  nie  jest zarejestrowany jako podatnik VAT'
		NIP_status_C = 'Podmiot   o   podanym identyfikatorze   podatkowym   NIP   jest zarejestrowany jako podatnik VAT czynny'
		NIP_status_Z = 'Podmiot   o   podanym   identyfikatorze   podatkowym   NIP   jest zarejestrowany jako podatnik VAT zwolniony'
		NIP_status_I = 'Blad zapytania - Nieprawidlowy Numer Identyfikacji Podatkowej'
		#NIP_status_10 = 'Blad zapytania - Nieprawidlowy Numer Identyfikacji Podatkowej lub NIP zagraniczny'
		NIP_true = 'NIP zagraniczny, zarejestrowany w systemie VIES'
		NIP_false = 'NIP zagraniczny, nie jest zarejestrowany w systmie VIES'
		NIP_brak = 'NIP nie analizowany'
		if NIP_x == 'BRAK' or NIP_x == 'Brak' or NIP_x == 'brak'  or NIP_x == '':
			print 'NIP_brak'
		#wypisane kody krajów ponieważ mają 9 lub mniej liczb w nipie
		elif NIP_len > 10 or NIP_len < 10 or NIP_x[0:2] == 'CY'  or NIP_x[0:2] == 'CZ' or NIP_x[0:2] == 'DK' or NIP_x[0:2] == 'FI' or NIP_x[0:2] == 'HU' or NIP_x[0:2] == 'MT' or NIP_x[0:2] == 'SI' or NIP_x[0:2] == 'LU' or NIP_x[0:2] == 'IE' or NIP_x[0:2] == 'RO':
			przekazany_parametr = str(connectVies_k(NIP_x))
			if przekazany_parametr == 'True':
				print str('NIP_true')
			if przekazany_parametr == 'False':
				print str('NIP_false')
			if przekazany_parametr == 'None':
				print str('NIP_status_I')
		else:
			if NIP_len == 10:
				if NIP_status == 'N':
					print str('NIP_status_N')
				if NIP_status == 'C':
					print str('NIP_status_C')
					
				if NIP_status == 'Z':
					print str('NIP_status_Z')
				if NIP_status == 'I':
					print str('NIP_status_I')


def konsola_json(nip,bank):
	
    
    tabela_nip = []
    tabela_bank = []
	
    tabela_nip.append(nip.split(","))
    tabela_nip.append(bank.split(","))
    #print tabela_nip
    #print len(tabela_nip)
    for x in xrange(len(tabela_nip[0])):
        x1 = int(x)
        #print x1
        nip = tabela_nip[0][x1]
        bank =  tabela_nip[1][x1]

        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        #time.sleep( 3 )
        try:
			
		
            headers = {'User-Agent': 'Lefthand Oprogramowanie ksiegowe'}
            r = requests.get('https://wl-api.mf.gov.pl/api/check/nip/'+str(nip)+'/bank-account/'+str(bank)+'?date='+d1+'',headers=headers,verify=False) 
            #r = requests.get('https://wl-test.mf.gov.pl:9091/wykaz-podatnikow/api/check/nip/'+str(nip)+'/bank-account/'+str(bank)+'?date='+d1+'',headers=headers,verify=False) 
			
            if str(r.status_code) == '200':
				
				
                data = json.loads(""+r.text+"")
                print str(r.status_code)+"|"+str(data['result']["accountAssigned"])+"|"+str(data['result']["requestId"])+"|"+d1
                #print r.headers
				
            if str(r.status_code) == '400':
                data = json.loads(""+r.text+"")
                print str(r.status_code)+"|"+str(data["code"])+"|"+str(data["message"].encode('iso 8859-2'))+"|"+d1
		
		
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
								
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
				
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
				
							
        except requests.exceptions.RequestException as err:
							
            print ("OOps: Something Else",err)
		
		
			
			
		
	
	
					 
class Ui_MainWindow(object):

	def val(self):
	
		import xmlschema
		from pprint import pprint
		from xml.etree import ElementTree

		my_schema = xmlschema.XMLSchema('Schemat_JPK_VAT(3)_v1-1.xsd')
		#my_schema = xmlschema.XMLSchema('PIT_28_v22_2019_schemat.xsd')
		
		#xt = ElementTree.parse(lokalizacja)
		
		if str(my_schema.is_valid((args.parametr2))) == 'True':
			self.label2.setStyleSheet('font-weight: bold; color: green')
			self.label2.setText(_translate("MainWindow",'POPRAWNY', None))
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setWindowTitle(_fromUtf8("Walidacja"))
			msg.setText(_fromUtf8('Plik xml poprawny'))
			msg.addButton(QPushButton('OK'),QMessageBox.YesRole)
			returnValue = msg.exec_()	
		else:
			try:
				my_schema.validate(args.parametr2)
			except Exception, e: 
				self.label2.setStyleSheet('font-weight: bold; color: red')
				self.label2.setText(_translate("MainWindow",'NIEPOPRAWNY', None))
				#print my_schema.validate(lokalizacja)
				msg = QMessageBox()
				msg.setText(_fromUtf8("Bład walidacji pliku"))
				msg.setWindowTitle("Informacja")
				msg.setDetailedText(str(e))
				msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
				retval = msg.exec_()	
		


		
		
		
		

	def keyPressEvent(self, event):
		if event.key() == Key_Q:
            
			self.connectMF_false()
		elif event.key() == Key_Enter:
			self.connectMF_false()
		event.accept()

	def lista_value_error(self,tabela1):
		
		zmienna_tabela = tabela1
		
		a = len(zmienna_tabela)/4

	
		
	def wynik_do_tabeli(self,ilosc):
		
		
		self.tableWidget.setRowCount(1)
		self.tableWidget.setItem(0,0, QTableWidgetItem(str('NIP'))	)
		self.tableWidget.setItem(0,1, QTableWidgetItem('DOKUMENT'))
		self.tableWidget.setItem(0,2, QTableWidgetItem(str('STATUS'))	)
		#color = QColor(250,0,0)
		#self.tableWidget.item(1, 2).setBackground(color)

	def lista_nip(self):
		thislist = []
		thislist_document = []
		kod_kraju = []
		# parser = argparse.ArgumentParser()
		# parser.add_argument('-i','--input-file', help='Description', required=False)
		# args = parser.parse_args()
		xmldoc = minidom.parse(args.parametr2)


				
		for node1 in xmldoc.getElementsByTagName("NrDostawcy"):	
			for node2 in node1.childNodes:
				#print(node2.data)
				thislist.append(node2.data)
				#print (thislist)
		
		# for node1 in xmldoc.getElementsByTagName("DowodSprzedazy"):	
			# for node2 in node1.childNodes:
				# thislist_document.append(node2.data)
				# print (thislist)
				
		for node1 in xmldoc.getElementsByTagName("DowodZakupu"):	
			for node2 in node1.childNodes:
				#print(node2.data)
				thislist_document.append(node2.data)
				#print (thislist)

		count_kraje = xmldoc.getElementsByTagName("KodKrajuNadaniaTIN")
		count_kraje1 = count_kraje.length

		if  count_kraje1 > 0:
			##sekcja pobierania kodu z pliku xml

			for node1 in xmldoc.getElementsByTagName("ZakupWiersz"):
				if not node1.getElementsByTagName("KodKrajuNadaniaTIN"):
					kod_kraju.append('')
				else:
					for node2 in node1.getElementsByTagName("KodKrajuNadaniaTIN"):
						for node3 in node2.childNodes:
							#nie ma jeszczce obsługi kiedy wartosc KodKrajuNadaniaTIN jest pusta
							#
							#
							if  node3.data == '':
								kod_kraju.append('aaaa')
							else:
								kod_kraju.append(node3.data)



		else:
				pozycje = xmldoc.getElementsByTagName("DowodZakupu")
				pozycje1 = pozycje.length

				while pozycje1 !=0:

					w_tabela = ''
					kod_kraju.append(w_tabela)
					pozycje1 = pozycje1 -1

		return thislist, thislist_document, kod_kraju

		
		#return x
	
	def connectVies(self, nip):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		try:
			vies = api.Vies()
			result = vies.request(nip)

			# works as well
			# result = vies.request('RO2785503')
			# result = vies.request('RO2785503', 'RO')

		except api.ViesValidationError as e:
			print (e)
		except api.ViesHTTPError as e:
			print (e)
			e1 = str(e)
			msg.setText("Http Error")
			msg.setWindowTitle("Informacja")
			msg.setDetailedText(e1)
			msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
			retval = msg.exec_()
            #tutaj wywala Got error from vies: MS_UNAVAILABLE
		except api.ViesError as e:
			print (e)
			e1 = str(e)
			msg.setText("Error")
			msg.setWindowTitle("Informacja")
			msg.setDetailedText(e1)
			msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
			retval = msg.exec_()
            
        
		else:
			#print (result)
			#print (result.vatNumber)
			#print(result.valid)
			value_vies = str(result.valid)
			return value_vies
			
            
	#tego nie ruszamy , nie obsługiwany
	def connectMF_true(self):		
	# def readData(self):
		
		
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		
		
		

		# parser = argparse.ArgumentParser()
		# parser.add_argument('-i','--input-file', help='Description', required=False)
		# args = parser.parse_args()
		#print(args.input_file)
		xmldoc = minidom.parse(args.parametr2)
		
		
		
		#get all departments
		ilosc_nip_s = xmldoc.getElementsByTagName("NrKontrahenta")
		ilosc_nip_z = xmldoc.getElementsByTagName("NrDostawcy")

		ilosc = 0
		count = ilosc_nip_s.length + ilosc_nip_z.length
		
		
			
		
		#if count <> 100:
		count_bar = 100/count # 33
		count_bat1 = 100-(count_bar*count) # 1
		print count_bat1
		count_bar2 = (count_bar*count) + count_bat1 # 33 + 1 = 34
		print count_bar2
		self.completed = count_bat1
		
	
		#print self.lista_nip()		
		x = self.lista_nip()[0]
		y = self.lista_nip()[1]
		z = self.lista_nip()[2]
		
		for node1 in zip(x,y,z):
			
			#print str(node1[0])
			node2 = str(node1[0])
			node3_dokument = str(node1[1])
			kod_kraju = str(node1[2])
			#print node3_dokument
			
			
		# for node1 in xmldoc.getElementsByTagName("NrKontrahenta"):	
			# for node2 in node1.childNodes:
				# print(node2.data)
				
	
		# with open('plik.csv','rb') as csvfile:
			# NIP_data = csv.reader(csvfile, delimiter=',')
			# ilosc = 0
			# count = len(open('plik.csv', 'rU').readlines())
				
			# for row in NIP_data:
				
				#print(row[0]) # wartość kolumny 1 z tego wiersza
				
			NIP = (kod_kraju)+(node2)
			NIP_x = NIP.replace("-", "")
			#print NIP
			
			self.tableWidget.setRowCount(count)
			#self.checkBox.setChecked(True)
			
			payload = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.mf.gov.pl/uslugiBiznesowe/uslugiDomenowe/AP/WeryfikacjaVAT/2018/03/01"><soapenv:Header/><soapenv:Body><ns:NIP>'''+str(NIP_x)+'''</ns:NIP></soapenv:Body></soapenv:Envelope>
								'''
			# payload = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.mf.gov.pl/uslugiBiznesowe/uslugiDomenowe/AP/WeryfikacjaVAT/2018/03/01"><soapenv:Header/><soapenv:Body><ns:NIP>6651633117</ns:NIP></soapenv:Body></soapenv:Envelope>
								# '''
			try:
				r = requests.post('https://sprawdz-status-vat.mf.gov.pl',
					headers = {
						'SOAPAction'  : 'http://www.mf.gov.pl/uslugiBiznesowe/uslugiDomenowe/AP/WeryfikacjaVAT/2018/03/01/WeryfikacjaVAT/SprawdzNIP',
						'Content-type': 'text/xml;charset=UTF-8'
					},
						
					data = payload,
				)
				
			except requests.exceptions.HTTPError as errh:
				print ("Http Error:",errh)
				errh1 = str(errh)
				msg.setText("Http Error")
				msg.setWindowTitle("Informacja")
				msg.setDetailedText(errh1)
				msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
				retval = msg.exec_()
						
			except requests.exceptions.ConnectionError as errc:
				print ("Error Connecting:",errc)
				errc1 = str(errc)
				msg.setText("Error Connecting")
				msg.setWindowTitle("Informacja")
				msg.setDetailedText(errc1)
				msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
				retval = msg.exec_()
				
			except requests.exceptions.Timeout as errt:
				print ("Timeout Error:",errt)
				errt1 = str(errt)
				msg.setText("Timeout Error")
				msg.setWindowTitle("Informacja")
				msg.setDetailedText(errt1)
				msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
				retval = msg.exec_()
					
			except requests.exceptions.RequestException as err:
					
				print ("OOps: Something Else",err)
				err1 = str(err)
				msg.setText("Error - Something Else")
				msg.setWindowTitle("Informacja")
				msg.setDetailedText(err1)
				msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
				retval = msg.exec_()
					
				
			#print (r.content)
			NIP_len = len(NIP_x)
			payload1 = str(r.content)
				
			# payload = '''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><WynikOperacji xmlns="http://www.mf.gov.pl/uslugiBiznesowe/uslugiDomenowe/AP/WeryfikacjaVAT/2018/03/01"><Kod>C</Kod><Komunikat>Podmiot o podanym identyfikatorze podatkowym NIP nie jest zarejestrowany jako podatnik VAT</Komunikat></WynikOperacji></s:Body></s:Envelope>'''
				
			#print (payload)
			NIP_len = len(NIP_x)
			payload1 = str(payload1)
			result = payload1.find('<Kod>') 
			NIP_status = payload1[result+5]
			#print '-------------'
			#print payload1
			#print 'NIP:________         '+NIP_x
			#print 'STATUS_____    '+NIP_status
			NIP_status_N = 'Podmiot  o  podanym  identyfikatorze  podatkowym  NIP  nie  jest zarejestrowany jako podatnik VAT'
			NIP_status_C = 'Podmiot   o   podanym identyfikatorze   podatkowym   NIP   jest zarejestrowany jako podatnik VAT czynny'
			NIP_status_Z = 'Podmiot   o   podanym   identyfikatorze   podatkowym   NIP   jest zarejestrowany jako podatnik VAT zwolniony'
			NIP_status_I = 'Blad zapytania - Nieprawidlowy Numer Identyfikacji Podatkowej'
			NIP_status_10 = 'Blad zapytania - Nieprawidlowy Numer Identyfikacji Podatkowej'
			NIP_true = 'NIP zagraniczny - jest zarejestrowany w systemie VIES'
			NIP_false = 'NIP zagraniczny - nie jest zarejestrowany w systmie VIES'
			NIP_brak = 'NIP nie analizowany'
				
			if NIP_len > 10 or NIP_len < 10:
				
				# if NIP_x == 'BRAK' or NIP_x == 'Brak' or NIP_x == 'brak'  or NIP_x == '':
					# self.tableWidget.setItem(ilosc,0, QTableWidgetItem(str(NIP_x))	)
					# self.tableWidget.setItem(ilosc,1, QTableWidgetItem(NIP_brak))
					# color = QColor(128,128,128)
					# self.tableWidget.item(ilosc, 1).setBackground(color)
					# ilosc = ilosc+1
					
							
				if NIP_status == 'I':
						
					if NIP_x == 'BRAK' or NIP_x == 'Brak' or NIP_x == 'brak':
						
						#print 'NIP status brak'
						self.tableWidget.setItem(ilosc,0, QTableWidgetItem(str(NIP_x))	)
						self.tableWidget.setItem(ilosc,1, QTableWidgetItem(_fromUtf8(node3_dokument)))
						self.tableWidget.setItem(ilosc,2, QTableWidgetItem(NIP_brak))
						
						color = QColor(128,128,128)
						self.tableWidget.item(ilosc, 2).setBackground(color)
						ilosc = ilosc+1
					else:
						self.tableWidget.setItem(ilosc,0, QTableWidgetItem(str(NIP_x))	)
						self.tableWidget.setItem(ilosc,1, QTableWidgetItem(_fromUtf8(node3_dokument)))
						self.tableWidget.setItem(ilosc,2, QTableWidgetItem(NIP_status_I))
						
						color = QColor(250,0,0)
						self.tableWidget.item(ilosc, 2).setBackground(color)
						ilosc = ilosc+1
					
				else:
					przekazany_parametr = str(self.connectVies(NIP_x))
					#print 'cccccccc '+przekazany_parametr
						
					if przekazany_parametr == 'True':
						count = count - 1
						# self.tableWidget.setItem(ilosc,1, QTableWidgetItem(NIP_true))
						# color = QColor(50,205,50)
						# self.tableWidget.item(ilosc, 1).setBackground(color)
						# ilosc = ilosc+1
						
					if przekazany_parametr == 'False':
						self.tableWidget.setItem(ilosc,0, QTableWidgetItem(str(NIP_x))	)
						self.tableWidget.setItem(ilosc,1, QTableWidgetItem(_fromUtf8(node3_dokument)))
						self.tableWidget.setItem(ilosc,2, QTableWidgetItem(NIP_false))
						
						color = QColor(250,0,0)
						self.tableWidget.item(ilosc, 2).setBackground(color)
						ilosc = ilosc+1
							
					if przekazany_parametr == 'None':
						self.tableWidget.setItem(ilosc,0, QTableWidgetItem(str(NIP_x))	)
						self.tableWidget.setItem(ilosc,1, QTableWidgetItem(_fromUtf8(node3_dokument)))
						self.tableWidget.setItem(ilosc,2, QTableWidgetItem(NIP_status_I))
						
						color = QColor(250,0,0)
						self.tableWidget.item(ilosc, 2).setBackground(color)
						ilosc = ilosc+1
							
			if NIP_len == 10:
					
				if NIP_status == 'N':
					self.tableWidget.setItem(ilosc,0, QTableWidgetItem(str(NIP_x))	)
					self.tableWidget.setItem(ilosc,1, QTableWidgetItem(_fromUtf8(node3_dokument)))
					self.tableWidget.setItem(ilosc,2, QTableWidgetItem(str(NIP_status_N))	)
					
					color = QColor(250,0,0)
					self.tableWidget.item(ilosc, 2).setBackground(color)
					ilosc = ilosc+1
				if NIP_status == 'C':
					count = count - 1
					# self.tableWidget.setItem(ilosc,1, QTableWidgetItem(str(NIP_status_C))	)
					# color = QColor(50,205,50)
					# self.tableWidget.item(ilosc, 1).setBackground(color)
					# ilosc = ilosc+1
				if NIP_status == 'Z':
					count = count - 1
					# self.tableWidget.setItem(ilosc,1, QTableWidgetItem(str(NIP_status_Z))	)
					# color = QColor(50,205,50)
					# self.tableWidget.item(ilosc, 1).setBackground(color)
					# ilosc = ilosc+1
				if NIP_status == 'I':
					self.tableWidget.setItem(ilosc,0, QTableWidgetItem(str(NIP_x))	)
					item1 = QTableWidgetItem(str(NIP))
					item1.setBackground(QColor(255, 128, 128))
					self.tableWidget.setItem(ilosc,1, QTableWidgetItem(_fromUtf8(node3_dokument)))
					self.tableWidget.setItem(ilosc,2, QTableWidgetItem(str(NIP_status_I)))
					
					color = QColor(250,0,0)
					self.tableWidget.item(ilosc, 2).setBackground(color)
					ilosc = ilosc+1
				
			self.completed += count_bar
			self.progressBar.setValue(self.completed)				
	################################################################################################################################
###################################################################################################################################	
	def connectMF_false(self):		
	# def readData(self):

    
		tabela = []
		
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg1 = QMessageBox()
		msg1.setIcon(QMessageBox.Information)
		
		#print lista_kraje
		
		# parser = argparse.ArgumentParser()
		# parser.add_argument('-i','--input-file', help='Description', required=False)
		# args = parser.parse_args()
		#print(args.input_file)
		# xmldoc = minidom.parse(args.input_file)
		#get all departments
		xmldoc = minidom.parse(args.parametr2)
		ilosc_nip_z = xmldoc.getElementsByTagName("NrDostawcy")
		ilosc = 0
        
        #count = ilosc_nip_s.length + ilosc_nip_z.length
		count = ilosc_nip_z.length
		
		if count == 0:
			msg1.setWindowTitle(_fromUtf8("Analiza pliku JPK_VAT"))
			msg1.setText(_fromUtf8("Plik nie zawiera pozycji zakupowych do analizy"))
			msg1.addButton(QPushButton('Ok'),QMessageBox.RejectRole)
			returnValue = msg1.exec_()	
			
			
			if returnValue == QMessageBox.RejectRole:
				MainWindow.close(); 
			
		else:
			
			
			
			#count_bar = 100/count # 33
			#print count
			count_bar = 100/float(count) # 0.22 * 450 = 99
			##############DO POPRAWKI PRZY 450 pozycjach
			#print round(count_bar,2)
			count_bat1 = 100-(round(count_bar,2)*count) # 1
			#print count_bat1
			if count_bat1 > 0:
				count_bat1 = count_bat1
				count_bar2 = (round(count_bar,2)*count) + count_bat1 # 33 + 1 = 34
			elif count_bat1 < 0:
				count_bat1 = -count_bat1
				count_bar2 = (round(count_bar,2)*count) - count_bat1 # 33 + 1 = 34
			#print count_bar2
			#print count_bat1
			self.completed = count_bat1





			#print self.lista_nip()		
			x = self.lista_nip()[0]
			y = self.lista_nip()[1]
			z = self.lista_nip()[2]
			lista_kraje = 0
			#print x
			#print z
			
			for node1 in zip(x,y,z):


				#print str(node1[0])
				node2 = str(node1[0])
				node3_dokument = node1[1]
				kod_k= node1[2]


			# for node1 in xmldoc.getElementsByTagName("NrKontrahenta"):
				# for node2 in node1.childNodes:
					# print(node2.data)
					
		
			# with open('plik.csv','rb') as csvfile:
				# NIP_data = csv.reader(csvfile, delimiter=',')
				# ilosc = 0
				# count = len(open('plik.csv', 'rU').readlines())
					
				# for row in NIP_data:
					
					#print(row[0]) # wartość kolumny 1 z tego wiersza
				NIP = (kod_k)+(node2)
				NIP_x = NIP.replace("-", "")
				self.tableWidget.setRowCount(count)
				#print NIP_x
				self.tableWidget.setItem(ilosc,0, QTableWidgetItem(str(NIP_x))	)
				#self.checkBox.setChecked(False)
				
		
					
				payload = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.mf.gov.pl/uslugiBiznesowe/uslugiDomenowe/AP/WeryfikacjaVAT/2018/03/01"><soapenv:Header/><soapenv:Body><ns:NIP>'''+str(NIP_x)+'''</ns:NIP></soapenv:Body></soapenv:Envelope>
									'''
					
				# payload = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.mf.gov.pl/uslugiBiznesowe/uslugiDomenowe/AP/WeryfikacjaVAT/2018/03/01"><soapenv:Header/><soapenv:Body><ns:NIP>6651633117</ns:NIP></soapenv:Body></soapenv:Envelope>
									# '''
				try:
					r = requests.post('https://sprawdz-status-vat.mf.gov.pl',
						headers = {
							'SOAPAction'  : 'http://www.mf.gov.pl/uslugiBiznesowe/uslugiDomenowe/AP/WeryfikacjaVAT/2018/03/01/WeryfikacjaVAT/SprawdzNIP',
							'Content-type': 'text/xml;charset=UTF-8'
						},
							
						data = payload,
					)
					
				except requests.exceptions.HTTPError as errh:
					print ("Http Error:",errh)
					errh1 = str(errh)
					msg.setText("Http Error")
					msg.setWindowTitle("Informacja")
					msg.setDetailedText(errh1)
					msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
					retval = msg.exec_()
							
				except requests.exceptions.ConnectionError as errc:
					print ("Error Connecting:",errc)
					errc1 = str(errc)
					msg.setText("Error Connecting")
					msg.setWindowTitle("Informacja")
					msg.setDetailedText(errc1)
					msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
					retval = msg.exec_()
					
				except requests.exceptions.Timeout as errt:
					print ("Timeout Error:",errt)
					errt1 = str(errt)
					msg.setText("Timeout Error")
					msg.setWindowTitle("Informacja")
					msg.setDetailedText(errt1)
					msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
					retval = msg.exec_()
						
				except requests.exceptions.RequestException as err:
						
					print ("OOps: Something Else",err)
					err1 = str(err)
					msg.setText("Error - Something Else")
					msg.setWindowTitle("Informacja")
					msg.setDetailedText(err1)
					msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
					retval = msg.exec_()
						
					
				#print (r.content)
				NIP_len = len(NIP_x)
				payload1 = str(r.content)
					
				# payload = '''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><WynikOperacji xmlns="http://www.mf.gov.pl/uslugiBiznesowe/uslugiDomenowe/AP/WeryfikacjaVAT/2018/03/01"><Kod>C</Kod><Komunikat>Podmiot o podanym identyfikatorze podatkowym NIP nie jest zarejestrowany jako podatnik VAT</Komunikat></WynikOperacji></s:Body></s:Envelope>'''
				
				#print (payload)
				NIP_len = len(NIP_x)
				payload1 = str(payload1)
				result = payload1.find('<Kod>') 
				NIP_status = payload1[result+5]
				#print '-------------'
				#print payload1
				#print 'aaaaaaaa'+NIP_status
				NIP_status_N = 'Podmiot  o  podanym  identyfikatorze  podatkowym  NIP  nie  jest zarejestrowany jako podatnik VAT'
				NIP_status_C = 'Podmiot   o   podanym identyfikatorze   podatkowym   NIP   jest zarejestrowany jako podatnik VAT czynny'
				NIP_status_Z = 'Podmiot   o   podanym   identyfikatorze   podatkowym   NIP   jest zarejestrowany jako podatnik VAT zwolniony'
				NIP_status_I = 'Blad zapytania - Nieprawidlowy Numer Identyfikacji Podatkowej'
				NIP_status_10 = 'Blad zapytania - Nieprawidlowy Numer Identyfikacji Podatkowej lub NIP zagraniczny'
				NIP_true = 'NIP zagraniczny, zarejestrowany w systemie VIES'
				NIP_truepl = 'NIP Polski, zarejestrowany w systemie VIES'
				NIP_false = 'NIP zagraniczny, nie jest zarejestrowany w systemie VIES'
				NIP_falsepl = 'NIP Polski, nie jest zarejestrowany w systemie VIES'

				NIP_brak = 'NIP nie analizowany'

				
				#print '-----------------------------'+NIP_x
				if NIP_x == 'BRAK' or NIP_x == 'Brak' or NIP_x == 'brak'  or NIP_x == '':
					czas1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 	
					#print 'wchodzi w 3 petle'
					#print 'NIP status brak'
					self.tableWidget.setItem(ilosc,0, QTableWidgetItem(str(NIP_x))	)
					self.tableWidget.setItem(ilosc,1, QTableWidgetItem(node3_dokument))
					self.tableWidget.setItem(ilosc,2, QTableWidgetItem(NIP_brak))
					color = QColor(128,128,128)
					self.tableWidget.item(ilosc, 2).setBackground(color)
					#tabela.append(ilosc)
					#tabela.append(NIP_x)
					#tabela.append(node3_dokument)
					#tabela.append(NIP_brak)
					
					tabela_pdf.append([ilosc+1,NIP_x,NIP_brak,'S',czas1,''])
					
					ilosc = ilosc+1
					#print NIP_x+'|'+node3_dokument:	
				elif NIP_len > 10 or NIP_len < 10 or NIP_x[0:2] == 'CY'  or NIP_x[0:2] == 'CZ' or NIP_x[0:2] == 'DK' or NIP_x[0:2] == 'FI' or NIP_x[0:2] == 'HU' or NIP_x[0:2] == 'MT' or NIP_x[0:2] == 'SI' or NIP_x[0:2] == 'LU' or NIP_x[0:2] == 'IE' or NIP_x[0:2] == 'RO':

						if NIP_x[0:2] == 'PL':
							NIP_true = NIP_truepl
							NIP_false = NIP_falsepl
						#print 'wchodzi w 4 petle'
						przekazany_parametr = str(self.connectVies(NIP_x))
						#print 'cccccccc '+przekazany_parametr
						#print NIP_x


						if przekazany_parametr == 'True':
							czas1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
							
							self.tableWidget.setItem(ilosc,1, QTableWidgetItem(node3_dokument))	
							self.tableWidget.setItem(ilosc,2, QTableWidgetItem(NIP_true))
								
							color = QColor(50,205,50)
							self.tableWidget.item(ilosc, 2).setBackground(color)
							tabela_pdf.append([ilosc+1,NIP_x,NIP_true,'Z',czas1,'VIES'])
							
							ilosc = ilosc+1
							
						
								
						if przekazany_parametr == 'False':
							czas1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
							self.tableWidget.setItem(ilosc,1, QTableWidgetItem(node3_dokument))	
							self.tableWidget.setItem(ilosc,2, QTableWidgetItem(NIP_false))
							color = QColor(250,0,0)
							self.tableWidget.item(ilosc, 2).setBackground(color)
							tabela.append(ilosc)
							tabela.append(NIP_x)
							tabela.append(node3_dokument)
							tabela.append(NIP_false)
							
							tabela_pdf.append([ilosc+1,NIP_x,NIP_false,'C',czas1,'VIES'])
					
							##print NIP_x+'|'+node3_dokument
							wynik.append(NIP_x+'|'+node3_dokument)
							ilosc = ilosc+1
							
						if przekazany_parametr == 'None':
							czas1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
							self.tableWidget.setItem(ilosc,1, QTableWidgetItem(node3_dokument))	
							self.tableWidget.setItem(ilosc,2, QTableWidgetItem(NIP_status_I))
							color = QColor(250,0,0)
							self.tableWidget.item(ilosc, 2).setBackground(color)
							tabela.append(ilosc)
							tabela.append(NIP_x)
							tabela.append(node3_dokument)
							tabela.append(NIP_status_I)
							
							
							tabela_pdf.append([ilosc+1,NIP_x,NIP_status_I,'C',czas1,'MF'])
							
							
							##print NIP_x+'|'+node3_dokument
							wynik.append(NIP_x+'|'+node3_dokument)
							ilosc = ilosc+1
							
				
				else:
					
					if NIP_len == 10:
						
						if NIP_status == 'N':
							czas1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
							self.tableWidget.setItem(ilosc,1, QTableWidgetItem(node3_dokument))
							self.tableWidget.setItem(ilosc,2, QTableWidgetItem(str(NIP_status_N))	)
								
							color = QColor(250,0,0)
							self.tableWidget.item(ilosc, 2).setBackground(color)
							tabela.append(ilosc)
							tabela.append(NIP_x)
							tabela.append(node3_dokument)
							tabela.append(NIP_status_N)
							
							
							tabela_pdf.append([ilosc+1,NIP_x,NIP_status_N,'C',czas1,'MF'])
							
							##print NIP_x+'|'+node3_dokument
							wynik.append(NIP_x+'|'+node3_dokument)
							ilosc = ilosc+1
						if NIP_status == 'C':
							czas1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
								
							self.tableWidget.setItem(ilosc,1, QTableWidgetItem(node3_dokument))
							self.tableWidget.setItem(ilosc,2, QTableWidgetItem(str(NIP_status_C)))
							color = QColor(50,205,50)
							self.tableWidget.item(ilosc, 2).setBackground(color)
							
							tabela_pdf.append([ilosc+1,NIP_x,NIP_status_C,'Z',czas1,'MF'])
							
							ilosc = ilosc+1
							
							
							
						if NIP_status == 'Z':
							czas1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
							self.tableWidget.setItem(ilosc,1, QTableWidgetItem(node3_dokument))
							self.tableWidget.setItem(ilosc,2, QTableWidgetItem(str(NIP_status_Z))	)
							color = QColor(50,205,50)
							self.tableWidget.item(ilosc, 2).setBackground(color)
							
							tabela_pdf.append([ilosc+1,NIP_x,NIP_status_Z,'Z',czas1,'MF'])
							
							ilosc = ilosc+1
							
							
						if NIP_status == 'I':
							czas1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
							item1 = QTableWidgetItem(str(NIP))
							item1.setBackground(QColor(255, 128, 128))
							self.tableWidget.setItem(ilosc,1, QTableWidgetItem(node3_dokument))
							self.tableWidget.setItem(ilosc,2, QTableWidgetItem(str(NIP_status_I)))
							color = QColor(250,0,0)
							self.tableWidget.item(ilosc, 2).setBackground(color)
							tabela.append(ilosc)
							tabela.append(NIP_x)
							tabela.append(node3_dokument)
							tabela.append(NIP_status_I)
							
							tabela_pdf.append([ilosc+1,NIP_x,NIP_status_I,'C',czas1,'MF'])
							
							##print NIP_x+'|'+node3_dokument
							wynik.append(NIP_x+'|'+node3_dokument)
							ilosc = ilosc+1
							
				#print 'aaaaaa'		
				self.centralwidget.update()	
				self.completed += count_bar
				self.progressBar.setValue(self.completed)	
				
				self.lista_value_error(tabela)
		if len(wynik) != 0:
			print wynik		
		if len(wynik) > 0:	
			pass		
		
		if len(tabela) == 0:
			msg.setWindowTitle(_fromUtf8("Analiza pliku JPK_VAT"))
			msg.setText(_fromUtf8("Plik poprawny"))
			
			msg.addButton(QPushButton(_fromUtf8('Sprawdz')), QMessageBox.RejectRole)
			msg.addButton(QPushButton('Zamknij'),QMessageBox.YesRole)
			
			returnValue = msg.exec_()	
			
			if returnValue == QMessageBox.RejectRole:
				MainWindow.close(); 
			
		else:
			
			
			msg.setWindowTitle(_fromUtf8("Analiza pliku JPK_VAT"))
			msg.setText(_fromUtf8("Wykryto błędne wpisy"))
			msg.addButton(QPushButton(_fromUtf8('Sprawdz')), QMessageBox.YesRole)
			msg.addButton(QPushButton('Zamknij'),QMessageBox.RejectRole)
			returnValue = msg.exec_()	
			
			if returnValue == QMessageBox.RejectRole:
				MainWindow.close(); 
				
		
	
	
						
	def showdialog():
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)

		msg.setText("This is a message box")
		msg.setInformativeText("This is additional information")
		msg.setWindowTitle("MessageBox demo")
		msg.setDetailedText("The details are as follows:")
		msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

	
		retval = msg.exec_()
		#print "value of pressed message box button:", retval
	
	
	def btnstate(self,b):
	
		#print b.isChecked()
		if b.isChecked() == True:
				#print  "selected"
				self.tableWidget.setRowCount(0);
				#self.wynik_do_tabeli(self.self.lista_value_error())
				return True
		else:
				#print "deselected"
				self.tableWidget.setRowCount(0);
				
				return False
	
	# def connect(self):
		
		# a = str(self.btnstate(self.checkBox))
		# #print a
		# if a == 'False':
			# self.connectMF_false()
		# if a == 'True':
		# # poprawiana funckja
			# self.connectMF_true()
			# #print (value_error)
			# #self.lista_nip()
	
	
	def pdf_save(self):
		import xml.etree.cElementTree as ET
		from io import BytesIO
		
		tablica_pdf_len = int(len(tabela_pdf))
		tablica_pdf_len1 = tablica_pdf_len/6
		
		if isAdmin():
			
			
			tablica_pdf_len = int(len(tabela_pdf))
			if tablica_pdf_len > 0:
			
				czas = time.strftime("%Y-%m-%d", time.localtime()) 
				invoice = ET.Element("invoice")
				ET.SubElement(invoice, "data").text = czas
						
				doc = ET.SubElement(invoice, "positions")
				
						
			
				for x in range(len(tabela_pdf)):
					for x1 in range(1):
						
						doc1 = ET.SubElement(doc, "position")
						ET.SubElement(doc1, "id").text = str(tabela_pdf[x][x1])
						ET.SubElement(doc1, "name").text = str(tabela_pdf[x][x1+1])
						ET.SubElement(doc1, "status").text = str(tabela_pdf[x][x1+2])
						ET.SubElement(doc1, "code").text = str(tabela_pdf[x][x1+3])
						ET.SubElement(doc1, "date_w").text = str(tabela_pdf[x][x1+4])
						ET.SubElement(doc1, "source").text = str(tabela_pdf[x][x1+5])
					
				if len(wynik) == 0:
					ET.SubElement(invoice, "validation").text = "0"	
				if len(wynik) != 0:	
					ET.SubElement(invoice, "validation").text = "1"				
				
				
				tree = ET.ElementTree(invoice)
				try:
					tree.write("raport_jpk.xml",encoding='utf-8', xml_declaration=True, )
							
											#pdf_save(args.parametr2)
					lok = []
					pathname = os.path.dirname(sys.argv[0])        #(2)
					lok = pathname.replace('lh_vat_status','lh_fop')
							#print 'path =', pathname
							#print 'full path =', os.path.abspath(pathname)
						#print 'aaa  '+lok	
					if os.path.exists(lok+'\\fop.bat'):
						import subprocess
							#os.popen('"'+lok+'\\fop.bat" -xml raport_jpk.xml -xsl raport_jpk.xsl -pdf C:\\raport_jpk.pdf')
							#os.system('"'+lok+'\\fop.bat" -xml raport_jpk.xml -xsl raport_jpk.xsl -pdf C:\\raport_jpk.pdf' )
						#subprocess.call('"'+lok+'\\fop.bat" -xml raport_jpk.xml -xsl raport_jpk.xsl -pdf C:\\raport_jpk.pdf')
						#subprocess.Popen('"'+lok+'\\fop.bat" -xml raport_jpk.xml -xsl raport_jpk.xsl -pdf C:\\raport_jpk.pdf', stdout=subprocess.PIPE, shell=True)
						FNULL = open(os.devnull, 'w')
						retcode = subprocess.call('"'+lok+'\\fop.bat" -xml raport_jpk.xml -xsl raport_jpk.xsl -pdf C:\\raport_jpk.pdf', stdout=FNULL, stderr=subprocess.STDOUT)
						if os.path.isfile('C:\\raport_jpk.pdf'):
							os.startfile('C:\\raport_jpk.pdf')
							
							#os.system( 'cls' )1
						else:
							msg = QMessageBox()
							msg.setIcon(QMessageBox.Information)
							msg.setWindowTitle(_fromUtf8("Raport"))
							msg.setText(_fromUtf8("Aby wygenerować raport konieczne jest uruchomienie programu w trybie Administratora (PPM na ikonie programu->uruchom jako administrator)"))
							msg.addButton(QPushButton('OK'),QMessageBox.YesRole)
							returnValue = msg.exec_()	
							
					else:
								
						msg = QMessageBox()
						msg.setIcon(QMessageBox.Information)
						msg.setWindowTitle(_fromUtf8("Raport dla pliku"))
						msg.setText(_fromUtf8("Proszę pobrać plugin do generowania dokumentów pdf (start-ustawienia globalne-ustawienia przeglądarki)"))
								
								
						msg.addButton(QPushButton('OK'),QMessageBox.YesRole)
								
						returnValue = msg.exec_()	
				except:
					
					msg = QMessageBox()
					msg.setIcon(QMessageBox.Information)
					msg.setWindowTitle(_fromUtf8("Raport dla pliku JPK_VAT"))
					msg.setText(_fromUtf8("Aby wygenerować raport konieczne jest uruchomienie programu w trybie Administratora (PPM na ikonie programu->uruchom jako administrator)"))
					msg.addButton(QPushButton('OK'),QMessageBox.YesRole)
					returnValue = msg.exec_()	
							
			
			else:
					
					msg = QMessageBox()
					msg.setIcon(QMessageBox.Information)
					msg.setWindowTitle(_fromUtf8("Raport dla pliku JPK_VAT"))
					msg.setText(_fromUtf8("Przed wygenerowaniem raportu sprawdz poprawnosc pliku JPK_VAT"))
					
					
					msg.addButton(QPushButton('OK'),QMessageBox.YesRole)
					
					returnValue = msg.exec_()	
		
		else:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setWindowTitle(_fromUtf8("Administrator"))
			msg.setText(_fromUtf8("Aby wygenerować raport konieczne jest uruchomienie programu w trybie Administratora (PPM na ikonie programu->uruchom jako administrator)"))
			msg.addButton(QPushButton('OK'),QMessageBox.YesRole)
			returnValue = msg.exec_()	
				
			
	
			

		
	
	
	def setupUi(self, MainWindow):
		
		#print 'OK'
		MainWindow.setObjectName(_fromUtf8("Lefthand Sprawdz, czy twój kontrahent jest czynnym podatnikiem VAT "))
		MainWindow.resize(760, 490)
		self.centralwidget = QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("Lefthand Sprawdz, czy twój kontrahent jest czynnym podatnikiem VAT"))
		self.tableWidget = QTableWidget(self.centralwidget)
		self.tableWidget.setGeometry(QRect(10, 50, 741, 300))
		self.tableWidget.setRowCount(1)
		self.tableWidget.setColumnCount(3)
		self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
		self.tableWidget.setHorizontalHeaderLabels(['NIP Kontrahenta','Numer Dokumentu', 'Status'])
	
		header = self.tableWidget.horizontalHeader()
		header.setResizeMode(QHeaderView.ResizeToContents)
		header.setResizeMode(2, QHeaderView.Stretch)
		
		self.pnt_load = QPushButton(self.centralwidget)
		self.pnt_load.setGeometry(QRect(280, 360, 181, 51))
		self.pnt_load.setObjectName(_fromUtf8("pnt_load"))
		self.pnt_load.raise_()
		self.pnt_load.clicked.connect(self.connectMF_false)
		self.pnt_load.setDefault(True)
		
		#self.pnt_load.clicked.connect(self.connectVies)
		self.label = QLabel(self.centralwidget)
		self.label.setGeometry(QRect(20, 10, 751, 16))
		self.label.setObjectName(_fromUtf8("label"))
		self.label1 = QLabel(self.centralwidget)
		self.label1.setGeometry(QRect(20, 30, 740, 16))
		self.label1.setObjectName(_fromUtf8("label1"))
		self.label2 = QLabel(self.centralwidget)
		self.label2.setGeometry(QRect(100, 30, 730, 16))
		self.label2.setObjectName(_fromUtf8("label2"))
		
		#self.label2.clicked.connect(self.connectVies)
		self.progressBar = QProgressBar(self.centralwidget)
		self.progressBar.setGeometry(QRect(10, 420, 750, 23))
		self.progressBar.setProperty("value", 0)
		self.progressBar.setObjectName(_fromUtf8("progressBar"))
		#self.checkBox = QCheckBox(self.centralwidget)
		#self.checkBox.setGeometry(QRect(20, 380, 201, 17))
		#self.checkBox.setObjectName(_fromUtf8("checkBox"))
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.menuBar = QMenuBar(MainWindow)
		self.menuBar.setGeometry(QRect(0, 0, 800, 21))
		self.menuBar.setObjectName(_fromUtf8("menuBar"))
		self.menuTEST = QMenu(self.menuBar)
		self.menuTEST.setObjectName(_fromUtf8("menuTEST"))
		MainWindow.setMenuBar(self.menuBar)
		self.actionTEST1 = QAction(MainWindow)
		self.actionTEST1.setObjectName(_fromUtf8("actionTEST1"))
		#self.actionTEST2 = QAction(MainWindow)
		#self.actionTEST2.setObjectName(_fromUtf8("actionTEST2"))
		self.menuTEST.addSeparator()
		self.menuTEST.addAction(self.actionTEST1)
		#self.menuTEST.addAction(self.actionTEST2)
		
		self.actionTEST1.triggered.connect(self.pdf_save)
		self.actionTEST1.setShortcut("Ctrl+Q")
		#self.actionTEST2.triggered.connect(self.val)
		#self.actionTEST2.setShortcut("Ctrl+W")
		self.menuBar.addAction(self.menuTEST.menuAction())	
		self.retranslateUi(MainWindow)
		QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		
		__sortingEnabled = self.tableWidget.isSortingEnabled()
		
		self.tableWidget.setSortingEnabled(False)
		self.tableWidget.setSortingEnabled(__sortingEnabled)
		
		MainWindow.setWindowTitle(_translate("MainWindow", "Lefthand Sprawdz, czy twój kontrahent jest czynnym podatnikiem VAT w GUS/VIES", None))
		self.pnt_load.setText(_translate("MainWindow", "Sprawdz plik", None))
		self.pnt_load.setShortcut(_translate("MainWindow", "Return", None))
		#self.checkBox.setText(_translate("MainWindow", "Wyswietl tylko nieprawidłowe wpisy", None))
		
		

		#self.label.setText('Hello, world!')
		self.label.setText(_translate("MainWindow",'Lokalizacja wczytanego pliku: '+args.parametr2, None))
		#self.label1.setText(_translate("MainWindow",'Walidacja pliku: ', None))
		#self.label2.setText(_translate("MainWindow",'Sprawdź poprawność xml (Ctrl+W) ', None))
		
		
		#self.checkBox.setChecked(False)
		#self.checkBox.toggled.connect(lambda:self.btnstate(self.checkBox))
		
		
		self.menuTEST.setTitle(_translate("MainWindow", "Opcje", None))
		self.actionTEST1.setText(_translate("MainWindow", "Wygeneruj raport", None))
		#self.actionTEST2.setText(_translate("MainWindow", "Walidacja pliku", None))


if __name__ == "__main__":

		if args.parametr1 == 'N':
			konsola(args.parametr2)
			
		elif args.parametr1 == 'R':
			pdf_save(args.parametr1)
			
			
		elif args.parametr1 == 'J':	
			
			app = QApplication(sys.argv)
			MainWindow = QMainWindow()
			ui = Ui_MainWindow()
			ui.setupUi(MainWindow)
			MainWindow.show()
			sys.exit(app.exec_())
			
		elif args.parametr1 == 'V':	
			# import xmlschema
			# from pprint import pprint
			# schema_file = open('StrukturyDanych_v4-0E.xsd')
			#schema_file = open('ElementarneTypyDanych_v4-0E.xsd')
			# xs = xmlschema.XMLSchema(schema_file)
			#print schema.validate('JPK_VAT_2019-01-106.xml')
			
			# xs = xmlschema.XMLSchema('StrukturyDanych_v4-0E.xsd', base_url='http://crd.gov.pl/xml/schematy/dziedzinowe/mf/2016/01/25/eD/DefinicjeTypy/')
			# print xs.to_dict('JPK_VAT_2019-01-106.xml')
			
			from lxml import etree
			parsed_doc = etree.parse("dokument.xml", etree.XMLParser(encoding='ISO-8859-1', ns_clean=True, recover=True)).getroot()
			print parsed_doc.tag
			
			
		
		elif (str(args.parametr1) != 'N' or args.parametr1 != 'V'  or args.parametr1 != 'R' or args.parametr1 != 'J'):
			konsola_json(args.parametr1, args.parametr2)	
	

