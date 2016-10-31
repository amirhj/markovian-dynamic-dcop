import threading, Queue


class MessageServer(threading.Thread):
	def __init__(self, opt):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.message_queue = Queue.Queue()
		self.opt = opt
		self.clients = None
		self.log = []
		self.terminate = False
		self.name = 'message-server'
		self.logfile = open('results/log.txt', 'w')
	
	def load(self, clients):
		self.clients = clients
		
	def run(self):
		while not self.terminate:
			if not self.message_queue.empty():
				m = self.message_queue.get()

				self.logfile.write(str(m)+'\n')
				self.log.append(m)
				self.clients[m[1]].receive(m[0], m[2]) # 0:sender, 2:content
	
	def send(self, sender, receiver, content, sendtime):
		self.message_queue.put((sender, receiver, content, sendtime))