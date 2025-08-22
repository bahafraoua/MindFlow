import base64
import io
import numpy as np
from PIL import Image
import streamlit as st


def resize_image_numpy(img_array, target_size=256):
    """
    Simple numpy-based image resize to fixed dimensions
    
    Args:
        img_array: numpy array of image
        target_size: target width and height (square)
    
    Returns:
        numpy array: resized image
    """
    original_height, original_width = img_array.shape[:2]

    y_step = original_height / target_size
    x_step = original_width / target_size
    
    y_indices = np.round(np.arange(target_size) * y_step).astype(int)
    x_indices = np.round(np.arange(target_size) * x_step).astype(int)
    
    y_indices = np.clip(y_indices, 0, original_height - 1)
    x_indices = np.clip(x_indices, 0, original_width - 1)
    
    if len(img_array.shape) == 3: 
        resized = img_array[np.ix_(y_indices, x_indices)]
    else:  
        resized = img_array[np.ix_(y_indices, x_indices)]
    
    return resized


def compress_image_to_base64(image, target_size=256, quality=85):
    """
    Compress PIL Image to fixed size using numpy and convert to base64
    
    Args:
        image: PIL Image object
        target_size: target width and height (default: 256x256)
        quality: JPEG quality (1-100)
    
    Returns:
        tuple: (base64_string, compression_info)
    """
    try:
        original_width, original_height = image.size
        print(f"Original: {original_width}x{original_height}")
        
        img_array = np.array(image)
        resized_array = resize_image_numpy(img_array, target_size)
        
        compressed_image = Image.fromarray(resized_array.astype(np.uint8))
        
        if compressed_image.mode in ('RGBA', 'LA', 'P'):
            rgb_image = Image.new('RGB', compressed_image.size, (255, 255, 255))
            if compressed_image.mode == 'P':
                compressed_image = compressed_image.convert('RGBA')
            rgb_image.paste(compressed_image, mask=compressed_image.split()[-1] if compressed_image.mode in ('RGBA', 'LA') else None)
            compressed_image = rgb_image
        
        img_byte_arr = io.BytesIO()
        compressed_image.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
        img_byte_arr = img_byte_arr.getvalue()
        image_base64 = base64.b64encode(img_byte_arr).decode('utf-8')

        compression_info = {
            'original_size': (original_width, original_height),
            'new_size': (target_size, target_size),
            'original_size_pixels': original_width * original_height,
            'current_size_pixels': target_size * target_size,
            'quality': quality,
            'method': 'numpy_fixed'
        }
        return image_base64, compression_info
        
    except Exception as e:
        st.error(f"❌ Compression failed: {str(e)}")
        return None, {'error': str(e)}
