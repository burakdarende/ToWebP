"""
Image to WebP Converter Core Module
Handles the conversion logic and folder structure replication
"""
import os
import shutil
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from typing import Callable, Optional


class ImageToWebPConverter:
    """Core converter class for image to WebP conversion"""
    
    # Supported image formats
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}
    
    def __init__(self, quality: int = 85, lossless: bool = False, method: int = 6, target_width: int = None, preserve_alpha: bool = True, create_bw: bool = False, fine_tuning: dict = None, make_horizontal: bool = False, uniform_size: bool = False, uniform_orientation: str = "horizontal"):
        """
        Initialize converter with settings
        
        Args:
            quality: Quality setting (0-100) for lossy compression
            lossless: Use lossless compression
            method: Compression method (0-6, higher = better compression but slower)
            target_width: Target width for resizing (height will be calculated proportionally)
            preserve_alpha: Preserve alpha/transparency channel (if False, converts to white background)
            create_bw: Create additional black & white version with _bw suffix
            fine_tuning: Dictionary of fine-tuning adjustments (exposure, contrast, etc.)
            make_horizontal: If True, vertical images will be padded to match target width (landscape mode)
            uniform_size: If True, all images will be cropped to same dimensions
            uniform_orientation: Target orientation for uniform size ('horizontal' or 'vertical')
        """
        self.quality = quality
        self.lossless = lossless
        self.method = method
        self.target_width = target_width
        self.preserve_alpha = preserve_alpha
        self.create_bw = create_bw
        self.fine_tuning = fine_tuning or {}
        self.make_horizontal = make_horizontal
        self.uniform_size = uniform_size
        self.uniform_orientation = uniform_orientation
        self.total_files = 0
        self.processed_files = 0
        self.errors = []
        self.should_stop = False
        self.uniform_dimensions = None  # Will store calculated uniform dimensions
        
    def convert_folder(
        self, 
        source_folder: str, 
        progress_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> tuple[str, int, int, list]:
        """
        Convert all images in source folder to WebP, maintaining folder structure
        
        Args:
            source_folder: Path to source folder
            progress_callback: Optional callback(message, current, total)
            
        Returns:
            Tuple of (output_folder, total_files, processed_files, errors)
        """
        source_path = Path(source_folder)
        if not source_path.exists():
            raise ValueError(f"Source folder does not exist: {source_folder}")
            
        # Create output folder name with versioning
        output_folder = self._get_unique_folder_name(source_folder)
        output_path = Path(output_folder)
        
        # Reset counters
        self.total_files = 0
        self.processed_files = 0
        self.errors = []
        
        # Count total files first
        self._count_images(source_path)
        
        # Analyze folder for uniform size if enabled
        if self.uniform_size and self.target_width:
            self.uniform_dimensions = self._calculate_uniform_dimensions(source_path, progress_callback)
        
        # Create output folder
        output_path.mkdir(exist_ok=True)
        
        # Process all files
        self._process_directory(source_path, output_path, source_path, progress_callback)
        
        return output_folder, self.total_files, self.processed_files, self.errors
    
    def convert_single_file(
        self,
        source_file: str,
        progress_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> tuple[str, int, int, list]:
        """
        Convert a single image file to WebP
        
        Args:
            source_file: Path to source image file
            progress_callback: Optional callback(message, current, total)
            
        Returns:
            Tuple of (output_file, total_files=1, processed_files, errors)
        """
        source_path = Path(source_file)
        if not source_path.exists():
            raise ValueError(f"Source file does not exist: {source_file}")
        
        if not source_path.is_file():
            raise ValueError(f"Source path is not a file: {source_file}")
        
        # Check if it's a supported format
        if source_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported file format: {source_path.suffix}")
        
        # Reset counters
        self.total_files = 1
        self.processed_files = 0
        self.errors = []
        self.should_stop = False
        
        # Create output file path with versioning
        output_file = self._get_unique_file_name(source_path)
        
        # Convert the file (check for stop)
        if not self.should_stop:
            self._convert_image(source_path, source_path.parent, progress_callback, output_file)
        
        return str(output_file), self.total_files, self.processed_files, self.errors
    
    def _count_images(self, directory: Path) -> None:
        """Count total number of images to process"""
        for item in directory.rglob('*'):
            if item.is_file() and item.suffix.lower() in self.SUPPORTED_FORMATS:
                self.total_files += 1
    
    def _process_directory(
        self, 
        source_dir: Path, 
        output_dir: Path, 
        root_source: Path,
        progress_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> None:
        """
        Recursively process directory and maintain structure
        
        Args:
            source_dir: Current source directory
            output_dir: Current output directory
            root_source: Root source directory for relative path calculation
            progress_callback: Progress callback function
        """
        for item in source_dir.iterdir():
            # Check if stop requested
            if self.should_stop:
                return
                
            if item.is_file():
                # Check if it's a supported image format
                if item.suffix.lower() in self.SUPPORTED_FORMATS:
                    self._convert_image(item, output_dir, progress_callback)
                else:
                    # Copy non-image files as-is
                    try:
                        shutil.copy2(item, output_dir / item.name)
                    except Exception as e:
                        self.errors.append(f"Error copying {item.name}: {str(e)}")
                        
            elif item.is_dir():
                # Create corresponding subdirectory (without _WebP suffix)
                new_output_dir = output_dir / item.name
                new_output_dir.mkdir(exist_ok=True)
                
                # Recursively process subdirectory
                self._process_directory(item, new_output_dir, root_source, progress_callback)
    
    def _convert_image(
        self, 
        image_path: Path, 
        output_dir: Path,
        progress_callback: Optional[Callable[[str, int, int], None]] = None,
        custom_output_path: Path = None
    ) -> None:
        """
        Convert a single image to WebP
        
        Args:
            image_path: Path to source image
            output_dir: Output directory
            progress_callback: Progress callback function
            custom_output_path: Custom output path (for single file conversion with versioning)
        """
        try:
            # Open and convert image
            with Image.open(image_path) as img:
                # Resize if target width is specified
                if self.target_width and self.target_width > 0:
                    original_width, original_height = img.size
                    
                    # Uniform size mode: crop all images to same dimensions
                    if self.uniform_size and self.uniform_dimensions:
                        target_w, target_h = self.uniform_dimensions
                        img = self._crop_to_uniform_size(img, target_w, target_h)
                    
                    elif original_width != self.target_width:
                        # Calculate proportional height
                        aspect_ratio = original_height / original_width
                        new_height = int(self.target_width * aspect_ratio)
                        img = img.resize((self.target_width, new_height), Image.Resampling.LANCZOS)
                        
                        # Make horizontal: crop vertical images to landscape format
                        if self.make_horizontal and new_height > self.target_width:
                            # Image is vertical (height > width), crop to square/landscape
                            # Calculate crop to make it landscape (width = height or width > height)
                            target_height = self.target_width  # Make it square based on target width
                            
                            # Calculate how much to crop from top and bottom
                            crop_total = new_height - target_height
                            crop_top = crop_total // 2
                            crop_bottom = crop_total - crop_top
                            
                            # Crop from center
                            left = 0
                            top = crop_top
                            right = self.target_width
                            bottom = new_height - crop_bottom
                            
                            img = img.crop((left, top, right, bottom))
                
                # Convert RGBA to RGB if necessary
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    if self.preserve_alpha:
                        # Keep alpha channel - convert to RGBA
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        elif img.mode == 'LA':
                            img = img.convert('RGBA')
                        # RGBA stays as is
                    else:
                        # Remove alpha channel - convert to RGB with white background
                        if img.mode in ('RGBA', 'LA'):
                            background = Image.new('RGB', img.size, (255, 255, 255))
                            if img.mode == 'RGBA':
                                background.paste(img, mask=img.split()[-1])
                            else:
                                background.paste(img.convert('RGB'))
                            img = background
                        elif img.mode == 'P':
                            img = img.convert('RGB')
                elif img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Apply fine-tuning adjustments if enabled
                if self.fine_tuning:
                    img = self._apply_fine_tuning(img)
                
                # Create output path with .webp extension
                if custom_output_path:
                    output_path = custom_output_path
                else:
                    output_path = output_dir / f"{image_path.stem}.webp"
                
                # Save color version as WebP
                img.save(
                    output_path,
                    'WEBP',
                    quality=self.quality,
                    lossless=self.lossless,
                    method=self.method
                )
                
                # Create black & white version if enabled
                if self.create_bw:
                    # Use custom output path for B&W version if provided
                    if custom_output_path:
                        # Get version suffix from custom output path if exists
                        if '_WebP_' in custom_output_path.stem:
                            # Extract version number (e.g., image_WebP_2 -> _bw_WebP_2)
                            base_name = image_path.stem
                            version_suffix = custom_output_path.stem.replace(base_name, '')
                            bw_output_path = output_dir / f"{base_name}_bw{version_suffix}.webp"
                        else:
                            bw_output_path = output_dir / f"{image_path.stem}_bw.webp"
                    else:
                        bw_output_path = output_dir / f"{image_path.stem}_bw.webp"
                    
                    # Convert to grayscale
                    if img.mode == 'RGBA':
                        # Convert RGBA to LA (grayscale with alpha)
                        bw_img = img.convert('LA').convert('RGBA')
                    else:
                        # Convert to grayscale (L mode)
                        bw_img = img.convert('L')
                    
                    # Save B&W version with same settings
                    bw_img.save(
                        bw_output_path,
                        'WEBP',
                        quality=self.quality,
                        lossless=self.lossless,
                        method=self.method
                    )
                
            self.processed_files += 1
            
            if progress_callback:
                resize_info = f" (resized to {self.target_width}px width)" if self.target_width else ""
                bw_info = " + B&W version" if self.create_bw else ""
                progress_callback(
                    f"Converted: {image_path.name}{resize_info}{bw_info}", 
                    self.processed_files, 
                    self.total_files
                )
                
        except Exception as e:
            error_msg = f"Error converting {image_path.name}: {str(e)}"
            self.errors.append(error_msg)
            if progress_callback:
                progress_callback(error_msg, self.processed_files, self.total_files)
    
    def _apply_fine_tuning(self, img: Image.Image) -> Image.Image:
        """
        Apply fine-tuning adjustments to image
        
        Args:
            img: PIL Image object
            
        Returns:
            Adjusted PIL Image object
        """
        # Work with a copy to preserve original
        adjusted = img.copy()
        
        # Convert to RGB for processing if needed (preserve alpha separately)
        has_alpha = adjusted.mode == 'RGBA'
        if has_alpha:
            alpha = adjusted.split()[-1]
            adjusted = adjusted.convert('RGB')
        
        # Check for Auto Tone
        if self.fine_tuning.get('auto_tone', False):
            # Apply automatic tone adjustments
            adjusted = self._apply_auto_tone(adjusted)
        else:
            # Manual adjustments
            # Brightness/Exposure
            if self.fine_tuning.get('exposure', 0) != 0:
                factor = 1.0 + (self.fine_tuning['exposure'] * 0.5)  # -2 to +2 becomes 0 to 2
                enhancer = ImageEnhance.Brightness(adjusted)
                adjusted = enhancer.enhance(factor)
        
            # Contrast
            if self.fine_tuning.get('contrast', 0) != 0:
                factor = 1.0 + (self.fine_tuning['contrast'] / 100.0)
                enhancer = ImageEnhance.Contrast(adjusted)
                adjusted = enhancer.enhance(max(0.1, factor))
            
            # Color/Saturation
            if self.fine_tuning.get('saturation', 0) != 0:
                factor = 1.0 + (self.fine_tuning['saturation'] / 100.0)
                enhancer = ImageEnhance.Color(adjusted)
                adjusted = enhancer.enhance(max(0, factor))
            
            # Vibrance (more subtle saturation on less saturated colors)
            if self.fine_tuning.get('vibrance', 0) != 0:
                factor = 1.0 + (self.fine_tuning['vibrance'] / 200.0)  # Half the effect of saturation
                enhancer = ImageEnhance.Color(adjusted)
                adjusted = enhancer.enhance(max(0, factor))
            
            # Temperature (warm/cool adjustment)
            if self.fine_tuning.get('temperature', 0) != 0:
                adjusted = self._adjust_temperature(adjusted, self.fine_tuning['temperature'])
            
            # Tint (green/magenta adjustment)
            if self.fine_tuning.get('tint', 0) != 0:
                adjusted = self._adjust_tint(adjusted, self.fine_tuning['tint'])
            
            # Shadows/Highlights/Whites/Blacks - simplified tone curve adjustment
            if any(self.fine_tuning.get(k, 0) != 0 for k in ['shadows', 'highlights', 'whites', 'blacks']):
                adjusted = self._adjust_tones(
                    adjusted,
                    self.fine_tuning.get('shadows', 0),
                    self.fine_tuning.get('highlights', 0),
                    self.fine_tuning.get('whites', 0),
                    self.fine_tuning.get('blacks', 0)
                )
        
        # Restore alpha channel if it existed
        if has_alpha:
            adjusted = adjusted.convert('RGBA')
            adjusted.putalpha(alpha)
        
        return adjusted
    
    def _adjust_temperature(self, img: Image.Image, temp: float) -> Image.Image:
        """Adjust color temperature (warm/cool)"""
        r, g, b = img.split()
        
        # Positive = warmer (more red/yellow), Negative = cooler (more blue)
        factor = temp / 100.0
        
        if factor > 0:  # Warmer
            r = ImageEnhance.Brightness(r).enhance(1.0 + factor * 0.3)
            b = ImageEnhance.Brightness(b).enhance(1.0 - factor * 0.3)
        else:  # Cooler
            r = ImageEnhance.Brightness(r).enhance(1.0 + factor * 0.3)
            b = ImageEnhance.Brightness(b).enhance(1.0 - factor * 0.3)
        
        return Image.merge('RGB', (r, g, b))
    
    def _adjust_tint(self, img: Image.Image, tint: float) -> Image.Image:
        """Adjust tint (green/magenta)"""
        r, g, b = img.split()
        
        # Positive = more magenta, Negative = more green
        factor = tint / 100.0
        
        if factor > 0:  # More magenta (reduce green)
            g = ImageEnhance.Brightness(g).enhance(1.0 - factor * 0.3)
        else:  # More green (reduce red/blue)
            g = ImageEnhance.Brightness(g).enhance(1.0 - factor * 0.3)
        
        return Image.merge('RGB', (r, g, b))
    
    def _adjust_tones(self, img: Image.Image, shadows: float, highlights: float, whites: float, blacks: float) -> Image.Image:
        """Adjust tonal ranges (shadows, highlights, whites, blacks)"""
        # Convert to numpy array for pixel-level manipulation
        img_array = np.array(img, dtype=np.float32)
        
        # Normalize adjustments
        shadows_adj = shadows / 100.0
        highlights_adj = highlights / 100.0
        whites_adj = whites / 100.0
        blacks_adj = blacks / 100.0
        
        # Create luminosity mask (0-1 range)
        luminosity = np.mean(img_array, axis=2) / 255.0
        
        # Apply adjustments based on tonal range
        # Shadows (dark areas, luminosity < 0.3)
        shadow_mask = np.maximum(0, 1 - (luminosity / 0.3)) ** 2
        shadow_mask = np.stack([shadow_mask] * 3, axis=2)
        img_array += shadow_mask * shadows_adj * 50
        
        # Highlights (bright areas, luminosity > 0.7)
        highlight_mask = np.maximum(0, (luminosity - 0.7) / 0.3) ** 2
        highlight_mask = np.stack([highlight_mask] * 3, axis=2)
        img_array += highlight_mask * highlights_adj * 50
        
        # Whites (very bright, luminosity > 0.85)
        white_mask = np.maximum(0, (luminosity - 0.85) / 0.15) ** 2
        white_mask = np.stack([white_mask] * 3, axis=2)
        img_array += white_mask * whites_adj * 30
        
        # Blacks (very dark, luminosity < 0.15)
        black_mask = np.maximum(0, 1 - (luminosity / 0.15)) ** 2
        black_mask = np.stack([black_mask] * 3, axis=2)
        img_array += black_mask * blacks_adj * 30
        
        # Clip values to valid range
        img_array = np.clip(img_array, 0, 255)
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    def _apply_auto_tone(self, img: Image.Image) -> Image.Image:
        """
        Apply automatic tone adjustments (like Photoshop Auto Tone)
        Uses histogram analysis for intelligent corrections
        
        Args:
            img: PIL Image object (RGB)
            
        Returns:
            Auto-corrected PIL Image object
        """
        # Convert to numpy for analysis
        img_array = np.array(img, dtype=np.float32)
        
        # Analyze histogram for each channel
        adjusted = img_array.copy()
        
        # 1. Auto Levels - Stretch histogram to full range
        for i in range(3):  # R, G, B
            channel = adjusted[:, :, i]
            
            # Find 1st and 99th percentile (ignore extreme outliers)
            low_percentile = np.percentile(channel, 1)
            high_percentile = np.percentile(channel, 99)
            
            # Stretch the histogram
            if high_percentile > low_percentile:
                channel = (channel - low_percentile) * (255.0 / (high_percentile - low_percentile))
                channel = np.clip(channel, 0, 255)
                adjusted[:, :, i] = channel
        
        # 2. Auto Contrast - Enhance overall contrast
        adjusted_img = Image.fromarray(adjusted.astype(np.uint8))
        enhancer = ImageEnhance.Contrast(adjusted_img)
        adjusted_img = enhancer.enhance(1.15)  # Slight contrast boost
        
        # 3. Recover blown highlights and blocked shadows
        adjusted = np.array(adjusted_img, dtype=np.float32)
        luminosity = np.mean(adjusted, axis=2) / 255.0
        
        # Recover highlights (reduce very bright areas slightly)
        highlight_mask = np.maximum(0, (luminosity - 0.85) / 0.15) ** 1.5
        highlight_mask = np.stack([highlight_mask] * 3, axis=2)
        adjusted -= highlight_mask * 25  # Reduce blown highlights
        
        # Open up shadows (brighten very dark areas)
        shadow_mask = np.maximum(0, 1 - (luminosity / 0.25)) ** 1.5
        shadow_mask = np.stack([shadow_mask] * 3, axis=2)
        adjusted += shadow_mask * 30  # Lift shadows
        
        # 4. Auto White Balance - Correct color cast
        # Calculate average color for mid-tones
        mid_tone_mask = (luminosity > 0.3) & (luminosity < 0.7)
        if np.any(mid_tone_mask):
            mid_tone_avg = np.mean(adjusted[mid_tone_mask], axis=0)
            target_gray = np.mean(mid_tone_avg)
            
            # Adjust each channel to neutral
            for i in range(3):
                if mid_tone_avg[i] > 0:
                    correction_factor = target_gray / mid_tone_avg[i]
                    # Apply subtle correction (limit the effect)
                    correction_factor = 1.0 + (correction_factor - 1.0) * 0.3
                    adjusted[:, :, i] *= correction_factor
        
        # 5. Enhance vibrance (boost muted colors more than saturated ones)
        adjusted_img = Image.fromarray(np.clip(adjusted, 0, 255).astype(np.uint8))
        
        # Calculate saturation per pixel
        adjusted_hsv = adjusted_img.convert('HSV')
        h, s, v = adjusted_hsv.split()
        s_array = np.array(s, dtype=np.float32)
        
        # Boost low saturation more than high saturation (vibrance effect)
        saturation_boost = (1 - s_array / 255.0) * 0.4  # More boost for less saturated
        s_array = s_array * (1 + saturation_boost)
        s_array = np.clip(s_array, 0, 255)
        
        # Reconstruct image
        adjusted_hsv = Image.merge('HSV', (h, Image.fromarray(s_array.astype(np.uint8)), v))
        adjusted_img = adjusted_hsv.convert('RGB')
        
        # 6. Final exposure adjustment based on overall brightness
        adjusted = np.array(adjusted_img, dtype=np.float32)
        avg_brightness = np.mean(adjusted) / 255.0
        
        # If image is too dark or too bright, adjust
        if avg_brightness < 0.45:
            # Image is too dark, brighten
            exposure_adjust = (0.5 - avg_brightness) * 0.6
            adjusted *= (1.0 + exposure_adjust)
        elif avg_brightness > 0.65:
            # Image is too bright, darken slightly
            exposure_adjust = (avg_brightness - 0.6) * 0.4
            adjusted *= (1.0 - exposure_adjust)
        
        # Final clip and return
        adjusted = np.clip(adjusted, 0, 255)
        return Image.fromarray(adjusted.astype(np.uint8))
    
    def _get_unique_folder_name(self, base_folder: str) -> str:
        """
        Generate unique folder name with version number if folder exists
        
        Args:
            base_folder: Base folder path
            
        Returns:
            Unique folder path with version suffix if needed
        """
        output_folder = f"{base_folder}_WebP"
        
        # Check if folder already exists
        if not Path(output_folder).exists():
            return output_folder
        
        # Find next available version number
        version = 2
        while True:
            versioned_folder = f"{base_folder}_WebP_{version}"
            if not Path(versioned_folder).exists():
                return versioned_folder
            version += 1
    
    def _get_unique_file_name(self, source_path: Path) -> Path:
        """
        Generate unique file name with version number if file exists
        
        Args:
            source_path: Source file path
            
        Returns:
            Unique output file path with version suffix if needed
        """
        output_file = source_path.parent / f"{source_path.stem}.webp"
        
        # Check if file already exists
        if not output_file.exists():
            return output_file
        
        # Find next available version number
        version = 2
        while True:
            versioned_file = source_path.parent / f"{source_path.stem}_WebP_{version}.webp"
            if not versioned_file.exists():
                return versioned_file
            version += 1
    
    def _calculate_uniform_dimensions(
        self,
        directory: Path,
        progress_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> tuple[int, int]:
        """
        Analyze all images in folder to calculate optimal uniform dimensions
        
        Args:
            directory: Source directory to analyze
            progress_callback: Progress callback function
            
        Returns:
            Tuple of (width, height) for uniform size
        """
        if progress_callback:
            progress_callback("🔍 Analyzing images for optimal dimensions...", 0, self.total_files)
        
        ratios = []
        
        # Collect aspect ratios from all images
        for item in directory.rglob('*'):
            if item.is_file() and item.suffix.lower() in self.SUPPORTED_FORMATS:
                try:
                    with Image.open(item) as img:
                        width, height = img.size
                        ratio = height / width
                        ratios.append(ratio)
                except Exception:
                    continue
        
        if not ratios:
            # Fallback: use target width with square dimensions
            return (self.target_width, self.target_width)
        
        # Calculate median ratio (more robust than mean)
        ratios.sort()
        median_ratio = ratios[len(ratios) // 2]
        
        # Calculate dimensions based on orientation preference
        if self.uniform_orientation == "horizontal":
            # Width is target_width, calculate height from median ratio
            target_width = self.target_width
            target_height = int(target_width * median_ratio)
            
            # Ensure it's landscape (width >= height)
            if target_height > target_width:
                # Flip: make it landscape
                target_height = int(target_width / median_ratio)
                if target_height > target_width:
                    # Still taller, force square
                    target_height = target_width
        else:  # vertical
            # Width is target_width, but we want portrait
            target_width = self.target_width
            target_height = int(target_width * median_ratio)
            
            # Ensure it's portrait (height >= width)
            if target_height < target_width:
                # Make it taller
                target_height = int(target_width * 1.5)  # 2:3 ratio for portrait
        
        if progress_callback:
            progress_callback(
                f"📐 Calculated uniform dimensions: {target_width}x{target_height} (ratio: {target_height/target_width:.2f})",
                0,
                self.total_files
            )
        
        return (target_width, target_height)
    
    def _crop_to_uniform_size(self, img: Image.Image, target_w: int, target_h: int) -> Image.Image:
        """
        Resize and crop image to exact uniform dimensions
        
        Args:
            img: PIL Image object
            target_w: Target width
            target_h: Target height
            
        Returns:
            Resized and cropped image
        """
        original_w, original_h = img.size
        target_ratio = target_h / target_w
        original_ratio = original_h / original_w
        
        # Resize image to cover target dimensions (larger dimension)
        if original_ratio > target_ratio:
            # Image is taller, fit to width
            new_width = target_w
            new_height = int(target_w * original_ratio)
        else:
            # Image is wider, fit to height
            new_height = target_h
            new_width = int(target_h / original_ratio)
        
        # Resize with high quality
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Calculate crop coordinates (center crop)
        left = (new_width - target_w) // 2
        top = (new_height - target_h) // 2
        right = left + target_w
        bottom = top + target_h
        
        # Crop to exact dimensions
        img = img.crop((left, top, right, bottom))
        
        return img


