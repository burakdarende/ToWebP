"""
Modern GUI for Image to WebP Converter
Cross-platform compatible interface using CustomTkinter

NOTE: This file now automatically loads the Premium UI (gui_premium.py) if available.
Legacy UI is kept as fallback.
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
        self.window.geometry("850x1150")
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
        self.preserve_alpha = ctk.BooleanVar(value=True)
        self.create_bw = ctk.BooleanVar(value=False)
        self.fine_tuning_enabled = ctk.BooleanVar(value=False)
        self.resize_enabled = ctk.BooleanVar(value=False)
        self.resize_width = ctk.StringVar(value="")
        self.make_horizontal = ctk.BooleanVar(value=False)
        self.uniform_size = ctk.BooleanVar(value=False)
        self.uniform_orientation = ctk.StringVar(value="horizontal")
        self.is_converting = False
        self.stop_conversion = False
        
        # Fine-tuning values
        self.auto_tone = ctk.BooleanVar(value=False)
        self.exposure = ctk.DoubleVar(value=0.0)
        self.contrast = ctk.DoubleVar(value=0.0)
        self.highlights = ctk.DoubleVar(value=0.0)
        self.shadows = ctk.DoubleVar(value=0.0)
        self.whites = ctk.DoubleVar(value=0.0)
        self.blacks = ctk.DoubleVar(value=0.0)
        self.temperature = ctk.DoubleVar(value=0.0)
        self.tint = ctk.DoubleVar(value=0.0)
        self.vibrance = ctk.DoubleVar(value=0.0)
        self.saturation = ctk.DoubleVar(value=0.0)
        
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
        
        # Alpha/Transparency checkbox
        alpha_check = ctk.CTkCheckBox(
            settings_frame,
            text="Preserve Alpha Channel (Transparency support for PNG images)",
            variable=self.preserve_alpha,
            font=ctk.CTkFont(size=11)
        )
        alpha_check.pack(anchor="w", padx=10, pady=8)
        
        # Black & White checkbox
        bw_check = ctk.CTkCheckBox(
            settings_frame,
            text="Create Black & White Version (Additional _bw file with same settings)",
            variable=self.create_bw,
            font=ctk.CTkFont(size=11)
        )
        bw_check.pack(anchor="w", padx=10, pady=8)
        
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
        
        # Fine-tuning option
        fine_tune_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        fine_tune_frame.pack(fill="x", padx=10, pady=(8, 8))
        
        fine_tune_top_frame = ctk.CTkFrame(fine_tune_frame, fg_color="transparent")
        fine_tune_top_frame.pack(fill="x")
        
        fine_tune_check = ctk.CTkCheckBox(
            fine_tune_top_frame,
            text="Fine-Tuning Adjustments (Exposure, Contrast, Colors...)",
            variable=self.fine_tuning_enabled,
            font=ctk.CTkFont(size=11),
            command=self._toggle_fine_tuning
        )
        fine_tune_check.pack(side="left")
        
        self.fine_tune_btn = ctk.CTkButton(
            fine_tune_top_frame,
            text="⚙️ Adjust",
            command=self._open_fine_tuning_dialog,
            width=90,
            height=28,
            font=ctk.CTkFont(size=11, weight="bold"),
            state="disabled"
        )
        self.fine_tune_btn.pack(side="left", padx=(10, 0))
        
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
        
        # Make horizontal option (for vertical images)
        horizontal_check = ctk.CTkCheckBox(
            resize_frame,
            text="📐 Make Vertical Images Horizontal (crop top/bottom to square based on target width)",
            variable=self.make_horizontal,
            font=ctk.CTkFont(size=11)
        )
        horizontal_check.pack(anchor="w", pady=(8, 0))
        
        # Uniform size option (advanced cropping)
        uniform_frame = ctk.CTkFrame(resize_frame, fg_color="transparent")
        uniform_frame.pack(fill="x", pady=(8, 0))
        
        uniform_check = ctk.CTkCheckBox(
            uniform_frame,
            text="⚖️ Make ALL Images Same Size (crops to uniform dimensions)",
            variable=self.uniform_size,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._toggle_uniform_size
        )
        uniform_check.pack(anchor="w")
        
        # Warning label
        uniform_warning = ctk.CTkLabel(
            uniform_frame,
            text="⚠️ This will crop ALL images to same dimensions. Analyzes folder to find optimal ratio.",
            font=ctk.CTkFont(size=9),
            text_color="#ff9800"
        )
        uniform_warning.pack(anchor="w", padx=(25, 0), pady=(2, 4))
        
        # Orientation selection
        self.orientation_frame = ctk.CTkFrame(uniform_frame, fg_color="transparent")
        self.orientation_frame.pack(fill="x", padx=(25, 0), pady=(4, 0))
        
        orientation_label = ctk.CTkLabel(
            self.orientation_frame,
            text="Target Orientation:",
            font=ctk.CTkFont(size=10)
        )
        orientation_label.pack(side="left", padx=(0, 8))
        
        self.horizontal_radio = ctk.CTkRadioButton(
            self.orientation_frame,
            text="Horizontal (Landscape)",
            variable=self.uniform_orientation,
            value="horizontal",
            font=ctk.CTkFont(size=10),
            state="disabled"
        )
        self.horizontal_radio.pack(side="left", padx=(0, 12))
        
        self.vertical_radio = ctk.CTkRadioButton(
            self.orientation_frame,
            text="Vertical (Portrait)",
            variable=self.uniform_orientation,
            value="vertical",
            font=ctk.CTkFont(size=10),
            state="disabled"
        )
        self.vertical_radio.pack(side="left")
        
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
            height=100,
            font=ctk.CTkFont(size=10, family="Consolas")
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        
        # Convert button (BÜYÜTÜLMÜŞ)
        self.convert_btn = ctk.CTkButton(
            main_frame,
            text="🚀 Start Conversion",
            command=self._start_conversion,
            height=95,  # daha da büyütüldü
            font=ctk.CTkFont(size=24, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            corner_radius=12
        )
        self.convert_btn.pack(fill="x", pady=(15, 12))
        
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
    
    def _toggle_uniform_size(self):
        """Toggle uniform size orientation options"""
        if self.uniform_size.get():
            self.horizontal_radio.configure(state="normal")
            self.vertical_radio.configure(state="normal")
        else:
            self.horizontal_radio.configure(state="disabled")
            self.vertical_radio.configure(state="disabled")
    
    def _toggle_fine_tuning(self):
        """Toggle fine-tuning button based on checkbox"""
        if self.fine_tuning_enabled.get():
            self.fine_tune_btn.configure(state="normal")
        else:
            self.fine_tune_btn.configure(state="disabled")
    
    def _open_fine_tuning_dialog(self):
        """Open fine-tuning adjustment dialog"""
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("Fine-Tuning Adjustments")
        dialog.geometry("500x650")
        dialog.resizable(False, False)
        
        # Make it modal
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() - 500) // 2
        y = self.window.winfo_y() + (self.window.winfo_height() - 650) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Main frame
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="⚙️ Fine-Tuning Adjustments",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 15))
        
        # Scrollable frame for sliders
        scroll_frame = ctk.CTkScrollableFrame(main_frame, height=450)
        scroll_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Auto Tone checkbox at the top
        auto_tone_frame = ctk.CTkFrame(scroll_frame, fg_color="#1a1a1a", corner_radius=8)
        auto_tone_frame.pack(fill="x", pady=(5, 15), padx=5)
        
        auto_tone_check = ctk.CTkCheckBox(
            auto_tone_frame,
            text="🪄 Auto Tone (Automatic adjustments - disables manual sliders)",
            variable=self.auto_tone,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: self._toggle_auto_tone(scroll_frame)
        )
        auto_tone_check.pack(anchor="w", padx=15, pady=12)
        
        auto_info = ctk.CTkLabel(
            auto_tone_frame,
            text="AI-powered automatic color correction, exposure, contrast and tone adjustments",
            font=ctk.CTkFont(size=9),
            text_color="gray"
        )
        auto_info.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Store slider frames for toggling
        self.slider_frames = []
        
        # Light section
        light_label = ctk.CTkLabel(
            scroll_frame,
            text="▼ Light",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        light_label.pack(anchor="w", pady=(10, 10))
        
        # Exposure
        self.slider_frames.append(self._create_slider(scroll_frame, "Exposure", self.exposure, -2.0, 2.0))
        
        # Contrast
        self.slider_frames.append(self._create_slider(scroll_frame, "Contrast", self.contrast, -100, 100))
        
        # Highlights
        self.slider_frames.append(self._create_slider(scroll_frame, "Highlights", self.highlights, -100, 100))
        
        # Shadows
        self.slider_frames.append(self._create_slider(scroll_frame, "Shadows", self.shadows, -100, 100))
        
        # Whites
        self.slider_frames.append(self._create_slider(scroll_frame, "Whites", self.whites, -100, 100))
        
        # Blacks
        self.slider_frames.append(self._create_slider(scroll_frame, "Blacks", self.blacks, -100, 100))
        
        # Color section
        color_label = ctk.CTkLabel(
            scroll_frame,
            text="▼ Color",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        color_label.pack(anchor="w", pady=(20, 10))
        
        # Temperature
        self.slider_frames.append(self._create_slider(scroll_frame, "Temperature", self.temperature, -100, 100))
        
        # Tint
        self.slider_frames.append(self._create_slider(scroll_frame, "Tint", self.tint, -100, 100))
        
        # Vibrance
        self.slider_frames.append(self._create_slider(scroll_frame, "Vibrance", self.vibrance, -100, 100))
        
        # Saturation
        self.slider_frames.append(self._create_slider(scroll_frame, "Saturation", self.saturation, -100, 100))
        
        # Apply initial state
        self._toggle_auto_tone(scroll_frame)
        
        # Button frame
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        # Reset button
        reset_btn = ctk.CTkButton(
            btn_frame,
            text="Reset All",
            command=self._reset_fine_tuning,
            width=120,
            height=35,
            font=ctk.CTkFont(size=12)
        )
        reset_btn.pack(side="left", padx=(0, 10))
        
        # Close button
        close_btn = ctk.CTkButton(
            btn_frame,
            text="Done",
            command=dialog.destroy,
            width=120,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        close_btn.pack(side="right")
    
    def _create_slider(self, parent, label_text, variable, min_val, max_val):
        """Create a labeled slider"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=5)
        
        # Label with value
        value_text = f"{variable.get():.2f}" if isinstance(min_val, float) else f"{int(variable.get())}"
        label = ctk.CTkLabel(
            frame,
            text=f"{label_text}: {value_text}",
            font=ctk.CTkFont(size=11),
            width=150,
            anchor="w"
        )
        label.pack(side="left", padx=(0, 10))
        
        # Slider
        slider = ctk.CTkSlider(
            frame,
            from_=min_val,
            to=max_val,
            variable=variable,
            command=lambda v: label.configure(
                text=f"{label_text}: {v:.2f}" if isinstance(min_val, float) else f"{label_text}: {int(v)}"
            )
        )
        slider.pack(side="left", fill="x", expand=True)
        
        return frame
    
    def _reset_fine_tuning(self):
        """Reset all fine-tuning values to defaults"""
        self.auto_tone.set(False)
        self.exposure.set(0.0)
        self.contrast.set(0.0)
        self.highlights.set(0.0)
        self.shadows.set(0.0)
        self.whites.set(0.0)
        self.blacks.set(0.0)
        self.temperature.set(0.0)
        self.tint.set(0.0)
        self.vibrance.set(0.0)
        self.saturation.set(0.0)
        
        # Re-enable sliders if they exist
        if hasattr(self, 'slider_frames'):
            for frame in self.slider_frames:
                for widget in frame.winfo_children():
                    if isinstance(widget, ctk.CTkSlider):
                        widget.configure(state="normal")
    
    def _toggle_auto_tone(self, parent):
        """Toggle manual sliders based on Auto Tone checkbox"""
        is_auto = self.auto_tone.get()
        
        # Disable/Enable all sliders
        if hasattr(self, 'slider_frames'):
            for frame in self.slider_frames:
                for widget in frame.winfo_children():
                    if isinstance(widget, ctk.CTkSlider):
                        if is_auto:
                            widget.configure(state="disabled")
                        else:
                            widget.configure(state="normal")
    
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
        self._log(f"Preserve Alpha: {self.preserve_alpha.get()}")
        self._log(f"Create B&W Version: {self.create_bw.get()}")
        self._log(f"Fine-Tuning: {self.fine_tuning_enabled.get()}")
        if self.fine_tuning_enabled.get():
            if self.auto_tone.get():
                self._log(f"  🪄 Auto Tone: Enabled (AI-powered automatic adjustments)")
            else:
                adjustments = []
                if self.exposure.get() != 0: adjustments.append(f"Exposure:{self.exposure.get():.1f}")
                if self.contrast.get() != 0: adjustments.append(f"Contrast:{self.contrast.get():.0f}")
                if self.saturation.get() != 0: adjustments.append(f"Saturation:{self.saturation.get():.0f}")
                if adjustments:
                    self._log(f"  Adjustments: {', '.join(adjustments)}")
        self._log(f"Compression level: {self.method_var.get()}")
        if target_width:
            self._log(f"Resize: Enabled (Target width: {target_width}px, height will be proportional)")
            if self.make_horizontal.get():
                self._log(f"  📐 Make Horizontal: Enabled (vertical images will be cropped to square)")
            if self.uniform_size.get():
                self._log(f"  ⚖️ Uniform Size: Enabled (ALL images will be same size)")
                self._log(f"  Target Orientation: {self.uniform_orientation.get().upper()}")
                self._log(f"  ⚠️ Will analyze folder and crop all images to optimal ratio")
        else:
            self._log("Resize: Disabled")
        self._log("=" * 60)
        
        self.is_converting = True
        self.stop_conversion = False
        self.convert_btn.configure(
            state="normal",
            text="⛔ STOP",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self._stop_conversion
        )
        
        thread = threading.Thread(target=self._convert_thread, args=(source, is_single_file, target_width))
        thread.daemon = True
        thread.start()
    
    def _convert_thread(self, source: str, is_single_file: bool = False, target_width: int = None):
        """Conversion thread"""
        try:
            # Prepare fine-tuning settings
            fine_tuning = None
            if self.fine_tuning_enabled.get():
                fine_tuning = {
                    'auto_tone': self.auto_tone.get(),
                    'exposure': self.exposure.get(),
                    'contrast': self.contrast.get(),
                    'highlights': self.highlights.get(),
                    'shadows': self.shadows.get(),
                    'whites': self.whites.get(),
                    'blacks': self.blacks.get(),
                    'temperature': self.temperature.get(),
                    'tint': self.tint.get(),
                    'vibrance': self.vibrance.get(),
                    'saturation': self.saturation.get()
                }
            
            converter = ImageToWebPConverter(
                quality=self.quality_var.get(),
                lossless=self.lossless_var.get(),
                method=self.method_var.get(),
                target_width=target_width,
                preserve_alpha=self.preserve_alpha.get(),
                create_bw=self.create_bw.get(),
                fine_tuning=fine_tuning,
                make_horizontal=self.make_horizontal.get(),
                uniform_size=self.uniform_size.get(),
                uniform_orientation=self.uniform_orientation.get()
            )
            
            # Store converter reference for stop functionality
            self.current_converter = converter
            
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
            
            # Check if stopped
            if self.stop_conversion:
                self._log("=" * 60)
                self._log(f"⚠️ Conversion stopped by user!")
                self._log(f"Processed: {processed}/{total} files before stopping")
                self._log("=" * 60)
                self.window.after(0, lambda: messagebox.showwarning(
                    "Stopped", 
                    f"Conversion stopped!\n\nProcessed: {processed}/{total} files"
                ))
                return
            
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
            self.stop_conversion = False
            self.window.after(0, lambda: self.convert_btn.configure(
                state="normal",
                text="🚀 Start Conversion",
                fg_color="#2ecc71",
                hover_color="#27ae60",
                command=self._start_conversion
            ))
    
    def _stop_conversion(self):
        """Stop the conversion process"""
        if self.is_converting:
            self.stop_conversion = True
            if hasattr(self, 'current_converter'):
                self.current_converter.should_stop = True
            self._log("⚠️ Stopping conversion... (current file will complete)")
            self.convert_btn.configure(
                state="disabled",
                text="⏳ Stopping...",
                fg_color="#95a5a6",
                hover_color="#7f8c8d"
            )
    
    def run(self):
        self.window.mainloop()


def main():
    """Main entry point - automatically uses Premium UI if available"""
    try:
        # Try to import and use Premium UI
        from gui_premium import WebPConverterPremiumGUI
        print("✨ Starting Premium UI...")
        app = WebPConverterPremiumGUI()
        app.run()
    except ImportError as e:
        # Fallback to legacy UI if premium not available
        print(f"⚠️ Premium UI not available ({e}), using legacy UI...")
        app = WebPConverterGUI()
        app.run()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
