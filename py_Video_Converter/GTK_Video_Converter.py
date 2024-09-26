#!/usr/bin/env python3

import ntpath #Getting file name from path

import datetime #Beautifully displaying video length

import threading #Avoiding window hangups

import subprocess #Calling terminal commands

from configobj import ConfigObj #Storing codec information


import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk #GUI Toolkit



class MyWindow(Gtk.Window):
	def __init__(self):
		
		#Set up window
		Gtk.Window.__init__(self, title="FFGUI")
		self.set_default_size(800,600)
		self.set_border_width(6)
		
		#Set up cell renderers
		text_renderer_A = Gtk.CellRendererText()
		
		#Import configuration
		self.config = ConfigObj('codecs.ini')


		#upper_buttons
		self.remove_button = Gtk.Button.new_from_icon_name("list-remove", 1)
		self.remove_button.connect("clicked", self.on_remove_clicked)
		
		self.add_button = Gtk.Button.new_from_icon_name("list-add",1)
		self.add_button.connect("clicked", self.on_add_clicked)
		
		tip = Gtk.Label(label = 'Add videos to convert and compress')
		
		self.about_button = Gtk.Button.new_from_icon_name("help-about",1)
		self.about_button.connect("clicked", self.on_about_clicked)
		
		button_subbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		button_subbox.pack_start(self.add_button, False, False, 0)
		button_subbox.pack_start(self.remove_button, False, False, 0)
		button_subbox.pack_start(tip, True, False, 0)
		button_subbox.pack_end(self.about_button, False, False, 0)
		

		
		
		#video codec settings
		self.video_description = Gtk.Label()
		self.video_description.set_line_wrap(True)
		self.video_description.set_max_width_chars(30)
		video_frame = Gtk.Frame()
		video_frame.add(self.video_description)
		
		self.video_store = Gtk.ListStore(str, str)
		
		self.video_combo = Gtk.ComboBox.new_with_model(self.video_store)
		self.video_combo.connect("changed",
			self.on_video_combo_changed)
		self.video_combo.pack_start(text_renderer_A,True)
		self.video_combo.add_attribute(text_renderer_A, 'text',0)
		
		video_subbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=6)
		label = Gtk.Label(label="Video Codec:")
		video_subbox.pack_start(label, True, True, 0)
		video_subbox.pack_start(self.video_combo, True, True, 0)
		
		self.video_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,18,30,1)

		
		video_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=6)
		video_box.pack_start(video_subbox, False, False, 0)
		video_box.pack_start(video_frame, False, False, 0)
		video_box.pack_start(self.video_scale, False, False, 0)
		
		#audio codec settings
		self.audio_description = Gtk.Label()
		self.audio_description.set_line_wrap(True)
		self.audio_description.set_max_width_chars(30)
		audio_frame = Gtk.Frame()
		audio_frame.add(self.audio_description)
		
		self.audio_store = Gtk.ListStore(str, str)
		
		self.audio_combo = Gtk.ComboBox.new_with_model(self.audio_store)
		self.audio_combo.connect("changed",
			self.on_audio_combo_changed)
		self.audio_combo.pack_start(text_renderer_A,True)
		self.audio_combo.add_attribute(text_renderer_A, 'text',0)
		
		audio_subbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=6)
		label = Gtk.Label(label="Audio Codec(if applicable):")
		audio_subbox.pack_start(label, True, True, 0)
		audio_subbox.pack_start(self.audio_combo, True, True, 0)
		
		self.audio_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,18,30,1)
		
		audio_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=6)
		audio_box.pack_start(audio_subbox, False, False, 0)
		audio_box.pack_start(audio_frame, False, False, 0)
		audio_box.pack_start(self.audio_scale, False, False, 0)
		

		#format settings
		self.format_description = Gtk.Label()
		self.format_description.set_line_wrap(True)
		self.format_description.set_max_width_chars(30)
		format_frame = Gtk.Frame()
		format_frame.add(self.format_description)
		
		self.format_store = Gtk.ListStore(str, str)
			
		for key, value in self.config['formats'].items():
			name = key
			description = value['description']
			self.format_store.append([name, description])
			
		
		self.format_combo = Gtk.ComboBox.new_with_model(self.format_store)
		self.format_combo.connect("changed",
			self.on_format_combo_changed)
		self.format_combo.pack_start(text_renderer_A,True)
		self.format_combo.add_attribute(text_renderer_A, 'text',0)
		self.format_combo.set_active(0)
		

		
		format_subbox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing=6)
		label = Gtk.Label(label="Container Format:")
		format_subbox.pack_start(label, True, True, 0)
		format_subbox.pack_start(self.format_combo, True, True, 0)
		
		self.convert_button = Gtk.Button.new_with_label("Convert")
		self.convert_button.set_sensitive(False)
		self.convert_button.connect('clicked', self.on_convert_button_clicked)
		
		format_box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing=6)
		format_box.pack_start(format_subbox, False, False, 0)
		format_box.pack_start(format_frame, False, False, 0)
		format_box.pack_start(self.convert_button, False, False, 0)
		

		
		
		#tree
		self.store = Gtk.ListStore(str,str,str,str,str)
		
		self.tree = Gtk.TreeView(model=self.store)
		sel=self.tree.get_selection()
		sel.set_mode(Gtk.SelectionMode.MULTIPLE)
		self.tree.set_rubber_banding(True)
		

		columnA = Gtk.TreeViewColumn("Name",text_renderer_A,text=1)
		columnA.set_min_width(50)
		columnA.set_max_width(800)
		columnA.set_resizable(True)
		self.tree.append_column(columnA)
		
		columnB = Gtk.TreeViewColumn("Duration",text_renderer_A,text=2)
		columnB.set_min_width(70)
		columnB.set_max_width(200)
		columnB.set_resizable(True)
		self.tree.append_column(columnB)
		
		columnC = Gtk.TreeViewColumn("Video Codec",text_renderer_A,text=3)
		columnC.set_min_width(94)
		columnC.set_max_width(200)
		columnC.set_resizable(True)
		self.tree.append_column(columnC)

		columnD = Gtk.TreeViewColumn("Audio Codec",text_renderer_A,text=4)
		columnD.set_min_width(94)
		columnD.set_max_width(200)
		columnD.set_resizable(True)
		self.tree.append_column(columnD)
		
		scrollable = Gtk.ScrolledWindow()
		scrollable.set_vexpand(True)
		scrollable.set_hexpand(True)
		scrollable.add(self.tree)
		
		#Separator
		separatorA = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
		separatorB = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
		separatorC = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
		
		#Boxes
		
		setting_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
		setting_box.pack_start(format_box, True, True, 0)
		setting_box.pack_start(separatorA, False, False, 0)
		setting_box.pack_start(video_box, True, True, 0)
		setting_box.pack_start(separatorB, False, False, 0)
		setting_box.pack_start(audio_box, True, True, 0)
		setting_box.pack_start(separatorC, False, False, 0)
		
		main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		main_box.pack_start(button_subbox, False, False, 0)
		main_box.pack_start(scrollable, True, True, 0)
		main_box.pack_start(setting_box, False, False, 0)
		self.add(main_box)
		

		
	def on_remove_clicked(self, button):
		
		selection = self.tree.get_selection()
		model, paths = selection.get_selected_rows()
		for path in reversed(paths):
			itr = model.get_iter(path)
			model.remove(itr)
		if len(self.store) == 0:
			self.convert_button.set_sensitive(False)
			
	
	def on_add_clicked(self, button):
		
		#Create a file chooser dialog
		dialog = Gtk.FileChooserDialog(title="Select videos",
			action= Gtk.FileChooserAction.OPEN,
			select_multiple=True)
		dialog.add_buttons(
			Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
			Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
		
		#Add video only filter
		filter_video = Gtk.FileFilter()
		filter_video.set_name("Video Files")
		filter_video.add_mime_type("video/*")
		dialog.add_filter(filter_video)
		
		#Launch dialog
		response = dialog.run()
		filenames = dialog.get_filenames()
		dialog.destroy()
		if response == Gtk.ResponseType.OK:
			
			for path in filenames:
				
				for row in self.store: #Remove duplicates
					if row[0] == path:
						self.store.remove(row.iter)
				
				directory, name = ntpath.split(path)
				self.store.append([directory+'/',name,'Calculating...','',''])
				
			
			self.add_button.set_sensitive(False)
			self.remove_button.set_sensitive(False)
			thread = threading.Thread(target=self.calculate_videos)
			thread.start()
			
	def calculate_videos(self):
				
		for i in range(len(self.store)):
			row = self.store[i]
			if row[2] == 'Calculating...':
				
				#Get video information for rows with "Calculaintg..."
				
				directory = row[0]
				name = row[1]
				cmd_command = ['ffprobe',
					'-v','error',
					'-show_entries','stream=codec_name:format=duration',
					'-of','default=noprint_wrappers=1',
					directory+name]
				cmd_output = subprocess.check_output(cmd_command)
				cmd_output = list(cmd_output.decode("utf-8").split())
				
				#Put FFprobe output into variables
				codecs = []
				for i in cmd_output:
					if 'codec_name=' in i:
						codecs.append(i.split('=')[1])
					elif 'duration=' in i:
						duration = i.split('=')[1]
				
				
				#Beautify output variables
				duration = int(float(duration.strip('\n')))
				duration = str(datetime.timedelta(seconds=duration))
				if len(codecs)<2:
					codecs.append('none')
				
				
				#Write output variables to rows	
				row[2] = duration
				row[3] = codecs[0]
				row[4] = codecs[1]
		self.add_button.set_sensitive(True)
		self.remove_button.set_sensitive(True)
		self.convert_button.set_sensitive(True)
		
		
	def on_format_combo_changed(self, combo):
		itr = combo.get_active_iter()
		model = combo.get_model()
		chosen = model[itr][0]
		self.audio_store.clear()
		self.video_store.clear()
		
		chosen_description = model[itr][1]
		self.format_description.set_text(chosen_description)

		for name in self.config['formats'][chosen]['common_video_codecs']:
			description = self.config['video_codecs'][name]['description']
			self.video_store.append([name, description])

		for name in self.config['formats'][chosen]['common_audio_codecs']:
			description = self.config['audio_codecs'][name]['description']
			self.audio_store.append([name, description])	


		self.video_combo.set_active(0)
		self.audio_combo.set_active(0)
		
		
	def on_video_combo_changed(self, combo):
		itr = combo.get_active_iter()
		if itr != None:
			model = combo.get_model()
			name = model[itr][0]
			description = model[itr][1]
			self.video_description.set_text(description)
			
			mini, maxi = self.config['video_codecs'][name]['slider_range']
			mini, maxi = map(int, [mini,maxi])
			self.video_scale.clear_marks()
			self.video_scale.set_range(mini,maxi)
			self.video_scale.add_mark(mini,Gtk.PositionType.BOTTOM,"high quality")
			self.video_scale.add_mark(maxi,Gtk.PositionType.BOTTOM,"small file")
		
	def on_audio_combo_changed(self, combo):
		itr = combo.get_active_iter()
		if itr != None:
			model = combo.get_model()
			name = model[itr][0]
			description = model[itr][1]
			self.audio_description.set_text(description)
			
			mini, maxi = self.config['audio_codecs'][name]['slider_range']
			try:
				mini, maxi = map(int, [mini,maxi])
				self.audio_scale.set_digits(0)
			except ValueError:
				mini, maxi = map(float, [mini,maxi])
				self.audio_scale.set_digits(1)
			self.audio_scale.clear_marks()
			self.audio_scale.set_range(mini,maxi)
			self.audio_scale.add_mark(mini,Gtk.PositionType.BOTTOM,"high quality")
			self.audio_scale.add_mark(maxi,Gtk.PositionType.BOTTOM,"small file")	
			
	def on_about_clicked(self, button):
		pass
		
	def on_convert_button_clicked(self, button):
		
		self.remove_button.set_sensitive(False)
		self.convert_button.set_sensitive(False)
		self.convert_button.set_label('Abort')
		
		for video in self.store:
			itr = self.video_combo.get_active_iter()
			model = self.video_combo.get_model()
			video_codec = model[itr][0]
			video_codec = self.config['video_codecs'][video_codec]['ffmpeg_name']
			
			itr = self.audio_combo.get_active_iter()
			model = self.audio_combo.get_model()
			audio_codec = model[itr][0]
			audio_codec = self.config['audio_codecs'][audio_codec]['ffmpeg_name']
			
			itr = self.format_combo.get_active_iter()
			model = self.format_combo.get_model()
			container = '.'+model[itr][0]
			
			crf = str(int(self.video_scale.get_value()))
			try:
				audio_quality = str(int(self.audio_scale.get_value()))
			except ValueError:
				audio_quality = str(self.audio_scale.get_value())
				
			
			video_name = video[1].split('.')[0]
			
			cmd_command = ['ffmpeg',
			'-hide_banner',
			'-loglevel', 'warning',
			'-i', video[0]+video[1],
			'-c:v', video_codec,
			'-c:a', audio_codec,
			'-q:a', audio_quality,
			'-b:v', '0',
			'-crf', crf,
			video[0]+'b-'+video_name+container]
			cmd_output = subprocess.call(cmd_command)
			
		
		
		dialog = Gtk.MessageDialog(
			parent = self,
			message_type = Gtk.MessageType.INFO,
			buttons = Gtk.ButtonsType.OK,
			text = "Finished!",
			secondary_text = "All videos have been converted! ")
		dialog.run()
		dialog.destroy()
		
		self.remove_button.set_sensitive(True)
		self.convert_button.set_sensitive(True)
		self.convert_button.set_label('Convert')
		

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
