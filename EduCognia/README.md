# EduCognia – Sensor-Free Cognitive Engagement Detection

EduCognia is an end-to-end machine learning system designed to detect a learner’s cognitive engagement state in online learning environments using passive behavioral interaction signals.

Unlike traditional engagement detection systems that rely on intrusive sensors such as webcams, EEG devices, eye tracking, or wearables, EduCognia is completely sensor-free and privacy-preserving.

## Problem

Online learning platforms rely on weak engagement signals such as:

- Session duration
- Video completion
- Page views
- Quiz scores

These metrics do not reflect a learner’s real cognitive state.

EduCognia addresses this by analyzing behavioral interaction signals.

## Behavioral Signals Used

- Mouse movement patterns
- Keyboard typing activity
- Idle time
- Window switching
- Application usage duration

## Machine Learning Model

The system uses **Gradient Boosted Decision Trees (XGBoost)** trained on behavioral interaction features.

## Features Engineered

- Interaction event count
- Session duration
- Mouse movement distance
- Idle time fraction
- Keyboard typing rate
- Window switch frequency
- Application usage share

## System Components

- Feature Engineering Pipeline
- Machine Learning Model (XGBoost)
- Real-time inference engine
- FastAPI backend
- Streamlit dashboard
- Browser extension prototype

## Real-Time Monitoring

The system captures interaction signals in 30-second windows and predicts engagement states:

- Engaged
- Focused
- Neutral
- Distracted
- Disengaged

## Competition Achievement

🏆 **2nd Place – National Data Science Competition**

## Tech Stack

Python  
XGBoost  
FastAPI  
Streamlit  
Pandas  
NumPy
