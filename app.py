
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="CareerCraft AI",
    page_icon="🎯",
    layout="wide"
)

# DATABASE
def init_database():
    conn = sqlite3.connect("career_profiles.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            degree TEXT,
            skills TEXT,
            interests TEXT,
            career TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_student(name, degree, skills, interests, career):
    conn = sqlite3.connect("career_profiles.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, degree, skills, interests, career)
        VALUES (?, ?, ?, ?, ?)
    """, (name, degree, skills, interests, career))

    conn.commit()
    conn.close()


# CAREER SKILL ANALYSIS
CAREER_SKILLS = {
    "AI Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "SQL", "Data Structures", "Git"
    ],
    "Data Scientist": [
        "Python", "Statistics", "SQL",
        "Pandas", "Machine Learning", "Data Visualization"
    ],
    "Software Developer": [
        "Python", "Data Structures", "Algorithms",
        "SQL", "Git", "Testing"
    ],
    "Data Analyst": [
        "SQL", "Excel", "Python",
        "Statistics", "Data Visualization"
    ]
}


# PROFESSIONAL SUMMARY
def generate_summary(name, degree, skills, career):
    return f"""
    {name} is a student pursuing {degree}.
    The student has knowledge of {skills} and aims
    to build a career as a {career}.

    The student is interested in developing technical
    knowledge, practical experience and professional
    skills to achieve career goals.
    """


# SKILL GAP ANALYSIS
def analyze_skills(skills, career):
    current = [s.strip().lower() for s in skills.split(",")]
    required = CAREER_SKILLS.get(career, [])

    matched = [
        s for s in required if s.lower() in current
    ]

    missing = [
        s for s in required if s.lower() not in current
    ]

    score = round(len(matched) / len(required) * 100)

    return matched, missing, score


# LEARNING ROADMAP
def learning_roadmap(missing):
    roadmap = []

    for skill in missing:
        roadmap.append(
            f"Study {skill}, practise its fundamentals "
            f"and build a small practical project."
        )

    return roadmap


# INTERVIEW PREPARATION
def interview_questions(career):
    return [
        f"Tell me about yourself and your interest in {career}.",
        "Explain one technical project you have completed.",
        "What are your strongest technical skills?",
        "How do you approach solving a difficult problem?",
        "What technical skill are you currently improving?"
    ]


# MAIN APPLICATION
init_database()

st.title("🎯 CareerCraft AI")
st.subheader("AI-Based Personalized Career Content Generator")

st.write(
    "Generate personalized professional profiles, "
    "skill-gap reports, learning recommendations "
    "and interview preparation."
)

st.divider()

st.header("👨‍🎓 Student Profile")

with st.form("student_form"):

    name = st.text_input("Student Name")

    degree = st.text_input(
        "Degree / Branch",
        placeholder="B.E. Artificial Intelligence and Machine Learning"
    )

    skills = st.text_input(
        "Current Skills",
        placeholder="Python, SQL, HTML"
    )

    interests = st.text_input(
        "Academic Interests",
        placeholder="Artificial Intelligence, Data Science"
    )

    career = st.selectbox(
        "Career Goal",
        list(CAREER_SKILLS.keys())
    )

    submit = st.form_submit_button(
        "Generate Career Profile"
    )


if submit:

    if not name.strip() or not degree.strip() or not skills.strip():
        st.error("Please fill in your name, degree and skills.")

    else:

        save_student(
            name, degree, skills, interests, career
        )

        matched, missing, score = analyze_skills(
            skills, career
        )

        st.success("Career profile generated successfully!")

        st.divider()

        st.header("📊 Career Analysis")

        c1, c2, c3 = st.columns(3)

        c1.metric("Skills Matched", len(matched))
        c2.metric("Skills to Develop", len(missing))
        c3.metric("Skill Match", f"{score}%")

        chart = pd.DataFrame({
            "Category": ["Matched Skills", "Missing Skills"],
            "Count": [len(matched), len(missing)]
        })

        fig = px.bar(
            chart,
            x="Category",
            y="Count",
            color="Category",
            title="Career Skill Analysis"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        st.header("📝 Professional Summary")

        summary = generate_summary(
            name, degree, skills, career
        )

        st.write(summary)

        st.download_button(
            "Download Professional Summary",
            summary,
            file_name="professional_summary.txt"
        )

        st.divider()

        st.header("📈 Skill Gap Report")

        st.write("Skills already matched:")

        for skill in matched:
            st.write("✅", skill)

        st.write("Skills to develop:")

        for skill in missing:
            st.write("📌", skill)

        st.divider()

        st.header("📚 Personalized Learning Roadmap")

        for i, item in enumerate(
            learning_roadmap(missing), 1
        ):
            st.write(f"{i}. {item}")

        st.divider()

        st.header("🎤 Interview Preparation")

        for i, question in enumerate(
            interview_questions(career), 1
        ):
            st.write(f"{i}. {question}")

        st.info(
            "Review generated content and ensure "
            "all professional claims are accurate."
        )

st.divider()

st.caption(
    "CareerCraft AI | M1-P1 Engineering Project"
)