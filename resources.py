import simpy

class TicketBooth:
    def __init__(self, env, num_booths):
        self.env = env
        self.booth = simpy.Resource(env, num_booths)