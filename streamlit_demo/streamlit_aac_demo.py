import streamlit as st
import numpy as np
import time
import json
import base64
from io import BytesIO

# Try to import optional packages
try:
    import qrcode
    from PIL import Image
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="AAC Device Demo - DAPP2",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'current_text' not in st.session_state:
    st.session_state.current_text = ""
if 'gaze_x' not in st.session_state:
    st.session_state.gaze_x = 200
if 'gaze_y' not in st.session_state:
    st.session_state.gaze_y = 200
if 'eye_tracking_active' not in st.session_state:
    st.session_state.eye_tracking_active = False

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .section-header {
        color: #2e8b57;
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .intro-text {
        font-size: 1.1rem;
        line-height: 1.6;
        text-align: justify;
    }
    .aac-interface {
        border: 2px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        background-color: #f8f9fa;
        margin: 20px 0;
        text-align: center;
    }
    .eye-tracking-status {
        background-color: #e8f4f8;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        text-align: center;
    }
    .emergency-panel {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .video-container {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .current-text-display {
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 8px;
        font-family: Monaco, monospace;
        font-size: 18px;
        text-align: center;
        margin: 20px 0;
        border: 2px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

class StreamlitAACInterface:
    def __init__(self):
        self.RIGHT = ['a', 'e', 'i', 'o', 'u']
        self.TOP = ["s", "t", "n", "r", "d", "l", "h"]
        self.LEFT = ["c", "w", "m", "g", "y", "p", "f"]
        self.BOTTOM = ["j", "b", "q", "k", "v", "z", "x"]

    def create_circular_interface_html(self):
        """Create an HTML/SVG representation of the circular interface"""
        current_text_display = st.session_state.current_text[-8:] if st.session_state.current_text else "AAC"
        
        html = f"""
        <div style="display: flex; justify-content: center; margin: 20px 0;">
            <svg width="400" height="400" viewBox="0 0 400 400" style="border: 3px solid #333; border-radius: 50%; background: black;">
                <!-- Outer ring -->
                <circle cx="200" cy="200" r="150" fill="none" stroke="white" stroke-width="3"/>
                
                <!-- Sector divisions -->
                <line x1="200" y1="50" x2="200" y2="350" stroke="white" stroke-width="2"/>
                <line x1="50" y1="200" x2="350" y2="200" stroke="white" stroke-width="2"/>
                <line x1="94" y1="94" x2="306" y2="306" stroke="white" stroke-width="2"/>
                <line x1="306" y1="94" x2="94" y2="306" stroke="white" stroke-width="2"/>
                
                <!-- Center circle -->
                <circle cx="200" cy="200" r="50" fill="black" stroke="white" stroke-width="3"/>
                
                <!-- TOP sector letters -->
                <text x="200" y="80" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="12">{', '.join(self.TOP)}</text>
                
                <!-- RIGHT sector letters -->
                <text x="320" y="205" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="12">{', '.join(self.RIGHT)}</text>
                
                <!-- BOTTOM sector letters -->
                <text x="200" y="330" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="12">{', '.join(self.BOTTOM)}</text>
                
                <!-- LEFT sector letters -->
                <text x="80" y="205" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="12">{', '.join(self.LEFT)}</text>
                
                <!-- Center text display -->
                <text x="200" y="210" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="16">{current_text_display}</text>
                
                <!-- Corner buttons -->
                <text x="50" y="50" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="10">NUM</text>
                <text x="350" y="50" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="10">⟲</text>
                <text x="50" y="370" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="10">X</text>
                <text x="350" y="370" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="10">✓</text>
                
                <!-- Gaze indicator (simulated) -->
                <circle cx="{min(400, max(0, st.session_state.gaze_x))}" cy="{min(400, max(0, st.session_state.gaze_y))}" r="6" fill="red" opacity="0.8"/>
            </svg>
        </div>
        """
        return html

def main():
    # Header
    st.markdown('<h1 class="main-header">🗣️ AAC Device Demo - DAPP2</h1>', unsafe_allow_html=True)
    
    # YouTube Video Embed
    st.markdown('<h2 class="section-header">📹 Project Demo Video</h2>', unsafe_allow_html=True)
    
    # Embed YouTube video properly
    st.markdown("""
    <div class="video-container">
        <iframe width="700" height="394" 
                src="https://www.youtube.com/embed/yzSJAeBg88E?autoplay=0&mute=0" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
        </iframe>
    </div>
    """, unsafe_allow_html=True)
    
    # Project Introduction
    st.markdown('<h2 class="section-header">📋 Project Introduction</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        **Cerebral palsy (CP)** is a neurological disorder affecting muscle control and coordination, impacting **17 million people worldwide**. Around **75% of children with CP** experience speech impairments, from mild articulation issues to complete loss of speech.
        
        While Alternative and Augmentative Communication (AAC) devices exist to help, consultations with specialists revealed that current AACs are often **bulky, impractical, and stigmatizing**.
        
        **This project aims to develop a wearable, user-friendly AAC device to improve communication and quality of life for patients and their caregivers.**
        """)
    
    # Final Product Description
    st.markdown('<h2 class="section-header">🎯 Final Product</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    The design uses **Google Glass** with a camera-based eye-tracking system and a circular keyboard interface projected onto the lens. Users select characters by focusing on keys, and the system converts this input into speech, enabling seamless, hands-free communication.
    
    **Enhanced functionality includes:**
    - **Head-tracking for emergency alerts:** Two consecutive left head tilts trigger a call for help, while two right tilts deactivate it.
    - **Visual feedback (LED indicators)** to notify others when the user is speaking.
    - **Speech volume control,** allowing users to adjust output discreetly.
    """)
    
    # Interactive Demo Section
    st.markdown('<h2 class="section-header">🎮 Interactive Demo</h2>', unsafe_allow_html=True)
    
    # Initialize AAC interface
    aac = StreamlitAACInterface()
    
    # Eye tracking status
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("🎯 Start Eye Tracking", key="start_tracking"):
            st.session_state.eye_tracking_active = True
    
    with col2:
        if st.session_state.eye_tracking_active:
            st.success("👁️ Eye tracking active - Use manual controls below!")
        else:
            st.info("👁️ Eye tracking inactive - Click 'Start Eye Tracking' to begin")
    
    with col3:
        if st.button("⏹️ Stop Eye Tracking", key="stop_tracking"):
            st.session_state.eye_tracking_active = False
    
    # AAC Interface Display
    st.markdown('<div class="aac-interface">', unsafe_allow_html=True)
    st.markdown("### Circular AAC Interface")
    
    # Display the circular interface using HTML
    interface_html = aac.create_circular_interface_html()
    st.markdown(interface_html, unsafe_allow_html=True)
    
    # Current text display
    st.markdown(f'<div class="current-text-display">Current Text: {st.session_state.current_text if st.session_state.current_text else "(empty)"}</div>', unsafe_allow_html=True)
    
    # Manual input for testing
    st.markdown("**Manual Testing (for demo purposes):**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Sector 1 (Top) → 's'", key="manual_1"):
            st.session_state.current_text += "s"
            st.rerun()
    with col2:
        if st.button("Sector 2 (Right) → 'a'", key="manual_2"):
            st.session_state.current_text += "a"
            st.rerun()
    with col3:
        if st.button("Sector 3 (Bottom) → 'j'", key="manual_3"):
            st.session_state.current_text += "j"
            st.rerun()
    with col4:
        if st.button("Sector 4 (Left) → 'c'", key="manual_4"):
            st.session_state.current_text += "c"
            st.rerun()
    
    # Text controls
    st.markdown("**Text Controls:**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ Add Space", key="add_space"):
            st.session_state.current_text += " "
            st.rerun()
    with col2:
        if st.button("⬅️ Delete Last", key="delete"):
            if st.session_state.current_text:
                st.session_state.current_text = st.session_state.current_text[:-1]
                st.rerun()
    with col3:
        if st.button("🗑️ Clear All", key="clear"):
            st.session_state.current_text = ""
            st.rerun()
    with col4:
        if st.button("🔊 Speak Text", key="speak"):
            if st.session_state.current_text:
                st.success(f"🔊 Speaking: '{st.session_state.current_text}'")
            else:
                st.warning("No text to speak!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Emergency System Demo
    st.markdown('<div class="emergency-panel">', unsafe_allow_html=True)
    st.markdown("### 🚨 Emergency System Demo")
    st.markdown("Simulate head-tilt emergency commands:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Left Head Tilt (Emergency)", key="left_tilt"):
            st.warning("🚨 Emergency activated!")
            st.session_state.current_text = "HELP ME PLEASE"
            st.rerun()
    with col2:
        if st.button("➡️ Right Head Tilt (Deactivate)", key="right_tilt"):
            st.info("✅ Emergency deactivated")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Technical Details
    st.markdown('<h2 class="section-header">⚙️ Technical Implementation</h2>', unsafe_allow_html=True)
    
    with st.expander("Eye-Tracking and Software Details", expanded=False):
        st.markdown("""
        **Eye-Tracking System:**
        - Receives video input from Raspberry Pi camera module 2
        - Locates pupil using color and contrast analysis
        - Preprocesses images through grayscaling, thresholding, and blurring
        - Tracks pupil movement using contour analysis and optical flow
        - Estimates gaze direction and determines keyboard focus
        
        **GUI Interface:**
        - Demo version: Python with Tkinter
        - Final version: Kotlin on Android Studio for Google Glass
        - Hierarchical command system based on gaze coordinates
        - Visual feedback through frame shifts and light intensity
        - Text-to-speech using Google TTS module
        
        **Emergency System:**
        - MPU 6050 IMU integrated with Raspberry Pi Zero 2W
        - Continuous head orientation monitoring via gyroscope
        - Predefined help messages triggered by head gestures
        
        **Hardware Integration:**
        - Raspberry Pi Zero 2W as core processing unit
        - 3D printed ABS frame for durability
        - Designed to support Google Glass lenses
        """)
    
    # QR Code section
    st.markdown('<h2 class="section-header">📱 QR Code for Poster</h2>', unsafe_allow_html=True)
    
    if QRCODE_AVAILABLE:
        if st.button("Generate QR Code for This Demo", key="generate_qr"):
            demo_url = "https://dapp2-aac-a4cmtepbtjymhgvilmewdi.streamlit.app"
            
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(demo_url)
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            buffered = BytesIO()
            qr_img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{img_str}" style="width: 200px;"></div>', unsafe_allow_html=True)
            st.success(f"✅ QR Code generated for: {demo_url}")
    else:
        st.info("📱 QR code generation requires the 'qrcode' package.")
        st.code("https://dapp2-aac-a4cmtepbtjymhgvilmewdi.streamlit.app")
    
    # Footer
    st.markdown("---")
    st.markdown("**DAPP2 Group Project** - AAC Device Development | University Project 2024")

if __name__ == "__main__":
    main()
