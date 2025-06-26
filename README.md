# DAPP2-AAC
This repository contains all scripts written for the DAPP 2 group 3 who's working the project about Wearable Augmented Alternative Communication (WAAC) Device.

Abstract

Speech impairments can make everyday communication a challenge, as it affects the individual’s ability to express themselves, engage in social interactions, and participate fully in everyday activities. One of the most common causes is Cerebral Palsy (CP). Cerebral Palsy is a neurological condition that impairs the motor control needed for verbal communication [1], affecting 17 million people in the world [2]. To address this, Augmentative Alternative Communication (AAC) devices were developed to provide a non-verbal means of communication. Despite their benefits, market research shows that existing AAC solutions have notable limitations, including bulkiness, impracticality, high costs, stability issues, and dependence on caregiver assistance for device mounting and operation.

The aim of the project is to develop a wearable solution for AAC devices that can tackle the challenges specified by eliminating the need for a mount or a screen and improving user interaction. The device is designed to facilitate communication through an eye-tracking system integrated with a custom-built graphical user interface, which consists of a radial keyboard. Once projected onto the near-eye display, users can select their intended key by fixating their gaze on the target for a predefined dwell time. The composed text is then converted into audio output. The system includes additional features that include the ability to issue emergency commands and inform interlocutors of active communication efforts.
    
The device consists of a 3D-printed frame integrating Google Glass, a camera for eye-tracking and other electronic components. The Google Glass is used to project the developed interface onto the lens. The camera allows for eye-tracking when the user is selecting keys through real-time analysis. This data is then sent to a Raspberry Pi which process and outputs coordinates corresponding to the pupil position. Additional components include an inertial measurement unit (IMU) for precise head-tracking and a battery.
    
Several tests were conducted to validate the requirements specified. These tests include eye-tracking accuracy, motion detection, surface temperature, battery, and other relevant functional tests. Experimental results demonstrated a speech output accuracy rate of 78.2%, IMU activation success rate of 91.8% and a run-time surface temperature below 30 °C. Alongside these tests, surveys were conducted and over 86.7% of the respondents rated the graphical user interface as user-friendly. 

The developed device has successfully met the key requirements outlined at the start of the design process. However, certain limitations include comfort, discreet design, and compatibility. Future iterations aim to incorporate advanced machine learning algorithms to elevate accuracy and responsiveness, implement compatibility with other more affordable AR glasses and re-design the frame for a more sleek and comfortable design. 
    
Ultimately, this wearable AAC device represents a significant step forward in providing individuals with CP an accessible, efficient, and user-centric communication solution, promoting independence and improved social interactions.

