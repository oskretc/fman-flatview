from fman import DirectoryPaneCommand, DirectoryPaneListener, show_alert
from fman.fs import FileSystem, exists, Column, is_dir, cached
from fman.url import as_human_readable, as_url, splitscheme, basename, dirname
from os import walk
from os.path import relpath

import os
import os.path

class FlatView(DirectoryPaneCommand):
	def __call__(self, url=None):
		if url is None:
			url = self.pane.get_file_under_cursor() or self.pane.get_path()
		if not is_dir(url):
			url = dirname(url)
		new_url = Flat.scheme + splitscheme(url)[1]
		self.pane.set_path(new_url)


_SEPARATOR = '|'

class Flat(FileSystem):
	scheme = 'flat://'
	def get_default_columns(self, path):
		return 'flat_view.Name', 'flat_view.Path'
	def iterdir(self, path):
		# Recommended way for turning C:/tmp/one into C:\tmp\one:
		local_path = as_human_readable('file://' + path)
		for (dir_path, _, file_names) in walk(local_path):
			for file_name in file_names:
				file_path = os.path.join(dir_path, file_name)
				# file_path is now eg. C:\tmp\one\sub1\file.txt.
				# If we're iterating C:\tmp\one, yield "sub1|file.txt":
				yield path_to_name(relpath(file_path, local_path))
				# The above tells fman that in example://C:/tmp/one, there
				# are "files" example://C:/tmp/one/sub1|file.txt etc.
	def resolve(self, path):
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
		return is_dir(to_file_url(path))



def path_to_name(path):
	# Turn sub1\sub2 into sub1|sub2
	return path.replace(os.sep, _SEPARATOR)

def to_file_url(path):
	# Turn example://C:/tmp/one/sub1|sub2 -> file://C:/tmp/one/sub1/sub2.
	return as_url(path.replace(_SEPARATOR, os.sep))



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
		self.pane.place_cursor_at(to_file_url(self.path))
		
		
			