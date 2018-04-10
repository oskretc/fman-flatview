from fman import DirectoryPaneCommand, show_alert, show_status_message
from fman.fs import FileSystem
from fman.url import dirname, as_human_readable

class FlatView(DirectoryPaneCommand):
	def __call__(self, url=None):
		if url is None:
			url = self.pane.get_file_under_cursor()		
		# show_alert('Hello World!')
		show_status_message(dirname(url))
		self.pane.set_path('flatview://'+ dirname(url))

class Example(FileSystem):

	scheme = 'flatview://'

	# def __init__(self, path):
	# 	self.current_dir= path
	# 	show_status_message('this is my paht' + dirname(url))

	def iterdir(self, path):
		# if path == '':
		# 	return ['Directory', 'File.txt', 'Image.jpg']
		# elif path == 'Directory':
		# 	return ['File in directory.txt']
		yield FileSystem.resolve(path.replace(scheme, ''))

	def is_dir(self, path):
		return path == 'Directory'		