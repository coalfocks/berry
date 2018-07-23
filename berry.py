import os
import time
import random
import datetime
import importlib
import config
import threading
from command import Command
from telepot.loop import MessageLoop

class Berry:

    def __init__(self):
        self.wake_word = 'berry'
        self.cmd_names = self.get_all_commands() #should initialize from previously found commands in text file
        thread = threading.Thread(target=self.listen_telegram, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        while 1:
            time.sleep(10)
            

    # make singleton

    # listen for wake word

    # listen for command + args

    # do command

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
                    #try / catch
                    with open(filepath) as the_file:
                        for line in the_file:
                            name, var = line.partition("=")[::2]
                            cmd_name_to_module[name.lower()] = var
        return cmd_name_to_module

    def do_cmd(self, unparsed):
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
        print( 'I am listening ...' )

        while 1:
            time.sleep(10) 
