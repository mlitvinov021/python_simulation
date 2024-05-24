import simpy
import random
from passenger import Passenger, Companion
from resources import Airport, Flight

def passenger_generator(env, airport, flights, arrival_interval):
    passenger_id = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / arrival_interval))
        passenger_id += 1
        flights = [flight for flight in flights if flight.time > env.now]
        if len(flights) == 0:
            print('all flights done')
            env.event.succeed()
        flight = random.choice(flights)
        Passenger(f'Passenger {passenger_id}', env, flight, airport.ticket_booth, airport.check_in, airport.passport_control)

# Funkce pro generace kompanionů, možná lze přesunout do funkce generace pasažerů.
def companion_generator(env, arrival_interval):
    companion_id = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / arrival_interval))
        companion_id += 1
        Companion(f'Companion {companion_id}', env)

def flight_generator(max) -> list[Flight]:
    destinations = ['Berlin', 'Paris', 'Madrid', 'Porto', 'Warsaw', 'Bratislava', 'Wien', 'Budapest']
    gates = [1, 2, 3, 4, 5, 6]
    flights = []
    i = 0
    while i < max:
        destination = random.choice(destinations)
        time = random.randint(0, 288) * 5 # nahodný čas mezi 00:00 a 24:00, každých 5 minut
        gate = random.choice(gates)
        # TODO: opravit aby lety neobsazely stejné gaty ve stejný čas
        flights.append(Flight(destination, time, gate))
        i += 1
    return flights

def input():
    pass
    # TODO: funkce pro obdržení informace o simulaci od uživatele.

def stats():
    pass
    # TODO: sebrat a popsat statistiku o provozu letiště.

def main():
    flights = flight_generator(10)
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

if __name__ == "__main__":
    main()