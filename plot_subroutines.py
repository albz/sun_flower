# Date:			02-02-2012
# Purpose:      plots
# Source:       python
#####################################################################

### loading shell commands
import os, os.path, glob, sys, shutil, scipy, numpy, pylab, matplotlib, csv, string
import time,datetime
from scipy import *
from numpy import *
from matplotlib import *
from pylab import *
import matplotlib
import matplotlib.pyplot as plt
#>>>
from day_production import *
### --- ###




#file-name-time-format
file_name_time_format = "%Y_%m_%d"





### --- ### utility
def create_name_and_folder(path_folder_images):
	name_file = datetime.date.today().strftime('%Y_%m_%d')
	folder    = path_folder_images
	folder    = os.path.join(folder,datetime.date.today().strftime('%Y'))
	folder    = os.path.join(folder,datetime.date.today().strftime('%m'))
	folder    = os.path.join(folder,datetime.date.today().strftime('%d'))
	if not os.path.exists(folder):
		os.makedirs(folder)
	return name_file, folder
	#note: file folder... 	folder    = os.path.join(stub,datetime.date.today().strftime('%Y/%m/%d'))
### --- ###




###--- generic PLOT ---###
def generic_plot(dates,values):
	years      = YearLocator()   # every year
	months     = MonthLocator()  # every month
	days       = DayLocator()    # every month
	hrs        = HourLocator()   # every hour
	mins       = MinuteLocator() # every minute
	yearsFmt = DateFormatter('%Y')
	monthFmt = DateFormatter('%M')
	daysFmt  = DateFormatter('%d')
	hrsFmt   = DateFormatter('%H')


	fig = figure()
	ax = fig.add_subplot(111)
	ax.plot_date(dates, values, '.-')

#  	ax.xaxis.set_major_locator(hrs)
# 	ax.xaxis.set_major_formatter(hrsFmt)
#  	
#  	ax.xaxis.set_minor_locator(mins)
#  	
#  	ax.autoscale_view()
# 
# 	ax.set_title('day = %d-%d-%d' % (dates[1].day,dates[1].month,dates[1].year))

 	ax.grid(True)
 	
 	fig.autofmt_xdate()
	show()

	return




###--- DAY PLOT ---###
def day_plot(dates,values,display,path_folder_images):
	years      = YearLocator()   # every year
	months     = MonthLocator()  # every month
	days       = DayLocator()    # every month
	hrs        = HourLocator()   # every hour
	mins       = MinuteLocator() # every minute
	yearsFmt = DateFormatter('%Y')
	monthFmt = DateFormatter('%M')
	daysFmt  = DateFormatter('%d')
	hrsFmt   = DateFormatter('%H')


	fig = figure()
	ax = fig.add_subplot(111)
	ax.plot_date(dates, values, '.-')

 	ax.xaxis.set_major_locator(hrs)
	ax.xaxis.set_major_formatter(hrsFmt)
 	
 	ax.xaxis.set_minor_locator(mins)
 	
 	ax.autoscale_view()

	ax.set_title('day = %d-%d-%d' % (dates[1].day,dates[1].month,dates[1].year))

 	ax.grid(True)
 	
 	fig.autofmt_xdate()
	if display == 0:
		show()

	return


###--- MONTH PLOT ---###
def month_plot(dates,values,display,path_folder_images):
	years      = YearLocator()   # every year
	months     = MonthLocator()  # every month
	days       = DayLocator()    # every month
	hrs        = HourLocator()   # every hour
	mins       = MinuteLocator() # every minute
	yearsFmt = DateFormatter('%Y')
	monthFmt = DateFormatter('%M')
	daysFmt  = DateFormatter('%d')
	hrsFmt   = DateFormatter('%H')


	fig = figure()
	ax = fig.add_subplot(111)
	ax.plot_date(dates, values, '.-')

 	ax.xaxis.set_major_locator(days)
	ax.xaxis.set_major_formatter(daysFmt)
 	
 	ax.xaxis.set_minor_locator(hrs)
 	
 	ax.autoscale_view()

	ax.set_title('month = %d-%d' % (dates[1].month,dates[1].year))

 	ax.grid(True)
 	
 	fig.autofmt_xdate()
	if display == 0:
		show()

	
	return



