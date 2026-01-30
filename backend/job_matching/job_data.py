# job_matching/job_data.py

from job_matching.job_schema import Job


JOB_LIST = [

    Job(
        job_id="backend_jr",
        title="Junior Backend Developer",
        description="Build and maintain backend APIs using Python frameworks.",
        required_skills={
            "languages": ["python"],
            "frameworks": ["fastapi", "django"],
            "core_cs": ["dbms", "os"],
            "tools": ["git"]
        },
        category_weights={
            "languages": 0.3,
            "frameworks": 0.3,
            "core_cs": 0.2,
            "tools": 0.2
        }
    ),

    Job(
        job_id="fullstack_jr",
        title="Junior Full Stack Developer",
        description="Develop frontend and backend features for web applications.",
        required_skills={
            "languages": ["python", "javascript"],
            "frameworks": ["react", "fastapi"],
            "core_cs": ["dbms"],
            "tools": ["git"]
        },
        category_weights={
            "languages": 0.25,
            "frameworks": 0.35,
            "core_cs": 0.2,
            "tools": 0.2
        }
    ),

    Job(
        job_id="data_analyst",
        title="Data Analyst",
        description="Analyze data and generate insights using Python and SQL.",
        required_skills={
            "languages": ["python", "sql"],
            "frameworks": [],
            "core_cs": ["dbms"],
            "tools": ["excel", "git"]
        },
        category_weights={
            "languages": 0.4,
            "frameworks": 0.1,
            "core_cs": 0.3,
            "tools": 0.2
        }
    ),

    Job(
        job_id="ml_intern",
        title="Machine Learning Intern",
        description="Assist in building and training machine learning models.",
        required_skills={
            "languages": ["python"],
            "frameworks": ["scikit-learn", "tensorflow"],
            "core_cs": ["statistics"],
            "tools": ["git"]
        },
        category_weights={
            "languages": 0.3,
            "frameworks": 0.4,
            "core_cs": 0.2,
            "tools": 0.1
        }
    ),

    Job(
        job_id="devops_intern",
        title="DevOps Intern",
        description="Support CI/CD pipelines and cloud infrastructure.",
        required_skills={
            "languages": ["python", "bash"],
            "frameworks": [],
            "core_cs": ["os", "networking"],
            "tools": ["docker", "git", "linux"]
        },
        category_weights={
            "languages": 0.2,
            "frameworks": 0.1,
            "core_cs": 0.3,
            "tools": 0.4
        }
    )
]
