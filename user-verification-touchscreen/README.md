# User Verification Touchscreen

## Overview
This research project focuses on user identity verification based on a pattern drawn on a touchscreen. The project was developed by a team of five individuals.

**Authors**:
- [juniorkowal](https://github.com/juniorkowal)
- [LahTay](https://github.com/LahTay)
- [tymek2906](https://github.com/tymek2906)
- [Daniel-Bil](https://github.com/Daniel-Bil)
- [xAliem](https://github.com/xAliem)

## Project Structure
- **kotlin_app**: This folder contains a phone application built with Kotlin for drawing patterns. The app captures data from the gyroscope, accelerometer, and time during the drawing process.
  
- **machine_learning**: This folder contains the machine learning components, including data preprocessing and model training using TensorFlow. We experimented with original preprocessing techniques to combine gyroscope, accelerometer, pattern, and time data into 3D space. We then created 2D projections of this data to serve as three channels for the Generative Adversarial Network (GAN) to generate additional data.

## Data Gathering Process
The data collection involved one user drawing a pattern while another person attempted to mimic it in various poses. Unfortunately, we faced challenges due to insufficient data.

### Key Findings
- Our LSTM model performed better without gyroscope and accelerometer data, suggesting that these sensors may not vary enough between individuals. This might also be attributed to differences in hardware, as the data was gathered from various phones.
- Other potential reasons for our results could include insufficient data, inadequate preprocessing techniques, or too simple model architecture.

## Original Repository
[Original Repository Link](https://github.com/LahTay/user-verification-touchscreen)
