from os import getcwd, walk
from os.path import join, normpath
import subprocess
import winreg
from shutil import rmtree
import logging

class System_Voices_Manager:
    def __init__(self, log_file):
        self.key_path = r"SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
        self.target_line = r"[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens"
        self.logging = logging
        self.logging.basicConfig(
            filename=log_file,
            level=self.logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.logging.info("\n\nSystem_Voices_Manager initialized.\n\n")

    def list_available_voices(self):
        voice_token_list = []
        self.logging.info("Listing available voices...")
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.key_path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    voice_key = winreg.EnumKey(key, i)
                    voice_token_list.append(f"HKEY_LOCAL_MACHINE\\{self.key_path}\\{voice_key}")
            self.logging.info("Available voices listed successfully.")
        except Exception as e:
            self.logging.error(f"Failed to list available voices: {e}")
        return voice_token_list

    def export_voice_registry(self, voice_path, export_path):
        try:
            export_command = ["reg", "export", voice_path, join(export_path, f"{voice_path.split('\\')[-1]}.reg"), "/y"]
            subprocess.run(export_command, check=True)
            self.logging.info(f"Exported voice registry for {voice_path} to {export_path}.")
        except subprocess.CalledProcessError as e:
            self.logging.error(f"Error exporting registry for {voice_path}: {e.stderr}")
        except Exception as e:
            self.logging.error(f"Unexpected error during export: {e}")

    def path_updator(self, filename):
        try:
            reg_file = f"{filename}.reg"
            with open(reg_file, 'r', encoding="UTF-16") as file:
                content = file.read()
                lines = content.splitlines()

            # Modify the registry path as needed
            for i, line in enumerate(lines):
                if line.startswith(self.target_line):
                    lines[i] = line.replace("Speech_OneCore", "Speech")

            modified_content = "\n".join(lines)
            with open(reg_file, 'w', encoding="UTF-16") as file:
                file.write(modified_content)
            self.logging.info(f"File '{reg_file}' updated successfully.")
        except FileNotFoundError:
            self.logging.error(f"File '{filename}.reg' not found.")
        except Exception as e:
            self.logging.error(f"An error occurred while updating path in '{filename}.reg': {e}")

    def install_voice(self, reg_file_path):
        try:
            result = subprocess.run(["reg", "import", f"{reg_file_path}.reg"], check=True, capture_output=True, text=True)
            self.logging.info(f"Registry file '{reg_file_path}.reg' imported successfully.")
        except subprocess.CalledProcessError as e:
            self.logging.error(f"Error importing registry file '{reg_file_path}.reg': {e.stderr}")

    def install_all_voices(self, export_path):
        voice_list = self.list_available_voices()
        self.logging.info("Starting installation of all voices.")
        for voice in voice_list:
            self.export_voice_registry(voice, export_path)
            reg_filename = join(normpath(export_path), voice.split("\\")[-1])
            self.path_updator(reg_filename)
            self.install_voice(reg_filename)
        try:
            rmtree(join(normpath(export_path)))
            self.logging.info(f"Export directory '{export_path}' deleted successfully.")
        except Exception as e:
            self.logging.error(f"Error deleting export directory '{export_path}': {e}")