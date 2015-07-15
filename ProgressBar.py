import sys
import os


class ProgressBar:
	def __init__(self, max):
		self.max = max
		self.terminal_width = int(os.popen('stty size', 'r').read().split()[1])


	def update(self, progress):
		terminal_width = int(os.popen('stty size', 'r').read().split()[1])
		width_progress = (terminal_width / 5) * 2
		part_length = float(width_progress) / 100
		percise_progress = (progress / (float(self.max) / 100))
		int_progress = int(percise_progress)
		if terminal_width != self.terminal_width:
			self.terminal_width = terminal_width
			sys.stdout.write("\r%s" % (" " * self.terminal_width))
			sys.stdout.flush()
		sys.stdout.write("\r[%s%s] (%s%s)" % ("#" * (int(percise_progress * part_length)), " " * (int(width_progress) - (int(percise_progress * part_length))), " " * (3 - len(str(int_progress))), str(int_progress) + "%"))
		sys.stdout.flush()
		if progress == self.max:
			print


if __name__ == "__main__":
	import time
	progress_bar = ProgressBar(30)
	i = 0
	while i <= 30:
		progress_bar.update(i)
		time.sleep(1)
		i += 1
