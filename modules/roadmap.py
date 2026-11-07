from datetime import datetime, timedelta


LEARNING_RESOURCES = {
    "python": "Python programming fundamentals",
    "machine learning": "Machine learning concepts and algorithms",
    "deep learning": "Neural networks and deep learning",
    "sql": "SQL and database management",
    "java": "Java programming",
    "statistics": "Statistics and probability",
    "pandas": "Data analysis using Pandas",
    "tensorflow": "Deep learning using TensorFlow",
    "pytorch": "Deep learning using PyTorch",
    "data structures": "Data structures and algorithms",
    "algorithms": "Algorithm design and problem solving",
    "excel": "Advanced Excel and data analysis",
    "git": "Git and GitHub version control",
    "data visualization": "Data visualization and dashboards"
}


def generate_learning_roadmap(missing_skills):
    roadmap = []
    start_date = datetime.today()

    for index, skill in enumerate(missing_skills):
        topic = LEARNING_RESOURCES.get(
            skill.lower(),
            f"Learn {skill}"
        )

        week_start = start_date + timedelta(weeks=index)

        roadmap.append({
            "week": index + 1,
            "skill": skill,
            "topic": topic,
            "duration": "1 week",
            "tasks": [
                f"Understand the basics of {skill}",
                f"Practice {skill} with exercises",
                f"Complete a small {skill} project"
            ],
            "target_date": week_start.strftime("%d %B %Y")
        })

    return roadmap


def calculate_roadmap_duration(roadmap):
    return len(roadmap)


def get_roadmap_summary(roadmap):
    return {
        "total_weeks": len(roadmap),
        "total_skills": len(roadmap),
        "message": (
            "Complete each week's learning tasks "
            "and track your progress regularly."
        )
    }