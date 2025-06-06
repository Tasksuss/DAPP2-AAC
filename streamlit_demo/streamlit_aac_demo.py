import streamlit as st
import base64
import os

def get_video_html(video_path, width="100%", height="400px"):
    """Generate HTML for video embedding"""
    if os.path.exists(video_path):
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()
            video_base64 = base64.b64encode(video_bytes).decode()
        
        video_html = f"""
        <video width="{width}" height="{height}" controls style="border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        """
        return video_html
    else:
        return f"""
        <div style="width: {width}; height: {height}; background: #f0f2f6; border: 2px dashed #ccc; 
                    border-radius: 10px; display: flex; align-items: center; justify-content: center;">
            <p style="color: #666; text-align: center;">Video file not found:<br><strong>{video_path}</strong></p>
        </div>
        """

def main():
    # Page configuration
    st.set_page_config(
        page_title="AAC Keyboard - Eye-Tracking Interface",
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
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>👁️ AAC Keyboard</h1>
        <p>Advanced Eye-Tracking Interface for Augmentative and Alternative Communication</p>
    </div>
    """, unsafe_allow_html=True)

    # Video Demonstrations Section
    st.markdown("## 🎥 Live Demonstrations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="video-container">
            <h3 style="color: #1e293b; text-align: center; margin-bottom: 1rem;">👁️ Eye-Tracking Technology</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Eye-tracking video
        video_html = get_video_html("Eye-tracking Demo.mp4")
        st.markdown(video_html, unsafe_allow_html=True)
        
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
        video_html = get_video_html("UI_Demo_Video.mp4")
        st.markdown(video_html, unsafe_allow_html=True)
        
        st.markdown("""
        <p style="color: #64748b; text-align: center; margin-top: 1rem; line-height: 1.5;">
        Complete walkthrough of the circular AAC interface showing letter selection, 
        word formation, and text-to-speech functionality in action.
        </p>
        """, unsafe_allow_html=True)

    # System Overview
    st.markdown("## 🔬 System Overview")
    st.markdown("""
    <p style="text-align: center; font-size: 1.2rem; color: #64748b; margin-bottom: 2rem;">
    Our AAC keyboard system combines cutting-edge eye-tracking technology with an intuitive 
    circular interface to provide fast, accurate communication for individuals with speech disabilities.
    </p>
    """, unsafe_allow_html=True)

    # Features Grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">👁️</div>
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
            <h3 style="color: #1e293b; margin-bottom: 1rem;">Circular Interface</h3>
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
            <h3 style="color: #1e293b; margin-bottom: 1rem;">Real-Time TTS</h3>
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

    # Technical Specifications
    st.markdown("## ⚙️ Technical Specifications")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="tech-spec">
            <h4 style="color: #a78bfa; margin-bottom: 0.5rem;">Eye-Tracking Precision:</h4>
            <p>Sub-degree accuracy with 60Hz sampling rate</p>
            <h4 style="color: #a78bfa; margin-bottom: 0.5rem;">Selection Method:</h4>
            <p>Dwell-time based (2-second threshold)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tech-spec">
            <h4 style="color: #a78bfa; margin-bottom: 0.5rem;">Interface Framework:</h4>
            <p>Python Tkinter with real-time rendering</p>
            <h4 style="color: #a78bfa; margin-bottom: 0.5rem;">Audio Output:</h4>
            <p>Google Text-to-Speech (gTTS) integration</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="tech-spec">
            <h4 style="color: #a78bfa; margin-bottom: 0.5rem;">Letter Organization:</h4>
            <p>Frequency-optimized circular sectors</p>
            <h4 style="color: #a78bfa; margin-bottom: 0.5rem;">Response Time:</h4>
            <p>&lt;250ms latency for seamless interaction</p>
        </div>
        """, unsafe_allow_html=True)

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
            <p>Lightweight design for everyday use</p>
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
            value="15-20 WPM",
            delta="3x faster than traditional"
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
            value="60 Hz",
            delta="Smooth tracking"
        )

    # Footer
    st.markdown("""
    <div class="footer">
        <p style="font-size: 1.1rem; font-weight: 500; margin: 0;">
        BME DAPP 2 Group 3, AAC Keyboard - Imperial College London 2025
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
