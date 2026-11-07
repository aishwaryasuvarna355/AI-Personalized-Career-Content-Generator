
"""
AI-Based Personalized Career Content Generator
Core AI engine using OpenAI API.

Responsibilities:
1. Professional summary generation
2. Skill-gap analysis
3. Personalized learning roadmap
4. Interview preparation
5. Consistent multi-format career content
"""

import os
import json
import re
from typing import Any

from openai import OpenAI


DEFAULT_MODEL = "gpt-4o-mini"


def validate_profile(profile: dict) -> dict:
    """Validate and normalize student profile information."""

    if not isinstance(profile, dict):
        raise ValueError("Student profile must be a dictionary.")

    normalized = {
        "name": str(profile.get("name", "")).strip(),
        "degree": str(profile.get("degree", "")).strip(),
        "branch": str(profile.get("branch", "")).strip(),
        "academic_interests": profile.get("academic_interests", []),
        "skills": profile.get("skills", []),
        "career_goal": str(profile.get("career_goal", "")).strip(),
        "projects": profile.get("projects", []),
        "certifications": profile.get("certifications", []),
        "experience_level": str(
            profile.get("experience_level", "Beginner")
        ).strip(),
    }

    if not normalized["career_goal"]:
        raise ValueError("Please provide a career goal.")

    if isinstance(normalized["skills"], str):
        normalized["skills"] = [
            item.strip()
            for item in normalized["skills"].split(",")
            if item.strip()
        ]

    if isinstance(normalized["academic_interests"], str):
        normalized["academic_interests"] = [
            item.strip()
            for item in normalized["academic_interests"].split(",")
            if item.strip()
        ]

    if not isinstance(normalized["skills"], list):
        raise ValueError("Skills must be provided as a list.")

    return normalized


def get_ai_client() -> OpenAI:
    """Create an OpenAI client using the environment API key."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add your API key "
            "to the project's .env file."
        )

    return OpenAI(api_key=api_key, timeout=60.0, max_retries=2)


def build_career_prompt(profile: dict) -> str:
    """Build a detailed prompt using the validated student profile."""

    return f"""
You are CareerCraft AI, an expert student career guidance assistant.

Analyze the following student profile and generate a personalized
career development report.

STUDENT PROFILE:
{json.dumps(profile, indent=2)}

REQUIREMENTS:

1. PROFESSIONAL SUMMARY
- Write a customized professional summary.
- Mention only skills and achievements supported by the profile.
- Never invent work experience, qualifications or certifications.
- Keep the language professional and natural.

2. CAREER SKILL-GAP ANALYSIS
- Identify skills relevant to the student's target career.
- Separate existing skills from missing skills.
- Explain why each missing skill is important.
- Give each skill a priority: High, Medium or Low.
- Suggest practical projects to improve missing skills.
- Calculate a transparent skill match percentage.
- Explain the calculation method.

3. PERSONALIZED LEARNING ROADMAP
- Divide the roadmap into four progressive stages.
- Include learning topics, practical tasks and milestones.
- Give realistic time estimates.
- Recommend recognized learning platforms or resources.
- Do not invent course URLs.

4. INTERVIEW PREPARATION
- Generate 10 role-specific interview questions.
- Include sample answers and the concept being tested.
- Include technical and behavioral questions.
- Adapt the difficulty to the student's experience level.

5. LINKEDIN PROFILE
- Generate a professional LinkedIn headline.
- Generate an About section.
- Use the same verified skills and career goal as the summary.

6. CAREER DEVELOPMENT RECOMMENDATIONS
- Suggest three practical portfolio projects.
- Explain the purpose of each project.
- Suggest measurable next steps.

IMPORTANT:
- All sections must use the SAME student profile.
- Do not create contradictory skills or qualifications.
- Clearly distinguish current skills from recommended skills.
- Never guarantee jobs, placements or salaries.
- Use simple, understandable professional English.

RETURN ONLY VALID JSON using this structure:

{{
  "student_profile": {{
    "name": "",
    "career_goal": "",
    "experience_level": ""
  }},
  "professional_summary": "",
  "skill_gap_analysis": {{
    "matched_skills": [],
    "missing_skills": [],
    "skill_match_percentage": 0,
    "calculation_method": "",
    "recommendations": []
  }},
  "learning_roadmap": [
    {{
      "stage": "",
      "duration": "",
      "topics": [],
      "practical_tasks": [],
      "milestone": ""
    }}
  ],
  "interview_preparation": [
    {{
      "question": "",
      "sample_answer": "",
      "concept_tested": "",
      "difficulty": ""
    }}
  ],
  "linkedin_profile": {{
    "headline": "",
    "about": ""
  }},
  "portfolio_projects": [
    {{
      "title": "",
      "description": "",
      "skills_to_learn": []
    }}
  ],
  "next_steps": []
}}
"""


def generate_career_content(
    student_profile: dict,
    model: str = DEFAULT_MODEL
) -> dict:
    """
    Generate a complete personalized career report using AI.

    Args:
        student_profile: Student information dictionary.
        model: OpenAI model name.

    Returns:
        Dictionary containing all career report sections.
    """

    profile = validate_profile(student_profile)
    client = get_ai_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional AI career advisor. "
                    "Return accurate, structured JSON only."
                )
            },
            {
                "role": "user",
                "content": build_career_prompt(profile)
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.4,
        max_tokens=5000
    )

    result_text = response.choices[0].message.content

    if not result_text:
        raise RuntimeError("The AI returned an empty response.")

    try:
        result = json.loads(result_text)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            "Could not read the AI-generated JSON response."
        ) from error

    required_sections = [
        "student_profile",
        "professional_summary",
        "skill_gap_analysis",
        "learning_roadmap",
        "interview_preparation",
        "linkedin_profile",
        "portfolio_projects",
        "next_steps"
    ]

    missing_sections = [
        section for section in required_sections
        if section not in result
    ]

    if missing_sections:
        raise RuntimeError(
            "AI response is missing sections: "
            + ", ".join(missing_sections)
        )

    # Attach the original profile for traceability.
    result["source_profile"] = profile

    return result


def generate_professional_summary(student_profile: dict) -> str:
    """Generate a personalized professional summary."""

    report = generate_career_content(student_profile)
    return report["professional_summary"]


def analyze_skill_gap(student_profile: dict) -> dict:
    """Generate a personalized skill-gap report."""

    report = generate_career_content(student_profile)
    return report["skill_gap_analysis"]


def generate_learning_roadmap(student_profile: dict) -> list:
    """Generate a personalized learning roadmap."""

    report = generate_career_content(student_profile)
    return report["learning_roadmap"]


def generate_interview_preparation(student_profile: dict) -> list:
    """Generate personalized interview preparation material."""

    report = generate_career_content(student_profile)
    return report["interview_preparation"]
