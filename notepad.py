import tkinter as tk
from tkinter import filedialog,messagebox
from tkinter import scrolledtext,font

class SimpleTextEditor:
	def __init__(self,root):
		self.root=root
		self.root.title("Text Editor")
		self.filename=None
		self.current_font=tk.StringVar(value="Arial")
		self.text_area=scrolledtext.ScrolledText(self.root,wrap=tk.WORD,undo=True,font=(self.current_font.get(),10))
		self.text_area.pack(expand=True,fill='both')
		self.menu=tk.Menu(self.root)
		self.root.config(menu=self.menu)
		file_menu=tk.Menu(self.menu,tearoff=0)
		file_menu.add_command(label="Open",command=self.open_file)
		file_menu.add_command(label="Save",command=self.save_file)
		file_menu.add_command(label="Save As",command=self.save_as_file)
		file_menu.add_separator()
		file_menu.add_command(label="Exit",command=self.root.quit)
		self.menu.add_cascade(label="File",menu=file_menu)
		view_menu=tk.Menu(self.menu,tearoff=0)
		self.word_wrap=tk.BooleanVar(value=True)
		view_menu.add_checkbutton(label="Word Wrap",onvalue=True,offvalue=False,variable=self.word_wrap,command=self.toggle_word_wrap)
		self.menu.add_cascade(label="View",menu=view_menu)
		font_menu=tk.Menu(self.menu,tearoff=0)
		font_menu.add_radiobutton(label="Arial",variable=self.current_font,value="Arial",command=self.change_font)
		font_menu.add_radiobutton(label="Monospace",variable=self.current_font,value="Courier",command=self.change_font)
		self.menu.add_cascade(label="Font",menu=font_menu)
		format_menu=tk.Menu(self.menu,tearoff=0)
		format_menu.add_command(label="Bold",command=self.make_bold)
		format_menu.add_command(label="Italic",command=self.make_italic)
		self.menu.add_cascade(label="Format",menu=format_menu)
		about_menu = tk.Menu(self.menu,tearoff=0)
		about_menu.add_command(label="About",command=self.about_window)
		self.setup_tags()

	def setup_tags(self):
		bold_font=font.Font(self.text_area,self.text_area.cget("font"))
		bold_font.configure(weight="bold")
		italic_font=font.Font(self.text_area,self.text_area.cget("font"))
		italic_font.configure(slant="italic")
		self.text_area.tag_configure("bold",font=bold_font)
		self.text_area.tag_configure("italic",font=italic_font)

	def toggle_word_wrap(self):
		self.text_area.config(wrap=tk.WORD if self.word_wrap.get() else tk.NONE)

	def change_font(self):
		self.text_area.config(font=(self.current_font.get(),10))
		self.setup_tags()

    
	def make_bold(self):
		try:
			sel=self.text_area.tag_ranges(tk.SEL)
			if sel:
				if "bold" in self.text_area.tag_names(tk.SEL_FIRST):
					self.text_area.tag_remove("bold",*sel)
				else:
					self.text_area.tag_add("bold",*sel)
		except:pass

	def make_italic(self):
		try:
			sel=self.text_area.tag_ranges(tk.SEL)
			if sel:
				if "italic" in self.text_area.tag_names(tk.SEL_FIRST):
					self.text_area.tag_remove("italic",*sel)
				else:
					self.text_area.tag_add("italic",*sel)
		except:pass

	def open_file(self):
		filepath=filedialog.askopenfilename(filetypes=[("Text Files","*.txt"),("All Files","*.*")])
		if not filepath:return
		try:
			with open(filepath,"r",encoding='utf-8') as file:
				content=file.read()
			self.text_area.delete("1.0",tk.END)
			self.text_area.insert(tk.END,content)
			self.filename=filepath
			self.root.title(f"Simple Text Editor - {filepath}")
		except Exception as e:
			messagebox.showerror("Error",f"Failed to open file: {e}")

	def save_file(self):
		if self.filename:
			try:
				with open(self.filename,"w",encoding='utf-8') as file:
					file.write(self.text_area.get("1.0",tk.END))
			except Exception as e:
				messagebox.showerror("Error",f"Failed to save file: {e}")
		else:self.save_as_file()

	def save_as_file(self):
		filepath=filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text Files","*.txt"),("All Files","*.*")])
		if not filepath:return
		try:
			with open(filepath,"w",encoding='utf-8') as file:
				file.write(self.text_area.get("1.0",tk.END))
			self.filename=filepath
			self.root.title(f"Simple Text Editor - {filepath}")
		except Exception as e:
			messagebox.showerror("Error",f"Failed to save file: {e}")

if __name__=="__main__":
	root=tk.Tk()
	editor=SimpleTextEditor(root)
	root.mainloop()