###--- YEAR PLOT ---###
def year_plot(dates,values,display,path_folder_images):
	years      = YearLocator()   # every year
	months     = MonthLocator()  # every month
	days       = DayLocator()    # every month
	hrs        = HourLocator()   # every hour
	mins       = MinuteLocator() # every minute
	yearsFmt = DateFormatter('%Y')
	monthFmt = DateFormatter('%M')
	daysFmt  = DateFormatter('%d')
	hrsFmt   = DateFormatter('%H')


	fig = figure()
	ax = fig.add_subplot(111)
	ax.plot_date(dates, values, '.-')

 	ax.xaxis.set_major_locator(months)
	ax.xaxis.set_major_formatter(monthFmt)
 	
 	ax.xaxis.set_minor_locator(days)
 	
 	ax.autoscale_view()

	ax.set_title('year = %d' % (dates[1].year))

 	ax.grid(True)
 	
 	fig.autofmt_xdate()
	if display == 0:
		show()
		
	if display == 1:
		name_file, folder = create_name_and_folder(path_folder_images)
		name_file = os.path.join(folder,name_file+'__yearly_production.png')
		plt.savefig(name_file,dpi=300,figsize=(8,8))

	return


###--- MONTLY SEQUENTIAL PLOT ---###
def montly_sequential_plot(dates,values,PVcomparison,display,path_folder_images):
	years      = YearLocator()   # every year
	months     = MonthLocator()  # every month
	days       = DayLocator()    # every month
	hrs        = HourLocator()   # every hour
	mins       = MinuteLocator() # every minute
	yearsFmt = DateFormatter('%Y')
	monthFmt = DateFormatter('%M-%Y')
	daysFmt  = DateFormatter('%d')
	hrsFmt   = DateFormatter('%H')

	fig = figure()
	plot_date(dates, values, 'ro', label='E-Prodotta')
	plot_date(dates, values, 'r--')
	plot_date(dates, PVcomparison, 'bo', label='PVGIS')
	
	legend(loc='best', shadow=False, fancybox=True)
	
	ylabel('Energy (kWh)')
	
# -> attach some text labels
	for i in range(0,len(values)):
		pylab.text(dates[i],1.05*values[i], '%1.2f' % (values[i]/PVcomparison[i]))
# <-

 	grid(True)
 	
 	fig.autofmt_xdate()
	if display == 0:
		show()

	return


###--- MONTLY SEQUENTIAL PLOT plus extimation from pyranometer ---###
def montly_sequential_plus_thestimation_plot(dates,values,PVcomparison,est_dates,est_values,display,path_folder_images):
	years      = YearLocator()   # every year
	months     = MonthLocator()  # every month
	days       = DayLocator()    # every month
	hrs        = HourLocator()   # every hour
	mins       = MinuteLocator() # every minute
	yearsFmt = DateFormatter('%Y')
	monthFmt = DateFormatter('%M-%Y')
	daysFmt  = DateFormatter('%d')
	hrsFmt   = DateFormatter('%H')

	fig = figure()
	plot_date(dates, values, 'ro', label='E-Prodotta')
	plot_date(dates, values, 'r--')
	plot_date(est_dates, est_values, 'go', label='E-Estimated')
	plot_date(est_dates, est_values, 'g--')
	plot_date(dates, PVcomparison, 'b^', label='PVGIS', markersize=9)
	
	legend(loc='best', shadow=False, fancybox=True)
	
	ylabel('Energy (kWh)')
	
# -> attach some text labels
	for i in range(0,len(values)):
		pylab.text(dates[i],1.05*values[i], '%1.0f%%' % (values[i]/PVcomparison[i]*100.))
# <-

 	grid(True)
 	
 	fig.autofmt_xdate()
	if display == 0:
		show()
		
	if display == 1:
		name_file, folder = create_name_and_folder(path_folder_images)
		name_file = os.path.join(folder,name_file+'__montly_sequential.png')
		plt.savefig(name_file,dpi=300,figsize=(8,8))
		

	return




###--- MONTLY CORRELATED PLOT ---###
def montly_correlated_plot(values,PV,display,path_folder_images):
	years      = YearLocator()   # every year
	months     = MonthLocator()  # every month
	days       = DayLocator()    # every month
	hrs        = HourLocator()   # every hour
	mins       = MinuteLocator() # every minute
	yearsFmt = DateFormatter('%Y')
	monthFmt = DateFormatter('%M-%Y')
	daysFmt  = DateFormatter('%d')
	hrsFmt   = DateFormatter('%H')


	#dim
	s = values.shape
	m = range(1,12+1)

	fig = figure()
	ax  = subplot(111)
	
	ax.plot(m, PV, 'k^', label='PVGIS', markersize=15)
	
	for y in range(0,s[1]):
		ax.plot(m, values[:,y], 'o--', label='year = %d' % (2011+y))
		
		
	params = {'legend.fontsize': 8}
	pylab.rcParams.update(params)
	ax.legend(loc=2, shadow=False, fancybox=True)
	
	xlim(1,12)
# 	ax.xaxis.get_major_ticks()
 	
 	ylabel('Energy (kWh)')
 	xlabel('month')

  	grid(True)

	if display == 0:
		show()

	if display == 1:
		name_file, folder = create_name_and_folder(path_folder_images)
		name_file = os.path.join(folder,name_file+'__montly_correlated.png')
		plt.savefig(name_file,dpi=300,figsize=(8,8))

	return




