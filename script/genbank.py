#!/usr/bin/env python3

#from Bio import Entrez
import pandas as pd
#from Bio import SeqIO

from functools import partial
import shutil
from PyQt5 import QtWidgets, QtCore
from pip import main
from ui import Ui_MainWindow
from downloader_thread import ThreadClass
from parser_class import ParserClass
import os
import asyncio

class Genbank(QtWidgets.QMainWindow, QtCore.QObject):

	region_signal = QtCore.pyqtSignal(list)
	kingdom_signal = QtCore.pyqtSignal(list)
	
	def __init__(self, parent = None, index = 0):
		super(Genbank, self).__init__(parent)
		QtWidgets.QMainWindow.__init__(self)
		self.isRunning = False
		self.index = index
		self.MainWindow = QtWidgets.QMainWindow()
		self.mainwindow = Ui_MainWindow()
		self.mainwindow.setupUi(self.MainWindow)
		self.thread={}
		self.mainwindow.connect_ui(self)
		self.parser = ParserClass()
		self.region_choice = []
		self.kingdom_choice = []
		self.mutex = QtCore.QMutex()

		
		

################################################################################
################################################################################

	def get_kingdom_choice(self):
		self.mutex.lock()
		selected_kingdoms = []
		if(self.mainwindow.checkBox_viruses.isChecked()):
			selected_kingdoms = selected_kingdoms + ["Viruses"]
		if(self.mainwindow.checkBox_archaea.isChecked()):
			selected_kingdoms = selected_kingdoms + ["Archaea"]
		if(self.mainwindow.checkBox_bacteria.isChecked()):
			selected_kingdoms = selected_kingdoms + ["Bacteria"]
		if(self.mainwindow.checkBox_eukaryota.isChecked()):
			selected_kingdoms = selected_kingdoms + ["Eukaryota"]
		if(len(self.mainwindow.inputKingdom.toPlainText())):
			selected_kingdoms = selected_kingdoms + [self.mainwindow.inputKingdom.toPlainText()]

		self.kingdom_choice = selected_kingdoms
		self.mutex.unlock()


################################################################################
################################################################################


	def get_region_choice(self):
		self.mutex.lock()
		selected_regions = []
		if(self.mainwindow.checkBox_rrna.isChecked()):
			selected_regions = selected_regions + ["rRNA"]
		if(self.mainwindow.checkBox_cds.isChecked()):
			selected_regions = selected_regions + ["CDS"]
		if(self.mainwindow.checkBox_trna.isChecked()):
			selected_regions = selected_regions + ["tRNA"]
		if(self.mainwindow.checkBox_centromere.isChecked()):
			selected_regions = selected_regions + ["centromere"]
		if(self.mainwindow.checkBox_telomere.isChecked()):
			selected_regions = selected_regions + ["telomere"]
		if(self.mainwindow.checkBox_3utr.isChecked()):
			selected_regions = selected_regions + ["3'UTR"]
		if(self.mainwindow.checkBox_5utr.isChecked()):
			selected_regions = selected_regions + ["5'UTR"]
		if(self.mainwindow.checkBox_mobile_element.isChecked()):
			selected_regions = selected_regions + ["mobile_element"]
		if(self.mainwindow.checkBox_mobile_ncrna.isChecked()):
			selected_regions = selected_regions + ["ncRNA"]
		if(self.mainwindow.checkBox_mobile_intron.isChecked()):
			selected_regions = selected_regions + ["intron"]
		if(len(self.mainwindow.inputRegion.toPlainText())):
			selected_regions = selected_regions + [self.mainwindow.inputRegion.toPlainText()]

		self.region_choice = selected_regions
		self.mutex.unlock()


################################################################################
################################################################################


	def start(self, msg):
		index = self.sender().index
		if(index == 1):
			self.log(str(msg))

	def get_result(self, organism_df):
		self.log("Organism dataframe received")
		self.organism_df = organism_df
		self.mainwindow.buttonStart.setEnabled(True)
		self.mainwindow.buttonStart.setText("Stop Parsing")
		self.mainwindow.buttonStart.setStyleSheet("background-color: rgb(100, 20, 15);\n" "color:rgb(255, 255, 255);")
		

