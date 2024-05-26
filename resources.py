import simpy

class Airport:
    def __init__(self, env, num_booths, num_check_ins, num_passport_controls):
        self.env = env
        
        # zdroje letiště
        # TODO: další etapa? (např. onboarding)
        self.ticket_booth = simpy.Resource(env, num_booths)
        self.check_in = simpy.Resource(env, num_check_ins)
        self.passport_control = simpy.Resource(env, num_passport_controls)

        # pro statistiku
        self.total_passengers = 0
        self.tickets_bought = 0
        self.registered = 0
        self.passport_controlled = 0

class Flight:
    def __init__(self, destination, time, gate):
        self.destination = destination
        self.time = time
        self.gate = gate