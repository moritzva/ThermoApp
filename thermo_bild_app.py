import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Thermobild:
	"""Erstelle ein PNG Thermogramm einer .txt Datei ('dateiname') aus dem Ordner 'ordnername'
	- breite ist die Breite des Bildausschnittes in mm (ermitteln zB via inkscape)
	- massstab, legende, show (soll Bild gezeigt werden?), speichern sind bool-Argumente
	- die __str__ Funktion gibt Informationen zu dem Thermogramm aus
	- (FrameIndex, Aufzeichnungszeit, vergangene Millisek seit Start der Serie, Dateianzehl in Ordner, Temperaturen)
	- die get_info Funktion gibt diese Informationen in einem np.array aus
	- wenn Bilder in einem loop erzeugt werden sollen, muss loop=True gesetzt werden
	- fuer Einzelbilder loop=False setzen"""

	def __init__(self, art, dateiname, referenzdatei, colorlimit, colormap, zuschneiden, xlimit, ylimit, bildgroesse):
		self.art = str(art)
		self.dateiname = str(dateiname)
		self.referenzdatei = str(referenzdatei)
		self.colorlimit = colorlimit
		self.colormap = str(colormap)
		self.zuschneiden = bool(zuschneiden)
		self.xlimit = xlimit
		self.ylimit = ylimit
		self.bildgroesse = bildgroesse

	def get_data(self):

		# skiprows, da pandas nicht mit dem ° Zeichen aus den Dateien klar kommt
		df = pd.read_csv(self.dateiname, sep='\t', skiprows=18, header=None)
		df = df.fillna(0)  # ersetze NaN mit 0en
		df = df.to_numpy()  # dataframe zu ndarray

		return df

	def get_referenz(self):

		# Lade das Referenzbild ein
		# skiprows, da pandas nicht mit dem ° Zeichen aus den Dateien klar kommt
		df_referenz = pd.read_csv(self.referenzdatei, sep='\t', skiprows=18, header=None)
		df_referenz = df_referenz.fillna(0)  # ersetze NaN mit 0en
		df_referenz = df_referenz.to_numpy()  # dataframe zu ndarray
		return df_referenz

	def get_info(self):

		# Informationen aus dem header des Bildes einlesen
		# Nur die Zeilen 10,12,13 einlesen, wichtig ist hier encoding='cp1252'
		zu_ladende_zeilen = [10, 12, 13]
		df_info = pd.read_csv(self.dateiname,
							  sep='\t', header=None, encoding='cp1252',
							  skiprows=lambda i: i not in zu_ladende_zeilen)
		df_info = df_info.to_numpy()  # dataframe zu ndarray

		# Strings aus header bearbeiten so dass nur relevante Info ausgegeben wird
		x = str(df_info[0])  # FrameIndex Information
		x_neu = x[13:len(x) - 2:]  # Entfernen von 'FrameIndex=', nur die Zahl bleibt
		df_info[0] = int(x_neu)

		y = str(df_info[1])  # RecTime Information
		y_neu = y[10:len(y) - 2:]  # Entfernen von 'RecTime=', nur das Datum bleibt
		df_info[1] = str(y_neu)

		z = str(df_info[2])  # Sekunden Information, in Datei als ms deshalb / 1000
		z_neu = z[5:len(z) - 2:]  # Entfernen von 'ms=', nur die Zahl bleibt
		df_info[2] = float(z_neu) / 1000

		df_info = np.append(df_info, df_info)
		return df_info

	def draw_thermo(self):

		fig, ax = plt.subplots(1, 1, figsize=(self.bildgroesse[0], self.bildgroesse[1]))
		plt.rcParams.update({'font.size': 14})  # schriftgroesse

		if self.zuschneiden:
			ax.set_xlim(self.xlimit[0], self.xlimit[1])  # x-Achse zuschneiden
			ax.set_ylim(self.ylimit[0], self.ylimit[1])  # y-Achse zuschneiden

		if self.art == 'referenz':
			df = Thermobild.get_data(self)
			df_referenz = Thermobild.get_referenz(self)
			df_delta = df - df_referenz
			image = ax.imshow(df_delta, cmap=self.colormap, origin='upper')  # cmap definiert colormap
			label = '\u0394T in °C'

		else:  # Absoluttemperatur
			image = ax.imshow(Thermobild.get_data(self), cmap=self.colormap, origin="upper")  # cmap definiert colormap
			label = 'Temperature in °C'

		image.set_clim(vmin=self.colorlimit[0], vmax=self.colorlimit[1])  # Intervall der Temperaturlegende

		fig.colorbar(image, orientation='vertical', label=label, shrink=0.9, pad=0.05, extend='both')
		# shrink verkleinert colorbar, pad richtet abstand zwischen colorbar und bild ein

		ax.set_axis_off()  # entfernt Achsenbeschriftungen
		plt.tight_layout()  # besseres layout

		# plt.show()
		return image

	def show(self):
		Thermobild.draw_thermo(self)
		plt.show()

	def destroy(self):
		plt.close(fig='all')

	def __str__(self):

		info = Thermobild.get_info(self)
		# definiere was bei dem command print(class) ausgegeben wird
		return 'FrameIndex \t= {0} \nRecTime \t= {1} \nSekunden \t= {2:.2f} \n'.format(info[0], info[1], info[2])


if __name__ == "__main__":

	thermo = Thermobild(art='absolut',
						dateiname='/home/moritz/PycharmProjects/Daten_Studienarbeit/Thermografie/'
								  'GW_1_Zyklus2/GW_1_Z2_863.txt',
						referenzdatei='/home/moritz/PycharmProjects/Daten_Studienarbeit/Thermografie/'
									  'GW_1_Zyklus2/GW_1_Z2_192.txt',
						colorlimit=[16, 20],
						colormap='jet',
						zuschneiden=False,
						xlimit=[205, 296],  # Achtung: wegen upper origin (kleine Zahl, grosse Zahl)
						ylimit=[353, 85],  # Achtung: wegen upper origin (grosse Zahl, kleine Zahl)
						bildgroesse=[4.92, 10.72])  # [bildbreite / 100, bildhoehe / 100]

	print(thermo)
	thermo.show()

