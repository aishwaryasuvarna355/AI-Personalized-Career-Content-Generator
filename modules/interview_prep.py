INTERVIEW_QUESTIONS = {
    "AI Engineer": [
        {
            "question": "What is Artificial Intelligence?",
            "answer": "Artificial Intelligence is a technology that enables machines to perform tasks that normally require human intelligence.",
            "difficulty": "Easy"
        },
        {
            "question": "What is Machine Learning?",
            "answer": "Machine Learning is a branch of AI where computers learn patterns from data and make predictions.",
            "difficulty": "Easy"
        },
        {
            "question": "What is the difference between AI and ML?",
            "answer": "AI is the broader concept of intelligent machines. ML is a technique that helps machines learn from data.",
            "difficulty": "Medium"
        },
        {
            "question": "What is overfitting?",
            "answer": "Overfitting happens when a model learns training data too closely and performs poorly on new data.",
            "difficulty": "Medium"
        }
    ],

    "Data Scientist": [
        {
            "question": "What is Data Science?",
            "answer": "Data Science uses statistics, programming and analytical methods to extract useful information from data.",
            "difficulty": "Easy"
        },
        {
            "question": "What is data preprocessing?",
            "answer": "Data preprocessing means cleaning and preparing raw data before analysis or model training.",
            "difficulty": "Easy"
        },
        {
            "question": "What is a dataset?",
            "answer": "A dataset is a collection of related data arranged in rows and columns or another structured format.",
            "difficulty": "Easy"
        },
        {
            "question": "What is correlation?",
            "answer": "Correlation measures how two variables are related to each other.",
            "difficulty": "Medium"
        }
    ],

    "Software Developer": [
        {
            "question": "What is object-oriented programming?",
            "answer": "OOP is a programming approach based on objects and classes.",
            "difficulty": "Easy"
        },
        {
            "question": "What is a data structure?",
            "answer": "A data structure is a way of organizing and storing data efficiently.",
            "difficulty": "Easy"
        },
        {
            "question": "What is an API?",
            "answer": "An API allows different software applications to communicate with each other.",
            "difficulty": "Medium"
        },
        {
            "question": "What is version control?",
            "answer": "Version control tracks changes in source code and helps developers work together.",
            "difficulty": "Medium"
        }
    ],

    "Data Analyst": [
        {
            "question": "What is data analysis?",
            "answer": "Data analysis is the process of examining data to find useful information and patterns.",
            "difficulty": "Easy"
        },
        {
            "question": "What is SQL?",
            "answer": "SQL is a language used to store, retrieve and manage data in relational databases.",
            "difficulty": "Easy"
        },
        {
            "question": "What is a dashboard?",
            "answer": "A dashboard displays important information and measurements using charts and visual elements.",
            "difficulty": "Easy"
        },
        {
            "question": "What is data visualization?",
            "answer": "Data visualization presents information through charts, graphs and other visual formats.",
            "difficulty": "Medium"
        }
    ]
}


def generate_interview_questions(career):
    return INTERVIEW_QUESTIONS.get(career, [])


def get_questions_by_difficulty(career, difficulty):
    questions = generate_interview_questions(career)

    return [
        question for question in questions
        if question["difficulty"].lower() == difficulty.lower()
    ]


def get_interview_summary(career):
    questions = generate_interview_questions(career)

    return {
        "career": career,
        "total_questions": len(questions),
        "easy": sum(
            1 for q in questions
            if q["difficulty"] == "Easy"
        ),
        "medium": sum(
            1 for q in questions
            if q["difficulty"] == "Medium"
        )
    }