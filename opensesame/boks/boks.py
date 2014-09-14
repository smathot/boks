"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame import item, generic_response, exceptions, debug, misc
from libqtopensesame import qtplugin
from libqtopensesame.misc import _
from openexp.keyboard import keyboard
import imp
import os
import os.path
from PyQt4 import QtGui, QtCore, uic

# First try to load libboks from source, from the plug-in folder. If this fails,
# try a plain import statement.
try:
	libboks = imp.load_source(u'libboks', os.path.join(os.path.dirname( \
		__file__).decode(misc.filesystem_encoding()), u'libboks.py'))
except:
	import libboks

class boks(item.item, generic_response.generic_response):

	"""A plug-in for using the Boks"""
	
	description = u'Collects input from a boks'
	
	def __init__(self, name, experiment, script=None):

		"""
		Constructor.

		Arguments:
		name 		--	Item name.
		experiment 	--	An experiment object.

		Keywords arguments:
		script 		--	Definition script (default=None)
		"""

		self.timeout = u'infinite'
		self.dev = u'autodetect'	
		self._dummy = u'no'
		self.process_feedback = True
		item.item.__init__(self, name, experiment, script)

	def prepare(self):

		"""Prepare the boks"""

		item.item.prepare(self)
		
		self._keyboard = keyboard(self.experiment)

		# Prepare the device string
		if self.get(u'_dummy') == u'yes':
			dev = u'dummy'
		else:
			dev = self.get(u'dev')
			if dev == u'autodetect':
				dev = None

		# Dynamically load a boks instance
		if not hasattr(self.experiment, u'boks'):
			self.experiment.boks = libboks.libboks(dev, experiment= \
				self.experiment)
			self.experiment.cleanup_functions.append(self.close)
		model, firmware_version = self.experiment.boks.info()
		self.experiment.set(u'boks_model', model)
		self.experiment.set(u'boks_firmware_version', firmware_version)
			
		# Prepare the allowed responses
		if self.has(u"allowed_responses"):
			self._allowed_responses = []
			for r in self.unistr(self.get(u"allowed_responses")).split(u";"):
				if r.strip() != u"":
					try:
						r = int(r)
					except:
						raise exceptions.runtime_error( \
							u"'%s' is not a valid response in boks '%s'. Expecting a number in the range 1 .. 4." \
							% (r, self.name))
					if r not in range(1,9):
						raise exceptions.runtime_error( \
							u"'%s' is not a valid response in boks '%s'. Expecting a number in the range 1 .. 8." \
							% (r, self.name))
					self._allowed_responses.append(r)
			if len(self._allowed_responses) == 0:
				self._allowed_responses = None
		else:
			self._allowed_responses = None			
		debug.msg(u"allowed responses set to %s" % self._allowed_responses)
			
		# Prepare the timeout
		self.prepare_timeout()

	def run(self):

		"""Run the Boks"""

		self.set_item_onset()
		self._keyboard.flush()

		# If no start response interval has been set, set it to the onset of
		# the current response item
		if self.experiment.start_response_interval == None:
			self.experiment.start_response_interval = self.get(u"time_%s" \
				% self.name)
				
		# Send the timeout and allowed responses to the boks
		self.experiment.boks.set_timeout(self._timeout)
		self.experiment.boks.set_buttons(self._allowed_responses)
				
		# Get the response
		self.experiment.response, self.experiment.end_response_interval = \
			self.experiment.boks.get_button_press()

		debug.msg(u"received %s" % self.experiment.response)		
		generic_response.generic_response.response_bookkeeping(self)

	def close(self):

		"""Neatly close the connection to the boks"""

		if not hasattr(self.experiment, u"boks") or self.experiment.boks == None:
			debug.msg(u"no active boks")
			return		
		try:
			self.experiment.boks.close()
			debug.msg(u"boks closed")
		except:
			debug.msg(u"failed to close boks")

	def var_info(self):

		return generic_response.generic_response.var_info(self)