###--- DAILY PRODUCTION PLOT ---###
def daily_production_plot(dates,values,display,path_folder_images):
	years      = YearLocator()   # every year
	months     = MonthLocator()  # every month
	days       = DayLocator()    # every month
	hrs        = HourLocator()   # every hour
	mins       = MinuteLocator() # every minute
	yearsFmt = DateFormatter('%Y')
	monthFmt = DateFormatter('%M-%Y')
	daysFmt  = DateFormatter('%d')
	hrsFmt   = DateFormatter('%H')


	fig = figure()
	
	width=1.0
	bar(dates, values, width, color='r', label='E-Prodotta')	
 	
 	legend(loc='best', shadow=False, fancybox=True)
 	ylabel('Energy (kWh)')
 
  	grid(True)
  	
  	fig.autofmt_xdate()

	if display == 0:
		show()

	return


###--- DAILY PRODUCTION PLOT plus extimation from pyranometer ---###
def daily_production_plus_thestimation_plot(dates,values,est_dates,est_values,days_back,display,path_folder_images):
	years      = YearLocator()   # every year
	months     = MonthLocator()  # every month
	days       = DayLocator()    # every month
	hrs        = HourLocator()   # every hour
	mins       = MinuteLocator() # every minute
	yearsFmt = DateFormatter('%Y')
	monthFmt = DateFormatter('%M-%Y')
	daysFmt  = DateFormatter('%d')
	hrsFmt   = DateFormatter('%H')

# 	for i in range(0,len(dates)):
# 		dates[i] = datetime.date(dates[i].year,dates[i].month,dates[i].day)
# 	for i in range(0,len(est_dates)):
# 		est_dates[i] = datetime.date(est_dates[i].year,est_dates[i].month,est_dates[i].day)

	fig = figure()

	ax1 = subplot(211)
	width=1.0
  	ax1.bar(est_dates, est_values, width, color='g', label='E-Extimated', edgecolor='g')	
  	ax1.bar(dates, values, width, color='r', label='E-Prodotta', edgecolor='r')	
	ylabel('Energy (kWh)')
	legend(loc='best', shadow=False, fancybox=True)
  	if days_back != 0:
		xlim(datetime.date.today()-days_back,datetime.date.today()+datetime.timedelta(days=1))

	ax2 = subplot(212)
	ax2.plot_date(est_dates, est_values, 'g-', label='E-Extimated', lw=2)
	ax2.plot_date(dates, values, 'r-', label='E-Prodotta', lw=2)
	ylabel('Energy (kWh)')
  	if days_back != 0:
		xlim(datetime.date.today()-days_back,datetime.date.today())
 	
#  	ax1.legend(loc='best', shadow=False, fancybox=True)
#  	ax1.ylabel('Energy (kWh)')
 
  	grid(True)

  	fig.autofmt_xdate()

	if display == 1 and days_back == 0:
		name_file, folder = create_name_and_folder(path_folder_images)
		name_file = os.path.join(folder,name_file+'__daily_production_since_0.png')
		plt.savefig(name_file,dpi=300,figsize=(8,8))

	if display == 1 and days_back == datetime.timedelta(days=7):
		name_file, folder = create_name_and_folder(path_folder_images)
		name_file = os.path.join(folder,name_file+'__daily_production_7days.png')
		plt.savefig(name_file,dpi=300,figsize=(8,8))

	if display == 1 and days_back == datetime.timedelta(days=30):
		name_file, folder = create_name_and_folder(path_folder_images)
		name_file = os.path.join(folder,name_file+'__daily_production_1month.png')
		plt.savefig(name_file,dpi=300,figsize=(8,8))


	if display == 0:
		show()

	return


###--- YEARLY SEQUENTIAL PLOT ---###
def yearly_sequential_plot(dates,values,PVcomparison,display,path_folder_images):
	years      = YearLocator()   # every year
	months     = MonthLocator()  # every month
	days       = DayLocator()    # every month
	hrs        = HourLocator()   # every hour
	mins       = MinuteLocator() # every minute
	yearsFmt = DateFormatter('%Y')
	monthFmt = DateFormatter('%M-%Y')
	daysFmt  = DateFormatter('%d')
	hrsFmt   = DateFormatter('%H')

	fig = figure()
	ax = fig.add_subplot(111)
	ax.plot_date(dates, values, 'ro', label='E-Prodotta')
	ax.plot_date(dates, values, 'r--')
	ax.plot_date(dates, PVcomparison*ones(len(dates)), 'bo--', label='PVGIS')

 	ax.xaxis.set_major_formatter(yearsFmt)
  	ax.xaxis.set_major_locator(years) 	
  	ax.xaxis.set_minor_locator(years)
  	ax.autoscale_view()
	
	ax.legend(loc='best', shadow=False, fancybox=True)
	
	ylabel('Energy (kWh)')
	
