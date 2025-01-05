import tkinter as tk
from tkinter import ttk, filedialog
from typing import Optional, Callable
import zipfile
import io
import os

# Constants
SUPPORTED_FORMATS = {
    'images': ['.jpg', '.jpeg', '.png'],
    'documents': ['.txt', '.md', '.json', '.pdf'],
    'archives': ['.zip'],
    'video': ['.mp4'],
    'audio': ['.mp3', '.wav']
}

FILETYPES_DIALOG = [
    ("All supported files", "*.jpg *.jpeg *.png *.txt *.md *.json *.zip *.pdf *.mp4 *.mp3 *.wav"),
    ("Images", "*.jpg *.jpeg *.png"),
    ("Documents", "*.txt *.md *.json *.pdf"),
    ("Video", "*.mp4"),
    ("Audio", "*.mp3 *.wav"),
    ("Archives", "*.zip"),
    ("All files", "*.*")
]

def get_file_extension(filename: str) -> str:
    """Get the file extension from a filename."""
    return os.path.splitext(filename)[1].lower()

def get_file_size(data: bytes) -> str:
    """Convert bytes to human-readable file size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if len(data) < 1024:
            return f"{len(data):.1f} {unit}"
        data = data[:len(data)//2] + data[len(data)//2:]
    return f"{len(data):.1f} TB"

class FileCompressor:
    """Handles file compression operations."""
    
    def __init__(self):
        self.supported_types = SUPPORTED_FORMATS
    
    def compress_file(self, file_data: bytes, filename: str) -> tuple[bytes, str]:
        """Compress the given file data based on its type."""
        output = io.BytesIO()
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr(filename, file_data)
        
        compressed_data = output.getvalue()
        return compressed_data, f"{filename}.zip"

    def is_supported_type(self, filename: str) -> bool:
        """Check if the file type is supported for compression."""
        ext = get_file_extension(filename)
        return any(ext in types for types in self.supported_types.values())

class CompressorUI:
    """Handles the graphical user interface."""
    
    def __init__(self, master, on_file_selected: Callable[[str], None]):
        self.master = master
        self.on_file_selected = on_file_selected
        self.setup_window()
        self.create_styles()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window."""
        self.master.title("File Compressor")
        self.master.geometry("500x600")
        self.master.configure(bg='#f0f0f0')
        
    def create_styles(self):
        """Create custom styles for widgets."""
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#f0f0f0')
        style.configure('Custom.TButton', 
                       padding=10, 
                       font=('Helvetica', 10))
        style.configure('Title.TLabel',
                       font=('Helvetica', 24, 'bold'),
                       background='#f0f0f0',
                       foreground='#333333')
        style.configure('Info.TLabel',
                       font=('Helvetica', 10),
                       background='#f0f0f0',
                       foreground='#666666')
        
    def create_widgets(self):
        """Create and arrange GUI elements."""
        # Main container
        self.main_frame = ttk.Frame(self.master, style='Custom.TFrame', padding="20")
        self.main_frame.pack(expand=True, fill='both')
        
        # Title
        title = ttk.Label(
            self.main_frame,
            text="File Compressor",
            style='Title.TLabel'
        )
        title.pack(pady=(0, 20))
        
        # Drop zone frame
        self.drop_frame = ttk.Frame(
            self.main_frame,
            style='Custom.TFrame',
            padding="20"
        )
        self.drop_frame.pack(fill='x', pady=10)
        
        self.drop_label = ttk.Label(
            self.drop_frame,
            text="Click to select a file",
            style='Info.TLabel'
        )
        self.drop_label.pack(pady=40)
        
        # Progress frame
        self.progress_frame = ttk.Frame(
            self.main_frame,
            style='Custom.TFrame'
        )
        self.progress_frame.pack(fill='x', pady=20)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=300
        )
        
        self.progress_label = ttk.Label(
            self.progress_frame,
            text="",
            style='Info.TLabel'
        )
        
        # Status label
        self.status_label = ttk.Label(
            self.main_frame,
            text="",
            wraplength=400,
            justify='center',
            style='Info.TLabel'
        )
        self.status_label.pack(pady=10)
        
        # Select file button
        self.select_btn = ttk.Button(
            self.main_frame,
            text="Select File",
            style='Custom.TButton',
            command=self.on_select_file
        )
        self.select_btn.pack(pady=10)
        
        # Bind click event to the drop frame
        self.drop_frame.bind('<Button-1>', lambda e: self.on_select_file())
        self.drop_label.bind('<Button-1>', lambda e: self.on_select_file())
        
        # Format info
        self.create_format_info()
    
    def create_format_info(self):
        """Create the supported formats information section."""
        formats_frame = ttk.Frame(
            self.main_frame,
            style='Custom.TFrame'
        )
        formats_frame.pack(fill='x', pady=20)
        
        formats_title = ttk.Label(
            formats_frame,
            text="Supported Formats",
            font=('Helvetica', 14, 'bold'),
            style='Info.TLabel'
        )
        formats_title.pack(pady=(0, 10))
        
        for category, extensions in SUPPORTED_FORMATS.items():
            format_text = f"• {category.title()}: {', '.join(ext[1:].upper() for ext in extensions)}"
            format_label = ttk.Label(
                formats_frame,
                text=format_text,
                style='Info.TLabel'
            )
            format_label.pack(anchor='w')
    
    def on_select_file(self):
        """Handle file selection via button."""
        filename = filedialog.askopenfilename(
            title="Select file to compress",
            filetypes=FILETYPES_DIALOG
        )
        if filename:
            self.on_file_selected(filename)
    
    def show_progress(self):
        """Show progress bar and label."""
        self.progress_bar.pack(pady=(0, 5))
        self.progress_label.pack()
        
    def hide_progress(self):
        """Hide progress bar and label."""
        self.progress_bar.pack_forget()
        self.progress_label.pack_forget()
    
    def update_progress(self, value: int, text: str):
        """Update progress bar and label."""
        self.progress_bar['value'] = value
        self.progress_label['text'] = text
        
    def set_status(self, message: str, is_error: bool = False):
        """Update the status label with a message."""
        self.status_label.config(
            text=message,
            foreground="red" if is_error else "green"
        )

