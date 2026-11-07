
CAREER_ROLES = {
    "AI Engineer": {
        "required_skills": [
            "Python", "Machine Learning", "Deep Learning",
            "TensorFlow", "PyTorch", "Data Structures"
        ],
        "interests": [
            "Artificial Intelligence", "Machine Learning",
            "Deep Learning", "Neural Networks"
        ],
        "description": "Develops intelligent systems and AI applications.",
        "projects": [
            "AI Chatbot",
            "Image Classification System",
            "Recommendation System"
        ]
    },

    "Data Scientist": {
        "required_skills": [
            "Python", "SQL", "Statistics",
            "Machine Learning", "Pandas", "Data Visualization"
        ],
        "interests": [
            "Data Science", "Data Analysis",
            "Statistics", "Predictive Analytics"
        ],
        "description": "Uses data to discover patterns and make predictions.",
        "projects": [
            "Sales Prediction",
            "Customer Segmentation",
            "Student Performance Analysis"
        ]
    },

    "Software Developer": {
        "required_skills": [
            "Python", "Java", "Data Structures",
            "Algorithms", "SQL", "Git"
        ],
        "interests": [
            "Software Development", "Application Development",
            "Programming", "Web Development"
        ],
        "description": "Designs and develops software applications.",
        "projects": [
            "Online Booking System",
            "Student Management System",
            "Task Management Application"
        ]
    },

    "Data Analyst": {
        "required_skills": [
            "SQL", "Excel", "Python",
            "Pandas", "Statistics", "Data Visualization"
        ],
        "interests": [
            "Data Analysis", "Business Analytics",
            "Data Visualization", "Statistics"
        ],
        "description": "Studies data and creates meaningful reports.",
        "projects": [
            "Business Dashboard",
            "Sales Data Analysis",
            "Customer Insights Report"
        ]
    }
}


def normalize_items(items):
    return {
        item.strip().lower()
        for item in items
        if item.strip()
    }


def analyze_career_profile(student_skills, student_interests=None):

    student_skills_set = normalize_items(student_skills)
    student_interests_set = normalize_items(student_interests or [])

    results = []

    for role, details in CAREER_ROLES.items():

        required_skills = normalize_items(
            details["required_skills"]
        )

        required_interests = normalize_items(
            details["interests"]
        )

        matched_skills = sorted(
            student_skills_set.intersection(required_skills)
        )

        missing_skills = sorted(
            required_skills.difference(student_skills_set)
        )

        matched_interests = sorted(
            student_interests_set.intersection(required_interests)
        )

        skill_score = (
            len(matched_skills) / len(required_skills)
        ) * 100

        interest_score = (
            len(matched_interests) / len(required_interests)
        ) * 100

        final_score = round(
            (skill_score * 0.70) +
            (interest_score * 0.30)
        )

        results.append({
            "career": role,
            "description": details["description"],
            "match_percentage": final_score,
            "skill_score": round(skill_score),
            "interest_score": round(interest_score),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "matched_interests": matched_interests,
            "projects": details["projects"]
        })

    results.sort(
        key=lambda item: item["match_percentage"],
        reverse=True
    )

    return results


def get_skill_recommendations(missing_skills):

    recommendations = {}

    for skill in missing_skills:
        recommendations[skill] = (
            f"Learn {skill} through structured lessons, "
            "practice exercises and practical projects."
        )

    return recommendations



def explain_career_match(career_result):

    career = career_result["career"]
    skill_score = career_result["skill_score"]
    interest_score = career_result["interest_score"]

    matched_skills = career_result["matched_skills"]
    matched_interests = career_result["matched_interests"]

    explanation = []

    explanation.append(
        f"{career} was recommended based on your profile."
    )

    explanation.append(
        f"Your technical skill match is {skill_score}%."
    )

    explanation.append(
        f"Your interest match is {interest_score}%."
    )

    if matched_skills:
        explanation.append(
            "Your matching skills include: "
            + ", ".join(matched_skills)
        )

    if matched_interests:
        explanation.append(
            "Your matching interests include: "
            + ", ".join(matched_interests)
        )

    if career_result["missing_skills"]:
        explanation.append(
            "Skills you can improve: "
            + ", ".join(career_result["missing_skills"])
        )

    return explanation



def get_project_recommendations(career_result):

    projects = career_result.get("projects", [])

    recommendations = []

    for index, project in enumerate(projects, start=1):
        recommendations.append({
            "project_id": index,
            "project_name": project,
            "career": career_result["career"],
            "purpose": (
                f"This project helps develop practical "
                f"skills related to {career_result['career']}."
            )
        })

    return recommendations
