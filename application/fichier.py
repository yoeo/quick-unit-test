#!/usr/bin/python
# -*- coding:Utf-8 -*-
# 
#
#
# Interface
# fichier.py
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

class Fichier:
	def __init__ (self):
		self.contenu = ""
		self.nom = None
		
	def ouvrir (self, nom):
		self.nom = nom
		try:
			f = open (nom, "r")
			self.contenu = f.read()
			f.close ()
			return True
		except Exception:
			self.alerte ("Impossible d'ouvrir le fichier spécifié.")
			return False
	
	def sauvegarder (self, nom = None):
		if (not nom):
			nom = self.nom
		try:
			f = open (nom, "w")
			f.write(self.contenu)
			f.close ()
			return True
		except Exception:
			self.alerte ("Impossible de sauvegarder le fichier spécifié.")
			return False

	def desactiver (self, txt_view):
		tampon = txt_view.get_buffer()
		self.contenu = tampon.get_text(tampon.get_start_iter(), tampon.get_end_iter())
	
	def activer (self, txt_view):
		tampon = txt_view.get_buffer()
		tampon.set_text(self.contenu)

	def alerte (self, message):
		dialog = gtk.MessageDialog (type = gtk.MESSAGE_ERROR, buttons = gtk.BUTTONS_OK, message_format = message)
		dialog.connect ("response", self.detruire)
		dialog.run ()
		
	def detruire (self, source = None, event = None):
		source.destroy ()

