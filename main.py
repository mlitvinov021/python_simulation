import simpy
import random
from passenger import Passenger, Companion
from resources import Airport

def passenger_generator(env, airport, flights, arrival_interval):
    passenger_id = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / arrival_interval))
        passenger_id += 1
        flight = random.choice(flights)
        Passenger(f'Passenger {passenger_id}', env, flight, airport.ticket_booth, airport.check_in, airport.passport_control)

# Funkce pro generace kompanionů, možná lze přesunout do funkce generace pasažerů.
def companion_generator(env, arrival_interval):
    companion_id = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / arrival_interval))
        companion_id += 1
        Companion(f'Companion {companion_id}', env)

def main():
    flights = ['Flight A', 'Flight B', 'Flight C']
    num_booths = 2
    num_check_ins = 2
    num_passport_controls = 2
    arrival_interval = 2
    simulation_time = 1440 # 24 hodiny

    env = simpy.Environment()
    airport = Airport(env, num_booths, num_check_ins, num_passport_controls)
    env.process(passenger_generator(env, airport, flights, arrival_interval))
    env.process(companion_generator(env, arrival_interval))
    env.run(until=simulation_time)
    stats()

def input():
    pass
    # TODO: funkce pro obdržení informace o simulaci od uživatele.

def stats():
    pass
    # TODO: sebrat a popsat statistiku o provozu letiště.

if __name__ == "__main__":
    main()