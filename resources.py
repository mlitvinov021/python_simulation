import simpy

""" class TicketBooth:
    def __init__(self, env, num_booths):
        self.env = env
        self.booth = simpy.Resource(env, num_booths) """

class Airport:
    def __init__(self, env, num_booths, num_check_ins, num_passport_controls):
        self.env = env
        self.ticket_booth = simpy.Resource(env, num_booths)
        self.check_in = simpy.Resource(env, num_check_ins)
        self.passport_control = simpy.Resource(env, num_passport_controls)

class Flight:
    def __init__(self, destination, time, gate):
        self.destination = destination
        self.time = time
        self.gate = gate