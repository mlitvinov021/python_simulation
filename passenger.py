import simpy

class Passenger():
    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())