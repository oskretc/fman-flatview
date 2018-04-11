from os import listdir
from fman import DirectoryPaneCommand, show_alert, show_status_message
from fman.url import dirname, as_human_readable, join, splitscheme
from fman.fs import FileSystem, Column, is_dir

class FlatView(DirectoryPaneCommand):
	def __call__(self, url=None):
		if url is None:
			url = self.pane.get_file_under_cursor()		
	
		self.pane.set_path('example://'+ dirname(url).replace('file://', ''))
		# show_alert(self.pane.get_path())

class Example(FileSystem):

	scheme = 'example://'

	def get_default_columns(self, path):
		return 'core.Name', 'flat_view.FullPath'
	

	def iterdir(self, path):
	
		baseurl = 'file://' + path

		return self.find_files(baseurl)		




	def find_files(self, path):

		list_files=[]
		for file_name in listdir(as_human_readable(path)):
			file_path=join(path, file_name)
			scheme, simplepath =splitscheme(file_path)
			# Remove folders and files starting with .   TODO: improve this
			if not file_name.startswith('.'):				
				if is_dir(file_path):
					list_files+=self.find_files(file_path)
				# Only add Files not Directories
				else:
					list_files.append(simplepath)

		return list_files

	def full_path(self, path):
		return path


class FullPath(Column):
	"""Returns the full path of a url"""
	def get_str(self, url):			
		scheme, path =splitscheme(url)
		return (path)