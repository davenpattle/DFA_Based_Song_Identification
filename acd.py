from __future__ import print_function, division, unicode_literals
import wave
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import os
import glob
import numpy
import cPickle
import aifc
import math
from numpy import NaN, Inf, arange, isscalar, array
from scipy.fftpack import rfft
from scipy.fftpack import fft
from scipy.fftpack.realtransforms import dct
from scipy.signal import fftconvolve
from matplotlib.mlab import find
import matplotlib.pyplot as plt
from scipy import linalg as la
from scipy.signal import lfilter, hamming

def stZCR(frame):
    	count = len(frame)
    	countZ = numpy.sum(numpy.abs(numpy.diff(numpy.sign(frame)))) / 2
    	return (numpy.float64(countZ) / numpy.float64(count-1.0))


def stEnergy(frame):
   	 return numpy.sum(frame ** 2) / numpy.float64(len(frame))

def avg(arr):
	s = 0
	for i in range(len(arr)):
		s+=abs(arr[i])
	return s/len(arr)
	

def music_extraction(audio_file):
	wr = wave.open(audio_file,'r')
	par = list(wr.getparams())
	par[3] = 0
		
	
	ww1 = wave.open('song1.wav', 'w')
	ww1.setparams(tuple(par))
	
	ww2 = wave.open('song2.wav', 'w')
	ww2.setparams(tuple(par))
	
	ww = (ww1,ww2)

	sz = wr.getframerate()
	c = int(wr.getnframes()/sz)

	da=np.fromstring(wr.readframes(wr.getnframes()),dtype=np.int16)
	start=0;
	tail=0;
	wr.close()
	wr = wave.open(audio_file,'r')
	i=0
	for num in range(c):
		temp=np.fromstring(wr.readframes(int(sz/1)),dtype=np.int16)
		print(temp)
		print("\n")
		freq=avg(temp)
		print(freq)
		print("\n")
		if freq < 500:
			if tail-start > 240:
				song=da[start*sz:tail*sz]
				ww[i].writeframes(song.tostring())
				ww[i].close()
				i+=1
				start=tail
				
			start+=1
				
		tail+=1
	wr.close()

def channel_filter(audio_file):
	wr = wave.open(audio_file,'r')
	par = list(wr.getparams())
	par[3] = 0
		
	ww = wave.open('filtered-talk.wav', 'w')
	ww.setparams(tuple(par))

	sz = wr.getframerate()
	c = int(wr.getnframes()/sz)
	lowpass=5000
	highpass=15000		

	for num in range(c):
	    	da = np.fromstring(wr.readframes(sz), dtype=np.int16)
	    	left, right = da[0::2], da[1::2]
	    	lf, rf = np.fft.rfft(left), np.fft.rfft(right)
	    	lf[:lowpass], rf[:lowpass] = 0, 0
	    	lf[55:66], rf[55:66] = 0, 0
	    	lf[highpass:], rf[highpass:] = 0,0
	    	nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
	    	ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
	    	ww.writeframes(ns.tostring())
	wr.close()
	ww.close()
	
def plot(audio_file):
	
	ww = wave.open(audio_file, 'r')
	signal = ww.readframes(ww.getnframes())
	signal = np.fromstring(signal, 'Int16')
	fs = ww.getframerate()

	Time=np.linspace(0, len(signal)/fs, num=len(signal))
	plt.figure(1)
	plt.title('Signal Wave...')
	try:
		plt.plot(Time,signal)
		plt.show()
		ww.close()
	except OverflowError:
		print("\nSorry the audio is too big to be plotted with your available memory configuration")

def song_extractor(audio_file):
	wr=wave.open(audio_file,'r')
	er=15
	I=50
	S=30
	V=60
	O=30
	chck,start,tail=0,0,0
	i,s,vs,vsi=0,0,0,0
	diffzcr=50
	diffenergy=50
	# The regular expression E= I+(S(V+S)+I)+O
	sz = wr.getframerate() 
	c = int(wr.getnframes()/sz)
	check=1
	for i in range(c):
		daba = np.fromstring(wr.readframes(sz), dtype=np.int16)
		zcr=stZCR(daba)
		energy=stEnergy(daba)
		zcrprev=0
		energyprev=0
		if abs(zcr-zcrprev)>diffzcr and abs(energy-energyprev)>diffenergy and not tail==0:
			if (tail-start)>I-er and (tail-start)<I+er and entry==0:
				start=tail
				i+=1
			elif (tail-start)>S-er and (tail-start)<S+er and i>0:
				start=tail
				s+=1
				entry=1
			elif ((tail-start)>V-er and (tail-start)<V+er) or ((tail-start)>S-er and (tail-start)<S-er) and s==1:
				start=tail
				vs+=1
			elif (tail-start)>I-er and (tail-start)<I+er and vs>0:
				start=tail
				vsi+=1
				s=0
			elif (tail-start)>O-er and (tail-start)>O+er and vsi>0:
				chck=1
				break
			else:
				chck=0
				break
		tail+=1

	if check==0:
		print("\n\nThe song is not a generic Bollywood or Lollywood song\n")
	else:
		print("\n\nThe song is a generic Bollywood or Lollywood song\n")
		
		
#main
print("Enter the audio file name")

audio_file=raw_input()
music_extraction(audio_file)
song_extractor(audio_file)
channel_filter(audio_file)
#plot(audio_file)		
