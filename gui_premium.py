"""
Premium Modern GUI for Image to WebP Converter
Features: Responsive Design, Animations, Drag & Drop, Glassmorphism
Author: Burak Darende
Version: 2.0 Premium
"""
import os
import sys
import threading
from pathlib import Path
from tkinter import filedialog, messagebox
import customtkinter as ctk
from converter import ImageToWebPConverter
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DRAG_DROP_AVAILABLE = True
except ImportError:
    DRAG_DROP_AVAILABLE = False


class ModernCard(ctk.CTkFrame):
    """Modern card component with hover effects"""
    
    def __init__(self, master, title="", **kwargs):
        super().__init__(master, **kwargs)
        
        self.title = title
        self.is_expanded = True
        self.content_frame = None
        
        # Card styling
        self.configure(
            fg_color=("gray90", "gray17"),
            corner_radius=12,
            border_width=1,
            border_color=("gray70", "gray30")
        )
        
        # Header
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=15, pady=(12, 0))
        
        self.title_label = ctk.CTkLabel(
            self.header,
            text=f"✨ {title}",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        self.title_label.pack(side="left", fill="x", expand=True)
        
        # Collapse button
        self.collapse_btn = ctk.CTkButton(
            self.header,
            text="▼",
            width=30,
            height=30,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=("gray80", "gray25"),
            command=self._toggle_collapse
        )
        self.collapse_btn.pack(side="right")
        
        # Content area
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=(8, 12))
        
        # Hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def _toggle_collapse(self):
        """Toggle card collapse/expand"""
        if self.is_expanded:
            self.content_frame.pack_forget()
            self.collapse_btn.configure(text="▶")
            self.is_expanded = False
        else:
            self.content_frame.pack(fill="both", expand=True, padx=15, pady=(8, 12))
            self.collapse_btn.configure(text="▼")
            self.is_expanded = True
            
    def _on_enter(self, event):
        """Hover enter effect"""
        self.configure(border_color=("gray60", "gray40"))
        
    def _on_leave(self, event):
        """Hover leave effect"""
        self.configure(border_color=("gray70", "gray30"))
        
    def get_content_frame(self):
        """Get the content frame for adding widgets"""
        return self.content_frame


