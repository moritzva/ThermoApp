#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
from create_thermo import Thermogram
from os import getcwd

REL_HEIGHT = 0.07
Y_FILENAME = 0.01
Y_TYPE = 0.12
Y_REFERENCE = 0.23
Y_COLORLIMIT = 0.34
Y_COLORMAP = 0.45
Y_CROP = 0.67
Y_COORDINATES = 0.78
Y_SIZE = 0.89


class ThermoApp:

	def __init__(self, root):
		self.root = root
		self.root.geometry('1000x600')
		self.root.title('ThermoApp')

		self.frame1 = tk.Frame(self.root, bg='grey', bd=2)
		self.frame1.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.85)
		self.frame2 = tk.Frame(self.root, bg='grey', bd=2)
		self.frame2.place(relx=0.01, rely=0.92, relheight=0.07, relwidth=0.98)

		self.entry_file = tk.Entry(self.frame1, state='disabled')
		self.entry_file.place(relx=0.17, rely=Y_FILENAME, relheight=REL_HEIGHT, relwidth=0.67)
		self.browse_file_button = tk.Button(self.frame1, text='Browse file', bg='lightgreen',
									   command=lambda: self.file_opener())
		self.browse_file_button.place(relx=0.85, rely=Y_FILENAME, relheight=REL_HEIGHT, relwidth=0.13)

		self.entry_reference = tk.Entry(self.frame1, state='disabled')
		self.entry_reference.place(relx=0.17, rely=Y_REFERENCE, relheight=REL_HEIGHT, relwidth=0.67)
		self.browse_reference_button = tk.Button(self.frame1, text='Browse reference', bg='gainsboro',
											command=lambda: self.reference_opener(), state='disabled')
		self.browse_reference_button.place(relx=0.85, rely=Y_REFERENCE, relheight=REL_HEIGHT, relwidth=0.13)

		self.variable_type = tk.StringVar()
		self.type_absolute = tk.Radiobutton(self.frame1, text='Absolute', variable=self.variable_type,
											value='absolute', command=lambda: self.deactivate_entry_reference())
		self.type_absolute.place(relx=0.42, relheight=REL_HEIGHT, rely=Y_TYPE, relwidth=0.1)
		self.type_reference = tk.Radiobutton(self.frame1, text='Relative', variable=self.variable_type,
											 value='reference', command=lambda: self.activate_entry_reference())
		self.type_reference.place(relx=0.55, relheight=REL_HEIGHT, rely=Y_TYPE, relwidth=0.1)
		self.variable_type.set('absolute')

		self.colorlimit_min = tk.Entry(self.frame1)
		self.colorlimit_min.place(relx=0.47, relheight=REL_HEIGHT, rely=Y_COLORLIMIT, relwidth=0.05)
		self.colorlimit_max = tk.Entry(self.frame1)
		self.colorlimit_max.place(relx=0.6, relheight=REL_HEIGHT, rely=Y_COLORLIMIT, relwidth=0.05)

		self.colormap_list = ['jet', 'magma', 'plasma', 'seismic', 'viridis']
		self.variable_colormap = tk.StringVar()
		self.variable_colormap.set(self.colormap_list)
		self.colormap_choice = tk.Listbox(self.frame1, selectbackground='lightgreen',
										  listvariable=self.variable_colormap)
		self.colormap_choice.place(relx=0.42, rely=Y_COLORMAP, relheight=0.11 + REL_HEIGHT, relwidth=0.23)

		self.variable_crop = tk.StringVar()
		self.crop_yes = tk.Radiobutton(self.frame1, text='Yes', variable=self.variable_crop, value='crop',
						  command=lambda: self.activate_coordinates())
		self.crop_yes.place(relx=0.42, relheight=REL_HEIGHT, rely=Y_CROP, relwidth=0.1)
		self.crop_no = tk.Radiobutton(self.frame1, text='No', variable=self.variable_crop, value='nocrop',
								 command=lambda: self.deactivate_coordinates())
		self.crop_no.place(relx=0.55, relheight=REL_HEIGHT, rely=Y_CROP, relwidth=0.1)
		self.variable_crop.set('nocrop')

		self.crop_x_min = tk.Entry(self.frame1, state='disabled')
		self.crop_x_min.place(relx=0.47, relheight=REL_HEIGHT, rely=Y_COORDINATES, relwidth=0.05)
		self.crop_x_max = tk.Entry(self.frame1, state='disabled')
		self.crop_x_max.place(relx=0.6, relheight=REL_HEIGHT, rely=Y_COORDINATES, relwidth=0.05)
		self.crop_y_min = tk.Entry(self.frame1, state='disabled')
		self.crop_y_min.place(relx=0.75, relheight=REL_HEIGHT, rely=Y_COORDINATES, relwidth=0.05)
		self.crop_y_max = tk.Entry(self.frame1, state='disabled')
		self.crop_y_max.place(relx=0.9, relheight=REL_HEIGHT, rely=Y_COORDINATES, relwidth=0.05)

		self.size_x = tk.Entry(self.frame1)
		self.size_x.insert(0, '10')
		self.size_x.place(relx=0.47, relheight=REL_HEIGHT, rely=Y_SIZE, relwidth=0.05)
		self.size_y = tk.Entry(self.frame1)
		self.size_y.insert(0, '8')
		self.size_y.place(relx=0.6, relheight=REL_HEIGHT, rely=Y_SIZE, relwidth=0.05)

		self.show_thermogram_button = tk.Button(self.frame2, text='Show thermogram', command=lambda: self.show_thermo(),
										   state='normal')
		self.show_thermogram_button.place(relx=0.84, rely=0.1, relwidth=0.15, relheight=0.8)

		self.label_error = tk.Label(self.frame2, anchor='w', text='', fg='black', bg='grey', font='bold')
		self.label_error.place(relx=0.01, rely=0.1, relheight=0.8, relwidth=0.51)

	def create_menu(self):
		menubar = tk.Menu(self.root)
		menubar.add_command(label='How to use', command=lambda: self.help_window())
		menubar.add_command(label='About', command=lambda: self.about_window())
		self.root.config(menu=menubar)

	def file_opener(self):
		file_path = filedialog.askopenfilename(initialdir=getcwd())
		if file_path:
			self.entry_file.config(state='normal')
			self.entry_file.delete(0, tk.END)
			self.entry_file.insert(0, file_path)

	def reference_opener(self):
		reference_path = filedialog.askopenfilename(initialdir=getcwd())
		if reference_path:
			self.entry_reference.config(state='normal')
			self.entry_reference.delete(0, tk.END)
			self.entry_reference.insert(0, reference_path)

	def help_window(self):
			help_win = tk.Toplevel(self.root)
			help_win.title('Information')
			help_win.geometry('650x420')
			txt = 'This script only works with .txt files which were exported through the IRBIS 3 software package. ' \
				'If used correctly, this tool will create customizable thermograms. \n\n' \
				'1. Load in a valid .txt file through the green "Browse file" button.\n' \
				'2. Choose between an absolute and a relative way of plotting your data. ' \
				'Load in a reference file if you checked "Relative".\n' \
				'3. Set the minimum and maximum values of the colorbar legend. Trial and error will lead to the best result.\n' \
				'4. You may choose between the listed colormaps. It is suggested to choose the "jet" version.\n' \
				'5. Choose whether you want to crop the figure. If so, enter the respective x- and y-coordinates. ' \
				'Do this by first plotting the uncropped image and hovering over the result with the cursor. ' \
				'The matplotlib figure should print the current coordinates somewhere on the canvas. ' \
				'Use these values for the cropping of your image.\n' \
				'Notice: Interchanging the xmin/xmax or ymin/ymax values will result in the mirroring of your image!!!\n' \
				'6. Choose if you want to change the standard image size of 1000 x 800 pixel.\n\n' \
				'Press the "Show thermogram" button to plot your image. ' \
				'To save the image, use the button on the matplotlib canvas under the created image. ' \
				'The button should look like a cartridge.'

			help_text = tk.Text(help_win, bg='lightgrey', wrap=tk.WORD)
			help_text.insert('1.0', txt)
			help_text.config(state='disabled')
			help_text.pack(pady=0.00, padx=0)

	def about_window(self):
		about_win = tk.Toplevel(self.root)
		about_win.title('About')
		about_win.geometry('600x120')
		txt = 'Script written by Moritz Müller.\n' \
			'Feel free to raise issues through the GitHub repository:\n' \
			'https://github.com/moritzva/ThermoApp'

		help_text = tk.Label(about_win, text=txt, anchor='center')
		help_text.config(state='normal')
		about_win.update()
		height = about_win.winfo_height()
		help_text.pack(pady=0.25*height)

	def activate_coordinates(self):
		self.crop_x_min.config(state='normal', bg='white')
		self.crop_x_max.config(state='normal', bg='white')
		self.crop_y_min.config(state='normal', bg='white')
		self.crop_y_max.config(state='normal', bg='white')

	def deactivate_coordinates(self):
		self.crop_x_min.config(state='disabled')
		self.crop_x_max.config(state='disabled')
		self.crop_y_min.config(state='disabled')
		self.crop_y_max.config(state='disabled')

	def activate_entry_reference(self):
		self.browse_reference_button.config(state='normal')
		self.browse_reference_button.config(bg='lightgreen')
		self.entry_reference.config(state='normal')

	def deactivate_entry_reference(self):
		self.browse_reference_button.config(state='disabled')
		self.browse_reference_button.config(bg='gainsboro')
		self.entry_reference.config(state='disabled')

	def labels(self):
		label_file = tk.Label(self.frame1, text='Selected file:', anchor='center')
		label_file.place(relx=0.01, rely=Y_FILENAME, relheight=REL_HEIGHT, relwidth=0.14)
		label_type = tk.Label(self.frame1, text='Type of temperature representation', anchor='center')
		label_type.place(relx=0.01, rely=Y_TYPE, relheight=REL_HEIGHT, relwidth=0.4)
		label_reference = tk.Label(self.frame1, text='Reference file:', anchor='center')
		label_reference.place(relx=0.01, rely=Y_REFERENCE, relheight=REL_HEIGHT, relwidth=0.14)
		label_colorlimit = tk.Label(self.frame1, text='Scaling limits of legend', anchor='center')
		label_colorlimit.place(relx=0.01, rely=Y_COLORLIMIT, relheight=REL_HEIGHT, relwidth=0.4)
		label_colorlimit_min = tk.Label(self.frame1, text='Min:')
		label_colorlimit_min.place(relx=0.42, rely=Y_COLORLIMIT, relheight=REL_HEIGHT, relwidth=0.05)
		label_colorlimit_max = tk.Label(self.frame1, text='Max:')
		label_colorlimit_max.place(relx=0.55, rely=Y_COLORLIMIT, relheight=REL_HEIGHT, relwidth=0.05)
		label_colormap = tk.Label(self.frame1, text='Colormap', anchor='center')
		label_colormap.place(relx=0.01, rely=Y_COLORMAP, relheight=REL_HEIGHT, relwidth=0.4)
		label_crop = tk.Label(self.frame1, text='Crop image?', anchor='center')
		label_crop.place(relx=0.01, rely=Y_CROP, relheight=REL_HEIGHT, relwidth=0.4)
		label_coordinates = tk.Label(self.frame1, text='Coordinates for cropping', anchor='center')
		label_coordinates.place(relx=0.01, rely=Y_COORDINATES, relheight=REL_HEIGHT, relwidth=0.4)
		label_coordiantes_xmin = tk.Label(self.frame1, text='Min x:')
		label_coordiantes_xmin.place(relx=0.42, rely=Y_COORDINATES, relheight=REL_HEIGHT, relwidth=0.05)
		label_coordinates_xmax = tk.Label(self.frame1, text='Max x:')
		label_coordinates_xmax.place(relx=0.55, rely=Y_COORDINATES, relheight=REL_HEIGHT, relwidth=0.05)
		label_coordinates_ymin = tk.Label(self.frame1, text='Min y:')
		label_coordinates_ymin.place(relx=0.7, rely=Y_COORDINATES, relheight=REL_HEIGHT, relwidth=0.05)
		label_coordinates_ymax = tk.Label(self.frame1, text='Max y:')
		label_coordinates_ymax.place(relx=0.85, rely=Y_COORDINATES, relheight=REL_HEIGHT, relwidth=0.05)
		label_size = tk.Label(self.frame1, text='Image size in pixel / 100', anchor='center')
		label_size.place(relx=0.01, rely=Y_SIZE, relheight=REL_HEIGHT, relwidth=0.4)
		label_size_x = tk.Label(self.frame1, text='Width:')
		label_size_x.place(relx=0.42, rely=Y_SIZE, relheight=REL_HEIGHT, relwidth=0.05)
		label_size_y = tk.Label(self.frame1, text='Height:')
		label_size_y.place(relx=0.55, rely=Y_SIZE, relheight=REL_HEIGHT, relwidth=0.05)

	def show_thermo(self):
		self.label_error.config(bg='grey', text='')
		filename = self.entry_file.get()

		if self.variable_type.get() == 'reference':
			type_temp = 'reference'
		else:
			type_temp = 'absolute'

		reference_file = str(self.entry_reference.get())

		self.colorlimit_min.config(bg='white')
		self.colorlimit_max.config(bg='white')
		try:
			colorlimitmin = float(self.colorlimit_min.get())
		except ValueError:
			self.colorlimit_min.config(bg='tomato')
			colorlimitmin = 0
		try:
			colorlimitmax = float(self.colorlimit_max.get())
		except ValueError:
			self.colorlimit_max.config(bg='tomato')
			colorlimitmin = 0
			colorlimitmax = 1

		try:
			cmap = self.colormap_choice.get('active')
		except ValueError:
			cmap = 'jet'

		if self.variable_crop.get() == 'nocrop':
			crop = False
			cropxmin, cropxmax, cropymin, cropymax = 1, 1, 1, 1

		else:
			crop = True
			try:
				cropxmin = float(self.crop_x_min.get())
				self.crop_x_min.config(bg='white')
			except ValueError:
				self.crop_x_min.config(bg='tomato')
				cropxmin, cropxmax, cropymin, cropymax = 1, 2, 1, 2
				crop = False
			try:
				cropxmax = float(self.crop_x_max.get())
				self.crop_x_max.config(bg='white')
			except ValueError:
				self.crop_x_max.config(bg='tomato')
				cropxmin, cropxmax, cropymin, cropymax = 1, 2, 1, 2
				crop = False
			try:
				cropymin = float(self.crop_y_min.get())
				self.crop_y_min.config(bg='white')
			except ValueError:
				self.crop_y_min.config(bg='tomato')
				cropxmin, cropxmax, cropymin, cropymax = 1, 2, 1, 2
				crop = False
			try:
				cropymax = float(self.crop_y_max.get())
				self.crop_y_max.config(bg='white')
			except ValueError:
				self.crop_y_max.config(bg='tomato')
				cropxmin, cropxmax, cropymin, cropymax = 1, 2, 1, 2
				crop = False

		self.size_x.config(bg='white')
		self.size_y.config(bg='white')
		try:
			width = float(self.size_x.get())
		except ValueError:
			width = 10
			self.size_x.config(bg='tomato')
		try:
			height = float(self.size_y.get())
		except ValueError:
			height = 8
			self.size_y.config(bg='tomato')

		therm = Thermogram(imagetype=type_temp,
						   referencefilename=reference_file,
						   colorlimit=[colorlimitmin, colorlimitmax],  # colorlimit
						   colormap=cmap,
						   crop=crop,
						   xlimit=[cropxmin, cropxmax],  # Attention: upper origin (small number, big number)
						   ylimit=[cropymin, cropymax],  # Attention: upper origin (big number, small number)
						   imagesize=[width, height],  # [width / 100, height / 100]
						   filename=filename)

		try:
			therm.show()
		except Exception:
			therm.destroy()
			self.label_error.config(bg='tomato', text='Error: Invalid file name')
			raise ValueError('Invalid file name')


if __name__ == '__main__':

	r = tk.Tk()
	app = ThermoApp(r)
	app.create_menu()
	app.labels()
	r.mainloop()
