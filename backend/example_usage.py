"""
Example usage of the RAG Resume Scorer API
"""

import requests
import json


BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_analyze_with_files(resume_path: str, jd_path: str):
    """
    Test analyzing with file uploads
    
    Args:
        resume_path: Path to resume file
        jd_path: Path to job description file
    """
    print(f"Analyzing resume '{resume_path}' against JD '{jd_path}'...")
    
    with open(resume_path, 'rb') as resume_file, open(jd_path, 'rb') as jd_file:
        files = {
            'resume': resume_file,
            'jd': jd_file
        }
        response = requests.post(f"{BASE_URL}/api/analyze", files=files)
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response:\n{json.dumps(result, indent=2)}\n")
    
    return result


def test_analyze_with_text(resume_text: str, jd_text: str):
    """
    Test analyzing with text input
    
    Args:
        resume_text: Resume content as text
        jd_text: Job description as text
    """
    print("Analyzing resume text against JD text...")
    
    payload = {
        "resume_text": resume_text,
        "jd_text": jd_text
    }
    
    response = requests.post(f"{BASE_URL}/api/analyze-text", json=payload)
    
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response:\n{json.dumps(result, indent=2)}\n")
    
    return result


def sample_resume():
    """Sample resume text"""
    return """
    JOHN DOE
    Email: john@example.com | Phone: +1-234-567-8900
    
    PROFESSIONAL SUMMARY
    Experienced Python Developer with 5+ years of experience developing web applications
    using FastAPI, Flask, and Django. Strong background in machine learning and data analysis.
    
    TECHNICAL SKILLS
    - Languages: Python, JavaScript, SQL
    - Frameworks: FastAPI, Flask, Django, React
    - Databases: PostgreSQL, MongoDB, Redis
    - Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
    - Tools: Git, Jenkins, Docker, Kubernetes, Apache Airflow
    
    WORK EXPERIENCE
    
    Senior Python Developer | Tech Corp | 2020 - Present
    - Led development of microservices architecture using FastAPI
    - Implemented machine learning models for data analysis
    - Deployed applications on AWS using Docker and Kubernetes
    - Mentored junior developers
    
    Python Developer | StartUp Inc | 2018 - 2020
    - Developed REST APIs using Flask and FastAPI
    - Implemented automated testing and CI/CD pipelines
    - Optimized database queries improving performance by 40%
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology, 2018
    """


def sample_jd():
    """Sample job description"""
    return """
    JOB DESCRIPTION
    
    Position: Senior Python Developer
    Location: Remote
    
    About the Role:
    We are looking for an experienced Python Developer to join our growing team.
    You will be responsible for designing and implementing scalable backend systems.
    
    Key Responsibilities:
    - Develop and maintain Python microservices using FastAPI
    - Design and implement RESTful APIs
    - Collaborate with data science team on ML integration
    - Implement automated testing and maintain code quality
    - Deploy and manage applications on cloud platforms
    
    Required Skills:
    - 5+ years of Python development experience
    - Strong knowledge of FastAPI or similar frameworks
    - Experience with microservices architecture
    - Proficiency with Docker and Kubernetes
    - Experience with AWS or similar cloud platforms
    - Strong SQL and database design knowledge
    - Git and version control expertise
    
    Preferred Skills:
    - Machine learning model integration
    - Experience with Apache Airflow
    - Knowledge of MongoDB and NoSQL databases
    - AWS certification
    
    Education:
    Bachelor's degree in Computer Science or related field
    """


if __name__ == "__main__":
    print("\n" + "="*60)
    print("RAG Resume Scorer - Example Usage")
    print("="*60 + "\n")
    
    # Test health check
    test_health_check()
    
    # Test with text
    resume = sample_resume()
    jd = sample_jd()
    
    print("Testing with text input:")
    print("-" * 60)
    result = test_analyze_with_text(resume, jd)
    
    print("\nAnalysis complete!")
    if result.get("success"):
        data = result.get("data", {})
        print(f"Score: {data.get('score')}/100")
        print(f"Assessment: {data.get('assessment')}")
