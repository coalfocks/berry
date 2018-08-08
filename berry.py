import os
import time
import random
import datetime
import importlib
import config
import threading
from command import Command

import speech_recognition as sr
from google_speech import Speech
from telepot.loop import MessageLoop

class Berry:

    def __init__(self):
        self.wake_word = config.wake_word
        self.cmd_names = self.get_all_commands() #should initialize from previously found commands in text file
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

        thread = threading.Thread(target=self.listen_telegram, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        self.init_listener()
            

    # make singleton

    # git clone is all to add new commands

    # get personalized stuff from config.txt

    # load modules more gracefully? as in, speak friendly?

    # dependencies

    def get_all_commands(self):
        # perhaps move this to a text file that only needs to search out the new additions
        # or db
        cmd_name_to_module = {}
        for subdir, dirs, files in os.walk('commands'):
            for file in files:
                filepath = subdir + os.sep + file
                if filepath.endswith("name.md"):
                    # put into try / catch
                    with open(filepath) as the_file:
                        for line in the_file:
                            name, var = line.partition("=")[::2]
                            cmd_name_to_module[name.lower()] = var
        return cmd_name_to_module

    def do_cmd(self, unparsed):
        print(unparsed)
        for trigger in self.cmd_names:
            if trigger in unparsed:
                cmd = self.cmd_names[trigger].strip()
                args = unparsed.replace(trigger, '').split(' ')
                dir = 'commands.{}.src'.format(cmd)
                module = importlib.import_module('commands.{}.src.{}'.format(cmd,cmd))
                importlib.invalidate_caches()
                command_class = getattr(module, cmd)
                c = command_class()
                args = c.getArgs(args)
                print(args)
                return c.do()
        

    # telegram handler
    def listen_telegram(self):
        # make telegram optional
        import telepot
        def handle(msg):
            chat_id = msg['chat']['id']
            command = msg['text'].split()
            print( 'Got command: %s' % command)
            print( 'calling do_cmd with: {}'.format(msg['text'])) 
            unparsed = msg['text'].lower()
            for trigger in self.cmd_names:
                if trigger in unparsed:
                    result = self.do_cmd(unparsed)
                    print ( 'result: {}'.format(result))
                    bot.sendMessage(chat_id, result)
            
        key = config.telegram_key
        bot = telepot.Bot(key)

        MessageLoop(bot, handle).run_as_thread()
        print( 'I am awaiting a telegram ...' )

        while 1:
            time.sleep(10) 


    def init_listener(self):
        try:
            print("A moment of silence, please...")
            with self.mic as source: self.r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(self.r.energy_threshold))
            while True:
                print("Listening!")
                with self.mic as source: audio = self.r.listen(source)
                print("Got it! Now to recognize it...")
                try:
                    # recognize speech
                    value = self.r.recognize_google(audio)
                    #value = self.r.recognize_sphinx(audio)
                    print('val: ' +value)
                    value = value.lower().split()
                    # recognizing wake word and extracting from command
                    if value.pop(0) == 'hey' and value.pop(0) == config.wake_word:
                        # we need some special handling here to correctly print unicode characters to standard output
                        value = ' '.join(value)
                        if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                            print(u"You said {}".format(value).encode("utf-8"))
                            value = value.encode("utf-8")
                        else:  # this version of Python uses unicode for strings (Python 3+)
                            print("You said {}".format(value))
                        result = self.do_cmd(value)
                        if result:
                            lang = "en"
                            speech = Speech(result, lang)
                            sox_effects = ('speed', '1.0')
                            speech.play(sox_effects)
                            print(result)
                    else:
                        print('not a command')
                        

                except sr.UnknownValueError:
                    print("Oops! Didn't catch that")
                except sr.RequestError as e:
                    print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
        except KeyboardInterrupt:
            pass

