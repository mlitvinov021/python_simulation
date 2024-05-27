import simpy
import random

class Passenger:
    def __init__(self, name, env, flight, airport):
        self.name = name
        self.env = env
        self.flight = flight
        self.ticket_booth = airport.ticket_booth
        self.check_in = airport.check_in
        self.passport_control = airport.passport_control
        self.airport = airport

         # Hlídání času
        self.start_time = env.now
        self.end_time = None

        # hned po vzniku pasažeru jde si kupovat letenky atd.
        self.action = env.process(self.start_journey())

        # sběr statistiky
        self.airport.total_passengers += 1
    
    # hlavní proces pasažera, který čeká na vyplnění všech podmínek (zakoupení si letenky, registrace, kontrola)
    def start_journey(self):
        print(f'{self.name} arrives for flight to {self.flight.destination}, {self.flight.time//60:2.0f}:{self.flight.time%60:2.0f} at {self.env.now//60:2.0f}:{self.env.now%60:2.0f}')
        if not (yield self.env.process(self.buy_ticket())):
            self.end_time = self.env.now
            self.airport.missed_flights += 1
            return
        if not (yield self.env.process(self.register())):
            self.end_time = self.env.now
            self.airport.missed_flights += 1
            return
        if not (yield self.env.process(self.passport_control_process())):
            self.end_time = self.env.now
            self.airport.missed_flights += 1
            return
        self.end_time = self.env.now
        self.airport.cumulative_time_spent += self.end_time - self.start_time    
        print(f'{self.name} has completed all processes at {self.env.now//60:2.0f}:{self.env.now%60:2.0f} and is ready for flight to {self.flight.destination}, {self.flight.time//60:2.0f}:{self.flight.time%60:2.0f}')

    # ověření, že let se neuskutečnil, aby pasažeři nestali ve frontách pro let, který se už uskutečnil
    def check_flight_time(self):
        if self.env.now > self.flight.time:
            print(f'{self.name} missed the flight to {self.flight.destination} at {self.env.now//60:2.0f}:{self.env.now%60:2.0f}')
            return False
        return True
    
    def buy_ticket(self):
        a = random.random()
        if a > 0.3:
            print(f'{self.name} already had a ticket at {self.env.now//60:2.0f}:{self.env.now%60:2.0f}')
        if a > 0.3:
            return True   
        with self.ticket_booth.request() as request:
            yield request
            start_time = self.env.now
            yield self.env.timeout(random.uniform(1, 3))
            self.airport.booth_usage_time += self.env.now - start_time
            if not self.check_flight_time():
                return False
            self.airport.tickets_bought += 1
            print(f'{self.name} has bought a ticket at {self.env.now//60:2.0f}:{self.env.now%60:2.0f}')
        return True

    def register(self):
        a = random.random()
        if a > 0.7:
            print(f'{self.name} already had a registred at {self.env.now//60:2.0f}:{self.env.now%60:2.0f}')
        if a > 0.7:
            return True  
        with self.check_in.request() as request:
            yield request
            start_time = self.env.now
            yield self.env.timeout(random.uniform(2, 5))
            self.airport.check_in_usage_time += self.env.now - start_time
            if not self.check_flight_time():
                return False
            self.airport.registered += 1
            print(f'{self.name} has registered at {self.env.now//60:2.0f}:{self.env.now%60:2.0f}')
        return True

    def passport_control_process(self):
        with self.passport_control.request() as request:
            yield request
            start_time = self.env.now
            yield self.env.timeout(random.uniform(1, 3))
            self.airport.passport_control_usage_time += self.env.now - start_time
            if not self.check_flight_time():
                return False
            self.airport.passport_controlled += 1
            print(f'{self.name} has passed passport control at {self.env.now//60:2.0f}:{self.env.now%60:2.0f}')
        return True


class Companion:
    def __init__(self, name, env):
        self.name = name
        self.env = env
        self.action = env.process(self.accompany())

    def accompany(self):
        print(f'{self.name} is accompanying a passenger at {self.env.now//60:2.0f}:{self.env.now%60:2.0f}')
        yield self.env.timeout(random.uniform(1, 2))
        print(f'{self.name} has finished accompanying at {self.env.now//60:2.0f}:{self.env.now%60:2.0f}')