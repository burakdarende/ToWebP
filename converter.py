"""
Image to WebP Converter Core Module
Handles the conversion logic and folder structure replication
"""
import os
import shutil
from pathlib import Path
from PIL import Image
from typing import Callable, Optional


class ImageToWebPConverter:
    """Core converter class for image to WebP conversion"""
    
    # Supported image formats
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}
    
    def __init__(self, quality: int = 85, lossless: bool = False, method: int = 6):
        """
        Initialize converter with settings
        
        Args:
            quality: Quality setting (0-100) for lossy compression
            lossless: Use lossless compression
            method: Compression method (0-6, higher = better compression but slower)
        """
        self.quality = quality
        self.lossless = lossless
        self.method = method
        self.total_files = 0
        self.processed_files = 0
        self.errors = []
        
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
            
        # Create output folder name
        output_folder = f"{source_folder}_WebP"
        output_path = Path(output_folder)
        
        # Reset counters
        self.total_files = 0
        self.processed_files = 0
        self.errors = []
        
        # Count total files first
        self._count_images(source_path)
        
        # Create output folder
        output_path.mkdir(exist_ok=True)
        
        # Process all files
        self._process_directory(source_path, output_path, source_path, progress_callback)
        
        return output_folder, self.total_files, self.processed_files, self.errors
    
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
        progress_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> None:
        """
        Convert a single image to WebP
        
        Args:
            image_path: Path to source image
            output_dir: Output directory
            progress_callback: Progress callback function
        """
        try:
            # Open and convert image
            with Image.open(image_path) as img:
                # Convert RGBA to RGB if necessary for lossy compression
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    # Keep alpha channel for lossless
                    if not self.lossless and img.mode == 'RGBA':
                        # Create white background for lossy
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    elif img.mode == 'P':
                        img = img.convert('RGBA' if self.lossless else 'RGB')
                elif img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Create output path with .webp extension
                output_path = output_dir / f"{image_path.stem}.webp"
                
                # Save as WebP
                img.save(
                    output_path,
                    'WEBP',
                    quality=self.quality,
                    lossless=self.lossless,
                    method=self.method
                )
                
            self.processed_files += 1
            
            if progress_callback:
                progress_callback(
                    f"Converted: {image_path.name}", 
                    self.processed_files, 
                    self.total_files
                )
                
        except Exception as e:
            error_msg = f"Error converting {image_path.name}: {str(e)}"
            self.errors.append(error_msg)
            if progress_callback:
                progress_callback(error_msg, self.processed_files, self.total_files)