# -> attach some text labels
	for i in range(0,len(values)):
		pylab.text(dates[i],1.05*values[i], '%1.2f' % (values[i]/PVcomparison))
# <-

 	grid(True)
 	
 	fig.autofmt_xdate()
	if display == 0:
		show()
		
	if display == 1:
		name_file, folder = create_name_and_folder(path_folder_images)
		name_file = os.path.join(folder,name_file+'__yearly_sequential_plot.png')
		plt.savefig(name_file,dpi=300,figsize=(8,8))

	return


###--- PLOT POWER VS IRR-EXPECTED-POWER ---###
def plot_pow_vs_expected(date_pow,pow,date_irr,irr_exp,display,path_folder_images):

	fig = figure()
	ax  = fig.add_subplot(111)

	ax.plot_date(date_irr, irr_exp, 'g-', label='Max E-Stimata')
	ax.plot_date(date_pow, pow, 'b-', label='E-Prodotta')

	ylabel('Power (kW)')
	legend(loc='best', shadow=False, fancybox=True)
	title('day = %d-%d-%d' % (date_pow[0].year,date_pow[0].month,date_pow[0].day))

	ax.grid(True)
	fig.autofmt_xdate()
	if display == 0:
		show()
		
	if display == 1:
		name_file, folder = create_name_and_folder(path_folder_images)
		name_file = os.path.join(folder,name_file+'__today_production.png')
		plt.savefig(name_file,dpi=300,figsize=(8,8))

	return


###--- PLOT POWER VS IRR-EXPECTED-POWER with Inverter 1-and-2 for comparison---###
def plot_pow_vs_expected_with_inverter_detached(date_pow,pow,date_irr,irr_exp,date_inv_1,pow_inv_1,date_inv_2,pow_inv_2,display,path_folder_images):

	fig = figure()
	ax  = fig.add_subplot(111)

	ax.plot_date(date_irr, irr_exp, 'g-o', label='Max E-Stimata')
	ax.plot_date(date_pow, pow, 'b-o', label='E-Prodotta')
	ax.plot_date(date_inv_1, pow_inv_1, 'r-o', label='Inverter 1')
	ax.plot_date(date_inv_2, pow_inv_2, 'k-o', label='Inverter 2')

	ylabel('Power (kW)')
	legend(loc='best', shadow=False, fancybox=True)
	title('day = %d-%d-%d' % (date_pow[0].year,date_pow[0].month,date_pow[0].day))

	ax.grid(True)
	fig.autofmt_xdate()
	if display == 0:
		show()
		
	if display == 1:
		name_file, folder = create_name_and_folder(path_folder_images)
		name_file = os.path.join(folder,name_file+'__today_production_inverter.png')
		plt.savefig(name_file,dpi=300,figsize=(8,8))
	return


###--- Plot whole year production as DayPower vs Time ---###
def plot_DayPower_vs_Time(datetime_pow,pow,display,path_folder_images):

	l = len(pow)

	fig = figure()
	ax = fig.add_subplot(111)
	colormap = plt.cm.gist_ncar
	plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, 365)])
		
	today          = datetime.datetime.today()
	today          = datetime.datetime(today.year,today.month,today.day,0,0,0)
	day_to_analyze = datetime.datetime(today.year,1,1,0,0,0)
	
	while day_to_analyze <= today:
		util_1,util_2 = selected_day(datetime_pow[:][0],pow[:][0],day_to_analyze)
		for i in range(1,l):
			util_3,util_4 = selected_day(datetime_pow[:][i],pow[:][i],day_to_analyze)
			util_5,util_6 = sum_datetime_vectors(util_1,util_2,util_3,util_4,datetime.timedelta(minutes=5))
			util_1        = util_5
			util_2        = util_6
			
		for i in range(0,len(util_5)):
			element   = util_5[i]
			element   = datetime.datetime(2012,1,1,element.hour,element.minute,element.second)
			util_5[i] = element
				
		if day_to_analyze<today:
			ax.plot_date(util_5, util_6,'-')
		else:
			ax.plot_date(util_5, util_6,'ko-',lw=2.0)
		day_to_analyze += one_day

		ax.grid(True)
		xlim(datetime.datetime(2012,1,1,0,0,0),datetime.datetime(2012,1,1,23,59,59))
		ax.set_title('Year-Power *** day = '+datetime.date.today().strftime('%Y_%m_%d'))
		xlabel('time')
		ylabel('Power (kW)')
	 	fig.autofmt_xdate()

	if display == 0:
		show()
		
	if display == 1:
		name_file, folder = create_name_and_folder(path_folder_images)
		name_file = os.path.join(folder,name_file+'__DayPower_vs_Time.png')
		plt.savefig(name_file,dpi=120,figsize=(8,8))
	return