class qtboks(boks, qtplugin.qtplugin):

	"""The GUI part of the boks plug-in."""

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.

		Arguments:
		name 		--	Item name.
		experiment 	--	An experiment object.

		Keywords arguments:
		script 		--	Definition script (default=None)
		"""

		boks.__init__(self, name, experiment, script)
		qtplugin.qtplugin.__init__(self, __file__)		

	def init_edit_widget(self):

		"""Setup the item controls"""

		self.lock = True
		qtplugin.qtplugin.init_edit_widget(self, False)	
		
		self.boks_widget = QtGui.QWidget()
		path = os.path.join(os.path.dirname(__file__), "boks_widget.ui")
		self.boks_widget.ui = uic.loadUi(open(path), self.boks_widget)
		self.experiment.main_window.theme.apply_theme(self.boks_widget)
		self.boks_widget.ui.label_boks_icon.setPixmap(QtGui.QPixmap( \
			self.experiment.resource(u"boks_large.png")))
		self.boks_widget.ui.label_boks.setText(unicode( \
			self.boks_widget.ui.label_boks.text()) % libboks.version)
			
		# Load icons for buttons
		self.icons = {}
		for i in range(1,9):
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(os.path.join( \
				os.path.dirname(__file__), 'icons', 'active%d.png' % i)),
				QtGui.QIcon.Normal)
			icon.addPixmap(QtGui.QPixmap(os.path.join( \
				os.path.dirname(__file__), 'icons', 'inactive%d.png' % i)),
				QtGui.QIcon.Disabled)
			getattr(self.boks_widget.ui, 'button_%d' % i).setIcon(icon)
		
		self.edit_vbox.addWidget(self.boks_widget)
		self.edit_vbox.addStretch()
		self.boks_widget.ui.widget_test.hide()
		self.boks_widget.ui.button_start_test.clicked.connect(self.start_test)
		self.boks_widget.ui.button_stop_test.clicked.connect(self.stop_test)
		self.auto_add_widget(self.boks_widget.ui.edit_dev, u'dev')
		self.auto_add_widget(self.boks_widget.ui.edit_correct_response, \
			u'correct_response')
		self.auto_add_widget(self.boks_widget.ui.edit_allowed_responses, \
			u'allowed_responses')
		self.auto_add_widget(self.boks_widget.ui.edit_timeout, \
			u'timeout')
		self.auto_add_widget(self.boks_widget.ui.checkbox_dummy, \
			u'_dummy')
		self.edit_vbox.addStretch()
		self.lock = True

	def apply_edit_changes(self):

		"""Apply the controls"""

		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return False
		self.experiment.main_window.refresh(self.name)
		return True

	def edit_widget(self):

		"""Update the controls"""

		self.lock = True
		qtplugin.qtplugin.edit_widget(self)
		self.lock = False
		return self._edit_widget	
		
	def start_test(self):
		
		"""Show the test controls and start the test thread"""
		
		self.boks_widget.ui.button_start_test.hide()
		self.boks_widget.ui.widget_test.show()
		self.test_thread = boks_test_thread(self)
		self.test_thread.start()

	def stop_test(self):
		
		"""Deactivate the test thread and hide the test controls"""
		
		self.boks_widget.ui.button_start_test.show()
		self.boks_widget.ui.widget_test.hide()
		self.test_thread.active = False

class boks_test_thread(QtCore.QThread):
	
	"""A thread that connects to the boks and polls the button state"""
	
	def __init__(self, parent):
		
		"""
		Constructor
		
		Arguments:
		parent -- the parent QWidget (a qtboks item)
		"""

		QtCore.QThread.__init__(self, parent)
		self.boks_item = parent		
		dev = self.boks_item.get(u"dev")
		if dev == u"autodetect":
			dev = None
		self.boks_item.boks_widget
		self.active = True
		path = os.path.join(os.path.dirname(__file__), "libboks.py")
		_boks = imp.load_source(u"libboks", path)
		try:
			self.boks = _boks.libboks(dev, experiment=self.boks_item.experiment)
			firmware_version, model = self.boks.info()
			button_count = self.boks.button_count()
			sid = self.boks.get_sid()
		except:
			firmware_version = u'NA'
			model = u'No boks detected'
			button_count = 0
			sid = u'000000'
			self.boks = None
		self.boks_item.boks_widget.ui.edit_firmware_version.setText( \
			firmware_version)
		self.boks_item.boks_widget.ui.edit_model.setText(model)
		self.boks_item.boks_widget.ui.spinbox_button_count.setValue( \
			button_count)
		self.boks_item.boks_widget.ui.edit_sid.setText(sid)
			
		# Change the icon for the buttons that are not reported by the device.
		# The trick is to set all buttons and then see which buttons are
		# actually accepted by the Boks.
		if self.boks != None:
			self.boks.set_buttons(range(1,9))
			l = self.boks.get_buttons()
			for i in range(1,9):
				if i not in l:
					icon = QtGui.QIcon()
					icon.addPixmap(QtGui.QPixmap(os.path.join( \
						os.path.dirname(__file__), 'icons', \
						'unavailable.png')), QtGui.QIcon.Disabled)
					getattr(self.boks_item.boks_widget.ui, u'button_%d' \
						% i).setIcon(icon)
		
	def run(self):
		
		"""Continuously poll the button state and toggle the QPushButtons"""
		
		while self.active and self.boks != None:
			pressed_buttons = self.boks.get_button_state()
			for i in range(1, 9):
				button = getattr(self.boks_item.boks_widget.ui, u'button_%d' \
					% i)
				button.setEnabled(i in pressed_buttons)
		if self.boks != None:
			self.boks.close()
