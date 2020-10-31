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
        # Remove the display word, trim and create an array of the words
        utterance = message.data.get('utterance')
        words = re.sub('^.*?' + message.data['Display'], '', utterance).strip()
	words_array = words.split(' ')

	speak_this = "oh dear, I did not recognise that"

        if words_array[0] == 'recipe':
            words_array.pop(0)
            if words_array[0] == 'for':
                words_array.pop(0)
            speak_this = "displaying recipe for " + " ".join(words_array)
        
        elif words_array[0] == 'weather':
            # todo
            speak_this = "displaying met office weather forecast"

        elif words_array[0] == 'garden' and words_array[1] == 'summary':
            # also todo
            speak_this = "displaying summary from garden"

        elif words_array[1] == 'clock':
            # more todo
            speak_this = "display the clock when Graham has built it"


        self.speak(speak_this)

    def stop(self):
        pass


def create_skill():
    return DisplayStuff()
