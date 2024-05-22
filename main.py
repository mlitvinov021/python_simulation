import simpy
import random
from passenger import Passenger
from resources import TicketBooth

def run_simulation(env, num_passengers, num_booths, arrival_interval):
    ticket_booth = TicketBooth(env, num_booths)
    for i in range(num_passengers):
        passenger = Passenger(f'Passenger {i+1}', env, ticket_booth.booth)
        yield env.timeout(random.expovariate(1.0 / arrival_interval))

def main():
    num_passengers = 10
    num_booths = 2
    arrival_interval = 2
    env = simpy.Environment()
    env.process(run_simulation(env, num_passengers, num_booths, arrival_interval))
    env.run()

if __name__ == "__main__":
    main()