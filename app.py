
import streamlit as st
import pandas as pd
import plotly.express as px
import json

from database import (
    init_database,
    save_profile,
    get_all_profiles,
    get_profile_by_id
)

from career_analyzer import (
    analyze_career_profile,
    explain_career_match,
    get_project_recommendations,
    get_skill_recommendations
)

from modules.roadmap import generate_learning_roadmap
from modules.interview_prep import generate_interview_questions
from utils.pdf_generator import generate_career_pdf


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CareerCraft AI",
    page_icon="🎯",
    layout="wide"
)

init_database()


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.title("🎯 CareerCraft AI")

st.subheader(
    "AI-Based Personalized Career Content Generator"
)

st.write(
    "An intelligent career guidance platform that helps "
    "students discover suitable careers, identify skill gaps "
    "and build personalized learning plans."
)

st.info(
    "Demo Mode: Career recommendations currently use "
    "a weighted rule-based analysis engine."
)


# --------------------------------------------------
# NAVIGATION TABS
# --------------------------------------------------

tab1, tab2, tab3 = st.tabs([
    "🎓 Career Assessment",
    "📊 Student Analytics",
    "ℹ️ About"
])


# ==================================================
# TAB 1: CAREER ASSESSMENT
# ==================================================

with tab1:

    st.header("Student Career Assessment")

    with st.form("career_form"):

        name = st.text_input("Student Name")

        email = st.text_input("Email Address")

        branch = st.selectbox(
            "Engineering Branch",
            ["AIML", "CSE", "ISE", "ECE", "EEE", "Other"]
        )

        skills_text = st.text_area(
            "Enter Your Technical Skills",
            placeholder="Python, SQL, Java, Machine Learning"
        )

        interests_text = st.text_area(
            "Enter Your Academic and Career Interests",
            placeholder="Artificial Intelligence, Data Science"
        )

        career_goal = st.selectbox(
            "Your Career Goal",
            [
                "Explore Career Options",
                "AI Engineer",
                "Data Scientist",
                "Software Developer",
                "Data Analyst"
            ]
        )

        experience = st.selectbox(
            "Experience Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

        submitted = st.form_submit_button(
            "Analyze My Career Profile",
            use_container_width=True
        )

    if submitted:

        if not name.strip():
            st.error("Please enter your name.")

        elif not skills_text.strip():
            st.error("Please enter at least one technical skill.")

        else:

            skills = [
                item.strip()
                for item in skills_text.split(",")
                if item.strip()
            ]

            interests = [
                item.strip()
                for item in interests_text.split(",")
                if item.strip()
            ]

            profile = {
                "name": name.strip(),
                "email": email.strip(),
                "branch": branch,
                "skills": skills,
                "interests": interests,
                "career_goal": career_goal,
                "experience_level": experience
            }

            # Career analysis using skills and interests
            results = analyze_career_profile(
                skills,
                interests
            )

            # Prioritize the selected career goal
            if career_goal != "Explore Career Options":

                results.sort(
                    key=lambda item: (
                        item["career"] != career_goal,
                        -item["match_percentage"]
                    )
                )

            best_career = results[0]

            # Generate personalized content
            roadmap = generate_learning_roadmap(
                best_career["missing_skills"]
            )

            questions = generate_interview_questions(
                best_career["career"]
            )

            analysis = {
                "career_results": results,
                "recommended_career": best_career["career"],
                "match_percentage": best_career["match_percentage"]
            }

            # Save student information
            save_profile(profile, analysis)

            # Store results for display
            st.session_state["profile"] = profile
            st.session_state["results"] = results
            st.session_state["best_career"] = best_career
            st.session_state["roadmap"] = roadmap
            st.session_state["questions"] = questions

            st.success(
                "Career assessment completed successfully!"
            )

    # --------------------------------------------------
    # DISPLAY CAREER REPORT
    # --------------------------------------------------

    if "best_career" in st.session_state:

        profile = st.session_state["profile"]
        results = st.session_state["results"]
        best = st.session_state["best_career"]
        roadmap = st.session_state["roadmap"]
        questions = st.session_state["questions"]

        st.divider()

        st.header("Your Personalized Career Report")

        # Career summary metrics
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Recommended Career",
            best["career"]
        )

        col2.metric(
            "Overall Match",
            f'{best["match_percentage"]}%'
        )

        col3.metric(
            "Skills to Improve",
            len(best["missing_skills"])
        )

        # Career comparison chart
        st.subheader("Career Suitability Analysis")

        chart_data = pd.DataFrame([
            {
                "Career": item["career"],
                "Match Percentage": item["match_percentage"]
            }
            for item in results
        ])

        fig = px.bar(
            chart_data,
            x="Career",
            y="Match Percentage",
            color="Career",
            title="Career Match Comparison",
            range_y=[0, 100]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Explainable recommendations
        st.divider()

        st.subheader("Why This Career Was Recommended")

        explanations = explain_career_match(best)

        for explanation in explanations:
            st.write("• " + explanation)

        st.write(
            "**Scoring method:** 70% technical skill match "
            "+ 30% interest match."
        )

        # Skill analysis
        st.divider()

        st.subheader("Skill Analysis")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("**Matched Skills**")

            if best["matched_skills"]:

                for skill in best["matched_skills"]:
                    st.success(skill)

            else:
                st.write("No matching skills identified.")

        with col2:

            st.markdown("**Skills to Improve**")

            if best["missing_skills"]:

                for skill in best["missing_skills"]:
                    st.warning(skill)

            else:
                st.success("No missing skills identified!")

        # Personalized skill improvement
        st.divider()

        st.subheader("Personalized Skill Improvement Plan")

        skill_recommendations = get_skill_recommendations(
            best["missing_skills"]
        )

        if skill_recommendations:

            for skill, recommendation in skill_recommendations.items():

                with st.expander(f"How to improve: {skill}"):

                    st.write(recommendation)

        else:

            st.success(
                "You match all the listed skills for this career!"
            )

        # Project recommendations
        st.divider()

        st.subheader("Recommended Portfolio Projects")

        project_recommendations = get_project_recommendations(best)

        for project in project_recommendations:

            with st.expander(project["project_name"]):

                st.write(project["purpose"])

                st.write(
                    "Recommended Career:",
                    project["career"]
                )

        # Learning roadmap
        st.divider()

        st.subheader("Personalized Learning Roadmap")

        if roadmap:

            for item in roadmap:

                with st.expander(
                    f'Week {item["week"]}: {item["skill"]}'
                ):

                    st.write(item["topic"])

                    st.write(
                        "Target Date:",
                        item["target_date"]
                    )

                    for task in item["tasks"]:
                        st.write("• " + task)

        else:

            st.success(
                "No skill gaps found for this career!"
            )

        # Interview preparation
        st.divider()

        st.subheader("Interview Preparation")

        for index, question in enumerate(questions, start=1):

            with st.expander(
                f'Question {index}: {question["question"]}'
            ):

                st.write("**Sample Answer:**")

                st.write(question["answer"])

                st.caption(
                    "Difficulty: " + question["difficulty"]
                )

        # PDF report
        st.divider()

        st.subheader("Download Your Career Report")

        pdf = generate_career_pdf(
            profile,
            best,
            roadmap,
            questions
        )

        st.download_button(
            label="📄 Download Career Report (PDF)",
            data=pdf,
            file_name="CareerCraft_AI_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        # JSON report
        st.download_button(
            label="Download Career Analysis (JSON)",
            data=json.dumps(
                {
                    "profile": profile,
                    "analysis": results,
                    "roadmap": roadmap,
                    "interview_questions": questions
                },
                indent=4
            ),
            file_name="CareerCraft_AI_Report.json",
            mime="application/json",
            use_container_width=True
        )


# ==================================================
# TAB 2: STUDENT ANALYTICS
# ==================================================

with tab2:

    st.header("Student Analytics Dashboard")

    records = get_all_profiles()

    if records:

        dataframe = pd.DataFrame(
            records,
            columns=[
                "ID",
                "Student Name",
                "Branch",
                "Career Goal",
                "Created At"
            ]
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Total Assessments",
            len(dataframe)
        )

        col2.metric(
            "Engineering Branches",
            dataframe["Branch"].nunique()
        )

        st.subheader("Student Assessment History")

        st.dataframe(
            dataframe,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("View Complete Assessment")

        selected_id = st.selectbox(
            "Select Student Assessment",
            dataframe["ID"].tolist()
        )

        record = get_profile_by_id(selected_id)

        if record:
            st.markdown("### Student Profile")
            st.write("**Name:**", record[1])
            st.write("**Email:**", record[2])
            st.write("**Branch:**", record[3])
            st.write("**Skills:**", ", ".join(json.loads(record[4] or "[]")))
            st.write("**Interests:**", ", ".join(json.loads(record[5] or "[]")))
            st.write("**Career Goal:**", record[6])
            st.write("**Experience Level:**", record[7])

            st.markdown("### Career Analysis")
            st.json(json.loads(record[8] or "{}"))


        csv = dataframe.to_csv(index=False)

        st.download_button(
            "Download Student Analytics (CSV)",
            data=csv,
            file_name="student_analytics.csv",
            mime="text/csv"
        )

        st.subheader("Branch Distribution")

        branch_data = (
            dataframe["Branch"]
            .value_counts()
            .reset_index()
        )

        branch_data.columns = ["Branch", "Students"]

        fig = px.pie(
            branch_data,
            names="Branch",
            values="Students",
            title="Student Branch Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No student assessments are available yet."
        )


# ==================================================
# TAB 3: ABOUT THE PROJECT
# ==================================================

with tab3:

    st.header("About CareerCraft AI")

    st.write("""
    CareerCraft AI is a personalized career guidance platform
    designed to help engineering students explore suitable
    career paths based on their technical skills and interests.

    The platform analyzes student profiles and generates
    career recommendations, skill improvement plans,
    learning roadmaps and interview preparation content.
    """)

    st.subheader("Core Features")

    features = [
        "Personalized career recommendations",
        "Weighted skill and interest analysis",
        "Explainable career recommendations",
        "Skill-gap identification",
        "Personalized skill improvement plans",
        "Portfolio project recommendations",
        "Weekly learning roadmaps",
        "Career-specific interview preparation",
        "Downloadable PDF reports",
        "Student profile history",
        "Student analytics dashboard"
    ]

    for feature in features:
        st.write("✅ " + feature)

    st.subheader("Technology Stack")

    technologies = [
        "Python",
        "Streamlit",
        "SQLite",
        "Pandas",
        "Plotly",
        "ReportLab"
    ]

    for technology in technologies:
        st.write("• " + technology)

    st.info(
        "Current version: Rule-based Demo Mode. "
        "The system provides educational career guidance "
        "and does not guarantee employment outcomes."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "CareerCraft AI | Personalized Career Development Platform"
)
