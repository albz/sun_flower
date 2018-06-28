# Date:			02-02-2012
# Purpose:      from solar irradiation to power produced by solar modules
# Source:       python
#####################################################################

### loading shell commands
import sys, os, getopt, getpass, ftplib, time, datetime, StringIO, string, datetime

###--- ---###
###--- ---###

globals = {
    'verbose': 1,
    'status': {
        'dirs_total': 0,
        'dirs_created': 0,
        'dirs_removed': 0,
        'files_total': 0,
        'files_created': 0,
        'files_updated': 0,
        'files_removed': 0,
        'bytes_transfered': 0,
        'bytes_total': 0,
        'time_started': datetime.datetime.now(),
        'time_finished': 0,
        },
    }

def log(msg, level=1, abort=False):
    if level <= globals['verbose'] or abort:
        if abort:
            sys.stdout = sys.stderr
            print
        print msg
    if abort:
        sys.exit(1)

def strfbytes(value):
    units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    value = float(value)
    for unit in units:
        if value < 1024: break
        value = value / 1024
    if unit == units[0]: fmt = '%.0f %s'
    else: fmt = '%.2f %s'
    return fmt % (value, unit)

class localHandler:
    """ Local file and directory functions"""
    def __init__(self, ftp, root):
        self.ftp = ftp
        self.root = root
        self.host = ''

    def storefile(self, src, dst):
        fh = open(dst, 'wb')
        self.ftp.retrbinary('RETR %s' % src, fh.write)
        fh.close()

    def storetext(self, text, dst):
        fh = open(dst, 'w')
        fh.write(text)
        fh.close()

    def readlines(self, path):
        fh = open(path, 'r')
        buffer = [line.strip() for line in fh.readlines()]
        fh.close()
        return buffer

    def list(self, dir, skip_mtime=False):
        dirs = []
        files = {}
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if os.path.isdir(path):
                dirs.append(name)
            else:
                if skip_mtime: mtime = 0
                else: mtime = os.path.getmtime(path)
                files[name] = {
                    'size': os.path.getsize(path),
                    'mtime': mtime,
                    }
        return (dirs, files)

    def makedir(self, path):
        print 'Directory missing, creating it. => %s' % (path)
        os.mkdir(path)
        globals['status']['dirs_created'] += 1

class remoteHandler:
    """Remote file and directory functions"""
    def __init__(self, ftp, root):
        self.ftp = ftp
        self.root = root
        self.host = ftp.host

    def storefile(self, src, dst):
        fh = open(src)
        self.ftp.storbinary('STOR %s' % dst, fh)
        fh.close()

    def storetext(self, text, dst):
        fh = StringIO.StringIO(text)
        self.ftp.storlines('STOR %s' % dst, fh)
        fh.close()

    def readlines(self, path):
        buffer = []
        self.ftp.retrlines('RETR %s' % path, buffer.append)
        return buffer

    def list(self, dir, skip_mtime=False):
        month_to_int = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
            'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9,
            'Oct': 10, 'Nov': 11, 'Dec': 12}
        try:
            buffer = []
            self.ftp.dir('-a ', dir, buffer.append)
        except ftplib.error_temp:
            buffer = []
            self.ftp.dir(dir, buffer.append)
        dirs = []
        files = {}
        for line in buffer:
            cols = line.split(None, 8)
            name = os.path.split(cols[8])[1]
            if cols[0] == 'total' or name in ('.', '..'):
                continue
            if cols[0].startswith('d'):
                dirs.append(name)
            else:
                if skip_mtime:
                    mtime = 0
                else:
                    month = month_to_int[cols[5]]
                    day = int(cols[6])
                    if cols[7].find(':') == -1:
                        year = int(cols[7])
                        hour = minute = 0
                    else:
                        year = datetime.date.today().year
                        hour, minute = [int(s) for s in cols[7].split(':')]
                    mtime = datetime.datetime(year, month, day, hour, minute)
                    mtime = int(time.mktime(mtime.timetuple()))
                size = int(cols[4])
                files[name] = {
                    'size': size,
                    'mtime': mtime,
                    }
        return (dirs, files)

    def makedir(self, path):
        print 'Directory missing, creating it. => %s' % (path)
        self.ftp.mkd(path)
        globals['status']['dirs_created'] += 1

def mirror(src, dst, start_import_date, subdir=''):
	src_path = os.path.normpath('%s/%s' % (src.root, subdir))
	dst_path = os.path.normpath('%s/%s' % (dst.root, subdir))
	print '>>> analyzing >>> %s' % (src_path)

	#-splitting root directory -#
	root = src_path.lstrip('//')
	root = root.split('/')
	root0 = []; root1 = []
	root0 = root[0].split('_')
	if len(root) == 2:
		root1 = root[1].split('_')
	#- -#



	src_dirs, src_files = src.list(src_path)
	if '.sfmstat' in src_files:
		del src_files['.sfmstat']

	globals['status']['dirs_total'] += len(src_dirs)
	globals['status']['files_total'] += len(src_files)

	dst_dirs, dst_files = dst.list(dst_path, True)
	if '.sfmstat' in dst_files:
		sfmstat = dst.readlines(os.path.join(dst_path, '.sfmstat'))
		del dst_files['.sfmstat']
	else:
		if dst_path == dst.root and (dst_dirs or dst_files):
			if globals['verbose']: abort = False
			else: abort = True
#             log('New mirror, but target directory not empty!', abort=abort)
			result = raw_input('Do you really want to replace this directory? [y|n]: ')
