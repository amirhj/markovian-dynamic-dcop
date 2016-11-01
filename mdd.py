import sys, json
from argparser import ArgParser
from grid import Grid
from scheduler import Scheduler
from agent import Agent
from messageserver import MessageServer

opt_pattern = { '--temperature': {'name': 'temperature', 'type': 'float', 'default': 1.0},
				'--test-temperature': {'name': 'test-temperature', 'type': 'float', 'default': 3.0},
				'--decay': {'name': 'decay', 'type': 'float', 'default': 1.0009},
				'-t': {'name': 'tests', 'type': 'int', 'default': 20},
				'-c': {'name': 'convergence_size', 'type': 'int', 'default': 30},
				'-s': {'name': 'standard_deviation', 'type': 'float', 'default': 2.0},
				'--beta': {'name': 'beta', 'type': 'float', 'default': 0.8}
				}
arg = ArgParser(sys.argv[2:], opt_pattern)
opt = arg.read()

fg = FactorGraph(opt)

fg.load(sys.argv[1])

environment = fg.environment

messageserver = MessageServer(opt)
agents = {}
for n in fg.nodes:
	agent = Agent(n, fg, environment, messageserver, opt)
	agents[a] = agent

scheduler = Scheduler(fg, agents, environment, messageserver, opt)

scheduler.initialize()
scheduler.run()
scheduler.terminate()