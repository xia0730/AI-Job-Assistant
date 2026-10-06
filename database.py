import sqlite3


# 数据库文件名称
DATABASE_NAME = "ai_job_assistant.db"


def get_connection():
    """
    连接 SQLite 数据库。
    如果数据库文件不存在，SQLite 会自动创建。
    """
    return sqlite3.connect(DATABASE_NAME)


def init_database():
    """
    初始化数据库，创建项目需要的数据表。
    """

    conn = get_connection()
    cursor = conn.cursor()

    # =========================
    # 1. 简历表
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # =========================
    # 2. 岗位表
    # =========================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            position TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# =========================
# 简历相关功能
# =========================

def save_resume(name, content):
    """
    保存一份简历。
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO resumes (name, content)
        VALUES (?, ?)
        """,
        (name, content)
    )

    conn.commit()
    conn.close()


def get_resumes():
    """
    查询数据库中的所有简历。
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, content, created_at
        FROM resumes
        ORDER BY id DESC
    """)

    resumes = cursor.fetchall()

    conn.close()

    return resumes


def get_resume_by_id(resume_id):
    """
    根据简历 ID 查询指定简历。
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, content, created_at
        FROM resumes
        WHERE id = ?
        """,
        (resume_id,)
    )

    resume = cursor.fetchone()

    conn.close()

    return resume


# =========================
# 岗位相关功能
# =========================

def save_job(company, position, content):
    """
    保存一份岗位信息。
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO jobs (company, position, content)
        VALUES (?, ?, ?)
        """,
        (company, position, content)
    )

    conn.commit()
    conn.close()


def get_jobs():
    """
    查询数据库中的所有岗位。
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, company, position, content, created_at
        FROM jobs
        ORDER BY id DESC
    """)

    jobs = cursor.fetchall()

    conn.close()

    return jobs


def get_job_by_id(job_id):
    """
    根据岗位 ID 查询指定岗位。
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, company, position, content, created_at
        FROM jobs
        WHERE id = ?
        """,
        (job_id,)
    )

    job = cursor.fetchone()

    conn.close()

    return job


# =========================
# 单独运行 database.py 时初始化数据库
# =========================

if __name__ == "__main__":
    init_database()
    print("数据库初始化成功。")