#             if result.lower() not in ('y', 'yes'):
#                 log('Aborted', abort=True)
		sfmstat = ['0 %s%s' % (src.host, src_path)]

	last_updated, mirror_path = sfmstat[0].split(None, 1)
	if mirror_path != (src.host + src_path):
		if globals['verbose']: abort = False
		else: abort = True
		error = 'Mirror mismatch!\n%s already contains another mirror of %s' % (dst_path, mirror_path)
#         log(error, abort=abort)
		result = raw_input('Do you really want to replace this mirror? [y|n]: ')
#         if result.lower() not in ('y', 'yes'):
#             log('Aborted', abort=True)
		sfmstat = ['0 %s%s' % (src.host, src_path)]

	for line in sfmstat[1:]:
		mtime, file = line.split(None, 1)
		if file in dst_files:
			dst_files[file]['mtime'] = int(mtime)

	newstat = ['%i %s%s' % (int(time.time()), src.host, src_path)]
	for file in src_files:
		if file not in dst_files or src_files[file]['mtime'] > dst_files[file]['mtime'] or src_files[file]['size'] != dst_files[file]['size']:
			src_file = os.path.join(src_path, file)
			dst_file = os.path.join(dst_path, file)
			if file in dst_files:
				print 'File old version: updatying it => %s' % (dst_file)
				globals['status']['files_updated'] += 1
				dst.storefile(src_file, dst_file)
			else:
				print 'File missing: copying it => %s' % (dst_file)
				globals['status']['files_created'] += 1
				dst.storefile(src_file, dst_file)
			globals['status']['bytes_transfered'] += src_files[file]['size']
		globals['status']['bytes_total'] += src_files[file]['size']
		newstat.append('%i %s' % (src_files[file]['mtime'], file))
	dst.storetext('\n'.join(newstat), os.path.join(dst_path, '.sfmstat'))

	for dir in src_dirs:
		if 'Remote' not in dir:
			folder = dir.lstrip('//')
			folder = folder.split('_')
# 			print '>>>>>>>>>>>',folder
 			if len(folder) == 2 and folder[0] != 'dd':
 				if int(folder[0]) >= start_import_date.year and int(folder[1]) >= start_import_date.month or int(folder[0]) == start_import_date.year+1:
#  					print '>>> Analyzing folder:  ',folder[0],folder[1]
					if dir not in dst_dirs:
						dst_dir = os.path.join(dst_path, dir)
						#log('-> Create directory %s' % dst_dir)
						dst.makedir(dst_dir)
						#dst.makedir(os.path.join(dst_dir, 'dd_01'))
					mirror(src, dst, start_import_date, os.path.join(subdir, dir))
#--- day analisys ---#
			elif len(folder) == 2 and folder[0] == 'dd':
#   				print '||| ||| |||',folder[1],root0[0],root0[1]
				ok_this_one = datetime.date(int(root0[0]),int(root0[1]),int(folder[1]))
				if ok_this_one >= start_import_date:
					if dir not in dst_dirs:
						dst_dir = os.path.join(dst_path, dir)
						#log('-> Create directory %s' % dst_dir)
						dst.makedir(dst_dir)
					mirror(src, dst, start_import_date, os.path.join(subdir, dir))
			else:
				#print '>>> I have entered this part of the program...'
				dst_dir = os.path.join(dst_path, dir)
				#log('-> Create directory %s' % dst_dir)
				dst.makedir(dst_dir)
				mirror(src, dst, start_import_date, os.path.join(subdir, dir))
# 				if dir not in dst_dirs:
# 					dst_dir = os.path.join(dst_path, dir)
# 					#log('-> Create directory %s' % dst_dir)
# 					dst.makedir(dst_dir)
# 				mirror(src, dst, start_import_date, os.path.join(subdir, dir))


def import_data(start_import_date,folder,username,password,host,port):
	try:
		ftp_connect_and_import(start_import_date,folder,username,password,host,port)
	except:
		print '>>> Cannot Connect to Internet <<<'
		pass
	return


def ftp_connect_and_import(start_import_date,folder,username,password,host,port):

#     port = 21
    remotedir = '/'
#     remotedir = './.' #windows
#     localdir = os.getcwd()
#     username = '----------'
#     password = '----------'
#     host     = '001.001.001.001'

    ftp = ftplib.FTP()
    ftp.connect(host, port)
    ftp.login(username, password, '')


    ftp.cwd('/')

    if os.path.exists(folder) == False:
		os.makedirs(folder)
    local = localHandler(ftp, folder)
    remote = remoteHandler(ftp, remotedir)

	#take action
    mirror(remote, local, start_import_date)

    ftp.quit()


###--- FIND THE LAST IMPORT to speed up the sfp-downloading process ---###
def find_start_import_date(folder):
	file = os.path.join(folder,'.start_import_date')
	if os.path.exists(file) == True:
		v = []
		f = open(file,'r')
		for line in f:
			try:
				v.append(int(line))
			except:
				pass
 		start_import_date = datetime.date(v[0],v[1],v[2])
 	else:
 		start_import_date = datetime.date(2000,1,1)

 	return start_import_date
###--- ---###


###--- WRITE THE LAST DATE IMPORTED to speed up the sfp-downloading process ---###
def write_last_day_analized(date,folder):
	file = os.path.join(folder,'.start_import_date')
 	if os.path.exists(file) == True:
 		os.remove(file)
 		f = open(file,'w')
 		f.write( "%s \n" % str(date.year) )
 		f.write( "%s \n" % str(date.month) )
 		f.write( "%s   " % str(date.day) )
 		f.close()
 	else:
 		f = open(file,'w')
 		f.write( "%s \n" % str(date.year) )
 		f.write( "%s \n" % str(date.month) )
 		f.write( "%s   " % str(date.day) )
 		f.close()

 	return
###--- ---###
