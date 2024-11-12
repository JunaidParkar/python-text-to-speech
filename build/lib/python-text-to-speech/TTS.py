from .Registry import System_Voices_Manager
from mtranslate import translate
from time import sleep
import pyttsx3
import logging

class Speaker:
    def __init__(self, input_file_path, stop_file_path, log_file, translate=True, speak_continous=True):
        self.logging = logging
        self.logging.basicConfig(
            filename=log_file,
            level=self.logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.logging.info(f"\n\nInitializing Speaker with input_file_path='input_file_path', stop_file_path='stop_file_path', translate=translate, speak_continous=speak_continous\n\n",)
        self.engine = pyttsx3.init("sapi5")
        self.voices = self.engine.getProperty('voices')
        self.current_voice = self.voices[0].id
        self.__input_file_path = input_file_path
        self.__speak_continous = speak_continous
        self.__stop_file_path = stop_file_path
        self.__translate = translate
        self.__fine = True
        self.__previous_text = None

        if not self.__check_arguments():
            self.__fine = False
            self.logging.error("Failed argument validation in Speaker initialization.")

    def add_more_voice(self, export_path, voice_install_log_file):
        self.logging.info("Adding more voices from export_path: %s", export_path)
        system = System_Voices_Manager(voice_install_log_file)
        system.install_all_voices(export_path)

    def __check_arguments(self):
        try:
            if not isinstance(self.__speak_continous, bool):
                self.logging.erro("\nParameter speak_continous must be boolean\n")
                return False
            if not isinstance(self.__translate, bool):
                self.logging.erro("\nParameter translate must be boolean\n")
                return False
            if not isinstance(self.__input_file_path, str):
                self.logging.erro("\nParameter input_file_path must be string\n")
                return False
            if not isinstance(self.__stop_file_path, str):
                self.logging.erro("\nParameter stop_file_path must be string\n")
                return False
            if not self.__input_file_path:
                self.logging.error("\nPlease provide the input_file_path\n")
                return False
            if self.__speak_continous and not self.__stop_file_path:
                self.logging.error("\nPlease provide stop_file_path\n")
                return False
            self.logging.info("Argument validation successful.")
            return True
        except (TypeError, ValueError) as e:
            self.logging.error(f"\nArgument validation error: {e}\n")
            return False

    def __translate_to_language(self, text):
        self.logging.info("Translating text.")
        return translate(to_translate=text, to_language="en-us")

    def __initiate_speak(self):
        self.logging.info("Initiating speak")
        with open(self.__stop_file_path, "w") as initiator_file:
            initiator_file.write("A")

    def quit_speak(self):
        self.logging.info("Quitting speak.")
        with open(self.__stop_file_path, "w") as initiator_file:
            initiator_file.write("B")

    def populate_voices(self):
        self.logging.info("Populating available voices.")
        return [{
            'ID': voice.id,
            'Name': voice.name,
            'Languages': voice.languages,
            'Gender': voice.gender,
            'Age': voice.age
        } for voice in self.voices]

    def set_voice(self, voice_name):
        self.logging.info("Setting voice to: %s", voice_name)
        for voice in self.voices:
            if voice.name == voice_name:
                self.engine.setProperty('voice', voice.id)
                self.current_voice = voice.id
                self.logging.info(f"Voice set to {voice.name}")
                return
        self.logging.warning(f"Voice '{voice_name}' not found. Using default voice.")
        self.engine.setProperty('voice', self.voices[0].id)
        self.current_voice = self.voices[0].id

    def speak(self):
        if not self.__fine:
            self.logging.error("\nSpeaker initialization was not fine. Exiting speak.\n")
            return
        self.__initiate_speak()
        if self.__speak_continous:
            self.logging.info("Starting continuous speaking mode.")
            while True:
                with open(self.__stop_file_path, "a+") as initiator_file:
                    initiator_file.seek(0)
                    to_speak = initiator_file.read()
                if to_speak != "A" and to_speak == "B":
                    self.logging.info("Stop signal received. Exiting continuous speaking mode.")
                    break
                with open(self.__input_file_path, "a+") as data_file:
                    data_file.seek(0)
                    data = data_file.read()
                if self.__previous_text != data:
                    self.__previous_text = data
                    self.engine.setProperty('voice', self.current_voice)
                    lengthcode = len(data)
                    self.engine.setProperty('rate', 180 if lengthcode > 30 else 170)
                    data = self.__translate_to_language(data) if self.__translate else data
                    self.logging.info("Speaking text.")
                    self.engine.say(data)
                    self.engine.runAndWait()
                sleep(0.333)
        else:
            self.logging.info("Starting single text speaking mode.")
            with open(self.__input_file_path, "a+") as data_file:
                data_file.seek(0)
                data = data_file.read()
            self.engine.setProperty('voice', self.current_voice)
            lengthcode = len(data)
            self.engine.setProperty('rate', 180 if lengthcode > 30 else 170)
            data = self.__translate_to_language(data) if self.__translate else data
            self.logging.info("Speaking text.")
            self.engine.say(data)
            self.engine.runAndWait()