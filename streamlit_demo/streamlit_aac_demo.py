import streamlit as st
import base64

def get_youtube_embed(video_url, width="100%", height="400"):
    """Generate HTML for YouTube video embedding"""
    # Extract video ID from YouTube URL
    if "youtu.be/" in video_url:
        video_id = video_url.split("youtu.be/")[1].split("?")[0]
    elif "youtube.com/watch?v=" in video_url:
        video_id = video_url.split("watch?v=")[1].split("&")[0]
    else:
        return f"<p>Invalid YouTube URL: {video_url}</p>"
    
    embed_html = f"""
    <iframe width="{width}" height="{height}" 
            src="https://www.youtube.com/embed/{video_id}" 
            title="YouTube video player" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen
            style="border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    </iframe>
    """
    return embed_html

def main():
    # Page configuration
    st.set_page_config(
        page_title="Wearable AAC System - Eye-Tracking Interface",
        page_icon="👁️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Custom CSS for styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.3rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 1rem;
        border: 2px solid transparent;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: #4f46e5;
    }
    
    .video-container {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .tech-spec {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    .benefit-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .workflow-step {
        background: #f1f5f9;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1rem;
        border-left: 4px solid #4f46e5;
    }
    
    .step-number {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .footer {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
    }
    
    .placeholder-video {
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
        border: 2px dashed #94a3b8;
        border-radius: 10px;
        height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        color: #64748b;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>Wearable AAC System</h1>
        <p>Advanced Eye-Tracking Interface for Augmentative and Alternative Communication</p>
    </div>
    """, unsafe_allow_html=True)

    def get_base64_image(image_path):
        """Convert image to base64 string"""
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except FileNotFoundError:
            print(f"File not found: {image_path}")
            return None
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    # Device CAD Visualization Section
    st.markdown("## 🔧 Device Design")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="background: #f8fafc; padding: 2rem; border-radius: 15px; 
                    box-shadow: 0 8px 25px rgba(0,0,0,0.1); text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #1e293b; margin-bottom: 1.5rem;">Wearable AAC Device - CAD Model</h3>
        """, unsafe_allow_html=True)
        
        # Try different path options - use whichever works for your setup
        image_paths = [
            "device_cad_model.jpg",           # Same folder as your .py file
            "./device_cad_model.jpg",         # Explicit current directory
            "../device_cad_model.jpg",        # Parent directory (repo root)
            "streamlit_demo/device_cad_model.jpg"  # If running from repo root
        ]
        
        img_base64 = None
        used_path = None
        
        for path in image_paths:
            img_base64 = get_base64_image(path)
            if img_base64:
                used_path = path
                break
        
        if img_base64:
            st.markdown(f"""
            <img src="data:image/jpeg;base64,{img_base64}" 
                 style="width: 100%; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <p style="color: #64748b; font-style: italic; margin-top: 0.5rem; font-size: 0.9rem;">
            Complete wearable AAC system with integrated eye-tracking camera and processing unit
            </p>
            <p style="color: #94a3b8; font-size: 0.8rem;">Loaded from: {used_path}</p>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Could not load image file. Please add 'device_cad_model.jpg' to the streamlit_demo folder.")
            st.info("💡 Expected location: `/streamlit_demo/device_cad_model.jpg`")
        
    st.markdown("""
        <p style="color: #64748b; text-align: center; margin-top: 1rem; line-height: 1.6; font-size: 1.1rem;">
        Our lightweight, ergonomic wearable device integrates advanced eye-tracking technology 
        with comfortable head-mounting design for extended daily use.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Video Demonstrations Section
    st.markdown("## 🎥 Live Demonstrations")
    
    # Three-column layout for videos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="video-container">
            <h3 style="color: #1e293b; text-align: center; margin-bottom: 1rem;">👁️ Eye-Tracking Technology</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Eye-tracking video
        youtube_embed = get_youtube_embed("https://youtu.be/yYKB8XmAFoY", width="100%", height="300")
        st.markdown(youtube_embed, unsafe_allow_html=True)
        
        st.markdown("""
        <p style="color: #64748b; text-align: center; margin-top: 1rem; line-height: 1.5;">
        Real-time demonstration of our advanced eye-tracking system detecting gaze patterns 
        and translating them into precise interface selections for seamless AAC communication.
        </p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="video-container">
            <h3 style="color: #1e293b; text-align: center; margin-bottom: 1rem;">💻 Interface Demonstration</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # UI demo video
        youtube_embed = get_youtube_embed("https://youtu.be/7FzhZJq1Ph8", width="100%", height="300")
        st.markdown(youtube_embed, unsafe_allow_html=True)
        
        st.markdown("""
        <p style="color: #64748b; text-align: center; margin-top: 1rem; line-height: 1.5;">
        Complete walkthrough of the circular AAC interface showing letter selection, 
        word formation, and text-to-speech functionality in action.
        </p>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="video-container">
            <h3 style="color: #1e293b; text-align: center; margin-bottom: 1rem;">🏃 IMU Motion Control</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # IMU demo placeholder
        youtube_embed = get_youtube_embed("https://youtu.be/MtpgdY0GcJI?si=PeeesH3wK1X3FBPq", width = "100%", height = "300")
        st.markdown(youtube_embed, unsafe_allow_html=True)

        """
        #st.markdown("""
        #<div class="placeholder-video">
        #    <div style="font-size: 3rem; margin-bottom: 1rem;">🎬</div>
        #    <h4 style="margin-bottom: 0.5rem;">Video Coming Soon</h4>
        #    <p>IMU Motion Control Demo</p>
        #</div>
        #""", unsafe_allow_html=True)
        """
        
        st.markdown("""
        <p style="color: #64748b; text-align: center; margin-top: 1rem; line-height: 1.5;">
        Demonstration of wearable IMU sensors enabling head movement and gesture-based 
        navigation as an alternative input method for the AAC interface.
        </p>
        """, unsafe_allow_html=True)

    # System Overview
    st.markdown("## 🔬 System Overview")
    st.markdown("""
    <p style="text-align: center; font-size: 1.2rem; color: #64748b; margin-bottom: 2rem;">
    Our wearable AAC system combines cutting-edge eye-tracking technology with an intuitive 
    circular interface to provide fast, accurate communication for individuals with speech disabilities.
    </p>
    """, unsafe_allow_html=True)

    # Features Grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">"👁️"</div>
            <h3 style="color: #1e293b; margin-bottom: 1rem;">Precision Eye-Tracking</h3>
            <p style="color: #64748b; line-height: 1.6;">
            Advanced computer vision algorithms detect and track eye movements with 
            millisecond precision, enabling hands-free interface control.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <h3 style="color: #1e293b; margin-bottom: 1rem;">Circular Interface Design</h3>
            <p style="color: #64748b; line-height: 1.6;">
            Ergonomically designed circular layout optimizes eye movement patterns 
            and reduces fatigue during extended communication sessions.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔊</div>
            <h3 style="color: #1e293b; margin-bottom: 1rem;">Real-Time Text-to-Speech</h3>
            <p style="color: #64748b; line-height: 1.6;">
            Instant voice synthesis converts typed text to natural-sounding speech, 
            enabling fluid conversation flow.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
            <h3 style="color: #1e293b; margin-bottom: 1rem;">High-Speed Communication</h3>
            <p style="color: #64748b; line-height: 1.6;">
            Optimized selection algorithms achieve communication speeds of 
            up to 15-20 words per minute with 95%+ accuracy.
            </p>
        </div>
        """, unsafe_allow_html=True)

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

    # How It Works
    st.markdown("## 🔄 How It Works")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="workflow-step">
            <div class="step-number">1</div>
            <h4 style="color: #1e293b; margin-bottom: 0.5rem;">Eye Detection</h4>
            <p style="color: #64748b;">Camera captures user's eye movements in real-time</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="workflow-step">
            <div class="step-number">2</div>
            <h4 style="color: #1e293b; margin-bottom: 0.5rem;">Gaze Mapping</h4>
            <p style="color: #64748b;">Algorithm translates gaze coordinates to interface positions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="workflow-step">
            <div class="step-number">3</div>
            <h4 style="color: #1e293b; margin-bottom: 0.5rem;">Selection Process</h4>
            <p style="color: #64748b;">Dwell-time triggers letter selection with visual feedback</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="workflow-step">
            <div class="step-number">4</div>
            <h4 style="color: #1e293b; margin-bottom: 0.5rem;">Voice Output</h4>
            <p style="color: #64748b;">Completed words are converted to speech instantly</p>
        </div>
        """, unsafe_allow_html=True)

    # Key Benefits
    st.markdown("## 🌟 Key Benefits")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="benefit-card">
            <h4 style="margin-bottom: 1rem;">🚀 Independence</h4>
            <p>Enables completely hands-free communication for users with limited mobility</p>
        </div>
        <div class="benefit-card">
            <h4 style="margin-bottom: 1rem;">🎯 Accuracy</h4>
            <p>High precision eye-tracking minimizes selection errors</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="benefit-card">
            <h4 style="margin-bottom: 1rem;">⚡ Speed</h4>
            <p>Rapid text input with optimized letter frequency placement</p>
        </div>
        <div class="benefit-card">
            <h4 style="margin-bottom: 1rem;">🔄 Adaptable</h4>
            <p>Customizable interface layouts and sensitivity settings</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="benefit-card">
            <h4 style="margin-bottom: 1rem;">💪 Accessibility</h4>
            <p>Designed specifically for cerebral palsy and motor impairment users</p>
        </div>
        <div class="benefit-card">
            <h4 style="margin-bottom: 1rem;">💻 Portable</h4>
            <p>Lightweight wearable design for everyday use</p>
        </div>
        """, unsafe_allow_html=True)

    # Performance Metrics
    st.markdown("## 📊 Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Selection Accuracy",
            value="95%+",
            delta="Industry Leading"
        )
    
    with col2:
        st.metric(
            label="Communication Speed",
            value="10-15 CPM",
            delta="Faster than traditional"
        )
    
    with col3:
        st.metric(
            label="Response Time",
            value="<250ms",
            delta="Real-time feedback"
        )
    
    with col4:
        st.metric(
            label="Eye-Track Frequency",
            value="30 Hz",
            delta="Smooth tracking"
        )

    # Footer
    st.markdown("""
    <div class="footer">
        <p style="font-size: 1.1rem; font-weight: 500; margin: 0;">
        BME DAPP 2 Group 3, Wearable AAC - Imperial College London 2025
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
