import re
from os.path import dirname, join

from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler

import websocket
import socketio
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
        json_command = None
        state_model = None


        speak_this = "oh dear, I did not recognise that"

        if words_array[0] == 'recipe':
            words_array.pop(0)
            if words_array[0] == 'for':
                words_array.pop(0)
            speak_this = "displaying recipe for " + " ".join(words_array)
            parm = "?q=" + "+".join(words_array)
            json_command = json.dumps({"action": "bbcSearch", "parameter": parm})
        
        elif words_array[0] == 'test' and words_array[1] == 'rainbow':
            speak_this = "rainbow is sad"
            state_model = {'message_date': json_serial(datetime.now()), 'source': 'mycroft',
                     'alert_type': 'failure', 'downtime': 'just a few mins',
                     'fail_count': 1, 'host': 'masta',
                     'description': 'simulated sad message from masta', 'additional': 'python is cool'}

        elif words_array[0] == 'happy' and words_array[1] == 'rainbow':
            speak_this = "rainbow is happy"
            state_model = {'message_date': json_serial(datetime.now()), 'source': 'mycroft',
                     'alert_type': 'success', 'downtime': 'just a few mins',
                     'fail_count': 1, 'host': 'masta',
                     'description': 'reset to happy state', 'additional': 'python is cool'}


        elif words_array[0] == 'forecast':
            # todo
            speak_this = "displaying met office weather forecast"
            json_command = json.dumps({"action": "metOffice"})

        elif words_array[0] == 'met':
            # todo
            speak_this = "displaying met office weather forecast"
            json_command = json.dumps({"action": "metOffice"})

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
            ws = websocket.create_connection("ws://192.168.0.20:9001")
            ws.send(json_command)

            ws.send(json.dumps({"action": "tie_display_on"}))

            ws.close()

        self.speak(speak_this)

        if not state_model is None:
            rainbow_message(state_model)

    def stop(self):
        pass



def rainbow_message(model):
    sio = socketio.Client()
    sio.connect('http://192.168.0.5:9002')
    sio.sleep(1)


    sio.emit('raise alert', model)

    sio.sleep(1)

    sio.disconnect()



def json_serial(obj):
    # Thanks https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable/36142844#36142844
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def create_skill():
    return DisplayStuff()