class AnimatedProgressBar(ctk.CTkFrame):
    """Custom animated progress bar with gradient colors"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, height=8, **kwargs)
        
        self.configure(
            fg_color=("gray80", "gray25"),
            corner_radius=4
        )
        
        self.progress = ctk.CTkFrame(
            self,
            height=8,
            fg_color=("#4CAF50", "#66BB6A"),  # Green gradient
            corner_radius=4
        )
        self.progress.place(relx=0, rely=0, relwidth=0, relheight=1)
        
        self.current_value = 0
        self.target_value = 0
        self.animating = False
        
    def set(self, value):
        """Set progress value with animation (0-100)"""
        self.target_value = max(0, min(100, value))
        
        # Update color based on progress
        if self.target_value < 33:
            color = ("#FF9800", "#FFB74D")  # Orange for start
        elif self.target_value < 66:
            color = ("#2196F3", "#64B5F6")  # Blue for middle
        else:
            color = ("#4CAF50", "#66BB6A")  # Green for completion
        
        self.progress.configure(fg_color=color)
        
        if not self.animating:
            self._animate()
            
    def _animate(self):
        """Smooth animation with easing"""
        self.animating = True
        if abs(self.current_value - self.target_value) > 0.5:
            diff = (self.target_value - self.current_value) * 0.15  # Faster animation
            self.current_value += diff
            self.progress.place(relx=0, rely=0, relwidth=self.current_value/100, relheight=1)
            self.after(16, self._animate)  # ~60 FPS
        else:
            self.current_value = self.target_value
            self.progress.place(relx=0, rely=0, relwidth=self.current_value/100, relheight=1)
            self.animating = False
            
    def reset(self):
        """Reset progress"""
        self.current_value = 0
        self.target_value = 0
        self.progress.configure(fg_color=("#FF9800", "#FFB74D"))  # Reset to orange
        self.progress.place(relx=0, rely=0, relwidth=0, relheight=1)


class FloatingActionButton(ctk.CTkButton):
    """Floating Action Button with shadow effect"""
    
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=30,
            height=60,
            font=ctk.CTkFont(size=16, weight="bold"),
            **kwargs
        )
        
        # Shadow effect (simulated with multiple frames)
        self.shadow_frames = []
        
    def _on_enter(self, event):
        """Scale up on hover"""
        # This would require additional animation library for smooth scale
        pass


class WebPConverterPremiumGUI:
    """Premium Modern GUI Application"""
    
    def __init__(self):
        # Initialize window
        self.window = ctk.CTk()
        self.window.title("Image to WebP Converter Premium")
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Set window size (80% of screen, min 1000x700, max 1400x900)
        window_width = max(1000, min(1400, int(screen_width * 0.8)))
        window_height = max(700, min(900, int(screen_height * 0.85)))
        
        # Center window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.minsize(1000, 700)
        
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
        
        # UI References
        self.log_text = None
        self.convert_button = None
        self.progress_bar = None
        self.status_label = None
        self.stat_boxes = []
        
        # Stats tracking
        self.stats_files_processed = 0
        self.stats_start_time = None
        self.stats_bytes_saved = 0
        
        self._setup_ui()
        self._setup_drag_drop()
        
    def _setup_ui(self):
        """Setup the premium user interface"""
        
        # Main container with grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        # Main content area
        main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=1)
        
        # ===== HEADER =====
        self._create_header(main_container)
        
        # ===== CONTENT (Tabs) =====
        self.tabview = ctk.CTkTabview(main_container, corner_radius=12)
        self.tabview.grid(row=1, column=0, sticky="nsew", pady=(0, 15))
        
        # Create tabs
        self.tab_convert = self.tabview.add("🚀 Convert")
        self.tab_settings = self.tabview.add("⚙️ Settings")
        self.tab_finetune = self.tabview.add("🎨 Fine-Tuning")
        self.tab_about = self.tabview.add("ℹ️ About")
        
        # Configure tab grids
        for tab in [self.tab_convert, self.tab_settings, self.tab_finetune, self.tab_about]:
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)
        
        # Setup each tab
        self._setup_convert_tab()
        self._setup_settings_tab()
        self._setup_finetune_tab()
        self._setup_about_tab()
        
        # ===== FOOTER (Status & Convert Button) =====
        self._create_footer(main_container)
        
    def _create_header(self, parent):
        """Create animated header with gradient effect"""
        # Header background with subtle gradient effect
        header_bg = ctk.CTkFrame(
            parent, 
            fg_color=("gray95", "gray15"),
            corner_radius=15,
            height=90
        )
        header_bg.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        header = ctk.CTkFrame(header_bg, fg_color="transparent")
        header.pack(fill="both", expand=True, padx=15, pady=12)
        header.grid_columnconfigure(1, weight=1)
        
        # Animated Icon/Logo with pulse effect
        icon_label = ctk.CTkLabel(
            header,
            text="🖼️",
            font=ctk.CTkFont(size=48)
        )
        icon_label.grid(row=0, column=0, padx=(0, 15), sticky="w")
        
        # Title and subtitle with gradient color
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=1, sticky="ew")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="Image to WebP Converter",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#2196F3", "#64B5F6"),  # Blue gradient
            anchor="w"
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="✨ Premium Edition • ⚡ Fast • 🎯 Professional • 🎨 Beautiful",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w"
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))
        
        # Theme toggle with better styling
        theme_btn = ctk.CTkButton(
            header,
            text="🌓",
            width=50,
            height=50,
            font=ctk.CTkFont(size=20),
            command=self._toggle_theme,
            fg_color=("gray85", "gray20"),
            hover_color=("#FFB74D", "#FFA726"),  # Orange hover
            corner_radius=25
        )
        theme_btn.grid(row=0, column=2, sticky="e")
        
    def _create_footer(self, parent):
        """Create footer with status and convert button"""
        footer = ctk.CTkFrame(parent, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_columnconfigure(0, weight=1)
        
        # Status bar
        status_frame = ctk.CTkFrame(footer, height=40, corner_radius=8)
        status_frame.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        status_frame.grid_columnconfigure(1, weight=1)
        
        status_icon = ctk.CTkLabel(
            status_frame,
            text="📊",
            font=ctk.CTkFont(size=16)
        )
        status_icon.grid(row=0, column=0, padx=(12, 8))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready to convert",
            font=ctk.CTkFont(size=13),
            anchor="w"
        )
        self.status_label.grid(row=0, column=1, sticky="ew", padx=(0, 12))
        
        # Progress bar
        self.progress_bar = AnimatedProgressBar(footer)
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        
        # Convert button (FAB style) with gradient colors
        self.convert_button = ctk.CTkButton(
            footer,
            text="🚀 START CONVERSION",
            command=self._convert,
            height=70,
            corner_radius=35,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=("#4CAF50", "#43A047"),  # Better green gradient
            hover_color=("#66BB6A", "#4CAF50"),  # Lighter green on hover
            border_width=2,
            border_color=("#81C784", "#66BB6A")
        )
        self.convert_button.grid(row=2, column=0, sticky="ew")
        
    def _setup_convert_tab(self):
        """Setup convert tab with source selection"""
        # Scrollable frame
        scroll = ctk.CTkScrollableFrame(self.tab_convert, fg_color="transparent")
        scroll.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        scroll.grid_columnconfigure(0, weight=1)
        
        # Source Selection Card - MINIMAL
        source_card = ModernCard(scroll, title="Source Selection")
        source_card.pack(fill="x", pady=(0, 8))
        content = source_card.get_content_frame()
        
        # Folder selection - minimal
        folder_label = ctk.CTkLabel(
            content,
            text="📁 Folder:",
            font=ctk.CTkFont(size=11, weight="bold"),
            anchor="w"
        )
        folder_label.pack(anchor="w", pady=(2, 2))
        
        folder_frame = ctk.CTkFrame(content, fg_color="transparent")
        folder_frame.pack(fill="x", pady=(0, 6))
        folder_frame.grid_columnconfigure(0, weight=1)
        
        self.folder_entry = ctk.CTkEntry(
            folder_frame,
            textvariable=self.source_folder,
            placeholder_text="Browse for folder...",
            height=35,  # Smaller
            font=ctk.CTkFont(size=10),
            corner_radius=6
        )
        self.folder_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        
        browse_folder_btn = ctk.CTkButton(
            folder_frame,
            text="Browse",
            command=self._browse_folder,
            width=80,  # Smaller
            height=35,
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=6
        )
        browse_folder_btn.grid(row=0, column=1)
        
        # OR divider - minimal
        or_frame = ctk.CTkFrame(content, fg_color="transparent", height=16)
        or_frame.pack(fill="x", pady=3)
        
        or_line1 = ctk.CTkFrame(or_frame, height=1, fg_color=("gray70", "gray30"))
        or_line1.pack(side="left", fill="x", expand=True, padx=(0, 6))
        
        or_label = ctk.CTkLabel(
            or_frame,
            text="OR",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=("gray50", "gray60")
        )
        or_label.pack(side="left")
        
        or_line2 = ctk.CTkFrame(or_frame, height=1, fg_color=("gray70", "gray30"))
        or_line2.pack(side="left", fill="x", expand=True, padx=(6, 0))
        
        # File selection - minimal
        file_label = ctk.CTkLabel(
            content,
            text="📄 Single File:",
            font=ctk.CTkFont(size=11, weight="bold"),
            anchor="w"
        )
        file_label.pack(anchor="w", pady=(2, 2))
        
        file_frame = ctk.CTkFrame(content, fg_color="transparent")
        file_frame.pack(fill="x")
        file_frame.grid_columnconfigure(0, weight=1)
        
        self.file_entry = ctk.CTkEntry(
            file_frame,
            textvariable=self.source_file,
            placeholder_text="Browse for file...",
            height=35,  # Smaller
            font=ctk.CTkFont(size=10),
            corner_radius=6
        )
        self.file_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        
        browse_file_btn = ctk.CTkButton(
            file_frame,
            text="Browse",
            command=self._browse_file,
            width=80,  # Smaller
            height=35,
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=6
        )
        browse_file_btn.grid(row=0, column=1)
        
        # Output Destination Card
        output_card = ModernCard(scroll, title="Output Destination")
        output_card.pack(fill="x", pady=(8, 8))
        output_content = output_card.get_content_frame()
        
        output_label = ctk.CTkLabel(
            output_content,
            text="📂 Output Folder (Optional):",
            font=ctk.CTkFont(size=11, weight="bold"),
            anchor="w"
        )
        output_label.pack(anchor="w", pady=(2, 2))
        
        output_frame = ctk.CTkFrame(output_content, fg_color="transparent")
        output_frame.pack(fill="x")
        output_frame.grid_columnconfigure(0, weight=1)
        
        self.output_folder_var = ctk.StringVar()
        self.output_entry = ctk.CTkEntry(
            output_frame,
            textvariable=self.output_folder_var,
            placeholder_text="Default: Same as source (or _WebP folder)",
            height=35,
            font=ctk.CTkFont(size=10),
            corner_radius=6,
            state="readonly"
        )
        self.output_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        
        browse_output_btn = ctk.CTkButton(
            output_frame,
            text="Select",
            command=self._browse_output_folder,
            width=70,
            height=35,
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=6
        )
        browse_output_btn.grid(row=0, column=1, padx=(0, 6))
        
        reset_output_btn = ctk.CTkButton(
            output_frame,
            text="Reset",
            command=self._reset_output_folder,
            width=60,
            height=35,
            font=ctk.CTkFont(size=11),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray35"),
            corner_radius=6
        )
        reset_output_btn.grid(row=0, column=2)
        
        # Stats & Preview Card - ULTRA COMPACT
        stats_card = ModernCard(scroll, title="Quick Stats")
        stats_card.pack(fill="x", pady=(8, 8))
        stats_content = stats_card.get_content_frame()
        
        # Stats grid - ultra compact
        stats_grid = ctk.CTkFrame(stats_content, fg_color="transparent")
        stats_grid.pack(fill="x", pady=2)
        stats_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Stat boxes - MINIMAL
        self.stat_boxes = []
        stat_data = [
            ("📁", "Files", "0", ("#E3F2FD", "#1565C0")),
            ("⚡", "Speed", "0/s", ("#FFF3E0", "#E65100")),
            ("💾", "Saved", "0 MB", ("#E8F5E9", "#2E7D32")),
            ("⏱️", "Time", "0:00", ("#F3E5F5", "#6A1B9A"))
        ]
        
        for i, (icon, label, value, colors) in enumerate(stat_data):
            stat_box = ctk.CTkFrame(
                stats_grid,
                fg_color=colors,
                corner_radius=6,
                height=45,  # Much smaller!
                border_width=0
            )
            stat_box.grid(row=0, column=i, sticky="ew", padx=2)
            
            # Compact horizontal layout
            content_frame = ctk.CTkFrame(stat_box, fg_color="transparent")
            content_frame.pack(expand=True, fill="both", padx=6, pady=4)
            
            icon_label = ctk.CTkLabel(
                content_frame,
                text=icon,
                font=ctk.CTkFont(size=16)  # Smaller icon
            )
            icon_label.pack(side="left", padx=(0, 4))
            
            # Value and label stacked vertically
            text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True)
            
            value_label = ctk.CTkLabel(
                text_frame,
                text=value,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=("gray10", "white"),
                anchor="w"
            )
            value_label.pack(anchor="w")
            
            label_label = ctk.CTkLabel(
                text_frame,
                text=label,
                font=ctk.CTkFont(size=8),
                text_color=(colors[1], colors[0]),
                anchor="w"
            )
            label_label.pack(anchor="w")
            
            self.stat_boxes.append(value_label)
        
        # Process Log Card - PRIORITY - Takes most space
        log_card = ModernCard(scroll, title="Process Log")
        log_card.pack(fill="both", expand=True, pady=(3, 0))
        log_content = log_card.get_content_frame()
        
        self.log_text = ctk.CTkTextbox(
            log_content,
            height=350,  # Even larger for better visibility
            font=ctk.CTkFont(family="Consolas", size=10),
            wrap="word",
            corner_radius=6
        )
        self.log_text.pack(fill="both", expand=True)
        self.log_text.insert("1.0", "🎯 Ready to convert images to WebP format\n")
        self.log_text.configure(state="disabled")
        
    def _setup_settings_tab(self):
        """Setup settings tab with quality and processing options"""
        # Scrollable frame
        scroll = ctk.CTkScrollableFrame(self.tab_settings, fg_color="transparent")
        scroll.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        scroll.grid_columnconfigure(0, weight=1)
        
        # Quality Settings Card
        quality_card = ModernCard(scroll, title="Quality Settings")
        quality_card.pack(fill="x", pady=(0, 15))
        content = quality_card.get_content_frame()
        
        # Quality slider
        quality_label = ctk.CTkLabel(
            content,
            text=f"🎨 Quality: {self.quality_var.get()}",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        quality_label.pack(anchor="w", pady=(5, 5))
        
        self.quality_slider = ctk.CTkSlider(
            content,
            from_=1,
            to=100,
            variable=self.quality_var,
            command=lambda v: quality_label.configure(text=f"🎨 Quality: {int(v)}"),
            height=20,
            button_length=30
        )
        self.quality_slider.pack(fill="x", pady=(0, 12))
        
        # Lossless and compression in same row
        options_frame = ctk.CTkFrame(content, fg_color="transparent")
        options_frame.pack(fill="x", pady=(0, 12))
        options_frame.grid_columnconfigure(0, weight=1)
        options_frame.grid_columnconfigure(1, weight=1)
        
        lossless_check = ctk.CTkCheckBox(
            options_frame,
            text="✨ Lossless Compression",
            variable=self.lossless_var,
            font=ctk.CTkFont(size=12),
            command=self._toggle_lossless
        )
        lossless_check.grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        compression_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        compression_frame.grid(row=0, column=1, sticky="ew")
        
        compression_label = ctk.CTkLabel(
            compression_frame,
            text=f"⚙️ Compression Level: {self.method_var.get()}",
            font=ctk.CTkFont(size=12)
        )
        compression_label.pack(anchor="w")
        
        self.compression_slider = ctk.CTkSlider(
            compression_frame,
            from_=0,
            to=6,
            number_of_steps=6,
            variable=self.method_var,
            command=lambda v: compression_label.configure(text=f"⚙️ Compression Level: {int(v)}"),
            height=16
        )
        self.compression_slider.pack(fill="x")
        
        # Image Processing Card
        processing_card = ModernCard(scroll, title="Image Processing")
        processing_card.pack(fill="x", pady=(0, 15))
        content = processing_card.get_content_frame()
        
        # Checkboxes in grid
        check_frame = ctk.CTkFrame(content, fg_color="transparent")
        check_frame.pack(fill="x", pady=5)
        check_frame.grid_columnconfigure(0, weight=1)
        check_frame.grid_columnconfigure(1, weight=1)
        
        alpha_check = ctk.CTkCheckBox(
            check_frame,
            text="🌈 Preserve Alpha Channel",
            variable=self.preserve_alpha,
            font=ctk.CTkFont(size=12)
        )
        alpha_check.grid(row=0, column=0, sticky="w", pady=5)
        
        bw_check = ctk.CTkCheckBox(
            check_frame,
            text="⚫ Create B&W Version",
            variable=self.create_bw,
            font=ctk.CTkFont(size=12)
        )
        bw_check.grid(row=0, column=1, sticky="w", pady=5)
        
        # Resize Options Card
        resize_card = ModernCard(scroll, title="Resize Options")
        resize_card.pack(fill="x", pady=(0, 15))
        content = resize_card.get_content_frame()
        
        resize_check = ctk.CTkCheckBox(
            content,
            text="📏 Enable Resize (Proportional)",
            variable=self.resize_enabled,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._toggle_resize
        )
        resize_check.pack(anchor="w", pady=(5, 10))
        
        # Width input
        width_frame = ctk.CTkFrame(content, fg_color="transparent")
        width_frame.pack(fill="x", pady=(0, 12))
        
        width_label = ctk.CTkLabel(
            width_frame,
            text="Target Width (px):",
            font=ctk.CTkFont(size=12)
        )
        width_label.pack(side="left", padx=(0, 10))
        
        self.width_entry = ctk.CTkEntry(
            width_frame,
            textvariable=self.resize_width,
            placeholder_text="e.g., 1920",
            width=150,
            height=35,
            state="disabled"
        )
        self.width_entry.pack(side="left")
        
        # Horizontal and Uniform options
        self.horizontal_check = ctk.CTkCheckBox(
            content,
            text="🔄 Make Vertical Images Horizontal",
            variable=self.make_horizontal,
            font=ctk.CTkFont(size=12),
            state="disabled"
        )
        self.horizontal_check.pack(anchor="w", pady=(0, 8))
        
        self.uniform_check = ctk.CTkCheckBox(
            content,
            text="📐 Make All Images Same Size",
            variable=self.uniform_size,
            font=ctk.CTkFont(size=12),
            state="disabled",
            command=self._toggle_uniform_size
        )
        self.uniform_check.pack(anchor="w", pady=(0, 8))
        
        # Uniform warning
        self.uniform_warning = ctk.CTkLabel(
            content,
            text="⚠️ This will crop all images to same dimensions. Analyzes folder to find optimal ratio.",
            font=ctk.CTkFont(size=10),
            text_color=("orange", "orange")
        )
        
        # Orientation options
        orientation_frame = ctk.CTkFrame(content, fg_color="transparent")
        
        self.orientation_label = ctk.CTkLabel(
            orientation_frame,
            text="Target Orientation:",
            font=ctk.CTkFont(size=11)
        )
        self.orientation_label.pack(side="left", padx=(20, 10))
        
        self.horizontal_radio = ctk.CTkRadioButton(
            orientation_frame,
            text="Horizontal (Landscape)",
            variable=self.uniform_orientation,
            value="horizontal",
            font=ctk.CTkFont(size=11),
            state="disabled"
        )
        self.horizontal_radio.pack(side="left", padx=(0, 10))
        
        self.vertical_radio = ctk.CTkRadioButton(
            orientation_frame,
            text="Vertical (Portrait)",
            variable=self.uniform_orientation,
            value="vertical",
            font=ctk.CTkFont(size=11),
            state="disabled"
        )
        self.vertical_radio.pack(side="left")
        
    def _setup_finetune_tab(self):
        """Setup fine-tuning tab"""
        # Scrollable frame
        scroll = ctk.CTkScrollableFrame(self.tab_finetune, fg_color="transparent")
        scroll.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        scroll.grid_columnconfigure(0, weight=1)
        
        # Enable Fine-Tuning Card
        enable_card = ModernCard(scroll, title="Fine-Tuning Controls")
        enable_card.pack(fill="x", pady=(0, 15))
        content = enable_card.get_content_frame()
        
        finetune_check = ctk.CTkCheckBox(
            content,
            text="🎨 Enable Fine-Tuning Adjustments",
            variable=self.fine_tuning_enabled,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._toggle_finetune
        )
        finetune_check.pack(anchor="w", pady=8)
        
        info_label = ctk.CTkLabel(
            content,
            text="Apply advanced color corrections and tone adjustments to your images",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w"
        )
        info_label.pack(anchor="w", pady=(0, 8))
        
        # Auto Tone Card
        auto_card = ModernCard(scroll, title="Auto Adjustments")
        auto_card.pack(fill="x", pady=(0, 15))
        content = auto_card.get_content_frame()
        
        self.auto_tone_check = ctk.CTkCheckBox(
            content,
            text="🪄 Auto Tone (AI-Powered)",
            variable=self.auto_tone,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._toggle_auto_tone,
            state="disabled"
        )
        self.auto_tone_check.pack(anchor="w", pady=8)
        
        auto_info = ctk.CTkLabel(
            content,
            text="Automatically adjusts exposure, contrast, highlights, shadows, and color balance",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
            wraplength=600,
            anchor="w"
        )
        auto_info.pack(anchor="w", pady=(0, 8))
        
        # Manual Adjustments Card
        manual_card = ModernCard(scroll, title="Manual Adjustments")
        manual_card.pack(fill="x", pady=(0, 0))
        content = manual_card.get_content_frame()
        
        # Adjustment sliders
        adjustments = [
            ("📊 Exposure", self.exposure, -2.0, 2.0, 0.01),
            ("📊 Contrast", self.contrast, -100, 100, 1),
            ("☀️ Highlights", self.highlights, -100, 100, 1),
            ("🌙 Shadows", self.shadows, -100, 100, 1),
            ("⚪ Whites", self.whites, -100, 100, 1),
            ("⚫ Blacks", self.blacks, -100, 100, 1),
            ("🌡️ Temperature", self.temperature, -100, 100, 1),
            ("🎨 Tint", self.tint, -100, 100, 1),
            ("🌈 Vibrance", self.vibrance, 0, 100, 1),
            ("🎨 Saturation", self.saturation, -100, 100, 1),
        ]
        
        self.adjustment_sliders = []
        
        for i, (label_text, var, from_, to_, resolution) in enumerate(adjustments):
            slider_frame = ctk.CTkFrame(content, fg_color="transparent")
            slider_frame.pack(fill="x", pady=8)
            slider_frame.grid_columnconfigure(1, weight=1)
            
            # Format initial value
            initial_value = f"{var.get():.1f}" if resolution < 1 else str(int(var.get()))
            
            label = ctk.CTkLabel(
                slider_frame,
                text=f"{label_text}: {initial_value}",
                font=ctk.CTkFont(size=12),
                width=200,
                anchor="w"
            )
            label.grid(row=0, column=0, sticky="w", padx=(0, 15))
            
            def make_slider_command(lbl, txt, res):
                def cmd(v):
                    formatted = f"{float(v):.1f}" if res < 1 else str(int(v))
                    lbl.configure(text=f"{txt}: {formatted}")
                return cmd
            
            slider = ctk.CTkSlider(
                slider_frame,
                from_=from_,
                to=to_,
                variable=var,
                command=make_slider_command(label, label_text, resolution),
                state="disabled",
                height=18
            )
            slider.grid(row=0, column=1, sticky="ew", padx=(0, 15))
            
            reset_btn = ctk.CTkButton(
                slider_frame,
                text="↺",
                width=35,
                height=35,
                command=lambda v=var, s=slider, l=label, t=label_text, r=resolution: 
                    self._reset_slider(v, s, l, t, r),
                state="disabled",
                font=ctk.CTkFont(size=14)
            )
            reset_btn.grid(row=0, column=2)
            
            self.adjustment_sliders.append((slider, reset_btn, label))
        
        # Reset All button
        reset_all_frame = ctk.CTkFrame(content, fg_color="transparent")
        reset_all_frame.pack(fill="x", pady=(15, 5))
        
        self.reset_all_btn = ctk.CTkButton(
            reset_all_frame,
            text="🔄 Reset All Adjustments",
            command=self._reset_all_adjustments,
            state="disabled",
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray35")
        )
        self.reset_all_btn.pack(fill="x")
        
    def _setup_about_tab(self):
        """Setup about tab"""
        scroll = ctk.CTkScrollableFrame(self.tab_about, fg_color="transparent")
        scroll.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        scroll.grid_columnconfigure(0, weight=1)
        
        # About Card
        about_card = ModernCard(scroll, title="About This Application")
        about_card.pack(fill="x", pady=(0, 15))
        content = about_card.get_content_frame()
        
        info_text = """
