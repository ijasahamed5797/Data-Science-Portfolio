# 🧠 EduCognia – Cognitive Engagement Detection System

## 📌 Project Overview

**EduCognia** is an end-to-end machine learning system designed to detect a learner’s **cognitive engagement state in real-time** during online learning sessions.

Unlike traditional engagement detection systems that rely on intrusive sensors such as webcams, EEG devices, eye tracking, or wearables, EduCognia is completely **sensor-free and privacy-preserving**.

The system infers engagement by analyzing **behavioral interaction signals** such as mouse activity, keyboard input, idle time, and window switching behavior.

---

# 🎯 Problem Statement

Most online learning platforms measure engagement using weak indicators such as:

• Session duration
• Video completion
• Page views
• Quiz scores

These metrics **do not accurately reflect a learner’s cognitive state**.

Existing engagement detection systems often rely on:

• Webcam facial expression tracking
• Eye tracking
• EEG sensors
• Wearable devices

These approaches introduce:

• Privacy concerns
• High hardware costs
• Poor scalability

EduCognia solves this by using **passive behavioral interaction signals captured from the operating system and browser.**

---

# 🔄 System Pipeline (How It Works)

## 1️⃣ Interaction Logging

The system captures behavioral interaction signals including:

• Mouse movement events
• Keyboard typing activity
• Idle time detection
• Window switching behavior
• Active application tracking

These events are collected in **fixed time windows (30 seconds)**.

---

## 2️⃣ Feature Engineering

Raw interaction logs are converted into behavioral features:

• Number of interaction events
• Session duration
• Mouse movement distance
• Idle time fraction
• Keyboard typing rate (keys/sec)
• Window switch count
• Window switch rate
• Dominant application usage
• Application time distribution

These features represent **user attention and interaction patterns.**

---

## 3️⃣ Machine Learning Model

The final model used is:

**Gradient Boosted Decision Trees (XGBoost)**

Reasons for choosing XGBoost:

• Excellent performance on structured/tabular data
• Captures complex non-linear behavioral patterns
• Robust probability outputs
• Efficient for real-time inference

The model predicts five cognitive states:

• Engaged
• Focused
• Neutral
• Distracted
• Disengaged

---

## 4️⃣ Real-Time Inference

During a live session:

1. Interaction signals are logged
2. Behavioral features are generated
3. The trained model predicts engagement state
4. Class probabilities are produced
5. A focus score is computed

---

## 5️⃣ Focus Score Calculation

EduCognia introduces a **Focus Score (0–100)**.

It is derived from:

• Idle time fraction
• Window switching frequency
• Application dominance
• Interaction intensity

This provides an **interpretable indicator of learner focus.**

---

## 6️⃣ Rule-Based Policy Layer

A rule-based policy layer ensures realistic predictions.

Example rule:

If the model predicts **Engaged** but the user spends most time on a **non-learning application**, the system downgrades the label to **Distracted**.

This prevents misleading predictions.

---

## 7️⃣ Streamlit Dashboard

The system includes an interactive **Streamlit dashboard** for monitoring engagement.

The dashboard displays:

• Live engagement prediction
• Focus score
• Class probability distribution
• Application usage breakdown
• Interaction timeline
• Window switching visualization
• Session history logs

---

# 🧩 Technologies Used

## Backend

• Python
• Pandas
• NumPy
• XGBoost

## Machine Learning

• Scikit-learn
• Gradient Boosted Trees

## Visualization

• Streamlit
• Matplotlib
• Plotly

## API

• FastAPI

---

# 🚀 Key Features

## 📊 Behavioral Analytics

• Interaction-based engagement detection
• Feature engineering from system events
• Behavioral pattern modeling

---

## 🤖 Machine Learning

• XGBoost engagement classification
• Probability confidence scoring
• Cross-validation evaluation

---

## ⚡ Real-Time Monitoring

• 30-second interaction windows
• Real-time inference pipeline
• Live cognitive state predictions

---

## 📈 Engagement Insights

• Focus score metric
• Application usage tracking
• Session history analytics

---

# 🏗 Project Structure

```
EduCognia/
│
├── notebooks/
│   ├── eda.ipynb
│   ├── feature_engineering.ipynb
│   └── model_training.ipynb
│
├── dashboard.py
├── requirements.txt
└── README.md
```

---

# ▶ Run Locally

Install dependencies:

```
pip install -r requirements.txt
```

Run the dashboard:

```
streamlit run dashboard.py
```

---

# 🏆 Competition Achievement

This project was presented in a **National Data Science Competition** and achieved:

🥈 **2nd Place Nationally**

Evaluation criteria included:

• Innovation and creativity
• Problem solving approach
• Technical implementation
• Presentation quality

---

# 🔮 Future Improvements

Possible future enhancements:

• Temporal deep learning models (LSTM / Transformers)
• Personalized engagement baselines
• LMS integration (Moodle / Canvas)
• Instructor analytics dashboards
• Federated learning for privacy

---

# 📌 Summary

EduCognia demonstrates how **behavioral interaction data can be used to detect learner engagement without intrusive sensors**.

The system combines:

• Behavioral feature engineering
• Machine learning classification
• Real-time inference
• Interactive visualization

to provide a **privacy-preserving engagement monitoring solution for online learning environments.**
