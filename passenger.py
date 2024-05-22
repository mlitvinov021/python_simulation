import simpy
import random

class Passenger:
    def __init__(self, name, env, ticket_booth):
        self.env = env
        self.name = name
        self.ticket_booth = ticket_booth
        self.action = env.process(self.buy_ticket())
    
    def buy_ticket(self):
        print(f'{self.name} arrives at the ticket booth at {self.env.now:.2f}')
        with self.ticket_booth.request() as req:
            yield req
            print(f'{self.name} is waiting to buy a ticket at {self.env.now:.2f}')
            yield self.env.process(self.wait())
            print(f'{self.name} has bought a ticket at {self.env.now:.2f}')
    
    def wait(self):
        yield self.env.timeout(random.uniform(1, 3))