import tkinter as tk
from tkinter import filedialog
from create_thermo import Thermogram

# object oriented version of ThermoApp

root = tk.Tk()
root.title('Thermo')
root.geometry('1000x600')


def create_menu():

	menubar = tk.Menu(root)
	menubar.add_command(label='Information', command=lambda: help_window())
	menubar.add_command(label='Exit', command=lambda: root.quit())
	root.config(menu=menubar)


create_menu()


def file_opener():
	file_path = filedialog.askopenfilename(initialdir='/home/moritz/PycharmProjects/Python_Studienarbeit/'
													  'ThermoApp/Daten')
	if file_path:
		entry_file.config(state='normal')
		entry_file.delete(0, tk.END)
		entry_file.insert(0, file_path)


def reference_opener():
	reference_path = filedialog.askopenfilename(initialdir='/home/moritz/PycharmProjects/Python_Studienarbeit/'
													  'ThermoApp/Daten')
	if reference_path:
		entry_reference.config(state='normal')
		entry_reference.delete(0, tk.END)
		entry_reference.insert(0, reference_path)


def help_window():
	help_win = tk.Toplevel(root)
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


def activate_coordinates():
	crop_x_min.config(state='normal', bg='white')
	crop_x_max.config(state='normal', bg='white')
	crop_y_min.config(state='normal', bg='white')
	crop_y_max.config(state='normal', bg='white')


def deactivate_coordinates():
	crop_x_min.config(state='disabled')
	crop_x_max.config(state='disabled')
	crop_y_min.config(state='disabled')
	crop_y_max.config(state='disabled')


def activate_entry_reference():
	browse_reference_button.config(state='normal')
	browse_reference_button.config(bg='lightgreen')
	entry_reference.config(state='normal')


def deactivate_entry_reference():
	browse_reference_button.config(state='disabled')
	browse_reference_button.config(bg='gainsboro')
	entry_reference.config(state='disabled')


frame1 = tk.Frame(root, bg='grey', bd=2)
frame1.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.85)

frame2 = tk.Frame(root, bg='grey', bd=2)
frame2.place(relx=0.01, rely=0.92, relheight=0.07, relwidth=0.98)

rel_height = 0.07
y_filename = 0.01
y_type = 0.12
y_reference = 0.23
y_colorlimit = 0.34
y_colormap = 0.45
y_crop = 0.67
y_coordinates = 0.78
y_size = 0.89


def area_file():

	label_file = tk.Label(frame1, text='Selected file:', anchor='center')
	label_file.place(relx=0.01, rely=y_filename, relheight=rel_height, relwidth=0.14)


area_file()

entry_file = tk.Entry(frame1, state='disabled')
entry_file.place(relx=0.17, rely=y_filename, relheight=rel_height, relwidth=0.67)

browse_file_button = tk.Button(frame1, text='Browse file', bg='lightgreen', command=lambda: file_opener())
browse_file_button.place(relx=0.85, rely=y_filename, relheight=rel_height, relwidth=0.13)


def area_type():

	label_type = tk.Label(frame1, text='Type of temperature representation', anchor='center')
	label_type.place(relx=0.01, rely=y_type, relheight=rel_height, relwidth=0.4)


area_type()

variable_type = tk.StringVar()
type_absolute = tk.Radiobutton(frame1, text='Absolute', variable=variable_type, value='absolute',
							   command=lambda: deactivate_entry_reference())
type_absolute.place(relx=0.42, relheight=rel_height, rely=y_type, relwidth=0.1)
type_reference = tk.Radiobutton(frame1, text='Relative', variable=variable_type, value='reference',
								command=lambda: activate_entry_reference())
type_reference.place(relx=0.55, relheight=rel_height, rely=y_type, relwidth=0.1)
variable_type.set('absolute')


def area_reference():

	label_reference = tk.Label(frame1, text='Reference file:', anchor='center')
	label_reference.place(relx=0.01, rely=y_reference, relheight=rel_height, relwidth=0.14)


area_reference()

entry_reference = tk.Entry(frame1, state='disabled')
entry_reference.place(relx=0.17, rely=y_reference, relheight=rel_height, relwidth=0.67)

