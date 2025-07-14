📊 Substance Abuse Analysis Dashboard for Women
This project presents an interactive Streamlit dashboard and a predictive analysis tool focused on understanding substance use patterns among women. Leveraging a subset of the National Survey on Drug Use and Health (NSDUH) dataset, the application provides insightful descriptive analyses, allows for predictive modeling of substance use likelihood, and offers comprehensive documentation on the dataset, technology, and team.

The primary goal is to explore how various factors such as parental presence, peer influence, and socioeconomic indicators correlate with and potentially influence substance use behaviors (specifically marijuana and alcohol) among female respondents.

✨ Features
Interactive Descriptive Analysis: Explore key demographic distributions, substance use prevalence (Marijuana and Alcohol), social factors, socioeconomic impacts, and treatment-related behaviors through dynamic and interactive charts and metrics. Filters are available to drill down into specific population segments.

Predictive Modeling: Utilize a pre-trained Logistic Regression model to predict the likelihood of marijuana or alcohol use for an individual based on a set of input characteristics. The page also displays the model's coefficients, indicating the influence of each factor.

Comprehensive Documentation: A dedicated section providing detailed information on:

Dataset Details: Overview of the NSDUH dataset, key variables used, and their classification (categorical vs. numerical).

Technology Stack: An interactive display of all the tools and libraries used in the project, with logos and descriptions.

Team Members: Introduction to the project team, including their roles and contributions.

Project Roadmap: Outlining current functionalities and future enhancements.

Resources & Materials: Access to relevant project documents (e.g., proposals, reports, presentations) embedded directly within the application for easy viewing.

Clean User Interface: Built with Streamlit, providing an intuitive and responsive user experience with custom styling and hidden default Streamlit elements for a cleaner look.

📁 Project Structure
The project is organized into a modular structure for better maintainability and readability:

your_project_folder/
├── app.py                      # Main Streamlit application entry point
├── data_loader.py              # Handles dataset loading and variable mappings
├── data_viz.py                 # Contains functions for descriptive data visualizations
├── predictive_model.py         # Manages the predictive model training and inference
├── utils.py                    # Utility functions (e.g., for mapping OHE features to readable names)
├── assets/                     # Directory for static assets like images and PDFs
│   ├── logos/                  # Contains all logo images for the technology stack
│   │   ├── 8110ce8ecd7903031e8567dc24e18d9a.png
│   │   ├── streamlit-logo-png_seeklogo-458260.png
│   │   ├── images.png
│   │   ├── Daco_6050027.png
│   │   ├── Daco_2081341.png
│   │   ├── images (1).png
│   │   ├── kaggle-logo-png_seeklogo-335156.png
│   │   ├── favpng_6ddb1184688372784e3bc0512c9260be.png
│   │   └── jupyter-logo-png_seeklogo-354673.png
│   └── pdfs/                   # Contains embedded PDF documents
│       ├── project_proposal.pdf
│       ├── data_dictionary.pdf
│       ├── technical_report.pdf
│       └── presentation_slides.pdf
├── pages/                      # Directory for page-specific UI components (prefixed with '_' to avoid auto-detection)
│   ├── __init__.py             # Makes 'pages' a Python package
│   ├── _home.py                # Defines the content and layout for the Home page
│   └── _documentation.py       # Defines the content and layout for the Documentation page
└── Cleaned Womens Dataset.csv  # The primary dataset used in the project

🚀 Getting Started
Follow these steps to set up and run the application locally.

Prerequisites
Python 3.7+

pip (Python package installer)

Downloading the Project
You can download this project in two ways:

Clone the repository (recommended for developers):

git clone https://github.com/adekite-ogunsami/Drug-Habits-in-Women-s-EDA.git
cd Drug-Habits-in-Women-s-EDA # Navigate into the project directory

Download as a ZIP file:
If you prefer not to use Git, you can download the entire project as a ZIP archive directly from GitHub.

Go to the repository page: https://github.com/adekite-ogunsami/Drug-Habits-in-Women-s-EDA

Click the green "Code" button.

Select "Download ZIP".

Extract the downloaded ZIP file to your desired location.

Installation
Navigate to the project directory:
If you cloned, you're already there. If you downloaded the ZIP, open your terminal or command prompt and navigate to the extracted project folder.

Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

Install the required Python packages:

pip install -r requirements.txt

(If you don't have a requirements.txt file, you can create one with pip freeze > requirements.txt after installing all dependencies, or manually install them: pip install streamlit pandas plotly scikit-learn numpy joblib)

Ensure Dataset and Assets are in Place:

Place your Cleaned Womens Dataset.csv file directly in the root of your project folder (your_project_folder/).

Ensure your logo images are in your_project_folder/assets/logos/ with the correct filenames as specified in pages/_documentation.py.

Place your PDF documents in your_project_folder/assets/pdfs/ with the correct filenames.

Running the Application
Navigate to the root of your project folder in the terminal and run:

streamlit run app.py

This will open the Streamlit application in your default web browser.

Important Note for Copy-Pasting: If you are copy-pasting this README content directly into a new file on your local machine or GitHub, please ensure your text editor is set to save with UTF-8 encoding and LF (Unix) line endings for optimal rendering on GitHub.

🛠️ Technology Stack
Tool

Description

Python

The core programming language for data analysis and application logic.

Streamlit

Framework for rapid creation of interactive web applications from Python scripts.

Pandas

Powerful library for data manipulation, analysis, and processing.

Plotly

Used for creating interactive, publication-quality graphs and visualizations.

Scikit-learn

Comprehensive machine learning library for building and evaluating models.

NumPy

Fundamental package for numerical computing, providing support for arrays and matrices.

Kaggle

Platform for data science competitions and hosting datasets, including NSDUH.

GitHub

Used for version control and collaborative development of the project's codebase.

Jupyter Notebook

An open-source web application used for creating and sharing documents that contain live code, equations, visualizations, and narrative text.

🤝 Contributing
We welcome contributions to this project! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeatureName).

Make your changes.

Commit your changes (git commit -m 'Add new feature').

Push to the branch (git push origin feature/YourFeatureName).

Open a Pull Request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

📧 Contact
For any questions or inquiries, please open an issue in the GitHub repository.