import simpy



class Airport:
    def __init__(self, env, num_booths, num_check_ins, num_passport_controls):
        self.env = env
        
        # zdroje letiště
        self.ticket_booth = simpy.Resource(env, num_booths)
        self.check_in = simpy.Resource(env, num_check_ins)
        self.passport_control = simpy.Resource(env, num_passport_controls)
        
        # pro statistiku
        self.total_passengers = 0
        self.tickets_bought = 0
        self.registered = 0
        self.passport_controlled = 0
        self.missed_flights = 0
        self.cumulative_time_spent = 0
        self.booth_usage_time = 0
        self.check_in_usage_time = 0
        self.passport_control_usage_time = 0
    
    def calculate_usage_statistics(self):
        total_time = self.env.now  # Total simulation time
        booth_usage_percentage = (self.booth_usage_time / (total_time * self.ticket_booth.capacity)) * 100
        check_in_usage_percentage = (self.check_in_usage_time / (total_time * self.check_in.capacity)) * 100
        passport_control_usage_percentage = (self.passport_control_usage_time / (total_time * self.passport_control.capacity)) * 100
        return {
            'booth_usage_percentage': booth_usage_percentage,
            'check_in_usage_percentage': check_in_usage_percentage,
            'passport_control_usage_percentage': passport_control_usage_percentage
        }

class Flight:
    def __init__(self, destination, time, gate):
        self.destination = destination
        self.time = time
        self.gate = gate