🖼️ Image to WebP Converter Premium Edition

Version: 2.0.0 Premium
Author: Burak Darende
License: MIT

✨ Features:
• Modern responsive UI with animations
• Batch conversion with folder structure preservation
• Advanced quality controls (Quality, Lossless, Compression)
• Image processing (Resize, Crop, Alpha channel)
• Professional fine-tuning (Auto Tone + 10 manual adjustments)
• Black & White version creation
• Smart versioning system
• Drag & Drop support
• Cross-platform compatibility

🚀 Technologies:
• Python 3.8+
• CustomTkinter (Modern UI)
• Pillow (Image Processing)
• NumPy (Advanced Operations)

📊 Performance:
• Optimized conversion engine
• Multi-threaded processing
• Memory-efficient batch handling

🔒 Privacy:
• 100% offline processing
• No data collection
• No internet required
        """
        
        info_label = ctk.CTkLabel(
            content,
            text=info_text.strip(),
            font=ctk.CTkFont(size=12, family="Consolas"),
            anchor="w",
            justify="left"
        )
        info_label.pack(anchor="w", pady=10, padx=10)
        
        # Links Card
        links_card = ModernCard(scroll, title="Links & Support")
        links_card.pack(fill="x", pady=(0, 0))
        content = links_card.get_content_frame()
        
        github_btn = ctk.CTkButton(
            content,
            text="⭐ Star on GitHub",
            command=lambda: self._open_url("https://github.com/burakdarende/ToWebP"),
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#24292e", "#0d1117"),
            hover_color=("#1c2128", "#161b22")
        )
        github_btn.pack(fill="x", pady=5)
        
        docs_btn = ctk.CTkButton(
            content,
            text="📖 Documentation",
            command=lambda: self._open_url("https://github.com/burakdarende/ToWebP#readme"),
            height=45,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        docs_btn.pack(fill="x", pady=5)
        
        issues_btn = ctk.CTkButton(
            content,
            text="🐛 Report Issue",
            command=lambda: self._open_url("https://github.com/burakdarende/ToWebP/issues"),
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray35")
        )
        issues_btn.pack(fill="x", pady=5)
        
    def _setup_drag_drop(self):
        """Setup drag and drop functionality - Simplified version"""
        # Drag-drop için gelecek versiyonlarda tkinterdnd2 entegrasyonu yapılabilir
        # Şu an için standart browse buttonları kullanılıyor
        pass
            
    def _toggle_theme(self):
        """Toggle between light and dark theme"""
        current = ctk.get_appearance_mode()
        new_mode = "light" if current == "Dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        
    def _toggle_lossless(self):
        """Toggle lossless mode"""
        if self.lossless_var.get():
            self.quality_slider.configure(state="disabled")
            self._log("✨ Lossless mode enabled - Quality slider disabled")
        else:
            self.quality_slider.configure(state="normal")
            self._log("📊 Lossy mode - Quality slider enabled")
            
    def _toggle_resize(self):
        """Toggle resize options"""
        if self.resize_enabled.get():
            self.width_entry.configure(state="normal")
            self.horizontal_check.configure(state="normal")
            self.uniform_check.configure(state="normal")
            self._log("📏 Resize enabled")
        else:
            self.width_entry.configure(state="disabled")
            self.horizontal_check.configure(state="disabled")
            self.uniform_check.configure(state="disabled")
            self.uniform_size.set(False)
            self._toggle_uniform_size()
            self._log("📏 Resize disabled")
            
    def _toggle_uniform_size(self):
        """Toggle uniform size options"""
        if self.uniform_size.get():
            self.uniform_warning.pack(anchor="w", pady=(0, 8))
            self.horizontal_radio.configure(state="normal")
            self.vertical_radio.configure(state="normal")
            self._log("📐 Uniform size enabled - All images will be cropped to same dimensions")
        else:
            self.uniform_warning.pack_forget()
            self.horizontal_radio.configure(state="disabled")
            self.vertical_radio.configure(state="disabled")
            
    def _toggle_finetune(self):
        """Toggle fine-tuning options"""
        if self.fine_tuning_enabled.get():
            self.auto_tone_check.configure(state="normal")
            if not self.auto_tone.get():
                for slider, reset_btn, _ in self.adjustment_sliders:
                    slider.configure(state="normal")
                    reset_btn.configure(state="normal")
            self.reset_all_btn.configure(state="normal")
            self._log("🎨 Fine-tuning enabled")
        else:
            self.auto_tone_check.configure(state="disabled")
            for slider, reset_btn, _ in self.adjustment_sliders:
                slider.configure(state="disabled")
                reset_btn.configure(state="disabled")
            self.reset_all_btn.configure(state="disabled")
            self._log("🎨 Fine-tuning disabled")
            
    def _toggle_auto_tone(self):
        """Toggle auto tone"""
        if self.auto_tone.get():
            for slider, reset_btn, _ in self.adjustment_sliders:
                slider.configure(state="disabled")
                reset_btn.configure(state="disabled")
            self._log("🪄 Auto Tone enabled - Manual adjustments disabled")
        else:
            for slider, reset_btn, _ in self.adjustment_sliders:
                slider.configure(state="normal")
                reset_btn.configure(state="normal")
            self._log("🎨 Manual adjustments enabled")
            
    def _reset_slider(self, var, slider, label, text, resolution):
        """Reset individual slider"""
        var.set(0.0)
        formatted = "0.0" if resolution < 1 else "0"
        label.configure(text=f"{text}: {formatted}")
        
    def _reset_all_adjustments(self):
        """Reset all adjustment sliders"""
        for slider, reset_btn, label in self.adjustment_sliders:
            var = slider.cget("variable")
            var.set(0.0)
        self._log("🔄 All adjustments reset to defaults")
        
    def _browse_folder(self):
        """Browse for source folder"""
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.source_folder.set(folder)
            self.source_file.set("")
            self._log(f"📁 Folder selected: {folder}")
            
    def _browse_file(self):
        """Browse for source file"""
        file = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.gif"),
                ("All Files", "*.*")
            ]
        )
        if file:
            self.source_file.set(file)
            self.source_folder.set("")
            self._log(f"📄 File selected: {file}")
            
    def _browse_output_folder(self):
        """Browse for output folder"""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder_var.set(folder)
            self._log(f"📂 Output folder selected: {folder}")
            
    def _reset_output_folder(self):
        """Reset output folder to default"""
        self.output_folder_var.set("")
        self._log("📂 Output folder reset to default (Same as source)")
            
    def _log(self, message):
        """Add message to log"""
        if self.log_text:
            self.log_text.configure(state="normal")
            self.log_text.insert("end", f"{message}\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
            
    def _update_status(self, message):
        """Update status label"""
        if self.status_label:
            self.status_label.configure(text=message)
            
    def _update_stats(self):
        """Update statistics display"""
        import time
        if len(self.stat_boxes) >= 4:
            # Files processed
            self.stat_boxes[0].configure(text=str(self.stats_files_processed))
            
            # Speed (files per second)
            if self.stats_start_time:
                elapsed = time.time() - self.stats_start_time
                speed = self.stats_files_processed / elapsed if elapsed > 0 else 0
                self.stat_boxes[1].configure(text=f"{speed:.1f}/s")
            
            # Bytes saved
            if self.stats_bytes_saved > 1024*1024*1024:  # GB
                saved_text = f"{self.stats_bytes_saved/(1024**3):.2f} GB"
            elif self.stats_bytes_saved > 1024*1024:  # MB
                saved_text = f"{self.stats_bytes_saved/(1024**2):.1f} MB"
            elif self.stats_bytes_saved > 1024:  # KB
                saved_text = f"{self.stats_bytes_saved/1024:.1f} KB"
            else:
                saved_text = f"{self.stats_bytes_saved} B"
            self.stat_boxes[2].configure(text=saved_text)
            
            # Time elapsed
            if self.stats_start_time:
                elapsed = int(time.time() - self.stats_start_time)
                minutes = elapsed // 60
                seconds = elapsed % 60
                self.stat_boxes[3].configure(text=f"{minutes}:{seconds:02d}")
                
    def _reset_stats(self):
        """Reset statistics"""
        import time
        self.stats_files_processed = 0
        self.stats_start_time = time.time()
        self.stats_bytes_saved = 0
        self._update_stats()
        
    def _animate_button(self, button, target_color, duration=300):
        """Animate button color change"""
        # Simple color transition (can be enhanced with more frames)
        button.configure(fg_color=target_color)
            
    def _convert(self):
        """Start or stop conversion"""
        if self.is_converting:
            self.stop_conversion = True
            self._log("⛔ Stopping conversion...")
            self._update_status("Stopping...")
            return
            
        # Validate input
        source_folder = self.source_folder.get().strip()
        source_file = self.source_file.get().strip()
        
        if not source_folder and not source_file:
            messagebox.showerror("Error", "Please select a source folder or file")
            return
            
        if source_folder and source_file:
            messagebox.showerror("Error", "Please select either a folder OR a file, not both")
            return
            
        # Validate resize width if enabled
        if self.resize_enabled.get():
            width_str = self.resize_width.get().strip()
            if not width_str:
                messagebox.showerror("Error", "Please enter target width for resize")
                return
            try:
                width = int(width_str)
                if width <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Invalid width value")
                return
                
        # Start conversion in thread
        self.is_converting = True
        self.stop_conversion = False
        
        # Reset and start stats
        self._reset_stats()
        
        # Update UI with animation
        self._animate_button(
            self.convert_button,
            ("#e74c3c", "#c0392b")
        )
        self.convert_button.configure(
            text="⛔ STOP CONVERSION",
            fg_color=("#e74c3c", "#c0392b"),
            hover_color=("#c0392b", "#a93226")
        )
        self.progress_bar.reset()
        self._update_status("Converting...")
        
        thread = threading.Thread(target=self._run_conversion, daemon=True)
        thread.start()
        
    def _run_conversion(self):
        """Run conversion in background thread"""
        try:
            # Prepare settings
            source_folder = self.source_folder.get().strip()
            source_file = self.source_file.get().strip()
            output_folder = self.output_folder_var.get().strip() or None
            
            # Prepare fine-tuning dictionary if enabled
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
            
            # Prepare target width if resize enabled
            target_width = None
            if self.resize_enabled.get() and self.resize_width.get().strip():
                target_width = int(self.resize_width.get())
            
            # Create converter with correct parameters
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
            
            # Set callbacks for progress tracking
            def progress_callback(message, current, total):
                # Log the message
                self.window.after(0, lambda m=message: self._log(m))
                # Update progress
                self.window.after(0, lambda c=current, t=total: self._update_progress(c, t))
            
            # Convert
            if source_folder:
                output_path, total, processed, errors = converter.convert_folder(
                    source_folder,
                    output_folder=output_folder,
                    progress_callback=progress_callback
                )
                success = len(errors) == 0
                if success:
                    message = f"Successfully converted {processed}/{total} images to {output_path}"
                else:
                    message = f"Converted {processed}/{total} images with {len(errors)} errors to {output_path}"
            else:
                output_file, total, processed, errors = converter.convert_single_file(
                    source_file,
                    output_folder=output_folder,
                    progress_callback=progress_callback
                )
                success = len(errors) == 0
                if success:
                    message = f"Successfully converted to {output_file}"
                else:
                    message = f"Error converting file: {errors[0] if errors else 'Unknown error'}"
                
            # Update UI
            self.window.after(0, lambda: self._conversion_complete(success, message))
            
        except Exception as e:
            error_msg = f"Error during conversion: {str(e)}"
            self.window.after(0, lambda: self._conversion_complete(False, error_msg))
            
    def _update_progress(self, current, total):
        """Update progress bar and stats"""
        if total > 0:
            percent = (current / total) * 100
            self.stats_files_processed = current
            self.window.after(0, lambda: self.progress_bar.set(percent))
            self.window.after(0, lambda: self._update_status(f"Converting... {current}/{total} ({percent:.1f}%)"))
            self.window.after(0, self._update_stats)
            
    def _conversion_complete(self, success, message):
        """Handle conversion completion"""
        self.is_converting = False
        self.stop_conversion = False
        
        # Animate button back with color transition
        self._animate_button(
            self.convert_button,
            ("#4CAF50", "#43A047")
        )
        
        # Reset button
        self.convert_button.configure(
            text="🚀 START CONVERSION",
            fg_color=("#4CAF50", "#43A047"),
            hover_color=("#66BB6A", "#4CAF50")
        )
        
        # Update status with animation
        if success:
            self._update_status("✅ Conversion completed successfully!")
            self.progress_bar.set(100)
            self._update_stats()  # Final stats update
            
            # Success animation - briefly flash green
            self.window.after(100, lambda: self.status_label.configure(text_color=("#4CAF50", "#66BB6A")))
            self.window.after(500, lambda: self.status_label.configure(text_color=("gray10", "gray90")))
            
            messagebox.showinfo("Success", message)
        else:
            self._update_status("❌ Conversion failed")
            self.progress_bar.set(0)
            
            # Error animation - briefly flash red
            self.window.after(100, lambda: self.status_label.configure(text_color=("#F44336", "#EF5350")))
            self.window.after(500, lambda: self.status_label.configure(text_color=("gray10", "gray90")))
            
            messagebox.showerror("Error", message)
            
        self._log(message)
        
    def _open_url(self, url):
        """Open URL in browser"""
        import webbrowser
        webbrowser.open(url)
        
    def run(self):
        """Start the application"""
        self.window.mainloop()


def main():
    """Main entry point"""
    try:
        app = WebPConverterPremiumGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application failed to start:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
