# CareerCraft AI – AI-Personalized Career Content Generator

## Project Overview
CareerCraft AI is an intelligent career guidance application designed to help students identify suitable career paths based on their skills, interests, educational background, and career goals.

The application analyzes student profiles and provides personalized career recommendations, skill-gap analysis, learning roadmaps, and interview preparation support.

## Key Features
- **Career Assessment:** Analyzes student skills, interests, and career goals.
- **Career Recommendations:** Suggests suitable career paths.
- **Skill Gap Analysis:** Identifies skills that students may need to improve.
- **Learning Roadmap:** Provides a structured learning path.
- **Interview Preparation:** Provides interview practice questions.
- **Professional Summary:** Helps generate career-related profile content.
- **Student Analytics:** Displays saved student assessments.
- **PDF Report:** Generates downloadable career assessment reports.

## Technologies Used
- Python
- Streamlit
- SQLite
- Pandas
- ReportLab

## Project Structure
```text
AI-Personalized-Career-Content-Generator/
│
├── app.py
├── ai_engine.py
├── career_analyzer.py
├── config.py
├── database.py
├── requirements.txt
├── README.md
│
├── modules/
├── utils/
├── tests/
└── docs/
```

## How to Run the Project

1. Clone the repository:

```bash
git clone https://github.com/aishwaryasuvarna355/AI-Personalized-Career-Content-Generator.git
```

2. Open the project folder:

```bash
cd AI-Personalized-Career-Content-Generator
```

3. Install the required libraries:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python -m streamlit run app.py
```

5. Open the local URL displayed in the terminal.

## Testing
Run the unit tests using:

```bash
python -m unittest discover -s tests -v
```

## Project Repository
[View CareerCraft AI on GitHub](https://github.com/aishwaryasuvarna355/AI-Personalized-Career-Content-Generator)

## Conclusion
CareerCraft AI aims to make career planning easier for students by providing personalized career guidance, skill development suggestions, and interview preparation support.
