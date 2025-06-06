<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wearable AAC System - Eye-Tracking Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .poster-container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 15px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.3rem;
            opacity: 0.9;
            max-width: 800px;
            margin: 0 auto;
        }

        .content {
            padding: 40px;
        }

        .section {
            margin-bottom: 50px;
        }

        .section h2 {
            color: #4f46e5;
            font-size: 2.2rem;
            margin-bottom: 25px;
            text-align: center;
            position: relative;
        }

        .section h2::after {
            content: '';
            display: block;
            width: 80px;
            height: 4px;
            background: linear-gradient(90deg, #4f46e5, #7c3aed);
            margin: 15px auto;
            border-radius: 2px;
        }

        .two-column {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            align-items: start;
        }

        .video-container {
            background: #f8fafc;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }

        .video-container:hover {
            transform: translateY(-5px);
        }

        .video-container h3 {
            color: #1e293b;
            font-size: 1.5rem;
            margin-bottom: 15px;
            text-align: center;
        }

        .video-wrapper {
            position: relative;
            width: 100%;
            padding-bottom: 56.25%; /* 16:9 aspect ratio */
            margin-bottom: 15px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .video-wrapper video {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .video-description {
            color: #64748b;
            font-size: 0.95rem;
            text-align: center;
            line-height: 1.5;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }

        .feature-card {
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 2px solid transparent;
        }

        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            border-color: #4f46e5;
        }

        .feature-icon {
            font-size: 3rem;
            margin-bottom: 20px;
            display: block;
        }

        .feature-card h3 {
            color: #1e293b;
            font-size: 1.3rem;
            margin-bottom: 15px;
        }

        .feature-card p {
            color: #64748b;
            line-height: 1.6;
        }

        .tech-specs {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 40px;
            border-radius: 15px;
            margin: 40px 0;
        }

        .tech-specs h3 {
            font-size: 1.8rem;
            margin-bottom: 25px;
            text-align: center;
        }

        .specs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
        }

        .spec-item {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }

        .spec-item strong {
            color: #a78bfa;
            display: block;
            margin-bottom: 8px;
            font-size: 1.1rem;
        }

        .workflow {
            background: #f8fafc;
            padding: 40px;
            border-radius: 15px;
            margin: 40px 0;
        }

        .workflow-steps {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            margin-top: 30px;
        }

        .workflow-step {
            text-align: center;
            flex: 1;
            min-width: 200px;
            margin: 10px;
        }

        .step-number {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: bold;
            margin: 0 auto 15px;
            box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
        }

        .workflow-step h4 {
            color: #1e293b;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }

        .workflow-step p {
            color: #64748b;
            font-size: 0.9rem;
        }

        .arrow {
            font-size: 2rem;
            color: #94a3b8;
            margin: 0 15px;
        }

        .benefits {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 40px;
            border-radius: 15px;
            text-align: center;
            margin: 40px 0;
        }

        .benefits h3 {
            font-size: 2rem;
            margin-bottom: 30px;
        }

        .benefits-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }

        .benefit-item {
            background: rgba(255,255,255,0.15);
            padding: 25px;
            border-radius: 12px;
            backdrop-filter: blur(10px);
        }

        .benefit-item h4 {
            font-size: 1.2rem;
            margin-bottom: 12px;
        }

        .footer {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 40px;
        }

        .footer p {
            font-size: 1.1rem;
            font-weight: 500;
        }

        .qr-section {
            background: #f1f5f9;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin: 30px 0;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .header p {
                font-size: 1.1rem;
            }
            
            .two-column {
                grid-template-columns: 1fr;
                gap: 30px;
            }
            
            .workflow-steps {
                flex-direction: column;
            }
            
            .arrow {
                transform: rotate(90deg);
                margin: 15px 0;
            }
            
            .content {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="poster-container">
        <div class="header">
            <h1>Wearable AAC System</h1>
            <p>Advanced Eye-Tracking Interface for Augmentative and Alternative Communication</p>
        </div>

        <div class="content">
            <!-- Video Demonstrations Section -->
            <div class="section">
                <h2>🎥 Live Demonstrations</h2>
                <div class="two-column">
                    <div class="video-container">
                        <h3>👁️ Eye-Tracking Technology</h3>
                        <div class="video-wrapper">
                            <video controls preload="metadata">
                                <source src="Eye-tracking Demo.mp4" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        </div>
                        <div class="video-description">
                            Real-time demonstration of our advanced eye-tracking system detecting gaze patterns and translating them into precise interface selections for seamless AAC communication.
                        </div>
                    </div>
                    
                    <div class="video-container">
                        <h3>💻 Interface Demonstration</h3>
                        <div class="video-wrapper">
                            <video controls preload="metadata">
                                <source src="UI_Demo_Video.mp4" type="video/mp4">
                                Your browser does not support the video tag.
                            </video>
                        </div>
                        <div class="video-description">
                            Complete walkthrough of the circular AAC interface showing letter selection, word formation, and text-to-speech functionality in action.
                        </div>
                    </div>
                </div>
            </div>

            <!-- System Overview -->
            <div class="section">
                <h2>🔬 System Overview</h2>
                <p style="text-align: center; font-size: 1.2rem; color: #64748b; margin-bottom: 30px;">
                    Our wearable AAC system combines cutting-edge eye-tracking technology with an intuitive circular interface to provide fast, accurate communication for individuals with speech disabilities.
                </p>
                
                <div class="features-grid">
                    <div class="feature-card">
                        <span class="feature-icon">👁️</span>
                        <h3>Precision Eye-Tracking</h3>
                        <p>Advanced computer vision algorithms detect and track eye movements with millisecond precision, enabling hands-free interface control.</p>
                    </div>
                    
                    <div class="feature-card">
                        <span class="feature-icon">🎯</span>
                        <h3>Circular Interface Design</h3>
                        <p>Ergonomically designed circular layout optimizes eye movement patterns and reduces fatigue during extended communication sessions.</p>
                    </div>
                    
                    <div class="feature-card">
                        <span class="feature-icon">🔊</span>
                        <h3>Real-Time Text-to-Speech</h3>
                        <p>Instant voice synthesis converts typed text to natural-sounding speech, enabling fluid conversation flow.</p>
                    </div>
                    
                    <div class="feature-card">
                        <span class="feature-icon">⚡</span>
                        <h3>High-Speed Communication</h3>
                        <p>Optimized selection algorithms achieve communication speeds of up to 15-20 words per minute with 95%+ accuracy.</p>
                    </div>
                </div>
            </div>

            <!-- Technical Specifications -->
            <div class="tech-specs">
                <h3>⚙️ Technical Specifications</h3>
                <div class="specs-grid">
                    <div class="spec-item">
                        <strong>Eye-Tracking Precision:</strong>
                        Sub-degree accuracy with 60Hz sampling rate
                    </div>
                    <div class="spec-item">
                        <strong>Interface Framework:</strong>
                        Python Tkinter with real-time rendering
                    </div>
                    <div class="spec-item">
                        <strong>Selection Method:</strong>
                        Dwell-time based (2-second threshold)
                    </div>
                    <div class="spec-item">
                        <strong>Audio Output:</strong>
                        Google Text-to-Speech (gTTS) integration
                    </div>
                    <div class="spec-item">
                        <strong>Letter Organization:</strong>
                        Frequency-optimized circular sectors
                    </div>
                    <div class="spec-item">
                        <strong>Response Time:</strong>
                        <250ms latency for seamless interaction
                    </div>
                </div>
            </div>

            <!-- How It Works -->
            <div class="workflow">
                <h3 style="text-align: center; color: #1e293b; font-size: 2rem; margin-bottom: 20px;">🔄 How It Works</h3>
                <div class="workflow-steps">
                    <div class="workflow-step">
                        <div class="step-number">1</div>
                        <h4>Eye Detection</h4>
                        <p>Camera captures user's eye movements in real-time</p>
                    </div>
                    <span class="arrow">→</span>
                    <div class="workflow-step">
                        <div class="step-number">2</div>
                        <h4>Gaze Mapping</h4>
                        <p>Algorithm translates gaze coordinates to interface positions</p>
                    </div>
                    <span class="arrow">→</span>
                    <div class="workflow-step">
                        <div class="step-number">3</div>
                        <h4>Selection Process</h4>
                        <p>Dwell-time triggers letter selection with visual feedback</p>
                    </div>
                    <span class="arrow">→</span>
                    <div class="workflow-step">
                        <div class="step-number">4</div>
                        <h4>Voice Output</h4>
                        <p>Completed words are converted to speech instantly</p>
                    </div>
                </div>
            </div>

            <!-- Benefits -->
            <div class="benefits">
                <h3>🌟 Key Benefits</h3>
                <div class="benefits-list">
                    <div class="benefit-item">
                        <h4>🚀 Independence</h4>
                        <p>Enables completely hands-free communication for users with limited mobility</p>
                    </div>
                    <div class="benefit-item">
                        <h4>⚡ Speed</h4>
                        <p>Rapid text input with optimized letter frequency placement</p>
                    </div>
                    <div class="benefit-item">
                        <h4>🎯 Accuracy</h4>
                        <p>High precision eye-tracking minimizes selection errors</p>
                    </div>
                    <div class="benefit-item">
                        <h4>💪 Accessibility</h4>
                        <p>Designed specifically for cerebral palsy and motor impairment users</p>
                    </div>
                    <div class="benefit-item">
                        <h4>🔄 Adaptable</h4>
                        <p>Customizable interface layouts and sensitivity settings</p>
                    </div>
                    <div class="benefit-item">
                        <h4>💻 Portable</h4>
                        <p>Lightweight wearable design for everyday use</p>
                    </div>
                </div>
            </div>

            <!-- QR Code Section -->
            <div class="qr-section">
                <h3 style="color: #1e293b; margin-bottom: 20px;">📱 Access Full Documentation</h3>
                <div style="display: flex; justify-content: center; align-items: center; gap: 40px; flex-wrap: wrap;">
                    <div style="text-align: center;">
                        <div style="width: 150px; height: 150px; background: #e2e8f0; border: 2px solid #94a3b8; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px;">
                            <span style="color: #64748b; font-size: 0.9rem;">QR Code<br>Coming Soon</span>
                        </div>
                        <p style="color: #64748b; font-weight: 500;">GitHub Repository</p>
                    </div>
                    <div style="color: #1e293b; max-width: 400px;">
                        <h4 style="margin-bottom: 15px;">📖 Complete Project Resources:</h4>
                        <ul style="text-align: left; color: #64748b; line-height: 1.8;">
                            <li>Full source code and documentation</li>
                            <li>Hardware setup instructions</li>
                            <li>Calibration and usage guides</li>
                            <li>Technical specifications</li>
                            <li>Research findings and validation</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>BME DAPP 2 Group 3, Wearable AAC - Imperial College London 2025</p>
        </div>
    </div>
</body>
</html>
