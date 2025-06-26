# DAPP2-AAC
This repository contains all scripts written for the DAPP 2 group 3 who's working the project about Wearable Augmented Alternative Communication (WAAC) Device.

Abstract

    Speech impairments can make everyday communication a challenge, as it affects the individual’s ability to express themselves, engage in social interactions, and participate fully in everyday activities. One of the most common causes is Cerebral Palsy (CP). Cerebral Palsy is a neurological condition that impairs the motor control needed for verbal communication [1], affecting 17 million people in the world [2]. To address this, Augmentative Alternative Communication (AAC) devices were developed to provide a non-verbal means of communication. Despite their benefits, market research shows that existing AAC solutions have notable limitations, including bulkiness, impracticality, high costs, stability issues, and dependence on caregiver assistance for device mounting and operation.
        
    The aim of the project is to develop a wearable solution for AAC devices that can tackle the challenges specified by eliminating the need for a mount or a screen and improving user interaction. The device is designed to facilitate communication through an eye-tracking system integrated with a custom-built graphical user interface, which consists of a radial keyboard. Once projected onto the near-eye display, users can select their intended key by fixating their gaze on the target for a predefined dwell time. The composed text is then converted into audio output. The system includes additional features that include the ability to issue emergency commands and inform interlocutors of active communication efforts.
    
    The device consists of a 3D-printed frame integrating Google Glass, a camera for eye-tracking and other electronic components. The Google Glass is used to project the developed interface onto the lens. The camera allows for eye-tracking when the user is selecting keys through real-time analysis. This data is then sent to a Raspberry Pi which process and outputs coordinates corresponding to the pupil position. Additional components include an inertial measurement unit (IMU) for precise head-tracking and a battery.
    
    Several tests were conducted to validate the requirements specified. These tests include eye-tracking accuracy, motion detection, surface temperature, battery, and other relevant functional tests. Experimental results demonstrated a speech output accuracy rate of 78.2%, IMU activation success rate of 91.8% and a run-time surface temperature below 30 °C. Alongside these tests, surveys were conducted and over 86.7% of the respondents rated the graphical user interface as user-friendly. 

    The developed device has successfully met the key requirements outlined at the start of the design process. However, certain limitations include comfort, discreet design, and compatibility. Future iterations aim to incorporate advanced machine learning algorithms to elevate accuracy and responsiveness, implement compatibility with other more affordable AR glasses and re-design the frame for a more sleek and comfortable design. 
    
    Ultimately, this wearable AAC device represents a significant step forward in providing individuals with CP an accessible, efficient, and user-centric communication solution, promoting independence and improved social interactions.

The project's software contains the following modules:
    
    UI Module: Manages the user interface for text input and selection.
    Text-to-Speech Module: Converts text input into speech output.
    Eye-Tracking Module: Handles eye movement detection and gaze tracking.
    IMU Module: Processes head movement data for additional input commands.
    Main Program: Implement the logic and functionality behind UI with OOP.
    Commuincation and Integration Module: Handles data transfer between the Raspberry Pi and Google Glass.
    Bluetooth Communication: Alternative for pairing devices and extension such as a speaker.

The communication module will be the most difficult to code, since developers need to refer to multiple APIs from Google, Rasperries Pi, and others to ensure the smooth communication; The Eye-tracking and IMU will be the second and third hard module because they need to handle input data in its raw form and will need to be programmed in lower-level language; The UI and TTS module are easier and can be written in Python leveraged on the existing packages ready to be installed.

Links to resources:

    Google Explorer Edition for the Developers working on the Google Glasses Softwares: https://developers.google.com/glass
    
    Guide: https://developers.google.com/glass/design/principles
    
    Code Samples: https://developers.google.com/glass-enterprise/samples/code-samples
    
    Google Glass Github Repositories: https://github.com/googleglass
    
    WebRTC for the curious: https://webrtcforthecurious.com/docs/01-what-why-and-how/
    
    Pypi gTTS Package (Not real Google Translate): https://pypi.org/project/gTTS/
    
    gTTS (Google Text-to-speech), can be used for generating MP3 files: https://gtts.readthedocs.io/en/latest/

    Raspberry Pi Bluetooth: https://www.sunfounder.com/blogs/news/mastering-raspberry-pi-bluetooth-a-comprehensive-guide-to-setup-use-cases-and-troubleshooting

    Raspberry Pi Documentation and Installation: https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system

    Raspberry Pi Open Source AR Glasses: https://gitee.com/shiliupi/OpenEyeTap/issues/I4JVUE

    基于树莓派的VR设备：https://blog.csdn.net/weixin_44040217/article/details/107254341

    基于树莓派和Vufine屏的谷歌眼镜：https://make.quwj.com/project/144

    树莓派相关项目（代码示例）：https://www.eetree.cn/doc/detail/572

    树莓派平台资源大全：https://www.eetree.cn/wiki/rpi

    OpenEyeTap：基于树莓派的开源AR智能眼镜：https://gitee.com/shiliupi/OpenEyeTap/issues/I4JVUE

    GPIO Zero, Python module, Can be used for LED control on Pi: https://gpiozero.readthedocs.io/en/stable/installing.html

    EyeTracking using OpenCV Blogs
        https://medium.com/analytics-vidhya/eye-tracking-using-opencv-2f40cc09183c
        https://medium.com/@amit25173/opencv-eye-tracking-aeb4f1b46aa3

    PyBluez, Bluetooth access: https://github.com/pybluez/pybluez

    MediaPipe, a ML solution for eyetracking and depth estimation: https://github.com/google-ai-edge/mediapipe/blob/master/docs/solutions/iris.md

    OpenCV Meanshift and CAMshift: https://docs.opencv.org/3.4/d7/d00/tutorial_meanshift.html
    
    Filterpy Package: https://filterpy.readthedocs.io/en/latest/


    
