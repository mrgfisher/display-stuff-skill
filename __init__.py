import re
from os.path import dirname, join

from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler

import requests
import json
from datetime import datetime, date

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

        speak_this = "oh dear, I did not recognise that"

        try:
            if words_array[0] == 'recipe':
                words_array.pop(0)
                if words_array[0] == 'for':
                    words_array.pop(0)
                speak_this = "displaying recipe for " + " ".join(words_array)
                parm = "?q=" + "+".join(words_array)
                model = { "parameter": parm }
                headers = {"Content-Type": "application/json"}
                _ = requests.put("http://192.168.0.20:8000/display/bbc", data=json.dumps(model), headers=headers)

            elif words_array[0] == 'camera':
                words_array.pop(0)
                speak_this = "displaying camera " + " ".join(words_array)
                _ = requests.put("http://192.168.0.20:8000/display/camera/" + str(words_array[0]), {})

            elif (words_array[0] == 'forecast') or (words_array[0] == 'met') or (words_array[0] == 'weather'):
                speak_this = "displaying met office weather forecast"
                _ = requests.put("http://192.168.0.20:8000/display/met", {})

            elif words_array[0] == 'garden':
                speak_this = "displaying summary from garden"
                _ = requests.put("http://192.168.0.20:8000/display/davis", {})
        except:
            speak_this = "od dear, that went wrong"

        self.speak(speak_this)

    def stop(self):
        pass


def json_serial(obj):
    # Thanks https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable/36142844#36142844
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def create_skill():
    return DisplayStuff()
