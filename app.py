import streamlit as st
import time
import zipfile
from io import BytesIO
from backend.aipipeline import runbatch_pipeline

# 1. SETUP: High-end config
st.set_page_config(page_title="V2 Retail AI", layout='wide')

# 2. THE AESTHETIC CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;400;600&display=swap');
    
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Background & Font */
    .stApp {
        background: radial-gradient(circle at top right, #34421e, #0f1208);
        color: #f1f8e9;
        font-family: 'Inter', sans-serif;
    }

    /* CENTERED MAIN TITLE [Requirement: Center & No "/"] */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 200;
        letter-spacing: 2px;
        margin-bottom: 0px;
    }
    .main-subtitle {
        text-align: center;
        opacity: 0.7;
        margin-bottom: 40px;
    }

    /* SIDEBAR STYLING [Requirement: White Headings] */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(25px);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    /* 1. Ensure the re-open arrow is visible and white */
    [data-testid="collapsedControl"] {
        color: white !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 0 10px 10px 0 !important;
    }

    /* 2. Fix potential 'hidden' conflict */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* 3. Make sure the sidebar doesn't stay 'hidden' when closed */
    [data-testid="stSidebar"] {
        transition: all 0.3s ease;
    }
    /* Center the Generation Button */
    .stButton>button {
        display: block;
        margin: 0 auto !important;
        background: linear-gradient(90deg, #828e5c, #556b2f) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 15px 50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SIDEBAR: Config & Download Zone
with st.sidebar:
    # Requirement: Logo removed
    st.markdown("## Configuration")
    
    # Requirement: Blank first index for dropdowns
    gender = st.selectbox("Model Gender", options=[None, "Female", "Male"], index=0, format_func=lambda x: "Select Gender" if x is None else x)
    body_type = st.selectbox("Frame Type", options=[None, "Full-Body", "Upper-Body", "Lower-Body"], index=0, format_func=lambda x: "Select Frame" if x is None else x)
    
    st.divider()
    st.markdown("## Export") # Requirement: White Heading
    download_placeholder = st.empty()
    # Requirement: Name change from "Generated renders" to "Download Zip"
    download_placeholder.info("Download Zip will appear here.")

# 4. MAIN PAGE: Centered Hero
st.markdown('<h1 class="main-title">V2 CREATIVE STUDIO</h1>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">High-Fidelity Fashion Synthesis Engine</p>', unsafe_allow_html=True)

# Upload Zone
col_left, col_right = st.columns(2)
with col_left:
    st.markdown("###  1. Design")
    design_files = st.file_uploader("Upload Cloth Designs (Compulsory) *", type=['png', 'jpg',"webp"], accept_multiple_files=True)

with col_right:
    st.markdown("###  2. Pattern")
    pattern_file = st.file_uploader("Upload Pattern/Texture (Optional)", type=['png', 'jpg',"webp"])

st.markdown("<br>", unsafe_allow_html=True)

# 5. EXECUTION LOGIC

if st.button("✨ START BATCH GENERATION"):
    if not gender or not body_type:
        st.error("⚠️ Please select both Gender and Frame Type in the sidebar.")
    elif not design_files:
        st.error("⚠️ Please upload at least one Cloth Design.")
    else:
        with st.status("🔮 V2 Neural Engine is rendering...", expanded=True) as status:
            st.write("📐 Analyzing garment silhouettes...")
            
            # 1. Check if pattern exists to determine the mode
            mode = "Texture Overlay" if pattern_file else "Virtual Try-On"
            st.write(f"🚀 Mode: {mode}")

            # 2. Call the backend
            # Note: We pass 'pattern_file' which might be None. 
            # Your backend should handle this if-else logic.
            results = runbatch_pipeline(design_files, gender, body_type, pattern_file)
            
            st.write("📸 Applying lighting and final touches...")
            time.sleep(1)
            status.update(label=f"✅ {mode} Complete!", state="complete", expanded=False)

        # 3. PREVIEW GALLERY (Main Page)
        st.markdown(f"### Results: {mode}")
        with st.container(height=600, border=False): 
            grid = st.columns(3) 
            zip_buffer = BytesIO()
            
            with zipfile.ZipFile(zip_buffer, "a") as zf:
                for i, res in enumerate(results):
                    with grid[i % 3]:
                        st.image(res['output'], caption=f"Render {i+1}", use_container_width=True)
                    
                    # Force PNG for ZIP
                    img_byte_arr = BytesIO()
                    res['output'].save(img_byte_arr, format='PNG') 
                    zf.writestr(f"V2_Studio_Render_{i+1}.png", img_byte_arr.getvalue())

        # 4. SIDEBAR DOWNLOAD
        with st.sidebar:
            st.success("✨ Batch Ready")
            download_placeholder.download_button(
                label="📥 DOWNLOAD ZIP", 
                data=zip_buffer.getvalue(),
                file_name="v2_studio_results.zip",
                mime="application/zip",
                use_container_width=True
            )