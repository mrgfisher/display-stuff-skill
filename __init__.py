import re
from os.path import dirname, join

from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler

import websocket
import json

# TODO - Localization

class DisplayStuff(MycroftSkill):

    def __init__(self):
        super(DisplayStuff, self).__init__(name="DisplayStuff")

    @intent_handler(IntentBuilder("").require("Display").require("Words"))
    def speak_back(self, message):
        """
            Repeat the utterance back to the user.

            TODO: The method is very english centric and will need
                  localization.
        """
        # Remove the display word, trim and create an array of the words
        utterance = message.data.get('utterance')
        words = re.sub('^.*?' + message.data['Display'], '', utterance).strip()

        words_array = words.split(' ')
        json_command = None

        ws = websocket.create_connection("ws://192.168.0.5:9001")

        speak_this = "oh dear, I did not recognise that"

        if words_array[0] == 'recipe':
            words_array.pop(0)
            if words_array[0] == 'for':
                words_array.pop(0)
            speak_this = "displaying recipe for " + " ".join(words_array)
            parm = "?q=" + "+".join(words_array)
            json_command = json.dumps({"action": "bbcSearch", "parameter": parm})
        
        elif words_array[0] == 'weather':
            # todo
            speak_this = "displaying met office weather forecast"
            json_command = json.dumps({"action": "metOffice"})

        elif words_array[0] == 'garden' and words_array[1] == 'summary':
            # also todo
            speak_this = "displaying summary from garden"
            json_command = json.dumps({"action": "davis"})

        elif words_array[0] == 'clock':
            # more todo
            speak_this = "displaying nothing"


        if not json_command is None:
            ws.send(json_command)

            ws.send(json.dumps({"action": "tie_display_on"}))

            ws.close()

        self.speak(speak_this)

    def stop(self):
        pass


def create_skill():
    return DisplayStuff()
