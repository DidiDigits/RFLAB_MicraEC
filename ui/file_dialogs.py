import tkinter as tk
from tkinter import filedialog


def _select_file(title, filetypes):
	root = tk.Tk()
	root.withdraw()
	root.attributes("-topmost", True)

	file_path = filedialog.askopenfilename(
		title=title,
		filetypes=filetypes
	)

	root.destroy()

	if not file_path:
		raise RuntimeError("No se seleccionó ningún archivo")

	return file_path


def select_s2p(title):
	"""Open file dialog to select a Touchstone S2P file.

	Parameters
	----------
	title : str
		Dialog window title

	Returns
	-------
	str
		Full path to selected file

	Raises
	------
	RuntimeError
		If user cancels the file dialog
	"""
	return _select_file(
		title=title,
		filetypes=[("Touchstone files", "*.s2p"), ("All files", "*.*")]
	)


def select_calkit(title="Seleccionar archivo de calibración"):
	"""Open file dialog to select a calibration kit (.xkt) file.

	Parameters
	----------
	title : str
		Dialog window title

	Returns
	-------
	str
		Full path to selected file

	Raises
	------
	RuntimeError
		If user cancels the file dialog
	"""
	return _select_file(
		title=title,
		filetypes=[("Archivos .xkt", "*.xkt"), ("All files", "*.*")]
	)
