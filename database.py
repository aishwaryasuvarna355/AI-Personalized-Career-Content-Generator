
import sqlite3
import json
from datetime import datetime

DATABASE_NAME = "career_profiles.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL DEFAULT '',
            email TEXT DEFAULT '',
            branch TEXT DEFAULT '',
            skills TEXT DEFAULT '[]',
            interests TEXT DEFAULT '[]',
            career_goal TEXT DEFAULT '',
            experience_level TEXT DEFAULT '',
            analysis TEXT DEFAULT '{}',
            created_at TEXT DEFAULT ''
        )
    """)

    cursor.execute("PRAGMA table_info(students)")
    existing_columns = {
        column[1] for column in cursor.fetchall()
    }

    required_columns = {
        "name": "TEXT DEFAULT ''",
        "email": "TEXT DEFAULT ''",
        "branch": "TEXT DEFAULT ''",
        "skills": "TEXT DEFAULT '[]'",
        "interests": "TEXT DEFAULT '[]'",
        "career_goal": "TEXT DEFAULT ''",
        "experience_level": "TEXT DEFAULT ''",
        "analysis": "TEXT DEFAULT '{}'",
        "created_at": "TEXT DEFAULT ''"
    }

    for column, definition in required_columns.items():
        if column not in existing_columns:
            cursor.execute(
                f"ALTER TABLE students ADD COLUMN {column} {definition}"
            )

    conn.commit()
    conn.close()


def save_profile(profile, analysis):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students (
            name, email, branch, skills, interests,
            career_goal, experience_level, analysis, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        profile.get("name", ""),
        profile.get("email", ""),
        profile.get("branch", ""),
        json.dumps(profile.get("skills", [])),
        json.dumps(profile.get("interests", [])),
        profile.get("career_goal", ""),
        profile.get("experience_level", ""),
        json.dumps(analysis),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_all_profiles():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, branch, career_goal, created_at
        FROM students
        ORDER BY id DESC
    """)

    records = cursor.fetchall()
    conn.close()

    return records


def get_profile_by_id(profile_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id, name, email, branch, skills, interests,
            career_goal, experience_level, analysis, created_at
        FROM students
        WHERE id = ?
    """, (profile_id,))

    record = cursor.fetchone()
    conn.close()

    return record
