import threading


class TestClass():
	def __init__(self, core):
		print(True)

	def prepare(self):
		print(False)

	def start(self):
		update_thread = threading.Thread(target=self.update, args=())
		update_thread.start()

	def update(self):
		print("end")