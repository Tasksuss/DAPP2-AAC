# DAPP2-AAC
This repository contains all programs and documentations for the BME DAPP2 2025 Group 3 project on the wearable Augmented Alternative Communication (wAAC) device.

# Abstract

Speech impairments can make everyday communication a challenge, as it affects the individual’s ability to express themselves, engage in social interactions, and participate fully in everyday activities. One of the most common causes is Cerebral Palsy (CP). Cerebral Palsy is a neurological condition that impairs the motor control needed for verbal communication [1], affecting 17 million people in the world [2]. To address this, Augmentative Alternative Communication (AAC) devices were developed to provide a non-verbal means of communication. Despite their benefits, market research shows that existing AAC solutions have notable limitations, including bulkiness, impracticality, high costs, stability issues, and dependence on caregiver assistance for device mounting and operation.

The aim of the project is to develop a wearable solution for AAC devices that can tackle the challenges specified by eliminating the need for a mount or a screen and improving user interaction. The device is designed to facilitate communication through an eye-tracking system integrated with a custom-built graphical user interface, which consists of a radial keyboard. Once projected onto the near-eye display, users can select their intended key by fixating their gaze on the target for a predefined dwell time. The composed text is then converted into audio output. The system includes additional features that include the ability to issue emergency commands and inform interlocutors of active communication efforts.
    
The device consists of a 3D-printed frame integrating Google Glass, a camera for eye-tracking and other electronic components. The Google Glass is used to project the developed interface onto the lens. The camera allows for eye-tracking when the user is selecting keys through real-time analysis. This data is then sent to a Raspberry Pi which process and outputs coordinates corresponding to the pupil position. Additional components include an inertial measurement unit (IMU) for precise head-tracking and a battery.
    
Several tests were conducted to validate the requirements specified. These tests include eye-tracking accuracy, motion detection, surface temperature, battery, and other relevant functional tests. Experimental results demonstrated a speech output accuracy rate of 78.2%, IMU activation success rate of 91.8% and a run-time surface temperature below 30 °C. Alongside these tests, surveys were conducted and over 86.7% of the respondents rated the graphical user interface as user-friendly. 

The developed device has successfully met the key requirements outlined at the start of the design process. However, certain limitations include comfort, discreet design, and compatibility. Future iterations aim to incorporate advanced machine learning algorithms to elevate accuracy and responsiveness, implement compatibility with other more affordable AR glasses and re-design the frame for a more sleek and comfortable design. 
    
Ultimately, this wearable AAC device represents a significant step forward in providing individuals with CP an accessible, efficient, and user-centric communication solution, promoting independence and improved social interactions.

# References

    [1] National Institute of Neurological Disorders and Stroke. Cerebral Palsy. [Internet]. 2025 [cited 2025 Jun 17]. Available from: https://www.ninds.nih.gov/health-information/disorders/cerebral-palsy 
    [2] Graham HK, Rosenbaum P, Paneth N, Dan B, Lin JP, Damiano DL, et al. Cerebral palsy. Nature Reviews Disease Primers [Internet]. 2016 Jan 7;2(1) [cited 2025 Jun 17]. Available from: https://www.nature.com/articles/nrdp201582 



    
