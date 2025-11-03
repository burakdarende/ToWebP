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
        self.window.geometry("850x860")
        self.window.resizable(False, False)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.source_folder = ctk.StringVar()
        self.source_file = ctk.StringVar()
        self.quality_var = ctk.IntVar(value=85)
        self.lossless_var = ctk.BooleanVar(value=False)
        self.method_var = ctk.IntVar(value=4)
        self.resize_enabled = ctk.BooleanVar(value=False)
        self.resize_width = ctk.StringVar(value="")
        self.is_converting = False
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="🖼️ Image to WebP Converter",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 15))
        
        # Source folder selection
        folder_frame = ctk.CTkFrame(main_frame)
        folder_frame.pack(fill="x", pady=(0, 8))
        
        folder_label = ctk.CTkLabel(
            folder_frame,
            text="Select Source Folder:",
            font=ctk.CTkFont(size=13)
        )
        folder_label.pack(anchor="w", padx=10, pady=(8, 4))
        
        folder_select_frame = ctk.CTkFrame(folder_frame, fg_color="transparent")
        folder_select_frame.pack(fill="x", padx=10, pady=(0, 8))
        
        self.folder_entry = ctk.CTkEntry(
            folder_select_frame,
            textvariable=self.source_folder,
            placeholder_text="Choose a folder containing images...",
            height=35,
            font=ctk.CTkFont(size=11)
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        browse_folder_btn = ctk.CTkButton(
            folder_select_frame,
            text="Browse",
            command=self._browse_folder,
            width=90,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        browse_folder_btn.pack(side="right")
        
        # OR separator
        or_label = ctk.CTkLabel(
            main_frame,
            text="- OR -",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        or_label.pack(pady=4)
        
        # Single file selection
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", pady=(0, 12))
        
        file_label = ctk.CTkLabel(
            file_frame,
            text="Select Single File:",
            font=ctk.CTkFont(size=13)
        )
        file_label.pack(anchor="w", padx=10, pady=(8, 4))
        
        file_select_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_select_frame.pack(fill="x", padx=10, pady=(0, 8))
        
        self.file_entry = ctk.CTkEntry(
            file_select_frame,
            textvariable=self.source_file,
            placeholder_text="Choose a single image file...",
            height=35,
            font=ctk.CTkFont(size=11)
        )
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        browse_file_btn = ctk.CTkButton(
            file_select_frame,
            text="Browse",
            command=self._browse_file,
            width=90,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        browse_file_btn.pack(side="right")
        
        # Settings frame
        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(fill="x", pady=(0, 12))
        
        settings_label = ctk.CTkLabel(
            settings_frame,
            text="Conversion Settings:",
            font=ctk.CTkFont(size=13)
        )
        settings_label.pack(anchor="w", padx=10, pady=(8, 8))
        
        # Quality slider
        quality_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        quality_frame.pack(fill="x", padx=10, pady=4)
        
        quality_label = ctk.CTkLabel(
            quality_frame,
            text=f"Quality: {self.quality_var.get()}",
            font=ctk.CTkFont(size=11)
        )
        quality_label.pack(anchor="w")
        
        self.quality_slider = ctk.CTkSlider(
            quality_frame,
            from_=1,
            to=100,
            variable=self.quality_var,
            command=lambda v: quality_label.configure(text=f"Quality: {int(v)}")
        )
        self.quality_slider.pack(fill="x", pady=(4, 0))
        
        # Lossless checkbox
        lossless_check = ctk.CTkCheckBox(
            settings_frame,
            text="Lossless Compression (Larger file size, perfect quality)",
            variable=self.lossless_var,
            font=ctk.CTkFont(size=11),
            command=self._toggle_quality
        )
        lossless_check.pack(anchor="w", padx=10, pady=8)
        
        # Method slider
        method_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        method_frame.pack(fill="x", padx=10, pady=(4, 8))
        
        method_label = ctk.CTkLabel(
            method_frame,
            text=f"Compression Level: {self.method_var.get()} (Higher = Better compression, slower)",
            font=ctk.CTkFont(size=11)
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
        method_slider.pack(fill="x", pady=(4, 0))
        
        # Resize option
        resize_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        resize_frame.pack(fill="x", padx=10, pady=(8, 8))
        
        resize_check = ctk.CTkCheckBox(
            resize_frame,
            text="Resize Images (Proportional)",
            variable=self.resize_enabled,
            font=ctk.CTkFont(size=11),
            command=self._toggle_resize
        )
        resize_check.pack(anchor="w")
        
        resize_input_frame = ctk.CTkFrame(resize_frame, fg_color="transparent")
        resize_input_frame.pack(fill="x", pady=(4, 0))
        
        resize_width_label = ctk.CTkLabel(
            resize_input_frame,
            text="Target Width (px):",
            font=ctk.CTkFont(size=11)
        )
        resize_width_label.pack(side="left", padx=(0, 8))
        
        self.resize_entry = ctk.CTkEntry(
            resize_input_frame,
            textvariable=self.resize_width,
            placeholder_text="e.g., 1920, 1200, 800...",
            width=200,
            height=30,
            font=ctk.CTkFont(size=11),
            state="disabled"
        )
        self.resize_entry.pack(side="left")
        
        resize_info_label = ctk.CTkLabel(
            resize_input_frame,
            text="(Height will be auto-calculated)",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        resize_info_label.pack(side="left", padx=(8, 0))
        
        # Progress section
        self.progress_frame = ctk.CTkFrame(main_frame)
        self.progress_frame.pack(fill="both", expand=True, pady=(0, 12))
        
        progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Progress:",
            font=ctk.CTkFont(size=13)
        )
        progress_label.pack(anchor="w", padx=10, pady=(8, 4))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=(0, 8))
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            self.progress_frame,
            text="Ready to convert",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(anchor="w", padx=10, pady=(0, 4))
        
        # Log text area
        self.log_text = ctk.CTkTextbox(
            self.progress_frame,
            height=110,
            font=ctk.CTkFont(size=10, family="Consolas")
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        
        # Convert button (BÜYÜTÜLMÜŞ)
        self.convert_btn = ctk.CTkButton(
            main_frame,
            text="🚀 Start Conversion",
            command=self._start_conversion,
            height=85,  # büyütüldü
            font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            corner_radius=12
        )
        self.convert_btn.pack(fill="x", pady=(12, 10))
        
        # Info label
        info_label = ctk.CTkLabel(
            main_frame,
            text="Output: Folder → [folder]_WebP  |  File → same location with .webp extension",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        info_label.pack(pady=(12, 0))
        
    def _toggle_quality(self):
        """Toggle quality slider based on lossless setting"""
        if self.lossless_var.get():
            self.quality_slider.configure(state="disabled")
        else:
            self.quality_slider.configure(state="normal")
    
    def _toggle_resize(self):
        """Toggle resize input based on checkbox"""
        if self.resize_enabled.get():
            self.resize_entry.configure(state="normal")
        else:
            self.resize_entry.configure(state="disabled")
    
    def _browse_folder(self):
        folder = filedialog.askdirectory(title="Select Folder with Images")
        if folder:
            self.source_folder.set(folder)
            self.source_file.set("")
    
    def _browse_file(self):
        file = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.gif *.webp"),
                ("All files", "*.*")
            ]
        )
        if file:
            self.source_file.set(file)
            self.source_folder.set("")
    
    def _log(self, message: str):
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.window.update_idletasks()
    
    def _update_progress(self, message: str, current: int, total: int):
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
        
        source_folder = self.source_folder.get().strip()
        source_file = self.source_file.get().strip()
        
        if not source_folder and not source_file:
            messagebox.showerror("Error", "Please select a source folder or file!")
            return
        
        if source_file:
            source = source_file
            is_single_file = True
        else:
            source = source_folder
            is_single_file = False
        
        if not os.path.exists(source):
            messagebox.showerror("Error", "Selected path does not exist!")
            return
        
        # Validate resize settings
        target_width = None
        if self.resize_enabled.get():
            resize_value = self.resize_width.get().strip()
            if not resize_value:
                messagebox.showerror("Error", "Please enter a target width for resize!")
                return
            try:
                target_width = int(resize_value)
                if target_width <= 0:
                    messagebox.showerror("Error", "Target width must be a positive number!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Target width must be a valid number!")
                return
        
        self.log_text.delete("1.0", "end")
        self._log("=" * 60)
        self._log("Starting conversion process...")
        self._log(f"Source: {source}")
        self._log(f"Quality: {self.quality_var.get()}")
        self._log(f"Lossless: {self.lossless_var.get()}")
        self._log(f"Compression level: {self.method_var.get()}")
        if target_width:
            self._log(f"Resize: Enabled (Target width: {target_width}px, height will be proportional)")
        else:
            self._log("Resize: Disabled")
        self._log("=" * 60)
        
        self.is_converting = True
        self.convert_btn.configure(state="disabled", text="Converting...")
        
        thread = threading.Thread(target=self._convert_thread, args=(source, is_single_file, target_width))
        thread.daemon = True
        thread.start()
    
    def _convert_thread(self, source: str, is_single_file: bool = False, target_width: int = None):
        """Conversion thread"""
        try:
            converter = ImageToWebPConverter(
                quality=self.quality_var.get(),
                lossless=self.lossless_var.get(),
                method=self.method_var.get(),
                target_width=target_width
            )
            
            if is_single_file:
                output_file, total, processed, errors = converter.convert_single_file(
                    source,
                    progress_callback=self._update_progress
                )
                output_info = output_file
            else:
                output_folder, total, processed, errors = converter.convert_folder(
                    source,
                    progress_callback=self._update_progress
                )
                output_info = output_folder
            
            self._log("=" * 60)
            self._log(f"Conversion completed!")
            self._log(f"Output: {output_info}")
            if not is_single_file:
                self._log(f"Total images found: {total}")
            self._log(f"Successfully converted: {processed}")
            if errors:
                self._log(f"Errors: {len(errors)}")
                for error in errors:
                    self._log(f"  - {error}")
            self._log("=" * 60)
            
            if is_single_file:
                msg = f"Conversion completed!\n\nOutput: {output_info}"
            else:
                msg = f"Conversion completed!\n\nProcessed: {processed}/{total} files\nOutput: {output_info}"
            
            self.window.after(0, lambda: messagebox.showinfo("Success", msg))
            
        except Exception as e:
            self._log(f"ERROR: {str(e)}")
            self.window.after(0, lambda: messagebox.showerror("Error", str(e)))
        
        finally:
            self.is_converting = False
            self.window.after(0, lambda: self.convert_btn.configure(
                state="normal",
                text="🚀 Start Conversion"
            ))
    
    def run(self):
        self.window.mainloop()


def main():
    app = WebPConverterGUI()
    app.run()


if __name__ == "__main__":
    main()
