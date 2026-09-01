import streamlit as st
import matplotlib.pyplot as plt
from src.preprocess import load_dicom_scan, apply_ct_window

st.set_page_config(page_title="CT Medical Imaging Pipeline", layout="wide")
st.title("🏥 Medical Imaging CT Scan Analysis Pipeline")

uploaded_file = st.sidebar.file_uploader("Upload DICOM (.dcm) file", type=["dcm"])
preset = st.sidebar.selectbox("Tissue Preset", ["Soft Tissue (40/400)", "Lung (-600/1500)", "Bone (400/1800)"])

# Set HU Center & Width
if preset == "Soft Tissue (40/400)": wc, ww = 40, 400
elif preset == "Lung (-600/1500)": wc, ww = -600, 1500
else: wc, ww = 400, 1800

if uploaded_file:
    with open("temp.dcm", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    image_hu, meta = load_dicom_scan("temp.dcm")
    processed_img = apply_ct_window(image_hu, window_center=wc, window_width=ww)
    
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        ax.imshow(processed_img, cmap="gray")
        ax.axis("off")
        st.pyplot(fig)
    with col2:
        st.json({
            "Patient ID": getattr(meta, "PatientID", "N/A"),
            "Modality": getattr(meta, "Modality", "CT"),
            "Slice Thickness": f"{getattr(meta, 'SliceThickness', 'N/A')} mm",
            "Dimensions": f"{image_hu.shape[0]}x{image_hu.shape[1]}"
        })
else:
    st.info("Upload a `.dcm` DICOM file in the sidebar to visualize.")