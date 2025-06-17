import re

def read_resume(file_path):
    resume_text = ''
    try:
        with open (file_path, 'r', encoding='utf-8') as f:
            resume_text = f.read()
        return resume_text
    except FileNotFoundError :
        print(f"Error: The file at '{file_path}' was not found.")
        return None
    
def extract_email(resume_text) :
    if not resume_text:
        return None

    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, resume_text)

    if match:
        return match.group(0) 
    
    return None 


def extract_phone_number(resume_text):
    if not resume_text:
        return None

    pattern = r'(?:\+?\d{1,3})?(?:[.\s\-/()]?\d){7,}'
    match = re.search(pattern, resume_text)

    if match:
        return re.sub(r'[^\d+]', '', match.group(0))
    
    return None 

def extract_skills(resume_text) :
    if not resume_text:
        return None
    
    SKILLS_DB = [
    # Programming Languages
    'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'C', 'PHP', 'Go', 'Ruby', 'Swift', 'Kotlin',

    # Web Frontend
    'HTML', 'CSS', 'Sass', 'React', 'Angular', 'Vue.js', 'jQuery', 'Bootstrap', 'Tailwind CSS',

    # Web Backend
    'Node.js', 'Express.js', 'Laravel', 'Django', 'Flask', 'Ruby on Rails', 'ASP.NET',

    # Databases
    'SQL', 'MySQL', 'PostgreSQL', 'Microsoft SQL Server', 'SQLite', 'MongoDB', 'Redis', 'NoSQL',

    # Networking & Protocols
    'Networking', 'TCP/IP', 'OSI Model', 'HTTP', 'HTTPS', 'DNS', 'FTP', 'SSH', 'SSL', 'TLS', 'Socket Programming',

    # DevOps & Cloud
    'Git', 'GitHub', 'Docker', 'Kubernetes', 'CI/CD', 'Jenkins', 'AWS', 'Azure', 'Google Cloud', 'Terraform',

    # Operating Systems
    'Linux', 'Ubuntu', 'CentOS', 'Windows Server',

    # Concepts & Methodologies
    'Agile', 'Scrum', 'REST API', 'GraphQL', 'Object-Oriented Programming', 'OOP', 'Data Structures', 'Algorithms'
    ]

    pattern = r'\b(' + '|'.join(re.escape(skill) for skill in SKILLS_DB) + r')\b'
    match = re.findall(pattern, resume_text, re.IGNORECASE)

    if match:
        return list(set(skill.strip() for skill in match))
    
    return None 



if __name__ == "__main__":
    resume_path = 'resume.txt'
    
    resume_content = read_resume(resume_path)

    if resume_content:
        print("--- Resume Content ---")
        print(resume_content)
        print("----------------------\n")
        
        extracted_email = extract_email(resume_content)
        print(f"Email: {extracted_email}" if extracted_email else "Email: Not Found")


        extracted_phone_number = extract_phone_number(resume_content)
        print(f"Phone: {extracted_phone_number}" if extracted_phone_number else "Phone: Not Found")


        extracted_skills = extract_skills(resume_content)
        if extracted_skills:
            print(f"Skills: {', '.join(extracted_skills)}")
        else:
            print("Skills: None Found")
        
        print("----------------------------------\n")

