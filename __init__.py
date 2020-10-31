import re
from os.path import dirname, join

from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler

# TODO - Localization

class DisplayStuff(MycroftSkill):
    @intent_handler(IntentBuilder("").require("Display").require("Words"))
    def speak_back(self, message):
        """
            Repeat the utterance back to the user.

            TODO: The method is very english centric and will need
                  localization.
        """
        # Remove everything up to the speak keyword and repeat that
        utterance = message.data.get('utterance')
        repeat = re.sub('^.*?' + message.data['Display'], '', utterance)
        self.speak(repeat.strip())

    def stop(self):
        pass


def create_skill():
    return DisplayStuff()
