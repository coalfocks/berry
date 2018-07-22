class Command:
    # what is command name
    def __init__(self):
        pass

    # what arguments does it take
    def getArgs(self, args):
        args.remove('')
        self.args = args

    # what does it do
    def do(self):
        raise NotImplementedError( "Should have implemented this" )
