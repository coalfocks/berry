from command import Command

class HelloWorld (Command):
    def do(self):
        username = self.args[0]
        print ('Hello, {}'.format(username))