References

    [1]     National Institute of Neurological Disorders and Stroke. Cerebral Palsy. [Internet]. 2025 [cited 2025 Jun 17]. Available from: https://www.ninds.nih.gov/health-information/disorders/cerebral-palsy 
    [2]     Graham HK, Rosenbaum P, Paneth N, Dan B, Lin JP, Damiano DL, et al. Cerebral palsy. Nature Reviews Disease Primers [Internet]. 2016 Jan 7;2(1) [cited 2025 Jun 17]. Available from: https://www.nature.com/articles/nrdp201582 
    [3]     Rubio‐Carbonero, G. Communication in Persons with Acquired Speech Impairment: The Role of Family as Language Brokers. Journal of Linguistic Anthropology, 32(1), pp.161–181. 2021 [cited 2025 Jun 17] Available from: https://doi.org/10.1111/jola.12340
    [4]	RCSLT. Communication access UK [Internet]. 2025. [cited 2025 Jun 17] Available from: https://www.rcslt.org/policy-and-influencing/communication-access-uk/
    [5] 	Larrazabal M. Speech Disorders in Cerebral Palsy Explained. [Internet]. Better Speech. 2022 [cited 2025 Jun 17] Available from: https://www.betterspeech.com/post/speech-and-language-disorders-among-those-with-cerebral-palsy
    [6]	   Cerebral Palsy Research Foundation - USA. Facts about Cerebral Palsy | Cerebral Palsy Research Foundation - USA [Internet]. Cparf.org. 2018. [cited 2025 Jun 17]. Available from: https://cparf.org/what-is-cerebral-palsy/facts-about-cerebral-palsy/
    [7]	   National Health Service (NHS). Overview | Cerebral Palsy. [Internet]. 2023 [cited 2025 Jun 17] Available from: https://www.nhs.uk/conditions/cerebral-palsy/ 
    [8]	   NHS. Alternative and Augmentative Communication (AAC). [Internet]. Children’s Integrated Therapies. 2021. [cited 2025 Jun 17]. Available from: https://www.oxfordhealth.nhs.uk/cit/resources/aac/
    [9]	   Our Communication Boards [Internet]. Create Visual Aids Ltd. 2025 [cited 2025 Jun 17]. Available from: https://www.createvisualaids.co.uk/collections/communication-boards
    [10]	Totally Tactile Communicator [Internet]. Liberator.co.uk. 2025 [cited 2025 Jun 17]. Available from: https://www.liberator.co.uk/totally-tactile-communicator
    [11]	GoTalk 20+ Lite Touch [Internet]. Liberator.co.uk. 2025 [cited 2025 Jun 17]. Available from: https://www.liberator.co.uk/gotalk-20-lite-touch
    [12]	NovaChat 10 Active [Internet]. Liberator.co.uk. 2025. [cited 2025 Jun 17]. Available from: https://www.liberator.co.uk/nova-chat-10.7-active
    [13] 	AssistiveWare. Proloquo2Go - AAC app with symbols [Internet]. Assistive Ware. 2019. [cited 2025 Jun 17]. Available from: https://www.assistiveware.com/products/proloquo2go
    [14]	UK TD. PCEye [Internet]. Tobii Dynavox UK. [cited 2025 Jun 17]. Available from: https://uk.tobiidynavox.com/products/pceye?variant=37068958793887
    [15]	Meddy Tech Limited. Speech Aid: AAC Text to Speech [Internet]. App Store. 2022 [cited 2025 Jun 17]. Available from: https://apps.apple.com/gb/app/speech-aid-aac-text-to-speech/id152899895
    [16]	Wristband Communicator [Internet]. Say it with Symbols. 2025 [cited 2025 Jun 17]. Available from: https://www.sayitwithsymbols.com/wristband-communicator/
    [17]	BrightSign Technology Limited. BrightSign Glove - Translate any sign into any language [Internet]. brightsignglove. 2022 [cited 2025 Jun 17]. Available from: https://www.brightsignglove.com/?_gl=1
    [18]	Graphene-based wearable strain sensor can detect and broadcast silently mouthed words [Internet]. Cambridge Enterprise. 2025 [cited 2025 Jun 17]. Available from: https://www.enterprise.cam.ac.uk/news/graphene-based-wearable-strain-sensor-can-detect-and-broadcast-silently-mouthed-words/
    [19]	Bache J. AAC specialist. Personal Communication.14th November 2024. 
    [20]	Cerebral Palsy Alliance. Gross Motor Function Classification System (GMFCS) [Internet]. Cerebral Palsy Alliance. 2023. [cited 2025 Jun 17]. Available from: https://cerebralpalsy.org.au/cerebral-palsy/gross-motor-function-classification-system/
    [21]	BME Group 3. BME Group 3 – PSD [undergraduate project report]. London: Imperial College London; 2025.
    [22]	Radcliffe A.J. Tolerance, Clearance and Fit. [Lecture Slides] Imperial College London.
    [23]	Essentra Components. A guide to butt hinges [Internet]. Essentracomponents.com. Essentra Components. 2022 [cited 2025 Jun 17]. Available from: https://www.essentracomponents.com/en-gb/news/solutions/access-hardware/a-guide-to-butt-hinges
    [24]     Raspberry Pi Ltd. Raspberry Pi Zero 2 W [Internet]. 2024 Apr. Available from: https://datasheets.raspberrypi.com/rpizero2/raspberry-pi-zero-2-w-product-brief.pdf
    [25]     Google Glass Enterprise Edition 2 – main features, use cases, benefits [Internet]. nsflow.com. Available from: https://nsflow.com/blog/google-glass-enterprise-edition-2-main-features-use-cases-benefits
    [26]     Python Software Foundation. socket — Low-level networking interface [Internet]. Python 3.12.3 documentation. Python Software Foundation; 2024 [cited 2025 Jun 15]. Available from: https://docs.python.org/3/library/socket.html
    [27]     Steeper Group [Internet]. Steeper Group. Steeper Group; 2024. Available from: https://www.steepergroup.com/accessible-technology/steeper-assistive-technology-products/communication-device/lumin-i-by-smartbox/
    [28]     CAM30NXT - IntelliGaze [Internet]. Intelligaze.com. 2025 [cited 2025 Jun 18]. Available from: https://www.intelligaze.com/en/platform/cam30nxt?utm
    [29]     Orosoo M, Raash N, Treve M, M. Lahza HF, Alshammry N, Ramesh JVN, et al. Transforming English language learning: Advanced speech recognition with MLP-LSTM for personalized education. Alexandria Engineering Journal. 2025 Jan;111:21–32.
    [30]     Shah N, Singh M, Takahashi N, Naoyuki Onoe. Nonparallel Emotional Voice Conversion for Unseen Speaker-Emotion Pairs Using Dual Domain Adversarial Network & Virtual Domain Pairing. ICASSP 2022 - 2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) [Internet]. 2023 May 5 [cited 2025 Jun 18];1–5. Available from: https://patents.google.com/patent/WO2024084330A1/en
    [31]     Web T, King G. Meta Smart Glasses for Visually Impaired People - MyVision Oxfordshire [Internet]. MyVision Oxfordshire. Technique Web; 2025 [cited 2025 Jun 17]. Available from: https://www.myvision.org.uk/meta-smart-glasses/

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


    
