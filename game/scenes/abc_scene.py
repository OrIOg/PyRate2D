# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class ABCScene(ABC):
	def __init__(self):
		self.load_info = {'percent': 0}

	def is_loaded(self):
		return self.load_info['percent'] == 1

	@abstractmethod
	def load(self):
		raise NotImplemented

	@abstractmethod
	def update(self, delta_time):
		raise NotImplemented

	@abstractmethod
	def draw(self, surface):
		raise NotImplemented
