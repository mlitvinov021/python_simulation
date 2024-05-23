import simpy
import random

class Passenger:
    def __init__(self, name, env, flight, ticket_booth, check_in, passport_control):
        self.name = name
        self.env = env
        self.flight = flight
        self.ticket_booth = ticket_booth
        self.check_in = check_in
        self.passport_control = passport_control
        self.action = env.process(self.start_journey())
    
    def start_journey(self):
        print(f'{self.name} arrives for flight {self.flight} at {self.env.now:.2f}')
        yield self.env.process(self.go_to_ticket_booth())
        yield self.env.process(self.register())
        yield self.env.process(self.passport_control_process())
        print(f'{self.name} has completed all processes at {self.env.now:.2f}\
              and is ready for flight {self.flight}')

    def go_to_ticket_booth(self):
        print(f'{self.name} arrives at the ticket booth at {self.env.now:.2f}')
        with self.ticket_booth.request() as request:
            yield request
            #print(f'{self.name} is waiting to buy a ticket at {self.env.now:.2f}')
            yield self.env.process(self.buy_ticket())
            print(f'{self.name} has bought a ticket at {self.env.now:.2f}')
    
    def buy_ticket(self):
        yield self.env.timeout(random.uniform(1, 3))
    
    def register(self):
        print(f'{self.name} arrives at the check-in desk at {self.env.now:.2f}')
        with self.check_in.request() as request:
            yield request
            yield self.env.process(self.check_in_process())
            print(f'{self.name} has registered at {self.env.now:.2f}')

    def check_in_process(self):
        yield self.env.timeout(random.uniform(2, 5))

    def passport_control_process(self):
        print(f'{self.name} arrives at passport control at {self.env.now:.2f}')
        with self.passport_control.request() as request:
            yield request
            yield self.env.process(self.passport_check())
            print(f'{self.name} has passed passport control at {self.env.now:.2f}')

    def passport_check(self):
        yield self.env.timeout(random.uniform(1, 3))


class Companion:
    def __init__(self, name, env):
        self.name = name
        self.env = env
        self.action = env.process(self.accompany())

    def accompany(self):
        print(f'{self.name} is accompanying a passenger at {self.env.now:.2f}')
        yield self.env.timeout(random.uniform(1, 2))
        print(f'{self.name} has finished accompanying at {self.env.now:.2f}')