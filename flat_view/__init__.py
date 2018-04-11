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
from fman.url import dirname, as_human_readable


class Example(FileSystem):

	scheme = 'example://'

	def get_default_columns(self, path):
		return 'core.Name', 'flat_view.FullPath'
	

	def iterdir(self, path):
		
	
		baseurl = 'file://' + path
		pathhuman = as_human_readable(baseurl)

		# list_directory_content = listdir(pathhuman)
		# 
		
		return self.find_files(baseurl)		
		
		# for file_name in list_directory_content:
		# 	completeurl=join(baseurl, file_name)
		# 	# f= open('c:\\tmp\\flat.txt', 'a')
		# 	# if is_dir(join(baseurl, file_name)):
		# 	# 	f.write(join('\n' +baseurl, file_name))
		# 	# else:
		# 	# 	f.write(join('\n not dir' +baseurl, file_name))

		# 	# f.close()			
		# 	if not is_dir(completeurl):
		# 		# yield pathhuman + '\\' + file_name
		# 		yield file_name


	def find_files(self, path):
		f= open('c:\\tmp\\flat.txt', 'a')
		# f.write('\n' + path)
		# f.close()
		list_files=[]
		for file_name in listdir(as_human_readable(path)):
			file_path=join(path, file_name)
			list_files.append(file_path)
			f.write('\n' + as_human_readable(file_path))
			if is_dir(file_path):
				list_files+=self.find_files(file_path)
		f.close()
		return list_files





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
		return (url)