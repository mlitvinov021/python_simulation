import simpy
import random
from passenger import Passenger, Companion
from resources import Airport, Flight

def flight_generator(max) -> list[Flight]:
    destinations = ['Berlin', 'Paris', 'Madrid', 'Lisbon', 'Warsaw', 'Bratislava', 'Wien', 'Budapest']
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

def passenger_generator(env, airport, flights, arrival_interval):
    passenger_id = 0
    companion_id = 0
    while True:
        yield env.timeout(random.expovariate(1.0 / arrival_interval))
        flights = [flight for flight in flights if flight.time > env.now]
        flight = random.choice(flights)
        num_passengers = int(random.triangular(1, 5, 3))
        num_companions = random.randint(0, 2)
        while num_passengers > 0:
            passenger_id += 1
            num_passengers -= 1
            Passenger(f'Passenger {passenger_id}', env, flight, airport.ticket_booth, airport.check_in, airport.passport_control)            
        while num_companions > 0:
            companion_id += 1
            num_companions -= 1
            Companion(f'Companion {companion_id}', env)

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
    env.run(until=simulation_time)

if __name__ == "__main__":
    main()