browse_reference_button = tk.Button(frame1, text='Browse reference', bg='gainsboro',
									command=lambda: reference_opener(), state='disabled')
browse_reference_button.place(relx=0.85, rely=y_reference, relheight=rel_height, relwidth=0.13)


def area_colorlimit():

	label_colorlimit = tk.Label(frame1, text='Scaling limits of legend', anchor='center')
	label_colorlimit.place(relx=0.01, rely=y_colorlimit, relheight=rel_height, relwidth=0.4)

	label_colorlimit_min = tk.Label(frame1, text='Min:')
	label_colorlimit_min.place(relx=0.42, rely=y_colorlimit, relheight=rel_height, relwidth=0.05)
	label_colorlimit_max = tk.Label(frame1, text='Max:')
	label_colorlimit_max.place(relx=0.55, rely=y_colorlimit, relheight=rel_height, relwidth=0.05)


area_colorlimit()

colorlimit_min = tk.Entry(frame1)
colorlimit_min.place(relx=0.47, relheight=rel_height, rely=y_colorlimit, relwidth=0.05)
colorlimit_max = tk.Entry(frame1)
colorlimit_max.place(relx=0.6, relheight=rel_height, rely=y_colorlimit, relwidth=0.05)


def area_colormap():
	label_colormap = tk.Label(frame1, text='Colormap', anchor='center')
	label_colormap.place(relx=0.01, rely=y_colormap, relheight=rel_height, relwidth=0.4)


area_colormap()

colormap_list = ['jet', 'magma', 'plasma', 'seismic', 'viridis']
variable_colormap = tk.StringVar()
variable_colormap.set(colormap_list)
colormap_choice = tk.Listbox(frame1, selectbackground='lightgreen', listvariable=variable_colormap)
colormap_choice.place(relx=0.42, rely=y_colormap, relheight=0.11 + rel_height, relwidth=0.23)


def area_crop():

	label_crop = tk.Label(frame1, text='Crop image?', anchor='center')
	label_crop.place(relx=0.01, rely=y_crop, relheight=rel_height, relwidth=0.4)


area_crop()

variable_crop = tk.StringVar()
crop_yes = tk.Radiobutton(frame1, text='Yes', variable=variable_crop, value='crop',
						  command=lambda: activate_coordinates())
crop_yes.place(relx=0.42, relheight=rel_height, rely=y_crop, relwidth=0.1)
crop_no = tk.Radiobutton(frame1, text='No', variable=variable_crop, value='nocrop',
						 command=lambda: deactivate_coordinates())
crop_no.place(relx=0.55, relheight=rel_height, rely=y_crop, relwidth=0.1)
variable_crop.set('nocrop')


def area_coordinates():

	label_coordinates = tk.Label(frame1, text='Coordinates for cropping', anchor='center')
	label_coordinates.place(relx=0.01, rely=y_coordinates, relheight=rel_height, relwidth=0.4)

	label_coordiantes_xmin = tk.Label(frame1, text='Min x:')
	label_coordiantes_xmin.place(relx=0.42, rely=y_coordinates, relheight=rel_height, relwidth=0.05)
	label_coordinates_xmax = tk.Label(frame1, text='Max x:')
	label_coordinates_xmax.place(relx=0.55, rely=y_coordinates, relheight=rel_height, relwidth=0.05)
	label_coordinates_ymin = tk.Label(frame1, text='Min y:')
	label_coordinates_ymin.place(relx=0.7, rely=y_coordinates, relheight=rel_height, relwidth=0.05)
	label_coordinates_ymax = tk.Label(frame1, text='Max y:')
	label_coordinates_ymax.place(relx=0.85, rely=y_coordinates, relheight=rel_height, relwidth=0.05)


area_coordinates()

state_crop = 'disabled'

