# MediLocker_AI

MediLocker_AI is an open-source, AI-powered healthcare management platform currently under active development. Although this version is not yet deployment-ready, we are working towards a stable release with improved features.

> ### 🚀 Open Source & In Progress
> This project is open-source & evolving!
>
> Although this version is **not yet deployment-ready**, we are working towards a stable release with improved features.  
>
> **Stay tuned for upcoming updates!** 🎉

## 📌 Preview

Here’s a quick look at MediLocker_AI in action:

### 🌐 Web Portal



### 🤖 AI Chatbot



### 📄 Report Analysis System



### 📺 Demo Video



## 📖 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [🚀 Features](#-features)
- [🏗️ Architecture & Components](#️-architecture--components)
- [🛠 Installation](#-installation)
  - [📌 Prerequisites](#-prerequisites)
  - [🐳 Setup via Docker (Recommended)](#-setup-via-docker-recommended)
  - [⚙️ Manual Setup (Without Docker)](#️-manual-setup-without-docker)
- [🚀 Usage](#-usage)
  - [🌍 Accessing Services](#-accessing-services)
  - [📡 API Example](#-api-example)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [📩 Contact](#-contact)
- [🔮 Future Roadmap](#-future-roadmap)
- [🙌 Acknowledgments](#-acknowledgments)

## 🎯 Project Overview

MediLocker_AI is a healthcare AI system integrating:

✅ **AI Chatbot →** NLP-powered symptom analysis & disease prediction

✅ **Medical Report Reader →** PDF lab metric extraction & comparison

✅ **Web Portal →** User engagement, feedback, and research resources

Built with Django, Flask, PostgreSQL, spaCy, NLTK, and Scikit-learn, this project uses Docker for deployment.

## 🚀 Features

**AI Chatbot:** Symptom assessment, disease prediction, medical recommendations

**Medical Report Reader:** PDF parsing, lab metric comparison, REST API

**Web Portal:** User feedback, pricing plans, research resources

**Containerized Deployment:** Docker-ready for ease of setup

**Scalable & Modular:** Independent services for flexibility

## 🏗️ Architecture & Components
```
MediLocker_AI/
├── chatbot/              # AI-powered symptom checker (Flask)
│   ├── model/            # Machine learning models (KNN, etc.)
│   ├── Medical_dataset/  # Training data
│   └── app.py            # Main Flask server
├── report_reader/        # Medical PDF analysis service
│   ├── api.py            # REST API for report analysis
│   └── static/           # Reference ranges
├── web_portal/           # Django web interface
│   ├── templates/        # HTML UI templates
│   └── models.py         # Feedback & user data models
└── MediLocker_AI/        # Django settings & configuration
    └── settings.py       # Project settings (PostgreSQL, static files, etc.)
```
This modular architecture ensures each component can evolve independently.

## 🛠 Installation

### Prerequisites

<ul>
  <li>Docker & Docker Compose (Recommended)</li>
  <li>Python 3.10+ (For manual installation)</li>
  <li>PostgreSQL (For database storage)</li>
</ul>

### Setup via Docker (Recommended)

```bash
git clone https://github.com/yourusername/MediLocker_AI.git
cd MediLocker_AI
docker-compose up --build
docker-compose exec web python manage.py migrate
```

### Manual Setup (Without Docker)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

For Flask Chatbot, run:

python chatbot/app.py
```

## 🚀 Usage

| Service       | URL                           |
|--------------|--------------------------------|
| Web Portal   | `http://localhost:8000`       |
| AI Chatbot   | `http://localhost:5000`       |
| Report Reader | `http://localhost:8000/report_reader` |


### API Example
```bash
curl -X POST http://localhost:8000/api/analyze/ \
  -F "file=@path/to/medical_report.pdf" \
  -F "gender=Male"
```

## 🤝 Contributing

Want to help? Here’s how:

<ol> <li>Fork the repo</li> <li>Create a branch: <code>git checkout -b feature/new-feature</code></li> <li>Commit changes: <code>git commit -m "Added a cool feature"</code></li> <li>Push to GitHub: <code>git push origin feature/new-feature</code></li> <li>Submit a Pull Request</li> </ol>
Check our <a href="CONTRIBUTING.md">CONTRIBUTING.md</a> (coming soon) for more details!

## 📜 License

MediLocker_AI is released under the MIT License. See LICENSE for details.

## 📩 Contact

Project Maintainers:

Saiyam Jain - @Saiyam-Sandhir-Jain - saiyam.sandhir.jain@gmail.com

Team Page (Coming Soon!)

## 🔮 Future Roadmap

🚀 Planned Features:

- Improved chatbot accuracy with deep learning models

- Advanced lab report analysis with AI

- Better UI/UX enhancements for web portal

- Scalability improvements & cloud deployment

Stay updated by starring ⭐ the repository!

## 🙌 Acknowledgments

- **Tech Stack: Django, Flask, PostgreSQL, spaCy, Scikit-learn**
- **Community Contributions Welcome!**