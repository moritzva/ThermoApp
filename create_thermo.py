#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Thermogram:

	def __init__(self, imagetype, filename, referencefilename, colorlimit, colormap, crop, xlimit, ylimit, imagesize):
		self.imagetype = str(imagetype)
		self.filename = str(filename)
		self.referencefilename = str(referencefilename)
		self.colorlimit = colorlimit
		self.colormap = str(colormap)
		self.crop = bool(crop)
		self.xlimit = xlimit
		self.ylimit = ylimit
		self.imagesize = imagesize

	def get_data(self):

		# skiprows, because pandas doesnt recognise the ° symbol
		df = pd.read_csv(self.filename, sep='\t', skiprows=18, header=None)
		df = df.fillna(0)  # NaN is now 0
		df = df.to_numpy()  # dataframe to ndarray

		return df

	def get_reference(self):

		# load in reference file
		# skiprows, because pandas doesnt recognise the ° symbol
		df_reference = pd.read_csv(self.referencefilename, sep='\t', skiprows=18, header=None)
		df_reference = df_reference.fillna(0)  # NaN is now 0
		df_reference = df_reference.to_numpy()  # dataframe to ndarray
		return df_reference

	def get_info(self):

		# read information from file header
		# just read lines 10, 12, 13. encoding='cp1252' is important
		lines_to_load = [10, 12, 13]
		df_info = pd.read_csv(self.filename,
							  sep='\t', header=None, encoding='cp1252',
							  skiprows=lambda i: i not in lines_to_load)
		df_info = df_info.to_numpy()  # dataframe to ndarray

		# edit strings so that only relevant info is displayed
		x = str(df_info[0])  # FrameIndex information
		x_new = x[13:len(x) - 2:]  # deletion of 'FrameIndex='. just the actual number is kept
		df_info[0] = int(x_new)

		y = str(df_info[1])  # RecTime information
		y_new = y[10:len(y) - 2:]  # deletion of 'RecTime='. just the actual date is kept
		df_info[1] = str(y_new)

		z = str(df_info[2])  # seconds information, in file as milliseconds therefore / 1000
		z_new = z[5:len(z) - 2:]  # deletion of 'ms=', just the actual number is kept
		df_info[2] = float(z_new) / 1000

		df_info = np.append(df_info, df_info)
		return df_info

	def draw_thermo(self):

		fig, ax = plt.subplots(1, 1, figsize=(self.imagesize[0], self.imagesize[1]))
		plt.rcParams.update({'font.size': 14})  # fontsize

		if self.crop:
			ax.set_xlim(self.xlimit[0], self.xlimit[1])  # crop x-axis
			ax.set_ylim(self.ylimit[0], self.ylimit[1])  # crop y-axis

		if self.imagetype == 'reference':
			df = Thermogram.get_data(self)
			df_referenz = Thermogram.get_reference(self)
			df_delta = df - df_referenz
			image = ax.imshow(df_delta, cmap=self.colormap, origin='upper')  # cmap defines colormap
			label = '\u0394T in °C'

		else:  # absolute
			image = ax.imshow(Thermogram.get_data(self), cmap=self.colormap, origin="upper")  # cmap defines colormap
			label = 'Temperature in °C'

		image.set_clim(vmin=self.colorlimit[0], vmax=self.colorlimit[1])  # scaling of legend

		fig.colorbar(image, orientation='vertical', label=label, shrink=0.9, pad=0.05, extend='both')
		# shrink shrinks colorbar, pad regulates distance between colorbar and image

		ax.set_axis_off()  # delete ax labels
		plt.tight_layout()  # better layout

		return image

	def show(self):
		Thermogram.draw_thermo(self)
		plt.show()

	def destroy(self):
		# important feature for GUI application:
		# should there be a bug, figure will be deleted from memory by this function
		plt.close(fig='all')

	def __str__(self):
		# define what the output of print(Thermogram) will be
		info = Thermogram.get_info(self)
		return 'FrameIndex \t= {0} \nRecTime \t= {1} \nSekunden \t= {2:.2f} \n'.format(info[0], info[1], info[2])


if __name__ == "__main__":

	thermo = Thermogram(imagetype='reference',
						filename='/home/moritz/PycharmProjects/Python_Studienarbeit/'
								 'ThermoApp/Daten/GW_1_Z2_863.txt',
						referencefilename='/home/moritz/PycharmProjects/Python_Studienarbeit/'
										  'ThermoApp/Daten/GW_1_Z2_860.txt',
						colorlimit=[-1, 1],
						colormap='magma',
						crop=False,
						xlimit=[205, 296],  # Attention: upper origin (small number, big number)
						ylimit=[353, 85],  # Attention: upper origin (big number, small number)
						imagesize=[4.92, 10.72])  # [width / 100, height / 100]

	print(thermo)
	thermo.show()

