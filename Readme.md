# Text to Speech (TTS) Project

This project leverages `pyttsx3` for microsoft's built-in text-to-speech feature. It's designed for simplicity and ease of use, allowing you to configure continuous text-to-speech functionality and optional English translation.

## Features

- **Continuous Text-to-Speech**: Decide if you want the text-to-speech functionality to run continuously.
- **Optional English Translation**: Choose whether to translate text to English before speaking.
- **Easy Configuration**: Simple setup using two text files.

## Prerequisites

- `pyttsx3`

## Setup

1. **Install dependencies**:
    ```sh
    pip install pyttsx3
    ```

2. **Create Configuration Files**:
    - `input_sentence_file.txt`: This file will contain the sentences that need to be spoken.
    - `stop_or_not_file.txt`: This file will control whether the text-to-speech function continues to check the input text file for new sentences. It should contain either "A" or "B".
        - "A" means the function will continue to work.
        - "B" means the function will stop.

## Usage

To use the text-to-speech functionality, import the `Speaker` class from `python-text-to-speech` and initialize it with the appropriate parameters.

```python
from python-text-to-speech import Speaker

ai = Speaker(
    input_file_path="input_sentence_file.txt",
    stop_file_path="stop_or_not_file.txt",
    log_file="TTS.log"
    translate=True | False,
    speak_continous=True | False
)

ai.add_more_voice("/temporary_directory_for_working", "voice_install_log_file.log") # Initialize all the voices avaliable in system

voices_list = ai.populate_voices() # to get list of available voices in your system

ai.set_voice(voice_name) # voice name should be the exact name of voice provided in vlices_list

ai.speak() # to speak sentences
```

## Parameters

* `input_file_path` (str): Path to the file containing sentences to be spoken.
* `stop_file_path` (str): Path to the file that controls whether to stop or continue.
* `log_file` (str): Path to a log file where all the logs will be stored.
* `translate` (bool): Set to True to translate the text to English before speaking, False otherwise.
* `speak_continous` (bool): Set to True for continuous text-to-speech, False for single execution.

## Continuous Usage

If you want the text-to-speech functionality to run continuously, it is recommended to use threading. This will prevent the function from blocking the execution of further code until it is stopped.

Example with Threading
```python
import threading
from python-text-to-speech import Speaker

def tts_thread():
    ai = Speaker(
        input_file_path="input_sentence_file.txt",
        stop_file_path="stop_or_not_file.txt",
        translate=True,
        speak_continous=True
    )
    ai.speak()

# Start TTS in a separate thread
thread = threading.Thread(target=tts_thread)
thread.start()
thread.join()
```

To make the program speak, update the sentence in input_sentence_file.txt. To stop the function, change the value in stop_or_not_file.txt from "A" to "B".

## How to add more voices

* Open windows setting and navigate to `Time & language  => Speech => Add voices` and download the language whose voice you need to use.
* Wait for 5 minutes the restart your device.
* import `System_Voices_Manager` from `python-text-to-speech.Register` and follow the code

```python
from python-text-to-speech.Register import System_Voices_Manager
import os

if __name__ == "__main__":
    sys = System_Voices_Manager("voice_install_log_file.log")
    sys.install_all_voices(os.path.join(os.getcwd(), "export"))
```

* Now all voices are ready to use. You can populate the voice and set it to engine. Read the usage to know how to set voice.

**This project is managed by Artex AI. Soon an improved and stable version will roll out**