class CompressorApp:
    """Main application class."""
    
    def __init__(self):
        self.window = tk.Tk()
        self.compressor = FileCompressor()
        self.ui = CompressorUI(self.window, self.process_file)
        
    def process_file(self, filename: str):
        """Process the selected file."""
        if not self.compressor.is_supported_type(filename):
            self.ui.set_status("Unsupported file type. Please select a supported file.", True)
            return
            
        try:
            self.ui.show_progress()
            self.ui.update_progress(0, "Reading file...")
            
            # Read the input file
            with open(filename, 'rb') as f:
                file_data = f.read()
            
            original_size = get_file_size(file_data)
            self.ui.update_progress(33, "Compressing...")
            
            # Compress the file
            compressed_data, output_filename = self.compressor.compress_file(
                file_data,
                os.path.basename(filename)
            )
            
            compressed_size = get_file_size(compressed_data)
            self.ui.update_progress(66, "Saving...")
            
            # Save the compressed file
            save_path = filedialog.asksaveasfilename(
                defaultextension=".zip",
                initialfile=output_filename,
                filetypes=[("ZIP files", "*.zip")]
            )
            
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(compressed_data)
                
                self.ui.update_progress(100, "Complete!")
                self.ui.set_status(
                    f"File compressed successfully!\n"
                    f"Original size > Compressed size"
                )

        except Exception as e:
            self.ui.set_status(f"An error occurred: {str(e)}", True)
        finally:
            self.ui.hide_progress()
    
    def run(self):
        """Start the application."""
        self.window.mainloop()

if __name__ == "__main__":
    app = CompressorApp()
    app.run()