"""
Modern GUI for Image to WebP Converter
Cross-platform compatible interface using CustomTkinter
"""
import os
import sys
import threading
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox
from converter import ImageToWebPConverter


class WebPConverterGUI:
    """Main GUI Application"""
    
    def __init__(self):
        # Initialize main window
        self.window = ctk.CTk()
        self.window.title("Image to WebP Converter")
        self.window.geometry("800x600")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.source_folder = ctk.StringVar()
        self.quality_var = ctk.IntVar(value=85)
        self.lossless_var = ctk.BooleanVar(value=False)
        self.method_var = ctk.IntVar(value=4)
        self.is_converting = False
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="🖼️ Image to WebP Converter",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Source folder selection
        folder_frame = ctk.CTkFrame(main_frame)
        folder_frame.pack(fill="x", pady=(0, 20))
        
        folder_label = ctk.CTkLabel(
            folder_frame,
            text="Select Source Folder:",
            font=ctk.CTkFont(size=14)
        )
        folder_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        folder_select_frame = ctk.CTkFrame(folder_frame, fg_color="transparent")
        folder_select_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.folder_entry = ctk.CTkEntry(
            folder_select_frame,
            textvariable=self.source_folder,
            placeholder_text="Choose a folder containing images...",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = ctk.CTkButton(
            folder_select_frame,
            text="Browse",
            command=self._browse_folder,
            width=100,
            height=40,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        browse_btn.pack(side="right")
        
        # Settings frame
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(fill="x", pady=(0, 20))
        
        settings_label = ctk.CTkLabel(
            settings_frame,
            text="Conversion Settings:",
            font=ctk.CTkFont(size=14)
        )
        settings_label.pack(anchor="w", padx=10, pady=(10, 10))
        
        # Quality slider
        quality_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        quality_frame.pack(fill="x", padx=10, pady=5)
        
        quality_label = ctk.CTkLabel(
            quality_frame,
            text=f"Quality: {self.quality_var.get()}",
            font=ctk.CTkFont(size=12)
        )
        quality_label.pack(anchor="w")
        
        self.quality_slider = ctk.CTkSlider(
            quality_frame,
            from_=1,
            to=100,
            variable=self.quality_var,
            command=lambda v: quality_label.configure(text=f"Quality: {int(v)}")
        )
        self.quality_slider.pack(fill="x", pady=(5, 0))
        
        # Lossless checkbox
        lossless_check = ctk.CTkCheckBox(
            settings_frame,
            text="Lossless Compression (Larger file size, perfect quality)",
            variable=self.lossless_var,
            font=ctk.CTkFont(size=12),
            command=self._toggle_quality
        )
        lossless_check.pack(anchor="w", padx=10, pady=10)
        
        # Method slider
        method_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        method_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        method_label = ctk.CTkLabel(
            method_frame,
            text=f"Compression Level: {self.method_var.get()} (Higher = Better compression, slower)",
            font=ctk.CTkFont(size=12)
        )
        method_label.pack(anchor="w")
        
        method_slider = ctk.CTkSlider(
            method_frame,
            from_=0,
            to=6,
            number_of_steps=6,
            variable=self.method_var,
            command=lambda v: method_label.configure(
                text=f"Compression Level: {int(v)} (Higher = Better compression, slower)"
            )
        )
        method_slider.pack(fill="x", pady=(5, 0))
        
        # Progress section
        self.progress_frame = ctk.CTkFrame(main_frame)
        self.progress_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Progress:",
            font=ctk.CTkFont(size=14)
        )
        progress_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=(0, 10))
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            self.progress_frame,
            text="Ready to convert",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        # Log text area
        self.log_text = ctk.CTkTextbox(
            self.progress_frame,
            height=150,
            font=ctk.CTkFont(size=11, family="Consolas")
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Convert button
        self.convert_btn = ctk.CTkButton(
            main_frame,
            text="🚀 Start Conversion",
            command=self._start_conversion,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.convert_btn.pack(fill="x")
        
        # Info label
        info_label = ctk.CTkLabel(
            main_frame,
            text="Output folder will be created as: [source_folder]_WebP",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info_label.pack(pady=(10, 0))
        
    def _toggle_quality(self):
        """Toggle quality slider based on lossless setting"""
        if self.lossless_var.get():
            self.quality_slider.configure(state="disabled")
        else:
            self.quality_slider.configure(state="normal")
    
    def _browse_folder(self):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory(title="Select Folder with Images")
        if folder:
            self.source_folder.set(folder)
    
    def _log(self, message: str):
        """Add message to log"""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.window.update_idletasks()
    
    def _update_progress(self, message: str, current: int, total: int):
        """Update progress bar and status"""
        if total > 0:
            progress = current / total
            self.progress_bar.set(progress)
            self.status_label.configure(text=f"Processing: {current}/{total} files")
        self._log(message)
    
    def _start_conversion(self):
        """Start the conversion process"""
        if self.is_converting:
            messagebox.showwarning("Warning", "Conversion is already in progress!")
            return
        
        source = self.source_folder.get().strip()
        if not source:
            messagebox.showerror("Error", "Please select a source folder!")
            return
        
        if not os.path.exists(source):
            messagebox.showerror("Error", "Selected folder does not exist!")
            return
        
        # Clear log
        self.log_text.delete("1.0", "end")
        self._log("=" * 60)
        self._log("Starting conversion process...")
        self._log(f"Source folder: {source}")
        self._log(f"Quality: {self.quality_var.get()}")
        self._log(f"Lossless: {self.lossless_var.get()}")
        self._log(f"Compression level: {self.method_var.get()}")
        self._log("=" * 60)
        
        # Disable convert button
        self.is_converting = True
        self.convert_btn.configure(state="disabled", text="Converting...")
        
        # Run conversion in separate thread
        thread = threading.Thread(target=self._convert_thread, args=(source,))
        thread.daemon = True
        thread.start()
    
    def _convert_thread(self, source: str):
        """Conversion thread"""
        try:
            # Create converter
            converter = ImageToWebPConverter(
                quality=self.quality_var.get(),
                lossless=self.lossless_var.get(),
                method=self.method_var.get()
            )
            
            # Convert
            output_folder, total, processed, errors = converter.convert_folder(
                source,
                progress_callback=self._update_progress
            )
            
            # Show results
            self._log("=" * 60)
            self._log(f"Conversion completed!")
            self._log(f"Output folder: {output_folder}")
            self._log(f"Total images found: {total}")
            self._log(f"Successfully converted: {processed}")
            if errors:
                self._log(f"Errors: {len(errors)}")
                for error in errors:
                    self._log(f"  - {error}")
            self._log("=" * 60)
            
            # Show success message
            self.window.after(0, lambda: messagebox.showinfo(
                "Success",
                f"Conversion completed!\n\n"
                f"Processed: {processed}/{total} files\n"
                f"Output: {output_folder}"
            ))
            
        except Exception as e:
            self._log(f"ERROR: {str(e)}")
            self.window.after(0, lambda: messagebox.showerror("Error", str(e)))
        
        finally:
            # Re-enable convert button
            self.is_converting = False
            self.window.after(0, lambda: self.convert_btn.configure(
                state="normal",
                text="🚀 Start Conversion"
            ))
    
    def run(self):
        """Run the application"""
        self.window.mainloop()


def main():
    """Main entry point"""
    app = WebPConverterGUI()
    app.run()


if __name__ == "__main__":
    main()
