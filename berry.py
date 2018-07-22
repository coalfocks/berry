import os
import time
import random
import datetime
import importlib
from command import Command
from config import *
from telepot.loop import MessageLoop

class Berry:

    def __init__(self):
        self.wake_word = 'berry'
        #self.listen_telegram()
        self.cmd_names = self.get_all_commands() #should initialize from previously found commands in text file

    # make singleton

    # listen for wake word

    # listen for command + args

    # do command

    # git clone is all to add new commands

    # get personalized stuff from config.txt

    # load modules more gracefully? as in, speak friendly?

    # dependencies

    def get_all_commands(self):
        # for each module in commands
            # find md file with wake word & module name
            # append to dictionary
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
                            cmd_name_to_module[name] = var
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
                c.do()
        

    # telegram handler
    def listen_telegram(self):
        # make telegram optional
        import telepot
        def handle(msg):
            chat_id = msg['chat']['id']
            command = msg['text'].split()

            print( 'Got command: %s' % command)

            if command[0] == '/roll':
                bot.sendMessage(chat_id, random.randint(1,6))
            elif command[0] == '/time':
                bot.sendMessage(chat_id, str(datetime.datetime.now()))

        #key = open('key.txt','r').read().replace('\n', '') 
        key = telegram_key
        bot = telepot.Bot(key)

        MessageLoop(bot, handle).run_as_thread()
        print( 'I am listening ...' )

        while 1:
            time.sleep(10) 
