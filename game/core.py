# -*- coding: utf-8 -*-

import os
import asyncio
import pygame
import json
import game.scenes as scenes

os.environ['SDL_VIDEO_CENTERED'] = '1'


class Game:
	DEFAULT_CONFIG = {'GRAPHICS': {
		'RESOLUTION': (1280, 720),
		'FULLSCREEN': False}
	}
	FLAGS = pygame.HWACCEL | pygame.DOUBLEBUF

	def __init__(self):
		pygame.init()
		self.__config = self.__read_config()
		pygame.display.set_caption("PyRate2D")
		flags = Game.FLAGS
		flags += pygame.FULLSCREEN if self.__config['GRAPHICS']['FULLSCREEN'] else 0
		self.__screen = pygame.display.set_mode(
			self.__config['GRAPHICS']['RESOLUTION'], flags)
		self.__running = False
		self.__clock = pygame.time.Clock()
		self.__scene = scenes.MainMenu()

	def __read_config(self):
		try:
			if os.path.isfile("config.json_fallback"):
				with open("config.json_fallback", 'r') as stream:
					config =  json.load(stream)
				try:
					with open('config.json', 'w') as json_file:
						json.dump(config, json_file)
						os.remove('config.json_fallback')
				except ValueError:
					with open('config.json_fallback', 'w') as json_file:
						json.dump(config, json_file)
			elif os.path.isfile("config.json"):
				with open("config.json", 'r') as stream:
					return json.load(stream)
		except ValueError:
			return Game.DEFAULT_CONFIG
		return Game.DEFAULT_CONFIG

	def __save_config(self, config):
		try:
			with open('config.json', 'w') as json_file:
				json.dump(config, json_file)
		except ValueError:
			with open('config.json_fallback', 'w') as json_file:
				json.dump(config, json_file)

	def __game_loop(self):
		self.__running = True
		clock = self.__clock

		self.__scene.load()

		while self.__running:
			delta_time = clock.tick() * 0.001
			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					self.__running = False
					break
			if not self.__running:
				break

			self.__scene.update(delta_time)
			self.__scene.draw(self.__screen)

			pygame.display.update()
		self.__save_config(self.__config)
		pygame.quit()

	def start(self):
		self.__game_loop()