crop_x_min = tk.Entry(frame1, state=state_crop)
crop_x_min.place(relx=0.47, relheight=rel_height, rely=y_coordinates, relwidth=0.05)
crop_x_max = tk.Entry(frame1, state=state_crop)
crop_x_max.place(relx=0.6, relheight=rel_height, rely=y_coordinates, relwidth=0.05)
crop_y_min = tk.Entry(frame1, state=state_crop)
crop_y_min.place(relx=0.75, relheight=rel_height, rely=y_coordinates, relwidth=0.05)
crop_y_max = tk.Entry(frame1, state=state_crop)
crop_y_max.place(relx=0.9, relheight=rel_height, rely=y_coordinates, relwidth=0.05)


def area_size():

	label_size = tk.Label(frame1, text='Image size in pixel / 100', anchor='center')
	label_size.place(relx=0.01, rely=y_size, relheight=rel_height, relwidth=0.4)

	label_size_x = tk.Label(frame1, text='Width:')
	label_size_x.place(relx=0.42, rely=y_size, relheight=rel_height, relwidth=0.05)
	label_size_y = tk.Label(frame1, text='Height:')
	label_size_y.place(relx=0.55, rely=y_size, relheight=rel_height, relwidth=0.05)


area_size()

size_x = tk.Entry(frame1)
size_x.insert(0, '10')
size_x.place(relx=0.47, relheight=rel_height, rely=y_size, relwidth=0.05)
size_y = tk.Entry(frame1)
size_y.insert(0, '8')
size_y.place(relx=0.6, relheight=rel_height, rely=y_size, relwidth=0.05)

show_thermogram_button = tk.Button(frame2, text='Show thermogram', command=lambda: show_thermo(), state='normal')
show_thermogram_button.place(relx=0.84, rely=0.1, relwidth=0.15, relheight=0.8)

label_error = tk.Label(frame2, anchor='w', text='', fg='black', bg='grey', font='bold')
label_error.place(relx=0.01, rely=0.1, relheight=0.8, relwidth=0.51)


def show_thermo():
	label_error.config(bg='grey', text='')
	filename = entry_file.get()

	if variable_type.get() == 'reference':
		type_temp = 'reference'
	else:
		type_temp = 'absolute'

	reference_file = str(entry_reference.get())

	colorlimit_min.config(bg='white')
	colorlimit_max.config(bg='white')
	try:
		colorlimitmin = float(colorlimit_min.get())
	except ValueError:
		colorlimit_min.config(bg='tomato')
		colorlimitmin = 0
	try:
		colorlimitmax = float(colorlimit_max.get())
	except ValueError:
		colorlimit_max.config(bg='tomato')
		colorlimitmin = 0
		colorlimitmax = 1

	try:
		cmap = colormap_choice.get('active')
	except ValueError:
		cmap = 'jet'

	if variable_crop.get() == 'nocrop':
		crop = False
		cropxmin, cropxmax, cropymin, cropymax = 1, 1, 1, 1

	else:
		crop = True
		try:
			cropxmin = float(crop_x_min.get())
			crop_x_min.config(bg='white')
		except ValueError:
			crop_x_min.config(bg='tomato')
			cropxmin, cropxmax, cropymin, cropymax = 1, 2, 1, 2
			crop = False
		try:
			cropxmax = float(crop_x_max.get())
			crop_x_max.config(bg='white')
		except ValueError:
			crop_x_max.config(bg='tomato')
			cropxmin, cropxmax, cropymin, cropymax = 1, 2, 1, 2
			crop = False
		try:
			cropymin = float(crop_y_min.get())
			crop_y_min.config(bg='white')
		except ValueError:
			crop_y_min.config(bg='tomato')
			cropxmin, cropxmax, cropymin, cropymax = 1, 2, 1, 2
			crop = False
		try:
			cropymax = float(crop_y_max.get())
			crop_y_max.config(bg='white')
		except ValueError:
			crop_y_max.config(bg='tomato')
			cropxmin, cropxmax, cropymin, cropymax = 1, 2, 1, 2
			crop = False

	size_x.config(bg='white')
	size_y.config(bg='white')
	try:
		width = float(size_x.get())
	except ValueError:
		width = 10
		size_x.config(bg='tomato')
	try:
		height = float(size_y.get())
	except ValueError:
		height = 8
		size_y.config(bg='tomato')

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
		label_error.config(bg='tomato', text='Error: Invalid file name')
		raise ValueError('Invalid file name')


root.mainloop()
