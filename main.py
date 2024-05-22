import simpy
from passenger import Passenger

env = simpy.Environment()

passenger = Passenger()

env.run(until=15)