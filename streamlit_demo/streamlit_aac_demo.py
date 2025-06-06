import streamlit as st
import numpy as np
import time
import json
import base64
from io import BytesIO
import qrcode
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="AAC Device Demo - DAPP2",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    }
    .eye-tracking-status {
        background-color: #e8f4f8;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .emergency-panel {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# WebGazer.js integration
webgazer_script = """
<script src="https://webgazer.cs.brown.edu/webgazer.js"></script>
<script>
    let gazeData = [];
    let isTracking = false;
    
    function initializeEyeTracking() {
        webgazer.setGazeListener(function(data, elapsedTime) {
            if (data == null) return;
            
            // Store gaze data
            gazeData.push({
                x: data.x,
                y: data.y,
                timestamp: elapsedTime
            });
            
            // Send gaze coordinates to Streamlit
            const event = new CustomEvent('gazeUpdate', {
                detail: { x: data.x, y: data.y }
            });
            window.dispatchEvent(event);
        }).begin();
        
        isTracking = true;
        console.log("Eye tracking initialized");
    }
    
    function stopEyeTracking() {
        webgazer.end();
        isTracking = false;
        console.log("Eye tracking stopped");
    }
    
    // Auto-initialize after page load
    window.addEventListener('load', function() {
        setTimeout(initializeEyeTracking, 2000);
    });
</script>
"""

class StreamlitAACInterface:
    def __init__(self):
        self.RIGHT = ['a', 'e', 'i', 'o', 'u']
        self.TOP = ["s", "t", "n", "r", "d", "l", "h"]
        self.LEFT = ["c", "w", "m", "g", "y", "p", "f"]
        self.BOTTOM = ["j", "b", "q", "k", "v", "z", "x"]
        
        self.current_text = ""
        self.state = "MAIN"
        self.selection_counters = {"TOP": 0, "RIGHT": 0, "BOTTOM": 0, "LEFT": 0}
        self.emergency_counter = 0
        
        if 'aac_interface' not in st.session_state:
            st.session_state.aac_interface = self
            st.session_state.current_text = ""
            st.session_state.gaze_x = 0
            st.session_state.gaze_y = 0
            st.session_state.eye_tracking_active = False

    def gaze_to_command(self, x, y, interface_center_x=400, interface_center_y=300):
        """Convert gaze coordinates to AAC commands"""
        # Calculate relative position from interface center
        rel_x = x - interface_center_x
        rel_y = y - interface_center_y
        
        # Calculate distance from center
        distance = np.sqrt(rel_x**2 + rel_y**2)
        
        # If too close to center, it's the space key (command 9)
        if distance < 50:
            return "9"
        
        # If too far from center, ignore
        if distance > 150:
            return None
        
        # Calculate angle to determine sector
        angle = np.arctan2(-rel_y, rel_x)  # Note: y is inverted in screen coordinates
        angle_degrees = np.degrees(angle) % 360
        
        # Map angles to sectors
        if 315 <= angle_degrees or angle_degrees < 45:  # Right sector
            return "2"
        elif 45 <= angle_degrees < 135:  # Top sector
            return "1"
        elif 135 <= angle_degrees < 225:  # Left sector
            return "4"
        elif 225 <= angle_degrees < 315:  # Bottom sector
            return "3"
        
        # Corner buttons (approximate positions)
        if distance > 200:
            if angle_degrees > 315 or angle_degrees < 45:
                return "6"  # Return
            elif 45 <= angle_degrees < 135:
                return "5"  # NUM
            elif 135 <= angle_degrees < 225:
                return "7"  # Delete
            elif 225 <= angle_degrees < 315:
                return "8"  # Confirm
        
        return None

    def create_circular_interface_svg(self):
        """Create an SVG representation of the circular interface"""
        svg = f"""
        <svg width="400" height="400" viewBox="0 0 400 400" style="border: 2px solid #333; border-radius: 50%; background: black;">
            <!-- Outer ring -->
            <circle cx="200" cy="200" r="150" fill="none" stroke="white" stroke-width="3"/>
            
            <!-- Sector divisions -->
            <line x1="200" y1="50" x2="200" y2="350" stroke="white" stroke-width="2"/>
            <line x1="50" y1="200" x2="350" y2="200" stroke="white" stroke-width="2"/>
            <line x1="94" y1="94" x2="306" y2="306" stroke="white" stroke-width="2"/>
            <line x1="306" y1="94" x2="94" y2="306" stroke="white" stroke-width="2"/>
            
            <!-- Center circle -->
            <circle cx="200" cy="200" r="50" fill="black" stroke="white" stroke-width="3"/>
            
            <!-- Letters in sectors -->
            <!-- TOP sector -->
            <text x="200" y="80" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="12">{', '.join(self.TOP)}</text>
            
            <!-- RIGHT sector -->
            <text x="320" y="205" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="12">{', '.join(self.RIGHT)}</text>
            
            <!-- BOTTOM sector -->
            <text x="200" y="330" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="12">{', '.join(self.BOTTOM)}</text>
            
            <!-- LEFT sector -->
            <text x="80" y="205" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="12">{', '.join(self.LEFT)}</text>
            
            <!-- Center text display -->
            <text x="200" y="205" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="16">{st.session_state.current_text[-8:]}</text>
            
            <!-- Corner buttons -->
            <text x="50" y="50" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="10">NUM</text>
            <text x="350" y="50" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="10">⟲</text>
            <text x="50" y="370" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="10">X</text>
            <text x="350" y="370" text-anchor="middle" fill="white" font-family="Monaco, monospace" font-size="10">✓</text>
            
            <!-- Gaze indicator -->
            <circle cx="{st.session_state.gaze_x * 0.5}" cy="{st.session_state.gaze_y * 0.5}" r="5" fill="red" opacity="0.7"/>
        </svg>
        """
        return svg

def main():
    # Header
    st.markdown('<h1 class="main-header">🗣️ AAC Device Demo - DAPP2</h1>', unsafe_allow_html=True)
    
    # YouTube Video Embed
    st.markdown('<h2 class="section-header">📹 Project Demo Video</h2>', unsafe_allow_html=True)
    
    video_html = """
    <div style="text-align: center; margin: 20px 0;">
        <iframe width="800" height="450" 
                src="https://www.youtube.com/embed/yzSJAeBg88E?autoplay=1&mute=1" 
                frameborder="0" 
                allow="autoplay; encrypted-media" 
                allowfullscreen>
        </iframe>
    </div>
    """
    st.markdown(video_html, unsafe_allow_html=True)
    
    # Project Introduction
    st.markdown('<h2 class="section-header">📋 Project Introduction</h2>', unsafe_allow_html=True)
    
    intro_text = """
    <div class="intro-text">
    <p><strong>Cerebral palsy (CP)</strong> is a neurological disorder affecting muscle control and coordination, impacting 17 million people worldwide. Around 75% of children with CP experience speech impairments, from mild articulation issues to complete loss of speech.</p>
    
    <p>While Alternative and Augmentative Communication (AAC) devices exist to help, consultations with specialists revealed that current AACs are often bulky, impractical, and stigmatizing.</p>
    
    <p><strong>This project aims to develop a wearable, user-friendly AAC device to improve communication and quality of life for patients and their caregivers.</strong></p>
    </div>
    """
    st.markdown(intro_text, unsafe_allow_html=True)
    
    # Final Product Description
    st.markdown('<h2 class="section-header">🎯 Final Product</h2>', unsafe_allow_html=True)
    
    product_text = """
    <div class="intro-text">
    <p>The design uses <strong>Google Glass</strong> with a camera-based eye-tracking system and a circular keyboard interface projected onto the lens. Users select characters by focusing on keys, and the system converts this input into speech, enabling seamless, hands-free communication.</p>
    
    <p><strong>Enhanced functionality includes:</strong></p>
    <ul>
        <li><strong>Head-tracking for emergency alerts:</strong> Two consecutive left head tilts trigger a call for help, while two right tilts deactivate it.</li>
        <li><strong>Visual feedback (LED indicators)</strong> to notify others when the user is speaking.</li>
        <li><strong>Speech volume control,</strong> allowing users to adjust output discreetly.</li>
    </ul>
    </div>
    """
    st.markdown(product_text, unsafe_allow_html=True)
    
    # Interactive Demo Section
    st.markdown('<h2 class="section-header">🎮 Interactive Demo</h2>', unsafe_allow_html=True)
    
    # Initialize AAC interface
    aac = StreamlitAACInterface()
    
    # Eye tracking controls
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("🎯 Start Eye Tracking", key="start_tracking"):
            st.session_state.eye_tracking_active = True
            st.markdown(webgazer_script, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="eye-tracking-status">', unsafe_allow_html=True)
        if st.session_state.eye_tracking_active:
            st.success("👁️ Eye tracking active - Look at the interface!")
        else:
            st.info("👁️ Eye tracking inactive - Click 'Start Eye Tracking' to begin")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("⏹️ Stop Eye Tracking", key="stop_tracking"):
            st.session_state.eye_tracking_active = False
    
    # AAC Interface Display
    st.markdown('<div class="aac-interface">', unsafe_allow_html=True)
    st.markdown("### Circular AAC Interface")
    
    # Display the circular interface
    interface_svg = aac.create_circular_interface_svg()
    st.markdown(interface_svg, unsafe_allow_html=True)
    
    # Manual input for testing
    st.markdown("**Manual Testing (for demo purposes):**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Sector 1 (Top)", key="manual_1"):
            st.session_state.current_text += "s"
    with col2:
        if st.button("Sector 2 (Right)", key="manual_2"):
            st.session_state.current_text += "a"
    with col3:
        if st.button("Sector 3 (Bottom)", key="manual_3"):
            st.session_state.current_text += "j"
    with col4:
        if st.button("Sector 4 (Left)", key="manual_4"):
            st.session_state.current_text += "c"
    
    # Text controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Add Space", key="add_space"):
            st.session_state.current_text += " "
    with col2:
        if st.button("Delete Last", key="delete"):
            if st.session_state.current_text:
                st.session_state.current_text = st.session_state.current_text[:-1]
    with col3:
        if st.button("🔊 Speak Text", key="speak"):
            if st.session_state.current_text:
                st.success(f"🔊 Speaking: '{st.session_state.current_text}'")
                # In a real implementation, this would use TTS
    
    # Current text display
    st.markdown(f"**Current Text:** `{st.session_state.current_text}`")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Emergency System Demo
    st.markdown('<div class="emergency-panel">', unsafe_allow_html=True)
    st.markdown("### 🚨 Emergency System Demo")
    st.markdown("Simulate head-tilt emergency commands:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Left Head Tilt", key="left_tilt"):
            st.warning("Left head tilt detected!")
            st.session_state.current_text = "HELP ME PLEASE"
    with col2:
        if st.button("➡️ Right Head Tilt", key="right_tilt"):
            st.info("Right head tilt detected - Emergency deactivated")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Technical Details
    st.markdown('<h2 class="section-header">⚙️ Technical Implementation</h2>', unsafe_allow_html=True)
    
    with st.expander("Eye-Tracking and Software Details", expanded=False):
        tech_text = """
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
        """
        st.markdown(tech_text)
    
    # Generate QR Code for deployment
    st.markdown('<h2 class="section-header">📱 QR Code for Poster</h2>', unsafe_allow_html=True)
    
    if st.button("Generate QR Code", key="generate_qr"):
        # This would be your actual Streamlit app URL after deployment
        demo_url = "https://your-streamlit-app.streamlit.app"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(demo_url)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64 for display
        buffered = BytesIO()
        qr_img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        st.markdown(f'<img src="data:image/png;base64,{img_str}" style="width: 200px;">', unsafe_allow_html=True)
        st.info(f"QR Code generated for: {demo_url}")
    
    # Footer
    st.markdown("---")
    st.markdown("**DAPP2 Group Project** - AAC Device Development | University Project 2024")

if __name__ == "__main__":
    main()
