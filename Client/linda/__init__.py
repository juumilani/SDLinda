#-*- coding: utf-8 -*-
import atexit

from . import utils
from socket  import *
from constCS import * #-

s = socket(AF_INET, SOCK_STREAM)

def connect():

	s.connect((HOST, PORT))
	print("Cliente conectado")
	atexit.register(exit_handler)
	pass

def exit_handler():
    print("Cliente desconectado")
    s.close()

class TupleSpace:
	def __init__(self, **kwargs):
		if kwargs and len(kwargs) == 1 and "blog_name" in kwargs:
			self.blog_name = kwargs["blog_name"]
		else:
			self.blog_name = ""

		self.dictionary = {}


	def _rd(self, t):

		publisher, topic, type_return = t

		msg_send = utils.tuple_to_bin((publisher, topic, type_return), "rd")
		s.send(msg_send)
		tuple_list_bin = b''
		r = b''

		while r.decode() != "." :
			tuple_list_bin+=r
			r = s.recv(1)
		tuple_list = utils.bin_to_tuple(tuple_list_bin, has_op=False)

		if tuple_list:
			return tuple_list
    
	def _in(self, t):

		publisher, topic, type_return = t
		msg_send = utils.tuple_to_bin((publisher, topic, type_return), "in")
		s.send(msg_send)

	def _out(self, t):

		publisher, topic, content = t


		msg_send = utils.tuple_to_bin((publisher, topic, content), "out")
		s.send(msg_send)


	def set_name(self, new_name):
		if new_name or new_name is not None:
			self.blog_name = new_name

class Universe():
	def __init__(self):
		pass
	
	def _rd(self, t):

		blog_name, tuplespace_class = t

		if tuplespace_class == TupleSpace:
			tuplespace = tuplespace_class(blog_name=blog_name)
		return "", tuplespace

	def _out(self, t):
		blog_name, tuplespace = t
		tuplespace.set_name(blog_name)
		pass

universe = Universe()