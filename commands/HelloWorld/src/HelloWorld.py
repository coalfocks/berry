from command import Command

class HelloWorld (Command):
    def do(self):
        username = self.args[0]
        result = 'Hello, {}'.format(username)
        print ('Hello, {}'.format(username))
        return result

