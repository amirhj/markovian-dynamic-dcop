import threading, Queue
from datetime import datetime


class Agent(threading.Thread):
	def __init__(self, name, grid, message_server, opt):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.message_queue = Queue.Queue()
		self.message_server = message_server
		self.terminate = False
		self.opt = opt
		self.grid = grid
		self.name = name

		self.proposal = None
		if self.grid.agents[self.name]['is_seller']:
			self.proposal = {'price':self.grid.agents[self.name]['price'], 'amount':self.grid.agents[self.name]['max_delivery']}
		else:
			self.proposal = {'price':self.grid.agents[self.name]['bid'], 'amount':self.grid.agents[self.name]['max_demand']}
		
	
	def run(self):
		while not self.terminate:
			self.read_message()
	def receive(self, sender, content):
		self.message_queue.put((sender, content))
	
	def send(self, receiver, content):
		self.message_server.send(self.name, receiver, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

	def read_message(self):
		while not self.message_queue.empty():
			sender, m = self.message_queue.get()
			if sender == 'auctioneer':
				if m['type'] == 'submission':
					self.send('auctioneer', {'type':'submission', 'content':self.proposal})
				elif m['type'] == 'result':
					self.update_proposal(m['content']['price'], m['content']['others-actions'], m['content']['in_sellers'], m['content']['in_buyers'])
				elif m['type'] == 'price':
					pass #self.calculate_utility(m['content'])
				elif m['type'] == 'out':
					pass #self.calculate_utility(m['content'])
				else:
					raise Exception('Invalid message type ' + m['type'])
			else:
				raise Exception('Invalid sender '+ sender)

	def update_proposal(self, price, actions, in_sellers, in_buyers):
		amount = self.proposal['amount']
		amount = (1 - self.opt['omega']) * self.best_response(actions, in_sellers, in_buyers) + self.opt['omega'] * amount
		self.proposal['amount'] = amount

	def utility(self, price, actions, in_sellers, in_buyers):
		utility = 0
		if self.grid.agents[self.name]['is_seller']:
			amount = self.quantity(actions, in_sellers, in_buyers)
			flow = amount / len(in_buyers)
			flow_cost = sum([flow*self.grid.get_transfer_cost(self.name, b) for b in in_buyers])
			utility = (price - self.proposal['price']) * amount - flow_cost
		else:
			utility = (self.proposal['price'] - price) * amount
		return utility

	def best_response(self, actions, in_sellers, in_buyers):
		return self.quantity(actions, in_sellers, in_buyers)

	def quantity(self, actions, in_sellers, in_buyers):
		demand = 0
		for b in in_buyers:
			demand += self.grid.agents[b]['max_demand']

		consomption = 0
		for s in in_sellers:
			if s == self.name:
				consomption += self.proposal['amount']
			else:
				consomption += actions[s]

		quantity = 0
		if demand >= consomption:
			quantity = self.proposal['amount']
		else:
			count = len(in_sellers)
			if count > 1:
				count -= 1
			beta = (consomption - demand) / count
			quantity = max([0, self.proposal['amount'] - beta])
			
		return quantity