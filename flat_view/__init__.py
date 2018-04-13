from fman import DirectoryPaneCommand, DirectoryPaneListener, show_prompt
from fman.fs import FileSystem, exists, Column, is_dir, cached
from fman.url import as_human_readable, as_url, splitscheme, basename, dirname
from os import walk
from os.path import relpath

import os
import os.path
import re
import fnmatch

class FlatView(DirectoryPaneCommand):
	def __call__(self, url=None):
		if url is None:
			url = self.pane.get_file_under_cursor() or self.pane.get_path()
		if not is_dir(url):
			url = dirname(url)
		new_url = Flat.scheme + splitscheme(url)[1]
		self.pane.set_path(new_url)

class FlatViewFiltered(DirectoryPaneCommand):
	def __call__(self, url=None):
		text, ok= show_prompt('Enter Filter e.g. *.txt', default="*.txt", selection_start=2 )
		if url is None:
			url = self.pane.get_file_under_cursor() or self.pane.get_path()
		if not is_dir(url):
			url = dirname(url)
		Flat.filtertext=text
		new_url = Flat.scheme + splitscheme(url)[1]
		# Not working yet
		if ok and text:
			self.pane.set_path(new_url + '?' + text)



_SEPARATOR = '|'
_QUERYSEPARATOR = '?'

class Flat(FileSystem):
	scheme = 'flat://'
	filtertext=""
	def __init__(self):

		# This is used to exclude folders and include files aka Filters
		self.excludes = ['.*']
		self.includes = ['*.*']
		self.convert_filters()		

		super().__init__()

	def convert_filters(self):
		self.excludes = r'|'.join([fnmatch.translate(x) for x in self.excludes]) or r'$.'
		self.includes = r'|'.join([fnmatch.translate(x) for x in self.includes])

	def get_default_columns(self, path):
		return 'flat_view.Name', 'flat_view.Path'
	def iterdir(self, path):
		# path=remove_query_text(path)
		# path is in the form of C:/tmp/one or C:/tmp/one?.*txt for filtered
		# Recommended way for turning C:/tmp/one into C:\tmp\one:
		local_path = as_human_readable('file://' + path)
		for (dir_path, dirs, file_names) in walk(local_path):
			# Adding posibility to filter out directories 
			# and files
			dirs[:] = [d for d in dirs if not re.match(self.excludes, d)]
			file_names = [f for f in file_names if re.match(self.includes, f)]
			for file_name in file_names:
				file_path = os.path.join(dir_path, file_name)
				# file_path is now eg. C:\tmp\one\sub1\file.txt.
				# If we're iterating C:\tmp\one, yield "sub1|file.txt":
				yield path_to_name(relpath(file_path, local_path))
				# The above tells fman that in example://C:/tmp/one, there
				# are "files" example://C:/tmp/one/sub1|file.txt etc.
	def resolve(self, path):
		# path=remove_query_text(path)
		# Tell fman about the "real" URL of the given file. This is important
		# eg. when you press Enter on a file. In this case, we want fman to
		# open file://directory/file.txt, not example://directory/file.txt
		url = self.scheme + path
		final_component = basename(url)
		if _SEPARATOR in final_component:
			return to_file_url(path)
		return url
	@cached
	def is_dir(self, path):
		# path=remove_query_text(path)
		return is_dir(to_file_url(path))



def path_to_name(path):
	# Turn sub1\sub2 into sub1|sub2
	return path.replace(os.sep, _SEPARATOR)

def to_file_url(path):
	# Turn example://C:/tmp/one/sub1|sub2 -> file://C:/tmp/one/sub1/sub2.
	return as_url(path.replace(_SEPARATOR, os.sep))

def remove_query_text(url):
	return url.split(_QUERYSEPARATOR)[0]

def get_query_text(url):
	if url.find(_QUERYSEPARATOR):
		return url.split(_QUERYSEPARATOR)[-1]
	else:
		return ''



class Name(Column):
	def get_str(self, url):
		# Turn example://C:/tmp/one/sub1|sub2 -> sub2:
		return basename(url).split(_SEPARATOR)[-1]

class Path(Column):
	def get_str(self, url):
		# Turn example://C:/tmp/one/sub1|sub2 -> C:/tmp/one/sub1/sub2:
		scheme, path = splitscheme(url)
		return splitscheme(to_file_url(path))[1]



class FlatViewOpenListener(DirectoryPaneListener):
	def on_command(self, command_name, args):
		if command_name == 'open_file':
			if 'url' in args:
				url= args['url']
				scheme, path =splitscheme(url)
				if scheme=='flat://':
					self.path=path
					self.pane.set_path('file://' + path.split(_SEPARATOR)[0], callback=self.callback)
					return 'open_directory', {'url':to_file_url(self.path)}

	def callback(self):	
		# self.pane.place_cursor_at(to_file_url(self.path))
		pass
		
		
			