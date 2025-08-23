import base64
import io
import numpy as np
import cv2
from PIL import Image
import streamlit as st


def resize_image_cv2(img_array, width=25, height=25):
    """
    Simple CV2-based image resize to fixed dimensions
    
    Args:
        img_array: numpy array of image
        width: target width (default: 25)
        height: target height (default: 25)
    
    Returns:
        numpy array: resized image
    """
    resized = cv2.resize(img_array, (width, height), interpolation=cv2.INTER_AREA)
    return resized


def compress_image_to_base64(image, width=25, height=25, quality=85):
    """
    Compress PIL Image to fixed size using cv2 and convert to base64
    
    Args:
        image: PIL Image object
        width: target width (default: 25)
        height: target height (default: 25)
        quality: JPEG quality (1-100)
    
    Returns:
        tuple: (base64_string, compression_info)
    """
    try:
        original_width, original_height = image.size
        
        # Convert to numpy and resize using cv2
        img_array = np.array(image)
        resized_array = resize_image_cv2(img_array, width, height)
        
        # Convert back to PIL
        compressed_image = Image.fromarray(resized_array.astype(np.uint8))
        
        # Ensure RGB mode for JPEG
        if compressed_image.mode in ('RGBA', 'LA', 'P'):
            rgb_image = Image.new('RGB', compressed_image.size, (255, 255, 255))
            if compressed_image.mode == 'P':
                compressed_image = compressed_image.convert('RGBA')
            rgb_image.paste(compressed_image, mask=compressed_image.split()[-1] if compressed_image.mode in ('RGBA', 'LA') else None)
            compressed_image = rgb_image
        
        # Convert to base64
        img_byte_arr = io.BytesIO()
        compressed_image.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
        img_byte_arr = img_byte_arr.getvalue()
        image_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
        
        # Create compression info
        compression_info = {
            'original_size': (original_width, original_height),
            'new_size': (width, height),
            'original_size_pixels': original_width * original_height,
            'current_size_pixels': width * height,
            'quality': quality,
            'method': 'cv2_resize'
        }
        return image_base64, compression_info
        
    except Exception as e:
        st.error(f"❌ Compression failed: {str(e)}")
        return None, {'error': str(e)}
