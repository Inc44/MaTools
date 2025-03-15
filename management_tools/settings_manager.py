import json
import os

SETTINGS_PATH = "settings.json"
CONSTANTS_PATH = "constants.json"


class SettingsManager:
	def __init__(self):
		self._settings = {}
		self._constants = {}
		self._load_settings()
		self._load_constants()

	def _load_settings(self):
		if os.path.exists(SETTINGS_PATH):
			with open(SETTINGS_PATH, "r", encoding="UTF-8") as file:
				self._settings = json.load(file)

	def _load_constants(self):
		if os.path.exists(CONSTANTS_PATH):
			with open(CONSTANTS_PATH, "r", encoding="UTF-8") as file:
				self._constants = json.load(file)

	def get_setting(self, key: str, default=None):
		return self._settings.get(key, default)

	def set_setting(self, key: str, value):
		self._settings[key] = value
		self._save_settings()

	def get_constant(self, key: str, default=None):
		return self._constants.get(key, default)

	def _save_settings(self):
		with open(SETTINGS_PATH, "w", encoding="UTF-8") as file:
			json.dump(self._settings, file)
