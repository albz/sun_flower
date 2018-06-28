# Date:			05-07-2012
# Purpose:      Albz's solar power plant analysis python script - send email report
# Source:       python
#####################################################################

### loading shell commands
import os, os.path, glob, sys, shutil, scipy, numpy, pylab, matplotlib, csv, string, ftplib
import time,datetime,codecs
import smtplib,codecs
from scipy import *
from numpy import *
from matplotlib import *
from pylab import *
import matplotlib
import matplotlib.pyplot as plt
###>>>
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64
###>>>

#- -#
gmail_user = 'test@gmail.com'
gmail_pwd  = '-------'
#- -#


def send_email(today_statistic,this_month_statistic,this_year_statistic,error_matrix,to_emails,folder_images):

#---email body
	msg_1 = '\n Risultati programma *human torch* eseguito il:\t' + str(datetime.datetime.today()) + '\n' + '\n' + '\n'

 	msg_2 = 'Produzione giornaliera --- Prodotta:\t' + '%1.2f' % (today_statistic[0])  + '\tkWh' +'\n'
 	msg_3 = 'Stimata da Solarimetro:\t' + '%1.2f' % (today_statistic[1])  + '\tkWh' + '\n'
 	msg_4 = 'Stimata da PVGIS:\t' + '%1.2f' % (today_statistic[2])  + '\tkWh' + '\n'
 	msg_5 = 'Percentuale [prodotta/stimata_solarimetro]:\t' + '%1.2f%%' % (today_statistic[0]/today_statistic[1]*100.) + '\n'
 	msg_6 = 'Percentuale [prodotta/stimata_PVGIS]:\t' + '%1.2f%%' % (today_statistic[0]/today_statistic[2]*100.) + '\n'+ '\n'+ '\n'

 	msg_7 = 'Produzione Mensile (ad oggi) --- Prodotta:\t' + '%1.2f' % (this_month_statistic[0]) + '\tkWh' + '\n'
 	msg_8 = 'Stimata da Solarimetro:\t' + '%1.2f' % (this_month_statistic[1]) + '\tkWh' + '\n'
 	msg_9 = 'Stimata da PVGIS:\t' + '%1.2f' % (this_month_statistic[2]) + '\tkWh' + '\n'
 	msg_10= 'Percentuale [prodotta/stimata_PVGIS]:\t' + '%1.2f%%' % (this_month_statistic[0]/this_month_statistic[2]*100.) + '\n'+ '\n'+ '\n'

 	msg_11= 'Produzione Annuale (ad oggi) --- Prodotta:\t' + '%1.2f' % (this_year_statistic[0]) + '\tkWh' + '\n'
 	msg_12= 'Stimata da PVGIS:\t' + '%1.2f' % (this_year_statistic[1]) + '\tkWh' + '\n'
 	msg_13= 'Percentuale [prodotta/stimata_PVGIS]:\t' + '%1.2f%%' % (this_year_statistic[0]/this_year_statistic[1]*100.) + '\n'+ '\n'+ '\n'

	body_text = msg_1 + msg_2 + msg_3 + msg_4 + msg_5 + msg_6 + msg_7 + msg_8 + msg_9 + msg_10 + msg_11 + msg_12 + msg_13

#- I am adding here the error report -#
	message_errors = '\n\n\n\n\n'
	message_errors = message_errors + 'Errori di produzione riscontrati oggi:\n'
	for i in range(0,len(error_matrix)):
#  		print ['Inverter = ', error_matrix[i][3], '-- Produzione Stimata =',error_matrix[i][2], '-- Produzione Effettiva',error_matrix[i][1], 'Ore:',error_matrix[i][0]]
		message_errors = message_errors + 'Inverter = ' + str(error_matrix[i][3]) + '     -- Produzione Stimata = ' + str(error_matrix[i][2]) + '     -- Produzione Effettiva = ' + str(error_matrix[i][1]) + '   Ore: ' + str(error_matrix[i][0])
		message_errors = message_errors + '\n'


	body_text = body_text + message_errors
