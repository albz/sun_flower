# Date:			10-09-2012
# Purpose:      copy only new data to dropbox - sync
# Source:       python
#####################################################################

### loading shell commands
import os, os.path, glob, sys, shutil, scipy, numpy, pylab, matplotlib, csv, string
import time,datetime
### --- ###

#- copy subroutine -#
def copy_from_to(from_file_dir,to_file):
	if os.path.isdir(from_file_dir):
		shutil.copytree(from_file_dir,to_file)
	if os.path.isfile(from_file_dir):
		if not os.path.isdir(os.path.split(to_file)[0]):
			os.makedirs(os.path.split(to_file)[0])
		shutil.copy2(from_file_dir, to_file)
#- -#		


#- compare structure and data -#
def copy_data_to_dropbox(source_path,destination_path):
	for root_dirs, sub_dirs, files in os.walk(source_path):
		for file in files:
			source_file_path      = os.path.join(root_dirs,file)
			destination_file_path = os.path.join(destination_path,os.path.join(root_dirs[len(source_path)+1:],file))
			if os.path.isfile(destination_file_path):
				if time.ctime(os.path.getmtime(source_file_path)) > time.ctime(os.path.getmtime(destination_file_path)):
					copy_from_to(source_file_path,destination_file_path)
			if not os.path.isfile(destination_file_path):
				copy_from_to(source_file_path,destination_file_path)
	return