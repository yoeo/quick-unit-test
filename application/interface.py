#!/usr/bin/python
# -*- coding:Utf-8 -*-
# 
#
#
# Interface
# interface.py
# Copyright (C) Intuitive 2009 <projet_fe@yahoo.com>
# 
#
#
# Interface is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# iTerminal is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.



import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade

import sys

from fichier import Fichier

class Interface:
	"""
	Les objets de l'ui:
	<objet> - <liste des evenements>
	
	fenetre - quitter
	commande - valider
	reponse
	aide
	aide_region
	interrupteur_aide - aide_visibilite
	"""
	# Les fonctions automatiques pour charger et gérer Glade
	# Pour appeller un élément "element" de Glade il suffit de taper self["element"]
	def __init__ (self):
		import os
		os.chdir (sys.path[0])
		self.Widgets = gtk.glade.XML ("interface.glade","fenetre")
		self.newProj = None
		self.AutoConnect (self.Widgets, "ui_")

		self.source = Fichier ()
		self.tu = Fichier ()
		self.cahier = Fichier ()
		self.editeur = False
		self.actif = "chg" # "tu" "src" "chg"
				
	def __getitem__ (self, key):
		return self.Widgets.get_widget(key)

	def AutoConnect(self, fenetre, ext):
		eventHandlers = {}
		for (itemName, value) in self.__class__.__dict__.items():
			if callable(value) and itemName.startswith(ext):
				eventHandlers[itemName[len(ext):]] = getattr(self,itemName)
		fenetre.signal_autoconnect(eventHandlers)
	
	def bascule (self, editeur):
		if (editeur):
			self["scl_fichier"].show ();
			self["scl_cahierchg"].hide ();
			self["btn_enregistrer"].show ();
			self["btn_enregistrer_tout"].show ();
			#self["btn_imprimer"].hide ();
		else:
			self["scl_cahierchg"].show ();
			self["scl_fichier"].hide ();
			self["btn_enregistrer"].hide ();
			self["btn_enregistrer_tout"].hide ();
			#self["btn_imprimer"].show ();
	
	def activePanneau (self, etat):
		if (self.actif != etat):
			precedant = self.actif
			self.actif = etat
			if (precedant == "src"):
				self.source.desactiver (self["txt_fichier"])
				self["btn_source"].set_active (False)
				if (etat == "tu"):
					self.tu.activer (self["txt_fichier"])
				elif (etat == "chg"):
					self.bascule (False)
			if (precedant == "tu"):
				self.tu.desactiver (self["txt_fichier"])
				self["btn_tu"].set_active (False)
				if (etat == "src"):
					self.source.activer (self["txt_fichier"])
				elif (etat == "chg"):
					self.bascule (False)
			if (precedant == "chg"):
				self.bascule (True)
				if (etat == "src"):
					self["btn_source"].set_active (True)
					self.source.activer (self["txt_fichier"])
				elif (etat == "tu"):
					self["btn_tu"].set_active (True)
					self.tu.activer (self["txt_fichier"])

	def toutSensibiliser (self):
		self["btn_source"].set_sensitive (True)
		self["btn_tu"].set_sensitive (True)
		self["btn_valider"].set_sensitive (True)
		self["btn_exe"].set_sensitive (True)
		#self["btn_imprimer"].set_sensitive (True)

	def compiler (self, commande):
		from subprocess import Popen, PIPE, STDOUT
		pipe = Popen(commande, shell=True, cwd=None, env=None, stdout=PIPE, stderr=STDOUT)
		(reponse, erreur) = pipe.communicate(input=input)
		if erreur:
			self.alerte ("Les données entrées ne sont pas valides.")
			return False
		return True

	def alerte (self, message):
		dialog = gtk.MessageDialog (type = gtk.MESSAGE_ERROR, buttons = gtk.BUTTONS_OK, message_format = message)
		dialog.connect ("response", self.detruire)
		dialog.run ()
		
	def detruire (self, source = None, event = None):
		source.destroy ()

	# Les gestionnaires d'évenements
	# Lorsqu'un évenement est définit comme "evenement" dans l'interface,
	# son gestionnaire doit s'appeler "ui_evenement (self, source = None, event = None)"

	def ui_quitter (self, source = None, event = None):
		gtk.main_quit()
		
	def ui_about (self, source = None, event = None):
		self.info = gtk.glade.XML ('interface.glade',"info")
		self.AutoConnect (self.info, "ui_info_")
	
	def ui_nouveauprojet (self, source = None, event = None):
		self.newProj = gtk.glade.XML ('interface.glade',"new_projet")
		self.AutoConnect (self.newProj, "ui_new_")
		src = self.newProj.get_widget("btn_source")
		tu = self.newProj.get_widget("btn_tu")
		src.set_current_folder ("../exemple")
		tu.set_current_folder ("../exemple")
		fc = gtk.FileFilter ()
		fc.set_name ("Fichier source")
		fc.add_pattern ("*.c")
		src.add_filter (fc)
		fxml = gtk.FileFilter ()
		fxml.set_name ("Fichier de définition de test")
		fxml.add_pattern ("*.xml")
		tu.add_filter (fxml)
	
	def ui_activer_tu (self, source = None, event = None):
		if (self["btn_tu"].get_active()):
			self.activePanneau ("tu")
		elif (self.actif == "tu"):
			self["btn_tu"].set_active(True)
			
	def ui_activer_source (self, source = None, event = None):
		if (self["btn_source"].get_active()):
			self.activePanneau ("src")
		elif (self.actif == "src"):
			self["btn_source"].set_active(True)
	
	def ui_executer (self, source = None, event = None):
		self.activePanneau ("chg")
		self.tu.sauvegarder ("tmp_tu.xml")
		self.source.sauvegarder ("tmp_src.c")
		self.compiler ("./generator tmp_tu.xml")
		self.compiler ("gcc tmp_tu.xml.c tmp_src.c -o tmp_exe")
		self.compiler ("./tmp_exe > ../cahier-de-charge.txt")
		self.compiler ("rm ./tmp_*")
		self.cahier.ouvrir ("../cahier-de-charge.txt")
		self.cahier.activer (self["txt_cahierchg"])
	
	def ui_enregistrer (self, source = None, event = None):
		if (self.actif == "tu"):
			self.tu.desactiver (self["txt_fichier"])
			self.tu.sauvegarder ()
		if (self.actif == "src"):
			self.source.desactiver (self["txt_fichier"])
			self.source.sauvegarder ()

	def ui_enregistrer_tout (self, source = None, event = None):
		if (self.actif == "tu"):
			self.tu.desactiver (self["txt_fichier"])
		if (self.actif == "src"):
			self.source.desactiver (self["txt_fichier"])
		self.tu.sauvegarder ()
		self.source.sauvegarder ()

	def ui_imprimer (self, source = None, event = None):
		self.alerte ("Non implémentée")
		
	def ui_ouvre_manuel (self, source = None, event = None):
		self.compiler ("firefox ./aide/test.html")
		
	# Les gestionnaires d'évenements
	# de la fenêtre d'informations
	
	def ui_info_quitter (self, source = None, event = None):
		fen = self.info.get_widget("info")
		fen.destroy ()
		
	# Les gestionnaires d'évenements
	# du dialogue de nouveau projet
	
	def ui_new_choix_source (self, source = None, event = None):
		tu = self.newProj.get_widget("btn_tu")
		if (tu.get_filename ()):
			ok = self.newProj.get_widget("btn_ok")
			ok.set_sensitive (True)

	def ui_new_choix_tu (self, source = None, event = None):
		src = self.newProj.get_widget("btn_source")
		if (src.get_filename ()):
			ok = self.newProj.get_widget("btn_ok")
			ok.set_sensitive (True)
	
	def ui_new_valider (self, source = None, event = None):
		tu = self.newProj.get_widget("btn_tu")
		src = self.newProj.get_widget("btn_source")
		if (self.source.ouvrir (src.get_filename ()) and self.tu.ouvrir (tu.get_filename ())):
			self.toutSensibiliser ()
			self.activePanneau ("tu")
		fen = self.newProj.get_widget("new_projet")
		fen.destroy ()
				
	def ui_new_quitter (self, source = None, event = None):
		fen = self.newProj.get_widget("new_projet")
		fen.destroy ()

if __name__ == '__main__':
	app = Interface()
	gtk.main()