################################################################################
################################################################################

	def end(self, msg):
		index = self.sender().index
		if(index == 1):
			self.log(str(msg))
			self.mainwindow.buttonStart.setText("Start Parsing")
			self.mainwindow.buttonStart.setStyleSheet("background-color: rgb(0, 250, 125);\n" "color:rgb(0, 4, 38);")
			self.thread[1].stop()
			self.isRunning = False
			self.mainwindow.inputKingdom.setEnabled(True)
			self.mainwindow.inputRegion.setEnabled(True)
			self.mainwindow.checkBox_archaea.setEnabled(True)
			self.mainwindow.checkBox_bacteria.setEnabled(True)
			self.mainwindow.checkBox_eukaryota.setEnabled(True)
			self.mainwindow.checkBox_viruses.setEnabled(True)
			self.mainwindow.checkBox_archaea.setEnabled(True)
			self.mainwindow.checkBox_cds.setEnabled(True)
			self.mainwindow.checkBox_centromere.setEnabled(True)
			self.mainwindow.checkBox_mobile_element.setEnabled(True)
			self.mainwindow.checkBox_mobile_intron.setEnabled(True)
			self.mainwindow.checkBox_rrna.setEnabled(True)
			self.mainwindow.checkBox_trna.setEnabled(True)
			self.mainwindow.checkBox_3utr.setEnabled(True)
			self.mainwindow.checkBox_5utr.setEnabled(True)
			self.mainwindow.checkBox_telomere.setEnabled(True)

################################################################################
################################################################################


	def reset(self):

		if os.getcwd().endswith("script"):
				os.chdir('../')
		try:
			if os.getcwd().endswith("GENOME_REPORTS"):
				os.chdir('../')
			shutil.rmtree('./GENOME_REPORTS')
		except: print("cannot delete GENOME_REPORTS")
		try:
			if os.getcwd().endswith("pickle"):
				os.chdir('../')
			shutil.rmtree('./pickle')
		except: print("cannot delete pickle")
		try:
			if os.getcwd().endswith("Results"):
				os.chdir('../')
			shutil.rmtree('./Results')
		except: print("cannot delete ../Results")

		self.mainwindow.logOutput.clear()
		self.mainwindow.progressBar.setValue(0)
		print("reset")


################################################################################
################################################################################

	# Logger
	def log(self, str):
		self.mutex.lock()
		self.mainwindow.logOutput.insertPlainText(str + '\n')
		sb =self.mainwindow.logOutput.verticalScrollBar()
		sb.setValue(sb.maximum())
		self.mutex.unlock()
		
	def update_progress_bar(self, value):
		self.mutex.lock()
		index = self.sender().index
		if index == 1:
			self.mainwindow.progressBar.setProperty("value", self.mainwindow.progressBar.value() + value)
		self.mutex.unlock()

	def worker(self):

		if( self.isRunning == False):

			self.get_kingdom_choice()
			self.get_region_choice()

			if not len(self.region_choice) or not len(self.kingdom_choice):
				self.log("Il faut choisir au moins une région fonctionnelle et une Kingdom!")
				return

			self.isRunning = True
			self.mainwindow.buttonStart.setStyleSheet("background-color: rgb(30, 30, 65);\n" "color:rgb(250, 204, 238);")
			self.mainwindow.buttonStart.setText("Téléchargement...")
			self.mainwindow.buttonStart.setEnabled(False)
			self.mainwindow.inputKingdom.setEnabled(False)
			self.mainwindow.inputRegion.setEnabled(False)
			self.mainwindow.checkBox_archaea.setEnabled(False)
			self.mainwindow.checkBox_bacteria.setEnabled(False)
			self.mainwindow.checkBox_eukaryota.setEnabled(False)
			self.mainwindow.checkBox_viruses.setEnabled(False)
			self.mainwindow.checkBox_archaea.setEnabled(False)
			self.mainwindow.checkBox_cds.setEnabled(False)
			self.mainwindow.checkBox_centromere.setEnabled(False)
			self.mainwindow.checkBox_mobile_element.setEnabled(False)
			self.mainwindow.checkBox_mobile_intron.setEnabled(False)
			self.mainwindow.checkBox_rrna.setEnabled(False)
			self.mainwindow.checkBox_trna.setEnabled(False)
			self.mainwindow.checkBox_3utr.setEnabled(False)
			self.mainwindow.checkBox_5utr.setEnabled(False)
			self.mainwindow.checkBox_telomere.setEnabled(False)

			self.thread[1] = ThreadClass(parent = self, index=1)
			self.thread[1].start()
			self.region_signal.emit(self.region_choice)
			self.kingdom_signal.emit(self.kingdom_choice)
			self.thread[1].any_signal.connect(self.start)
			self.thread[1].dataframe_result.connect(self.get_result)
			self.thread[1].progress_signal.connect(self.update_progress_bar)
			self.thread[1].time_signal.connect(self.start)
			self.thread[1].end_signal.connect(self.end)
			self.mainwindow.logOutput.clear()
			self.mainwindow.logOutput.insertPlainText('Parsing Started\n')

		else:
			self.mainwindow.buttonStart.setText("Start Parsing")
			self.mainwindow.buttonStart.setStyleSheet("background-color: rgb(0, 250, 125);\n" "color:rgb(0, 4, 38);")
			self.thread[1].stop()
			self.isRunning = False
			self.mainwindow.logOutput.clear()
			self.mainwindow.logOutput.insertPlainText('Parsing stopped\n')
		
		
