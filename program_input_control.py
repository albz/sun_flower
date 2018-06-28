# Date:			15-09-2012
# Purpose:      controls program inputs
# Source:       python
#####################################################################

### loading shell commands
import os, os.path, glob, sys, shutil, scipy, numpy, pylab, matplotlib, csv, string
import time,datetime
### --- ###

def input_control_parameters(inputs):

	#default parameters
	graph_style = 0       # 0 - display
	loop        = False   # no loop
	#- -#


	if len(inputs) > 1:
		#-loop or no loop-#
		if inputs[0] == 'loop':
			loop = True
		if inputs[0] == 'noloop':
			loop = False

		#- print or dispaly -#
		# 0 - display
		# 1 - print on file
		if loop == True:
			graph_style = 1
		else:
			if len(inputs) == 2:
				if inputs[1] == 'display':
					graph_style = 0
				if inputs[1] == 'print':
					graph_style = 1
			else:
				graph_style = 0

	return graph_style, loop
