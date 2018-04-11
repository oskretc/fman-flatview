from fman import DirectoryPaneCommand, show_alert, show_status_message
from fman.url import dirname, as_human_readable, as_url, join


# from .Example import *

class FlatView(DirectoryPaneCommand):
	def __call__(self, url=None):
		if url is None:
			url = self.pane.get_file_under_cursor()		
	
		self.pane.set_path('example://'+ dirname(url).replace('file://', ''))
		# show_alert(self.pane.get_path())

from fman.fs import FileSystem, exists
from os import listdir, path
from os import path as ppp
from fman.url import dirname, as_human_readable


class Example(FileSystem):

	scheme = 'example://'

	# def __init__(self, path):
	# 	self.current_dir= path
	# 	show_status_message('this is my paht' + dirname(url))

	# TODO: implement columns
	def get_default_columns(self, path):
		# return 'core.Name', 'core.Size', 'core.Modified'
		return 'core.Name', 'flat_view.FullPath'
	# def size_bytes(self, path):
	# 	if path == 'File.txt':
	# 		return 4 * 1024
	# 	elif path == 'Image.jpg':
	# 		return 1300 * 1024
	# def modified_datetime(self, path):
	# 	if path == 'File.txt':
	# 		return datetime(2018, 2, 1, 12, 7)
	# 	elif path == 'Image.jpg':
	# 		return datetime(2017, 4, 15, 9, 36)		

	def iterdir(self, path):
		
	
		baseurl = 'file://' + path
		pathhuman = as_human_readable(baseurl)

		list_directory_content = listdir(pathhuman)
		
		
		for file_name in list_directory_content:
			completeurl=join(baseurl, file_name)
			# f= open('c:\\tmp\\flat.txt', 'a')
			# if is_dir(join(baseurl, file_name)):
			# 	f.write(join('\n' +baseurl, file_name))
			# else:
			# 	f.write(join('\n not dir' +baseurl, file_name))

			# f.close()			
			if not is_dir(completeurl):
				# yield pathhuman + '\\' + file_name
				yield file_name


	def is_dir(self, path):
		# f= open('c:\\tmp\\flat.txt', 'a')
		# f.write('\n' + path)
		# f.close()
		# if ppp.isdir(path):
		# 	return path
		# else:
		return path == 'as'		

	def full_path(self, path):
		return path

from fman.fs import Column

class FullPath(Column):
	"""Returns the full path of a url"""
	def get_str(self, url):			
		return as_human_readable(url.replace('example://', 'file://'))