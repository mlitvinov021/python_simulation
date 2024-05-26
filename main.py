import simpy
import random
from passenger import Passenger, Companion
from resources import Airport, Flight

# Generátor letů, vezme si random cíl, čas a gate (gate se zatím nepoužívá)
def flight_generator(max, sim_time) -> list[Flight]:
    destinations = ['Berlin', 'Paris', 'Madrid', 'Lisbon', 'Warsaw', 'Bratislava', 'Wien', 'Budapest']
    gates = [1, 2, 3, 4, 5, 6]
    flights = []
    i = 0
    while i < max:
        destination = random.choice(destinations)
        time = random.randint(0, int(sim_time/5)) * 5 # nahodný čas mezi 00:00 a 24:00, každých 5 minut
        gate = random.choice(gates)
        flights.append(Flight(destination, time, gate))
        i += 1
    return flights

# Generátor pasažerů, funguje nonstop, pokud existuje let pro který lze vygenerovat pasažera.
def passenger_generator(env, airport, flights, arrival_interval):
    passenger_id = 0
    companion_id = 0
    while True:
        # nahodný timeout pro generáci příštího batche pasažerů
        yield env.timeout(random.expovariate(1.0 / arrival_interval))

        # vyřazení letů, které se už uskutečnily v minulosti a vyběr nahodného letu
        flights = [flight for flight in flights if flight.time > env.now]
        if not flights:
            break
        flight = random.choice(flights)

        # nahodný počet pasažerů a doprovazejících
        num_passengers = int(random.triangular(1, 5, 3))
        num_companions = random.randint(0, 2)

        # tvorba pasažerů a doprovazejících
        while num_passengers > 0:
            passenger_id += 1
            num_passengers -= 1

            # pokud se let už uskutečnil, pasažer se nevytvaří (nebude si kupovat letenku pro minulý let)
            if flight.time <= env.now:
                print(f'Passenger {passenger_id} missed their flight to {flight.destination} at {flight.time//60:2.0f}:{flight.time%60:2.0f}.')
            else:    
                Passenger(f'Passenger {passenger_id}', env, flight, airport)
        while num_companions > 0:
            companion_id += 1
            num_companions -= 1
            Companion(f'Companion {companion_id}', env)
    print('All flights done')

def main():
    # parametry simulaci
    # TODO: převzetí parametrů od uživatele
    num_booths = 2
    num_check_ins = 4
    num_passport_controls = 4
    arrival_interval = 2
    simulation_time = 1440 # 24 hodiny v minutách
    flights = flight_generator(10, simulation_time)

    env = simpy.Environment()
    airport = Airport(env, num_booths, num_check_ins, num_passport_controls)
    env.process(passenger_generator(env, airport, flights, arrival_interval))
    env.run(until=simulation_time)

    # Print the statistics
    print(f"Total passengers entered the airport: {airport.total_passengers}")
    print(f"Total tickets bought: {airport.tickets_bought}")
    print(f"Total passengers registered: {airport.registered}")
    print(f"Total passengers passed passport control: {airport.passport_controlled}")

if __name__ == "__main__":
    main()