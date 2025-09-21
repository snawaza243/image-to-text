import os
import sys
import tempfile
import zipfile
import io
import requests
from tkinter import Tk, Label, Button, Listbox, Scrollbar, filedialog, messagebox, StringVar, Toplevel, Frame
from tkinter.ttk import Progressbar, Style
from PIL import Image
import pytesseract
import subprocess
import threading
import shutil

# Determine if running as a PyInstaller bundle
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class ImageToTextConverter:
    def __init__(self, master):
        self.master = master
        master.title("Image to Text Converter")
        master.geometry("850x750")
        master.minsize(800, 650)
        
        # Configure style
        style = Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = '#f0f8ff'  # Light blue background
        header_color = '#33cccc'
        button_color = '#009999'
        button_hover = '#008888'
        reset_color = '#ff6666'
        reset_hover = '#ff5555'
        accent_color = '#6699cc'
        
        # Configure root window background
        master.configure(bg=bg_color)
        
        # Create main container with padding
        main_container = Frame(master, bg=bg_color, padx=20, pady=15)
        main_container.pack(fill='both', expand=True)
        
        # Hero Header
        self.hero_label = Label(main_container, text="Image to Text Converter", 
                               font=('Helvetica', 18, 'bold'), bg=header_color, 
                               fg='white', pady=15, relief='raised')
        self.hero_label.pack(fill='x', pady=(0, 20))
        
        # Create frames for better organization
        folder_frame = Frame(main_container, bg=bg_color)
        folder_frame.pack(fill='x', pady=5)
        
        output_frame = Frame(main_container, bg=bg_color)
        output_frame.pack(fill='x', pady=5)
        
        button_frame = Frame(main_container, bg=bg_color)
        button_frame.pack(fill='x', pady=10)
        
        listbox_frame = Frame(main_container, bg=bg_color)
        listbox_frame.pack(fill='both', expand=True, pady=10)
        
        progress_frame = Frame(main_container, bg=bg_color)
        progress_frame.pack(fill='x', pady=10)
        
        bottom_button_frame = Frame(main_container, bg=bg_color)
        bottom_button_frame.pack(fill='x', pady=10)
        
        # Folder selection
        self.label_folder = Label(folder_frame, text="Image Folder:", bg=bg_color, 
                                 font=('Helvetica', 10, 'bold'))
        self.label_folder.pack(anchor='w')
        
        self.folder_path_var = StringVar()
        self.folder_path_label = Label(folder_frame, textvariable=self.folder_path_var, 
                                      bg=bg_color, fg='#555555', wraplength=600, justify='left')
        self.folder_path_label.pack(anchor='w', fill='x')
        
        # Output file selection
        self.label_output = Label(output_frame, text="Output Text File:", bg=bg_color, 
                                 font=('Helvetica', 10, 'bold'))
        self.label_output.pack(anchor='w')
        
        self.output_path_var = StringVar()
        self.output_path_label = Label(output_frame, textvariable=self.output_path_var, 
                                      bg=bg_color, fg='#555555', wraplength=600, justify='left')
        self.output_path_label.pack(anchor='w', fill='x')
        
        # Buttons
        self.select_folder_button = Button(button_frame, text="Select Folder", 
                                          command=self.select_folder, bg=button_color, 
                                          fg='white', font=('Helvetica', 9, 'bold'),
                                          padx=12, pady=5, cursor='hand2')
        self.select_folder_button.pack(side='left', padx=5)
        
        self.select_output_button = Button(button_frame, text="Select Output File", 
                                          command=self.select_output, bg=button_color, 
                                          fg='white', font=('Helvetica', 9, 'bold'),
                                          padx=12, pady=5, cursor='hand2')
        self.select_output_button.pack(side='left', padx=5)
        
        self.convert_button = Button(button_frame, text="Convert", 
                                    command=self.start_conversion, bg=button_color, 
                                    fg='white', font=('Helvetica', 9, 'bold'),
                                    padx=12, pady=5, cursor='hand2')
        self.convert_button.pack(side='left', padx=5)
        
        # Listboxes with scrollbars
        listbox_container = Frame(listbox_frame, bg=bg_color)
        listbox_container.pack(fill='both', expand=True)
        
        # Selected images
        selected_frame = Frame(listbox_container, bg=bg_color)
        selected_frame.pack(fill='both', expand=True, side='left', padx=(0, 10))
        
        self.selected_images_label = Label(selected_frame, text="Selected Images:", 
                                          bg=bg_color, font=('Helvetica', 10, 'bold'))
        self.selected_images_label.pack(anchor='w')
        
        selected_listbox_frame = Frame(selected_frame)
        selected_listbox_frame.pack(fill='both', expand=True)
        
        self.selected_images_listbox = Listbox(selected_listbox_frame, selectmode="multiple", 
                                              height=6, font=('Helvetica', 9))
        self.selected_images_listbox.pack(side='left', fill='both', expand=True)
        
        selected_scrollbar = Scrollbar(selected_listbox_frame, orient="vertical")
        selected_scrollbar.pack(side='right', fill='y')
        
        self.selected_images_listbox.config(yscrollcommand=selected_scrollbar.set)
        selected_scrollbar.config(command=self.selected_images_listbox.yview)
        
        # Converted images
        converted_frame = Frame(listbox_container, bg=bg_color)
        converted_frame.pack(fill='both', expand=True, side='right', padx=(10, 0))
        
        self.converted_images_label = Label(converted_frame, text="Converted Images:", 
                                           bg=bg_color, font=('Helvetica', 10, 'bold'))
        self.converted_images_label.pack(anchor='w')
        
        converted_listbox_frame = Frame(converted_frame)
        converted_listbox_frame.pack(fill='both', expand=True)
        
        self.converted_images_listbox = Listbox(converted_listbox_frame, height=6, 
                                               font=('Helvetica', 9))
        self.converted_images_listbox.pack(side='left', fill='both', expand=True)
        
        converted_scrollbar = Scrollbar(converted_listbox_frame, orient="vertical")
        converted_scrollbar.pack(side='right', fill='y')
        
        self.converted_images_listbox.config(yscrollcommand=converted_scrollbar.set)
        converted_scrollbar.config(command=self.converted_images_listbox.yview)
        
        # Progress bar
        self.progress_label = Label(progress_frame, text="Progress:", bg=bg_color, 
                                   font=('Helvetica', 10, 'bold'))
        self.progress_label.pack(anchor='w')
        
        self.progress_bar = Progressbar(progress_frame, orient="horizontal", 
                                       length=300, mode="determinate")
        self.progress_bar.pack(fill='x', pady=5)
        
        # Status label
        self.status_var = StringVar()
        self.status_var.set("Ready")
        self.status_label = Label(progress_frame, textvariable=self.status_var, 
                                 bg=bg_color, fg='#555555')
        self.status_label.pack(anchor='w')
        
        # Bottom buttons
        self.reset_selected_button = Button(bottom_button_frame, text="Reset Selected List", 
                                           command=self.reset_selected_list, bg=reset_color, 
                                           fg='white', font=('Helvetica', 9, 'bold'),
                                           padx=12, pady=5, cursor='hand2')
        self.reset_selected_button.pack(side='left', padx=5)
        
        self.reset_converted_button = Button(bottom_button_frame, text="Reset Converted List", 
                                            command=self.reset_converted_list, bg=reset_color, 
                                            fg='white', font=('Helvetica', 9, 'bold'),
                                            padx=12, pady=5, cursor='hand2')
        self.reset_converted_button.pack(side='left', padx=5)
        
        self.open_text_file_button = Button(bottom_button_frame, text="Open Text File", 
                                           command=self.open_text_file, bg=button_color, 
                                           fg='white', font=('Helvetica', 9, 'bold'),
                                           padx=12, pady=5, cursor='hand2')
        self.open_text_file_button.pack(side='left', padx=5)
        
        # Info and About buttons
        self.info_button = Button(bottom_button_frame, text="Info", 
                                 command=self.show_info, bg=accent_color, 
                                 fg='white', font=('Helvetica', 9, 'bold'),
                                 padx=12, pady=5, cursor='hand2')
        self.info_button.pack(side='right', padx=5)
        
        self.about_button = Button(bottom_button_frame, text="About", 
                                  command=self.show_about, bg=accent_color, 
                                  fg='white', font=('Helvetica', 9, 'bold'),
                                  padx=12, pady=5, cursor='hand2')
        self.about_button.pack(side='right', padx=5)
        
        # Close button
        self.close_button = Button(bottom_button_frame, text="Close", 
                                  command=self.master.destroy, bg=reset_color, 
                                  fg='white', font=('Helvetica', 9, 'bold'),
                                  padx=12, pady=5, cursor='hand2')
        self.close_button.pack(side='right', padx=5)
        
        # Add hover effects
        buttons = [self.select_folder_button, self.select_output_button, self.convert_button,
                  self.reset_selected_button, self.reset_converted_button, self.open_text_file_button,
                  self.info_button, self.about_button, self.close_button]
        
        for button in buttons:
            if button.cget('bg') == button_color:
                self.add_hover_effect(button, button_color, button_hover)
            elif button.cget('bg') == reset_color:
                self.add_hover_effect(button, reset_color, reset_hover)
            else:
                self.add_hover_effect(button, accent_color, '#5588bb')
        
        # Initialize Tesseract
        self.tesseract_path = None
        self.setup_tesseract()
        
    def add_hover_effect(self, button, color, hover_color):
        def on_enter(e):
            button.config(bg=hover_color)
        
        def on_leave(e):
            button.config(bg=color)
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
    def setup_tesseract(self):
        """Set up Tesseract OCR from embedded resources"""
        try:
            # First, try to use existing Tesseract installation
            existing_path = self.find_tesseract()
            if existing_path and os.path.isfile(existing_path):
                self.tesseract_path = existing_path
                pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
                self.status_var.set("Using system Tesseract OCR")
                return
            
            # If not found, try to use embedded Tesseract
            app_dir = os.path.dirname(os.path.abspath(__file__))
            embedded_tesseract = resource_path('Tesseract-OCR/tesseract.exe')
            
            if os.path.isfile(embedded_tesseract):
                self.tesseract_path = embedded_tesseract
                pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
                self.status_var.set("Using embedded Tesseract OCR")
                return
                
            # If still not found, show error
            self.status_var.set("Tesseract OCR not found. Please install it.")
            messagebox.showerror("Error", 
                "Tesseract OCR is required but not found.\n\n"
                "Please install Tesseract OCR from:\n"
                "https://github.com/UB-Mannheim/tesseract/wiki\n\n"
                "Then restart this application.")
                
        except Exception as e:
            self.status_var.set(f"Tesseract setup error: {str(e)}")
            messagebox.showerror("Error", f"Failed to setup Tesseract OCR: {str(e)}")
    
    def find_tesseract(self):
        """Try to find Tesseract OCR executable in common locations"""
        possible_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            resource_path('Tesseract-OCR/tesseract.exe'),
            'tesseract'  # If it's in PATH
        ]
        
        for path in possible_paths:
            if os.path.isfile(path):
                return path
                
        return None

    def select_folder(self):
        self.image_folder = filedialog.askdirectory()
        if self.image_folder:
            self.folder_path_var.set(f"Selected: {self.image_folder}")

            # Clear previous selections
            self.selected_images_listbox.delete(0, 'end')

            # Display selected images in the listbox
            for filename in os.listdir(self.image_folder):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                    self.selected_images_listbox.insert('end', filename)

    def select_output(self):
        self.output_file = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if self.output_file:
            self.output_path_var.set(f"Output: {self.output_file}")

    def start_conversion(self):
        """Start conversion in a separate thread to keep UI responsive"""
        if not self.tesseract_path or not os.path.isfile(self.tesseract_path):
            messagebox.showerror("Error", "Tesseract OCR is not available. Please install it first.")
            return
            
        if not hasattr(self, 'image_folder') or not self.image_folder:
            messagebox.showwarning("Warning", "Please select an image folder first.")
            return
            
        if not hasattr(self, 'output_file') or not self.output_file:
            messagebox.showwarning("Warning", "Please select an output text file first.")
            return
            
        # Disable buttons during conversion
        self.set_buttons_state('disabled')
        
        # Start conversion in a separate thread
        thread = threading.Thread(target=self.convert_images)
        thread.daemon = True
        thread.start()

    def convert_images(self):
        try:
            total_images = self.selected_images_listbox.size()
            if total_images == 0:
                self.master.after(0, lambda: messagebox.showwarning("Warning", "No images found in the selected folder."))
                return
                
            self.master.after(0, lambda: self.progress_bar.config(maximum=total_images))
            self.master.after(0, lambda: self.progress_bar.config(value=0))
            self.master.after(0, lambda: self.status_var.set("Starting conversion..."))

            # Clear the output file at the start
            try:
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    f.write("Image to Text Conversion Results\n")
                    f.write("=" * 50 + "\n\n")
            except Exception as e:
                self.master.after(0, lambda: messagebox.showerror("Error", f"Cannot create output file: {str(e)}"))
                return

            for i in range(total_images):
                filename = self.selected_images_listbox.get(i)
                image_path = os.path.join(self.image_folder, filename)
                
                # Update status
                self.master.after(0, lambda f=filename: self.status_var.set(f"Processing: {f}"))
                
                try:
                    text = self.image_to_text(image_path)
                    
                    # Write the extracted text to the output file
                    with open(self.output_file, 'a', encoding='utf-8') as output_file:
                        output_file.write(f"--- Text from {filename} ---\n")
                        output_file.write(text + '\n\n')
                    
                    # Update converted images listbox
                    self.master.after(0, lambda f=filename: self.converted_images_listbox.insert('end', f))
                    
                except Exception as e:
                    # Write error to output file
                    with open(self.output_file, 'a', encoding='utf-8') as output_file:
                        output_file.write(f"--- Error processing {filename} ---\n")
                        output_file.write(f"Error: {str(e)}\n\n")
                    
                    # Still add to converted list but mark as error
                    self.master.after(0, lambda f=filename: self.converted_images_listbox.insert('end', f"{filename} (Error)"))

                # Update progress bar
                self.master.after(0, lambda v=i+1: self.progress_bar.config(value=v))

            # Display notification upon completion
            self.master.after(0, lambda: messagebox.showinfo("Conversion Complete", "Text extraction from images is complete!"))
            self.master.after(0, lambda: self.status_var.set("Conversion complete"))
            
        except Exception as e:
            self.master.after(0, lambda: messagebox.showerror("Error", f"Unexpected error during conversion: {str(e)}"))
            self.master.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
        
        finally:
            # Re-enable buttons
            self.master.after(0, lambda: self.set_buttons_state('normal'))

    def set_buttons_state(self, state):
        """Enable or disable all buttons"""
        buttons = [
            self.select_folder_button, self.select_output_button, self.convert_button,
            self.reset_selected_button, self.reset_converted_button, self.open_text_file_button,
            self.info_button, self.about_button, self.close_button
        ]
        
        for button in buttons:
            button.config(state=state)

    def image_to_text(self, image_path):
        """Convert image to text with error handling"""
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text if text.strip() else "No text detected in the image."
        except Exception as e:
            raise Exception(f"Failed to process image: {str(e)}")

    def reset_selected_list(self):
        self.selected_images_listbox.delete(0, 'end')

    def reset_converted_list(self):
        self.converted_images_listbox.delete(0, 'end')

    def open_text_file(self):
        if hasattr(self, 'output_file') and self.output_file:
            try:
                if os.path.exists(self.output_file):
                    if sys.platform == "win32":
                        os.startfile(self.output_file)
                    else:
                        opener = "open" if sys.platform == "darwin" else "xdg-open"
                        subprocess.call([opener, self.output_file])
                else:
                    messagebox.showwarning("Warning", "The output file doesn't exist yet. Please convert images first.")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to open the text file.\nError: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please select the output text file first.")

    def show_info(self):
        info_text = (
            "Image to Text Converter\n\n"
            "This application allows you to convert text from multiple images using OCR.\n\n"
            "How to use:\n"
            "1. Click 'Select Folder' to choose the folder containing your images.\n"
            "2. Click 'Select Output File' to choose the output text file.\n"
            "3. Click 'Convert' to start the conversion process.\n"
            "4. The progress bar will show the status of the conversion.\n"
            "5. Once the conversion is complete, you can open the extracted text file using 'Open Text File'.\n\n"
            "Requirements:\n"
            "1. Tesseract OCR must be installed on your system or embedded with this application.\n"
            "2. Images should be in common formats such as PNG, JPG, JPEG, or GIF."
        )

        info_window = Toplevel(self.master)
        info_window.title("Information")
        info_window.geometry("500x400")
        info_window.configure(bg='#f0f8ff')
        info_label = Label(info_window, text=info_text, padx=20, pady=20, justify='left', bg='#f0f8ff')
        info_label.pack()

    def show_about(self):
        about_text = (
            "About Image to Text Converter\n\n"
            "Version: 2.0\n"
            "Developed by: IndianTechnoEra\n\n"
            "Contact:\n"
            "Email: indiantechnoera@gmail.com\n"
            "Website: https://www.indiantechnoera.in\n\n"
            "This application includes Tesseract OCR engine."
        )

        about_window = Toplevel(self.master)
        about_window.title("About")
        about_window.geometry("400x300")
        about_window.configure(bg='#f0f8ff')
        about_label = Label(about_window, text=about_text, padx=20, pady=20, justify='left', bg='#f0f8ff')
        about_label.pack()

if __name__ == "__main__":
    root = Tk()
    app = ImageToTextConverter(root)
    root.mainloop()