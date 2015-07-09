from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import picamera
import time
import urllib2
import os

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication

# config
interval = 2

photo = [];

def takepicture():
	global photo
	with picamera.PiCamera() as camera:
		filename = 'Pipy_'+timestamp()
		# camera.start_preview()
		# Camera warm-up time
		time.sleep(1)
		camera.resolution = (2592, 1944)
		camera.iso = 0
		camera.exposure_mode = 'auto'
		g = camera.awb_gains
		camera.awb_mode = 'auto'
		camera.awb_gains = g
		camera.capture('./phototemp/'+filename+'.jpg')
		photo.append(filename)
		print "capture!!!"
	pass
def checkupload(num):
	global gauth, photo
	drive = GoogleDrive(gauth)
	if networkcheck():
		try:
			filename = photo[num]
			file_list = drive.ListFile({'q': "title='"+filename+".jpg'"}).GetList()
			for file1 in file_list:
					print 'title: %s, id: %s' % (file1['title'], file1['id'])
			if len(file_list)!=0:
				deletefile(num)
				photo.pop(num)
				print "upload checked"
				pass
		except:
			print 'fail to  check upload state'
		pass
	pass
def uploadfile(num):
	global gauth, photo
	drive = GoogleDrive(gauth)
	if networkcheck():
		
		try:
			filename = photo[num]
			f = drive.CreateFile({'title':str(filename)+'.jpg', 'mimeType':'image/jpeg',"parents": [{"kind":"drive#fileLink","id": "0B_yoHL2CjU_eflVLYm8zY3JQQ2hvWDhPczdSRVdiSmJ6RFJqZVkyU2tMaWdzNURzekhqZWs"}]})
			f.SetContentFile('phototemp/'+str(filename)+'.jpg')
			f.Upload()
			print 'upload success!!!'
		except:
			print 'upload failed!!!'
		pass
	pass
def networkcheck():
	try:
		response=urllib2.urlopen('http://140.112.2.197/',timeout=1)
		return True
	except urllib2.URLError as err:
		return False
	pass
def deletefile(num):
	global photo
	try:
		filename = photo[num]
		os.remove('phototemp/'+filename+'.jpg')
	except OSError:
	    pass

def getmin():
	
	minute = (time.time()/60)
	return minute
	pass
def timestamp():
	t = time.time()
	return time.strftime('%Y-%m-%d %H:%M:00', time.localtime(t))
	pass

premin = 0;
while 1:
	if getmin()-premin>interval:
		takepicture()
		premin = getmin()
		pass
	elif len(photo)>=1:
		uploadfile(0)
		time.sleep(5)
		checkupload(0)
		time.sleep(3)
		pass
	else:
		value = 100*round((getmin()-premin)/interval,2)
		print('waiting...'+str(value)+'%')
		time.sleep(5)	
		pass
# upload

print('title: %s, mimeType: %s' % (f['title'], f['mimeType']))