#---< end


	msg = MIMEMultipart()
	msg['From'] = gmail_user
	msg['Subject'] = 'fotovoltaico - impianto ' + os.path.split(os.getcwd())[1] + ' - statistica al ' + str(datetime.datetime.today())
	msg.attach(MIMEText(body_text))
	png_folder = os.path.join(folder_images,datetime.date.today().strftime('%Y'))
	png_folder = os.path.join(png_folder,datetime.date.today().strftime('%m'))
	png_folder = os.path.join(png_folder,datetime.date.today().strftime('%d'))
	for (root, dirs, files) in os.walk(png_folder):
		for file in files:
			fp = open(os.path.join(root,file), 'rb')
			img = MIMEImage(fp.read())
			fp.close()
			msg.attach(img)


	for to_email in to_emails:
		msg['To'] = to_email
		mailServer = smtplib.SMTP('smtp.gmail.com', 587)
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		mailServer.login(gmail_user, gmail_pwd)
		mailServer.sendmail(gmail_user, to_email, msg.as_string())
		mailServer.close()

	#msg_1 = '\n Il programma ''human_torch'' e'' stato eseguito... questi i dati statistici al \t',str(datetime.datetime.today())
	# name = 'caf\xE9'
	# name = str(name.encode('utf-8'))
	# print(name)



def send_email_failure(inverter_number,email_sent,first_failure,to_emails):

#---email body
	body_text = '\n\n\n Inverter ' + str(inverter_number) + ' - down o sottoproducente: '
	if email_sent == 1: '==> piu di un ora'
	if email_sent == 2: '==> piu di 3 ore'
	if email_sent == 3: '==> piu di 1 giorno!'
	if email_sent == 4: '==> piu di 2 giorni consecutivi!'
	body_text += '\n'
	body_text += 'prima sottoproduzione registrata   '+str(first_failure)+'\n'
	body_text += 'tempo intercorso dalla prima sottoproduzione registrata   '+str(datetime.datetime.today()-first_failure)
#---

	msg = MIMEMultipart()
	msg['From'] = gmail_user
	if email_sent == 1: msg['Subject'] = 'Inverter ' + str(inverter_number) + ' - down   >1h'
	if email_sent == 2: msg['Subject'] = 'Inverter ' + str(inverter_number) + ' - down   >3h'
	if email_sent == 3: msg['Subject'] = 'Inverter ' + str(inverter_number) + ' - down   >1gg !'
	if email_sent == 4: msg['Subject'] = 'Inverter ' + str(inverter_number) + ' - down   >2gg !!!'
	msg.attach(MIMEText(body_text))

	for to_email in to_emails:
		msg['To'] = to_email
		mailServer = smtplib.SMTP('smtp.gmail.com', 587)
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		mailServer.login(gmail_user, gmail_pwd)
		mailServer.sendmail(gmail_user, to_email, msg.as_string())
		mailServer.close()


### --- ###
### --- ###
### --- ###
def send_email_failure_inverters(email_sent,first_failure,to_emails):

#---email body
	body_text = '\n\n\n Inverter 1 e Inverter 2 differiscono da Produzione, verificare'
	if email_sent == 1: '==> piu di un ora'
	if email_sent == 2: '==> piu di 3 ore'
	if email_sent == 3: '==> piu di 1 giorno!'
	if email_sent == 4: '==> piu di 2 giorni consecutivi!'
	body_text += '\n'
	body_text += 'prima discrepanza registrata   '+str(first_failure)+'\n'
	body_text += 'tempo intercorso dalla prima discrepanzas registrata   '+str(datetime.datetime.today()-first_failure)
#---

	msg = MIMEMultipart()
	msg['From'] = gmail_user
	if email_sent == 1: msg['Subject'] = 'Discrepanza Produzione Inverter    >1h'
	if email_sent == 2: msg['Subject'] = 'Discrepanza Produzione Inverter    >3h'
	if email_sent == 3: msg['Subject'] = 'Discrepanza Produzione Inverter    >1gg'
	if email_sent == 4: msg['Subject'] = 'Discrepanza Produzione Inverter    >2gg'
	msg.attach(MIMEText(body_text))

	for to_email in to_emails:
		msg['To'] = to_email
		mailServer = smtplib.SMTP('smtp.gmail.com', 587)
		mailServer.ehlo()
		mailServer.starttls()
		mailServer.ehlo()
		mailServer.login(gmail_user, gmail_pwd)
		mailServer.sendmail(gmail_user, to_email, msg.as_string())
		mailServer.close()
