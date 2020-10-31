from mycroft import MycroftSkill, intent_file_handler


class DisplayStuff(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('stuff.display.intent')
    def handle_stuff_display(self, message):
        self.speak_dialog('stuff.display')


def create_skill():
    return DisplayStuff()

