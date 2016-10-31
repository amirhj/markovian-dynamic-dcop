import sys, json
from argparser import ArgParser
from grid import Grid
from scheduler import Scheduler
from agent import Agent
from messageserver import MessageServer

opt_pattern = {'-c': {'name': 'convergence_size', 'type': 'int', 'default': 4},
               '-s': {'name': 'standard_deviation', 'type': 'float', 'default': 2.0},
               '--omega': {'name': 'omega', 'type': 'float', 'default': 0.5}
               }
arg = ArgParser(sys.argv[2:], opt_pattern)
opt = arg.read()

grid = Grid(json.loads(open(sys.argv[1], 'r').read()), opt)

messageserver = MessageServer(opt)
agents = {}
for a in grid.agents:
	agent = Agent(a, grid, messageserver, opt)
	agents[a] = agent

scheduler = Scheduler(grid, agents, auctioneer, messageserver, opt)

scheduler.initialize()
scheduler.run()
scheduler.terminate()