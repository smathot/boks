#-*- coding:utf-8 -*-

"""
This file is part of Boks.

Boks is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Boks is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Boks.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import serial
import struct
import time

# The command byes that are used to communicate with the Arduino
CMD_RESET			= chr(1)
CMD_IDENTIFY 		= chr(2)
CMD_WAIT_PRESS 		= chr(3)
CMD_WAIT_RELEASE 	= chr(4)
CMD_WAIT_SLEEP		= chr(5)
CMD_BUTTON_STATE	= chr(6)
CMD_SET_T1			= chr(7)
CMD_SET_T2			= chr(8)
CMD_SET_TIMEOUT		= chr(9)
CMD_SET_BUTTONS		= chr(10)
CMD_SET_CONTINUOUS	= chr(11)
CMD_GET_T1			= chr(12)
CMD_GET_T2			= chr(13)
CMD_GET_TD			= chr(14)
CMD_GET_TIME		= chr(15)
CMD_GET_TIMEOUT		= chr(16)
CMD_GET_BUTTONS		= chr(17)
CMD_LED_ON			= chr(18)
CMD_LED_OFF			= chr(19)
CMD_GET_BTNCNT		= chr(20)
CMD_GET_SID			= chr(21)
CMD_LINK_LED		= chr(22)

version = '1.0.1'
baudrate = 115200
button_timeout = 255
all_buttons = [] # Except the photodiode, which is button 8
firmware_version_length = 5
model_length = 16
sid_length = 6

class boks_exception(Exception):

	"""
	desc:
		A custom Exception class for nice error messages.
	"""

	pass

class libboks(object):

	"""
	desc: |
		A Python library to interface with Boks, a button box for psychological
		and neuroscientific experiments.

		If there is a Boks plug-in in your OpenSesame experiment, the `boks`
		object can be accessed as `exp.boks` or `self.experiment.boks`.

		__Example__:

		~~~ {.python}
		# Collect a response time with a 2000ms timeout
		exp.boks.set_timeout(2000)
		t1 = self.time()
		button, t2 = exp.boks.get_button_press()
		exp.set('response', button)
		exp.set('response_time', t2-t1)
		~~~

		__Function list:__

		%--
		toc:
			mindepth: 2
			maxdepth: 2
		--%

		%--
		constant:
			ret_button: |
				A (button, timestamp) tuple. If a timeout occured, `button` is
				`None`, otherwise `button` is an integers. `timestamp` is a
				float value in milliseconds.
		--%
	"""

	def __init__(self, port=None, experiment=None, baudrate=115200,
		buttons=None, timeout=None, led=False):

		"""
		desc:
			Constructor. A Boks object is created automatically the first time
			that a Boks plug-in is prepared in OpenSesame.

		keywords:
			port:
				desc:	The port to which the device is connected, `None`
						for autodetect, or 'dummy' to use the keyboard as
						dummy-boks.
				type:	[str, unicode, NoneType]
			experiment:
				desc:	An OpenSesame experiment, or `None` to run in plain
						Python mode.
				type:	[experiment, NoneType]
			baudrate:
				desc:	The baudrate of the boks, or `None` to use default.
				type:	[int, NoneType]
			buttons:
				desc:	A list of buttons that are used, or None to use all
						buttons.
				type:	[list, NoneType]
			timeout:
				desc:	A timeout in milliseconds when collecting responses or
						`None` for no timeout.
				type:	[float, int, NoneType]
			led:
				desc:	Indicates whether the LED should be switched on.
				type:	bool

		example: |
			# Collect a response with a 2000ms timeout
			exp.boks.set_timeout(2000)
			t1 = self.time()
			button, t2 = exp.boks.get_button_press()
			exp.set('response', button)
			exp.set('response_time', t2-t1)
		"""

		# In dummy mode, we morph into the dummy class
		if port == 'dummy':
			if experiment == None:
				raise boks_exception( \
					'In order to use dummy mode, libboks must be used in OpenSesame mode')
			self.__class__ = dummy
			self.__init__(experiment=experiment, timeout=timeout, buttons= \
				buttons)
			return

		# Use OpenSesame if possible
		if experiment != None:
			from libopensesame import debug
			self.time = experiment.time
			self.msg = debug.msg
			self.experiment = experiment

		self.msg('initializing')

		# Autodetect the port
		if port == None:
			if os.name == 'posix':
				self.port = '/dev/ttyACM0'
			else:
				self.port = 'COM3'
		else:
			self.port = port
		self.msg('port: %s' % self.port)
		self.dev = serial.Serial(self.port, baudrate=baudrate)

		# Set up link
		self.identify()
		self.set_buttons(buttons)
		self.set_timeout(timeout)
		self.set_led(on=led)
		self.msg('ready')		

	def _get_button(self, cmd_byte):

		"""
		visible:
			False

		desc:
			Collect a button press or release, depending on value.

		arguments:
			cmd_byte:
				desc:	CMD_WAIT_PRESS or CMD_WAIT_RELEASE
				type:	int

		returns:
			desc:	"%ret_button"
			type:	tuple
		"""

		# Mark the start of the response interval
		start_time = self.time()
		self.dev.write(CMD_SET_T1)
		# Wait for a response
		self.dev.write(cmd_byte)
		button = self.read_byte()
		# Get the response time and use this to determine the end time
		self.dev.write(CMD_GET_TD)
		time = start_time + .001 * self.read_ulong()
		# Return
		if button == button_timeout:
			return None, time
		return button, time

	def byte_to_list(self, b):

		"""
		visible:
			False

		desc:
			Converts a byte to a list, so that the first bit corresponds to 1,
			the second to 2, etc.

		arguments:
			b:
				desc:	A numeric value.
				type:	int

		returns:
			desc:	A list of integers.
			type:	list
		"""

		l = []
		for i in range(0, 8):
			if b & 2**i:
				l.append(i+1)
		return l
	
	def button_count(self):
		
		"""
		desc:
			Gets the number of buttons that are physically present on the
			device. This number includes the photodiode, so a Boks with four
			buttons and a photodiode will be reported as having five buttons.
		
		returns:
			desc:	The number of buttons
			type:	int
		
		example: |
			i = exp.boks.button_count()
			print('Your Boks has %d buttons' % i)
		"""
		
		self.dev.write(CMD_GET_BTNCNT)
		return self.read_byte()

	def close(self):

		"""
		desc:
			Neatly close the device. This will deactivate the boks and close the
			serial port connection. OpenSesame will do this automatically when
			the experiment ends.
		
		example: |
			exp.boks.close()
		"""

		self.msg('closing')
		self.dev.close()
		self.msg('closed')

	def connection_error(self):

		"""
		visible:
			False

		desc:
			Raises an exception to indicate a connection error.
		"""

		raise boks_exception('There was an error connecting to the boks')

	def get_button_press(self):

		"""
		desc:
			Collects a button press.

		returns:
			desc:	"%ret_button"
			type:	tuple
		
		example: |
			# Collect a response with a 2000ms timeout
			exp.boks.set_timeout(2000)
			t1 = self.time()
			button, t2 = exp.boks.get_button_press()
			exp.set('response', button)
			exp.set('response_time', t2-t1)
		"""

		return self._get_button(CMD_WAIT_PRESS)

	def get_button_release(self):

		"""
		desc:
			Collects a button release.

		returns:
			desc:	"%ret_button"
			type:	tuple

		example: |
			# Collect a button release with a 2000ms timeout
			exp.boks.set_timeout(2000)
			t1 = self.time()
			button, t2 = exp.boks.get_button_release()
			exp.set('response', button)
			exp.set('response_time', t2-t1)
		"""

		return self._get_button(CMD_WAIT_RELEASE)

	def get_button_state(self):

		"""
		desc:
			Checks which buttons are currently pressed.

		returns:
			desc:	A list of buttons that are currently pressed.
			type:	list

		example: |
			l = exp.boks.get_button_state()
			if 1 in l:
				print('Button 1 is pressed')
		"""

		self.dev.write(CMD_BUTTON_STATE)
		return self.byte_to_list(self.read_byte())

	def get_buttons(self):

		"""
		desc:
			Retrieves the list of buttons that are 'active', i.e. that are used
			by [get_button_press], [get_button_release], and [get_button_state].

		returns:
			desc:	A list of active buttons.
			type:	list

		example: |
			l = exp.boks.get_buttons()
			if 1 in l:
				print('Button 1 is currently being monitored')
		"""

		self.dev.write(CMD_GET_BUTTONS)
		return self.byte_to_list(self.read_byte())
	
	def get_sid(self):
		
		"""
		desc:
			Retrieves the Arduino serial ID.
		
		returns:
			desc:	A 7 character string containing the Arduino serial ID.
			type:	str
		
		example: |
			sid = exp.boks.get_sid()
			print('The Arduino serial ID of the Boks is %s' % sid)
		"""
		
		self.dev.write(CMD_GET_SID)
		return self.dev.read(sid_length)

	def get_timeout(self):

		"""
		desc:
			Gets the timeout used by [get_button_press] and
			[get_button_release].

		returns:
			desc:	A timeout value in milliseconds or `None` if no timeout is
					set.
			type:	int
		
		example: |
			exp.boks.set_timeout(2000)
			t = exp.boks.get_timeout()
			print('The Boks timeout is currently set to %d ms' % t)
		"""

		self.dev.write(CMD_GET_TIMEOUT)
		return .001 * self.read_ulong()

	def identify(self):

		"""
		visible:
			False

		desc:
			Retrieves the model and firmware version from the boks, in order to
			check whether we are dealing with a real boks.
		"""

		self.dev.timeout = 2
		while True:
			self.dev.write(CMD_IDENTIFY)
			s = self.dev.read(firmware_version_length)
			if s != '':
				break
		self.firmware_version = s
		self.msg('firmware version: %s' % s)
		s = self.dev.read(model_length).strip()
		self.model = s
		self.msg('model: %s' % s)
		self.dev.timeout = None

	def info(self):

		"""
		desc:
			Gets boks device info.

		returns:
			desc:	A (firmware_version, model) tuple. The firmware_version is a
					string of the format X.Y.Z. The model is a short string.
			type:	tuple
		
		example: |
			firmware, model = exp.boks.info()
			print('Boks model: %s' % model)
			print('Boks firmware: %s' % firmware)
		"""

		return self.firmware_version, self.model

	def msg(self, msg):

		"""
		visible:
			False

		desc:
			Prints a debugging message. In OpenSesame mode, the OpenSesame debug
			functionality will be used instead.

		arguments:
			msg:
				desc:	A message.
				type:	[str, unicode]
		"""

		print('libboks: %s' % msg)

	def read_byte(self):

		"""
		visible:
			False

		desc:
			Reads a single byte from the Boks.

		returns:
			desc:	An integer between 0 and 255.
			type:	int
		"""

		v = self.dev.read(1)
		if v == '':
			self.connection_error()
		return ord(v)

	def read_ulong(self):

		"""
		visible:
			False

		desc:
			Reads a single unsigned long from the Boks, which consists of 4
			bytes.

		returns:
			desc:	An integer between 0 and 4,294,967,295.
			type:	int
		"""

		v = self.dev.read(4)
		if v == '':
			self.connection_error()
		return struct.unpack('I', v)[0]

	def set_buttons(self, buttons):

		"""
		desc:
			Sets which buttons should be used for [get_button_press],
			[get_button_release], and [get_button_state].

		arguments:
			buttons:
				desc:	A list of buttons, where each button is an integer. To
						enable all buttons (except for the photodiode), use
						`None`.
				type:	[list, NoneType]

		example: |
			# Only use buttons 1 and 2
			exp.boks.set_buttons([1,2])
			# Use all buttons except for the photodiode
			exp.boks.set_buttons(None)
			# Only use the photodiode (button 8)
			exp.boks.set_buttons([8])
		"""

		if buttons == None:
			buttons = all_buttons
		try:
			buttons = list(buttons)
		except:
			raise boks_exception( \
				'Expecting a list of integers, or similar parameter')
		v = 0
		for button in buttons:
			try:
				button = int(button)
			except:
				raise boks_exception( \
					'Expecting a list of integers, or similar parameter')
			v += 1 << (button-1)
		if v > 255:
			raise boks_exception( \
				'Expecting button numbers between 1 and 8')
		self.msg('Setting buttons %s with value %s' % (buttons, bin(v)))
		self.dev.write(CMD_SET_BUTTONS)
		self.dev.write(chr(v))

	def set_continuous(self, continuous=True):

		"""
		desc:
			Determines whether [get_button_press] and [get_button_release] are
			triggered only by signal changes (discontinuous) or also by
			continuous signals. The Boks is by default in discontinuous mode,
			which is generally what you want. For example, in continuous mode,
			[get_button_press] will respond right away if any of the buttons
			is already pressed, whereas you are generally interested only in
			buttons that go from not being pressed to being pressed.


		keywords:
			continuous:
				desc:	True for continuous, False for discontinuous.
				type:	bool
							
		example: |
			exp.boks.set_continuous(True)
			t1 = exp.time()
			# If some button is not pressed, this will return right away
			button, t2 = exp.boks.get_button_release()
			exp.set('response', button)
			exp.set('response_time', t2-t1)
		"""

		self.dev.write(CMD_SET_CONTINUOUS)
		if continuous:
			self.dev.write(chr(1))
		else:
			self.dev.write(chr(0))
			
	def set_led(self, on=True):
		
		"""
		desc:
			Turns the LED on or off.

		keywords:
			"on":
				desc:	Indicates whether the LED should be on or off.
				type:	bool

		example: |
			# Blink LED five time
			for i in range(5):
				exp.boks.set_led(True)
				self.sleep(500)
				exp.boks.set_led(False)
				self.sleep(500)
		"""
		
		if on:
			self.dev.write(CMD_LED_ON)
		else:
			self.dev.write(CMD_LED_OFF)

	def set_timeout(self, timeout):

		"""
		desc:
			Sets the timeout used by [get_button_press] and
			[get_button_release].

		arguments:
			timeout:
				desc:	A value in milliseconds. Use 0 or `None` to disable
						timeout (i.e. to wait infinitely).
				type:	[int, NoneType]
							
		example: |
			exp.boks.set_timeout(2000)
			t = exp.boks.get_timeout()
			print('The Boks timeout is currently set to %d ms' % t)
		"""

		if timeout == None:
			timeout = 0
		try:
			timeout = int(timeout)
		except:
			raise boks_exception('Expecting a numeric value or None')
		if timeout < 0:
			raise boks_exception( \
				'Expecting a non-negative numeric value or None')
		self.msg('Setting timeout to %d' % timeout)
		self.dev.write(CMD_SET_TIMEOUT)
		self.write_ulong(1000*timeout)

	def time(self):

		"""
		visible:
			False

		desc:
			A time function. In OpenSesame mode, the OpenSesame timer will be
			used instead.

		returns:
			desc:	A timestamp in milliseconds
			type:	float
		"""

		return 1000. * time.time()

	def write_ulong(self, l):

		"""
		visible:
			False

		desc:
			Writes an integer as an unsigned long to the Boks.

		arguments:
			l:
				desc:	An integer.
				type:	int
		"""

		self.dev.write(struct.pack('I', l))

class dummy(libboks):
	
	"""
	desc:
		Emulates libboks using the keyboard. Only works when an OpenSesame
		experiment is available.
	"""

	def __init__(self, experiment, buttons, timeout):
		
		"""See libboks."""

		from libopensesame import debug
		self.experiment = experiment
		self.msg = debug.msg
		self.time = experiment.time
		self.buttons = buttons
		self.timeout = timeout
		self.msg('initializing dummy mode')
		self.identify()

	def close(self):
		
		"""See libboks."""

		pass

	def get_button_press(self):
		
		"""See libboks."""

		from openexp.keyboard import keyboard
		_buttons = [str(b) for b in self.buttons]
		kb = keyboard(self.experiment, keylist=_buttons, timeout=self.timeout)
		key, timestamp = kb.get_key()
		# Make sure that we return `int`s instead of `str`s
		if key != None:
			key = int(key)
		return key, timestamp

	def get_button_release(self):
		
		"""See libboks."""

		return self.get_button_press()

	def get_button_state(self):
		
		"""See libboks."""

		from openexp.keyboard import keyboard
		_buttons = [str(b) for b in self.buttons]
		kb = keyboard(self.experiment, keylist=_buttons, timeout=0)
		key, timestamp = kb.get_key()
		if key == None:
			return []
		return [int(key)]

	def get_buttons(self):
		
		"""See libboks."""

		return self.buttons
	
	def get_sid(self):
		
		"""See libboks."""
		
		return 'AA0000'

	def get_timeout(self):
		
		"""See libboks."""

		return self.timeout

	def identify(self):
		
		"""See libboks."""

		self.firmware_version = '0.0.0'
		self.model = 'dummy.boks'

	def set_buttons(self, buttons):
		
		"""See libboks."""

		if buttons == None:
			# Accept only digits between 1 and 8 (incl.)
			self.buttons = [str(i) for i in range(1, 9)]
		else:
			self.buttons = buttons

	def set_continuous(self, continuous=True):
		
		"""See libboks."""

		pass

	def set_led(self, on=True):
		
		"""See libboks."""

		pass

	def set_timeout(self, timeout):
		
		"""See libboks."""

		self.timeout = timeout
