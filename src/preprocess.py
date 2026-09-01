import numpy as np
import pydicom

def load_dicom_scan(file_path):
    """Loads a DICOM file and returns the pixel array converted to Hounsfield Units (HU)."""
    dicom = pydicom.dcmread(file_path)
    image = dicom.pixel_array.astype(np.float32)
    
    # Convert raw values to Hounsfield Units using metadata rescale values
    if hasattr(dicom, 'RescaleSlope') and hasattr(dicom, 'RescaleIntercept'):
        slope = dicom.RescaleSlope
        intercept = dicom.RescaleIntercept
        image = image * slope + intercept
        
    return image, dicom

def apply_ct_window(image, window_center=40, window_width=400):
    """Applies tissue-specific HU windowing and normalizes image to [0, 1]."""
    min_value = window_center - (window_width / 2.0)
    max_value = window_center + (window_width / 2.0)
    
    windowed = np.clip(image, min_value, max_value)
    normalized = (windowed - min_value) / (max_value - min_value)
    return normalized