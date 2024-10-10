# Shoplifting Detection System

## Overview
This project aims to detect shoplifting in real-time using a computer vision model built with 3D Convolutional Neural Networks (3D-CNN). The system processes video feeds from security cameras and identifies suspicious actions that may indicate theft, providing alerts when potential shoplifting is detected.

## Features
- Real-time monitoring and detection of suspicious activities.
- Lightweight 3D-CNN model optimized for edge devices.
- Focus on detecting theft-related behaviors like concealing items.
- Scalable to various retail environments.

## Architecture
The model uses a combination of RGB and optical flow data to detect suspicious behavior:
- **3D-CNN** for analyzing both appearance and motion.
- **SlowFast architecture** inspired by action recognition models for robust detection.
- Outputs are processed through temporal pooling to provide final theft detection.

## Setup Instructions

### Prerequisites
- Python 3.7+
- TensorFlow 2.x
- OpenCV 4.x

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/shoplifting-detection.git
   cd shoplifting-detection

 
