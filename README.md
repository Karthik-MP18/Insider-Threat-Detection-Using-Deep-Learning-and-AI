# Insider Threat Detection Using Deep Learning and AI

A Deep Neural Network (DNN) model that analyzes user behavior logs to accurately identify malicious insider activities with **94.5% accuracy** and **100% recall**.

## 📖 Overview

This project tackles the critical challenge of insider threat detection by leveraging deep learning. By analyzing integrated behavioral data—including device usage, logon events, and web access patterns—the model identifies subtle anomalies indicative of malicious intent, significantly improving upon traditional rule-based detection methods.

**Key Achievement:** The model successfully identified all 159 malicious instances in the test set with zero false negatives.

## ✨ Features

-   **Multi-Source Data Analysis:** Processes and correlates logs from three distinct data sources (device, logon, HTTP).
-   **Advanced Feature Engineering:** Derives critical behavioral indicators from raw system logs, including after-hours activity, removable device usage, and suspicious website visits.
-   **High-Performance DNN Model:** A feedforward neural network architecture with dropout regularization for robust classification.
-   **Comprehensive Evaluation:** Includes accuracy, precision, recall, F1-score, ROC curves, precision-recall curves, and confusion matrix analysis.

## ⚙️ Model Architecture

The core of this project is a Deep Neural Network built with TensorFlow and Keras.

Input Layer (7 features)
↓
Dense Layer (128 neurons, ReLU activation)
↓
Dense Layer (64 neurons, ReLU activation)
↓
Dropout Layer (0.5 rate)
↓
Dense Layer (32 neurons, ReLU activation)
↓
Output Layer (1 neuron, Sigmoid activation)


## 📊 Results and Evaluation

The model was evaluated on a comprehensive test set, demonstrating exceptional performance:

| Metric | Score | Implication |
| :--- | :--- | :--- |
| **Accuracy** | 94.5% | High overall prediction correctness |
| **Precision** | 93.5% | Low false positive rate |
| **Recall** | 100% | **No malicious activities were missed** |
| **F1-Score** | 96.7% | Excellent balance between precision and recall |

-   **Confusion Matrix:** Showed zero false negatives, correctly classifying all 159 malicious instances.
-   **ROC Curve:** Achieved a perfect Area Under the Curve (AUC) score of 1.0.

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   pip (Python package manager)

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Karthik-MP18/Insider-Threat-Detection-Using-Deep-Learning-and-AI.git
    cd Insider-Threat-Detection-Using-Deep-Learning-and-AI
    ```

2.  **Install required dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download the Dataset**
    -   **Important:** Before running the code, you must obtain the dataset.
    -   Follow the detailed instructions in the [`data/README.md`](data/README.md) file to download and place the required CSV files in the `data/` directory.

### Usage

**The scripts must be executed in the following order:**

1.  **Preprocess the data:**
    ```bash
    python preprocess.py
    ```
    *Loads raw data from CSV files and handles initial cleaning.*

2.  **Engineer features:**
    ```bash
    python feature_engineer.py
    ```
    *Creates behavioral features and labels from the processed data.*

3.  **Train the model:**
    ```bash
    python train_model.py
    ```
    *Defines the Neural Network architecture and trains the model.*

4.  **Evaluate the model:**
    ```bash
    python evaluate.py
    ```
    *Generates performance metrics, visualizations, and analysis reports.*

## 🗂️ Project Structure
Insider-Threat-Detection/
├── data/
│ └── README.md # Dataset download instructions
├── imports.py # Centralized import statements
├── preprocess.py # Data loading and cleaning
├── feature_engineer.py # Feature engineering pipeline
├── train_model.py # Model definition and training
├── evaluate.py # Model evaluation and visualization
├── requirements.txt # Python dependencies
├── .gitignore # Files to ignore in version control
└── README.md # This file

## 🔮 Future Enhancements

-   Deploy the model as a real-time monitoring API
-   Experiment with LSTMs or Transformers to capture temporal patterns
-   Integrate with SIEM tools for enterprise-level deployment
-   Develop a user-friendly dashboard for visualization
-   Implement real-time monitoring capabilities

## 👨‍💻 Author

**Karthik Puranikamath**
- [GitHub Portfolio](https://github.com/Karthik-MP18) (In Progress)
- [LinkedIn](www.linkedin.com/in/karthik-puranikmath-6b412b211)

## 📄 License

This project is licensed for academic and personal use. The dataset may be subject to its own licensing terms.

---

**Disclaimer:** This project is for academic and research purposes only. Always ensure you have proper authorization before testing security systems.

<div align="center">
  
**⭐️ If you find this project useful, please give it a star on GitHub!**

</div>
