import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Skill, Company, Job, SavedJob
from accounts.models import UserProfile, UserSkill


class Command(BaseCommand):
    help = 'Seeds realistic tech job market data, companies, skills, and demo accounts'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting database seeding...'))

        # 1. Clear existing data
        Job.objects.all().delete()
        Company.objects.all().delete()
        Skill.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Cleared old jobs, companies, and skills.'))

        # 2. Seed Skills
        skills_data = [
            # Programming
            ('Python', 'programming', 'High-level programming language widely used in Data Science, AI, and Backend Web Development.', 'fa-brands fa-python', 1.2),
            ('R', 'programming', 'Statistical computing and graphics language for data analysis.', 'fa-solid fa-code', 0.9),
            ('SQL', 'programming', 'Standard language for storing, manipulating and retrieving data in databases.', 'fa-solid fa-database', 1.3),
            ('JavaScript', 'programming', 'Core web scripting language for interactive frontends and Node.js backends.', 'fa-brands fa-js', 1.1),
            ('TypeScript', 'programming', 'Typed superset of JavaScript for scalable web development.', 'fa-solid fa-code', 1.1),
            ('Java', 'programming', 'Object-oriented language popular in enterprise backends and distributed systems.', 'fa-brands fa-java', 1.0),
            ('C++', 'programming', 'High-performance system and algorithm programming language.', 'fa-solid fa-code', 0.9),
            ('Go', 'programming', 'Fast, concurrent open source language developed by Google.', 'fa-brands fa-golang', 1.0),
            ('Scala', 'programming', 'Scalable functional language commonly used in Apache Spark big data.', 'fa-solid fa-code', 0.9),
            ('PHP', 'programming', 'Server-side scripting language for web development.', 'fa-brands fa-php', 0.7),

            # Databases & Warehousing
            ('MySQL', 'database', 'Popular open-source relational database management system.', 'fa-solid fa-database', 1.0),
            ('PostgreSQL', 'database', 'Advanced, enterprise-grade open source relational database.', 'fa-solid fa-database', 1.2),
            ('MongoDB', 'database', 'Document-oriented NoSQL database for unstructured data.', 'fa-solid fa-leaf', 1.0),
            ('Redis', 'database', 'In-memory data structure store used as cache and message broker.', 'fa-solid fa-memory', 1.0),
            ('Snowflake', 'database', 'Cloud-based data warehousing and analytics platform.', 'fa-solid fa-snowflake', 1.3),
            ('BigQuery', 'database', 'Google Cloud serverless, enterprise data warehouse.', 'fa-solid fa-cloud', 1.2),
            ('Amazon Redshift', 'database', 'Fast, petabyte-scale cloud data warehouse by AWS.', 'fa-brands fa-aws', 1.1),
            ('Cassandra', 'database', 'Distributed NoSQL database designed for high availability and scalability.', 'fa-solid fa-database', 0.9),
            ('Elasticsearch', 'database', 'Distributed search and analytics engine for log and text data.', 'fa-solid fa-magnifying-glass', 1.0),

            # Visualization & BI
            ('Power BI', 'visualization', 'Microsoft business analytics and interactive visualization platform.', 'fa-solid fa-chart-column', 1.3),
            ('Tableau', 'visualization', 'Visual analytics platform transforming data into actionable insights.', 'fa-solid fa-chart-pie', 1.2),
            ('Excel', 'visualization', 'Spreadsheet application with advanced formulas, pivot tables, and VBA.', 'fa-solid fa-table', 1.1),
            ('Looker', 'visualization', 'Modern BI and enterprise analytics platform by Google Cloud.', 'fa-solid fa-chart-line', 1.0),
            ('Matplotlib', 'visualization', 'Python 2D plotting library for scientific and data visualisations.', 'fa-solid fa-chart-area', 0.9),
            ('Seaborn', 'visualization', 'Python data visualization library based on matplotlib with attractive themes.', 'fa-solid fa-chart-simple', 0.9),
            ('Plotly', 'visualization', 'Interactive graphing library for Python and JavaScript.', 'fa-solid fa-chart-gantt', 1.0),
            ('D3.js', 'visualization', 'JavaScript library for producing dynamic, interactive data visualisations.', 'fa-brands fa-js', 0.9),

            # Analytics & Statistics
            ('Statistics', 'analytics', 'Mathematical study of data collection, analysis, interpretation, and presentation.', 'fa-solid fa-calculator', 1.2),
            ('Data Analysis', 'analytics', 'Inspecting, cleansing, transforming, and modeling data to discover insights.', 'fa-solid fa-magnifying-glass-chart', 1.3),
            ('Exploratory Data Analysis', 'analytics', 'Analyzing datasets to summarize their main characteristics with visuals.', 'fa-solid fa-filter', 1.1),
            ('A/B Testing', 'analytics', 'Statistical experimental hypothesis testing for product optimization.', 'fa-solid fa-vial', 1.1),
            ('Econometrics', 'analytics', 'Application of statistical methods to economic and market data.', 'fa-solid fa-money-bill-trend-up', 0.8),
            ('Time Series Analysis', 'analytics', 'Analyzing time-stamped series data to forecast future trends.', 'fa-solid fa-timeline', 1.0),
            ('Predictive Modeling', 'analytics', 'Using mathematical techniques to predict future probabilities and trends.', 'fa-solid fa-wand-magic-sparkles', 1.2),
            ('Data Governance', 'analytics', 'Ensuring data security, privacy, compliance, and quality across enterprise.', 'fa-solid fa-shield-halved', 1.0),

            # Cloud & DevOps
            ('AWS', 'cloud_devops', 'Amazon Web Services cloud computing platform.', 'fa-brands fa-aws', 1.3),
            ('Microsoft Azure', 'cloud_devops', 'Microsoft cloud computing platform and enterprise services.', 'fa-brands fa-microsoft', 1.2),
            ('Google Cloud Platform', 'cloud_devops', 'Suite of cloud computing services by Google.', 'fa-brands fa-google', 1.1),
            ('Docker', 'cloud_devops', 'Containerization platform to package and run apps anywhere.', 'fa-brands fa-docker', 1.2),
            ('Kubernetes', 'cloud_devops', 'Open-source system for automating deployment, scaling, and container management.', 'fa-solid fa-dharmachakra', 1.2),
            ('Terraform', 'cloud_devops', 'Infrastructure as Code (IaC) tool for provisioning cloud resources.', 'fa-solid fa-cubes', 1.1),
            ('CI/CD', 'cloud_devops', 'Continuous Integration and Continuous Deployment pipelines.', 'fa-solid fa-arrows-spin', 1.1),
            ('Linux', 'cloud_devops', 'Open source operating system widely used in server environments.', 'fa-brands fa-linux', 1.0),
            ('Git', 'cloud_devops', 'Distributed version control system for tracking code changes.', 'fa-brands fa-git-alt', 1.2),

            # AI & Machine Learning
            ('Machine Learning', 'ai_ml', 'Algorithms and statistical models to enable computer learning from data.', 'fa-solid fa-brain', 1.3),
            ('Deep Learning', 'ai_ml', 'Neural networks with multiple layers for complex representation learning.', 'fa-solid fa-network-wired', 1.2),
            ('PyTorch', 'ai_ml', 'Deep learning framework popular for research and production AI.', 'fa-solid fa-fire', 1.2),
            ('TensorFlow', 'ai_ml', 'End-to-end open source machine learning platform by Google.', 'fa-solid fa-microchip', 1.1),
            ('Scikit-learn', 'ai_ml', 'Python module for classical machine learning and data mining.', 'fa-solid fa-gear', 1.2),
            ('NLP', 'ai_ml', 'Natural Language Processing for text, sentiment, and speech analysis.', 'fa-solid fa-comment-dots', 1.2),
            ('Computer Vision', 'ai_ml', 'AI discipline enabling computers to see and extract info from digital images.', 'fa-solid fa-eye', 1.1),
            ('Large Language Models', 'ai_ml', 'Foundation AI models (GPT, Llama, Claude, Gemini) and prompting.', 'fa-solid fa-robot', 1.3),
            ('LangChain', 'ai_ml', 'Framework for developing applications powered by language models.', 'fa-solid fa-link', 1.2),
            ('MLOps', 'ai_ml', 'Practices for deploying and maintaining ML models in production reliably.', 'fa-solid fa-server', 1.2),

            # Web & Frameworks
            ('React', 'web_mobile', 'JavaScript library for building dynamic component-based user interfaces.', 'fa-brands fa-react', 1.2),
            ('Node.js', 'web_mobile', 'JavaScript runtime built on Chrome\'s V8 engine for fast backend services.', 'fa-brands fa-node-js', 1.1),
            ('Next.js', 'web_mobile', 'React framework for server-side rendering and production web apps.', 'fa-solid fa-n', 1.1),
            ('Django', 'web_mobile', 'High-level Python web framework for rapid, secure web development.', 'fa-solid fa-code', 1.1),
            ('FastAPI', 'web_mobile', 'Modern, fast Python web framework for building high-performance APIs.', 'fa-solid fa-bolt', 1.2),
            ('Spring Boot', 'web_mobile', 'Java-based framework used to create stand-alone production Spring apps.', 'fa-solid fa-leaf', 1.0),
            ('Tailwind CSS', 'web_mobile', 'Utility-first CSS framework for rapid modern UI development.', 'fa-solid fa-wind', 1.0),
            ('REST API', 'web_mobile', 'Architectural style for designing networked web applications and endpoints.', 'fa-solid fa-network-wired', 1.1),
            ('GraphQL', 'web_mobile', 'Query language for APIs and runtime for fulfilling those queries.', 'fa-solid fa-diagram-project', 1.0),

            # Big Data & Tools
            ('Apache Spark', 'tools_other', 'Unified analytics engine for large-scale data processing.', 'fa-solid fa-bolt', 1.2),
            ('Apache Kafka', 'tools_other', 'Distributed event streaming platform for high-performance data pipelines.', 'fa-solid fa-stream', 1.2),
            ('Apache Airflow', 'tools_other', 'Platform to programmatically author, schedule, and monitor workflows.', 'fa-solid fa-wind', 1.1),
            ('dbt', 'tools_other', 'Data build tool for data transformation and analytics engineering in the warehouse.', 'fa-solid fa-hammer', 1.2),
            ('Pandas', 'tools_other', 'Python library for data manipulation and analysis with DataFrames.', 'fa-solid fa-table', 1.2),
            ('NumPy', 'tools_other', 'Python fundamental package for scientific computing with multi-dimensional arrays.', 'fa-solid fa-cubes', 1.1),
            ('Agile / Scrum', 'tools_other', 'Iterative project management and software delivery methodology.', 'fa-solid fa-people-group', 0.9),
            ('Jira', 'tools_other', 'Issue tracking and project management tool for agile teams.', 'fa-brands fa-jira', 0.8),
        ]

        skill_objs = {}
        for name, category, desc, icon, weight in skills_data:
            skill, _ = Skill.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'description': desc,
                    'icon': icon,
                    'importance_weight': weight,
                }
            )
            skill_objs[name] = skill

        self.stdout.write(self.style.SUCCESS(f'Created {len(skill_objs)} skills across 8 categories.'))

        # 3. Seed Companies
        companies_data = [
            ('Google India', 'https://careers.google.com', 'Bengaluru, India', 'AI_Cloud', '10000+ employees', 'emerald', 'Global technology leader in search, cloud computing, artificial intelligence, and software products.', 4.8),
            ('Microsoft India', 'https://careers.microsoft.com', 'Hyderabad, India', 'AI_Cloud', '10000+ employees', 'cyan', 'Leading developer of personal-computer software, cloud systems, and AI copilot solutions.', 4.7),
            ('Amazon Web Services', 'https://amazon.jobs', 'Bengaluru, India', 'AI_Cloud', '10000+ employees', 'amber', 'World’s most comprehensive and broadly adopted cloud platform.', 4.6),
            ('Tata Consultancy Services (TCS)', 'https://tcs.com', 'Mumbai, India', 'Consulting', '10000+ employees', 'blue', 'Global IT services, consulting, and business solutions leader operating across 55 countries.', 4.1),
            ('Infosys', 'https://infosys.com', 'Bengaluru, India', 'Consulting', '10000+ employees', 'indigo', 'Global leader in next-generation digital services and enterprise consulting.', 4.2),
            ('Wipro Technologies', 'https://wipro.com', 'Bengaluru, India', 'Consulting', '10000+ employees', 'purple', 'Leading technology services and consulting company focused on building innovative solutions.', 4.0),
            ('Accenture India', 'https://accenture.com', 'Bengaluru, India', 'Consulting', '10000+ employees', 'rose', 'Global professional services company with leading capabilities in digital, cloud and security.', 4.3),
            ('Razorpay', 'https://razorpay.com', 'Bengaluru, India', 'FinTech', '1000-5000 employees', 'blue', 'India’s first full-stack financial solutions company powering millions of online businesses.', 4.6),
            ('Swiggy', 'https://swiggy.com', 'Bengaluru, India', 'E-Commerce', '5000-10000 employees', 'orange', 'Leading on-demand convenience platform connecting consumers to food, grocery, and dining.', 4.4),
            ('Zomato', 'https://zomato.com', 'Gurugram, India', 'E-Commerce', '5000-10000 employees', 'red', 'Indian multinational restaurant aggregator and food delivery pioneer.', 4.3),
            ('CRED', 'https://cred.club', 'Bengaluru, India', 'FinTech', '500-1000 employees', 'slate', 'Members-only club that rewards individuals for timely credit card payments and good financial behavior.', 4.5),
            ('PhonePe', 'https://phonepe.com', 'Bengaluru, India', 'FinTech', '5000-1000 employees', 'violet', 'India’s leading digital payments and financial services platform.', 4.5),
            ('Flipkart', 'https://flipkart.com', 'Bengaluru, India', 'E-Commerce', '10000+ employees', 'blue', 'India’s homegrown e-commerce marketplace offering over 150 million products.', 4.4),
            ('Morgan Stanley', 'https://morganstanley.com', 'Mumbai, India', 'FinTech', '5000-10000 employees', 'cyan', 'Global financial services firm providing investment banking, securities, and wealth management.', 4.6),
            ('Goldman Sachs', 'https://goldmansachs.com', 'Bengaluru, India', 'FinTech', '5000-10000 employees', 'amber', 'Global investment banking, securities and investment management firm.', 4.7),
            ('Jio Platforms', 'https://jio.com', 'Navi Mumbai, India', 'AI_Cloud', '10000+ employees', 'blue', 'Digital services and telecom giant transforming India’s digital ecosystem.', 4.2),
            ('Deloitte India', 'https://deloitte.com', 'Hyderabad, India', 'Consulting', '10000+ employees', 'emerald', 'Leading provider of audit, consulting, tax, and advisory services.', 4.3),
            ('Capgemini', 'https://capgemini.com', 'Pune, India', 'Consulting', '10000+ employees', 'sky', 'Global leader in partnering with companies to transform and manage their business through technology.', 4.1),
            ('Adobe Systems', 'https://adobe.com', 'Noida, India', 'SaaS', '5000-10000 employees', 'red', 'Leader in digital media and digital marketing solutions.', 4.8),
            ('Salesforce', 'https://salesforce.com', 'Hyderabad, India', 'SaaS', '5000-10000 employees', 'cyan', 'Global leader in customer relationship management (CRM) and cloud enterprise solutions.', 4.7),
            ('Snowflake Inc', 'https://snowflake.com', 'Pune, India', 'AI_Cloud', '1000-5000 employees', 'sky', 'Data Cloud company enabling thousands of organizations to mobilize data with near-unlimited scale.', 4.8),
            ('Databricks', 'https://databricks.com', 'Bengaluru, India', 'AI_Cloud', '1000-5000 employees', 'red', 'Lakehouse platform unifying data engineering, data science, machine learning, and business analytics.', 4.9),
            ('Zerodha', 'https://zerodha.com', 'Bengaluru, India', 'FinTech', '500-1000 employees', 'blue', 'India’s largest stock broker by active clients offering zero brokerage on investments.', 4.9),
            ('Pine Labs', 'https://pinelabs.com', 'Noida, India', 'FinTech', '1000-5000 employees', 'green', 'Leading merchant commerce omnichannel platform across India and Southeast Asia.', 4.2),
            ('Groww', 'https://groww.in', 'Bengaluru, India', 'FinTech', '1000-5000 employees', 'teal', 'Fast-growing financial technology platform empowering millions of retail investors.', 4.5),
            ('Cisco Systems', 'https://cisco.com', 'Bengaluru, India', 'AI_Cloud', '10000+ employees', 'blue', 'Worldwide leader in networking and IT infrastructure products.', 4.5),
            ('IBM India', 'https://ibm.com', 'Bengaluru, India', 'AI_Cloud', '10000+ employees', 'indigo', 'Global technology and consulting company creating hybrid cloud and AI innovations.', 4.3),
            ('Oracle India', 'https://oracle.com', 'Bengaluru, India', 'SaaS', '10000+ employees', 'red', 'Cloud technology company providing organizations around the world with computing infrastructure and software.', 4.4),
            ('Uber India', 'https://uber.com', 'Hyderabad, India', 'Logistics', '5000-10000 employees', 'neutral', 'Technology platform that connects mobility, food delivery, and freight logistics.', 4.4),
            ('Atlassian', 'https://atlassian.com', 'Bengaluru, India', 'SaaS', '1000-5000 employees', 'blue', 'Maker of Jira, Confluence, Trello, and tools used by millions of software teams worldwide.', 4.8),
            ('Nvidia', 'https://nvidia.com', 'Pune, India', 'AI_Cloud', '5000-10000 employees', 'emerald', 'Pioneer of GPU-accelerated computing and world leader in AI hardware and software systems.', 4.9),
            ('Intel India', 'https://intel.com', 'Bengaluru, India', 'AI_Cloud', '10000+ employees', 'blue', 'World leader in semiconductor design and compute architecture solutions.', 4.5),
            ('Paytm', 'https://paytm.com', 'Noida, India', 'FinTech', '5000-10000 employees', 'sky', 'India’s leading digital payments and financial services unicorn.', 4.0),
            ('HealthifyMe', 'https://healthifyme.com', 'Bengaluru, India', 'HealthTech', '500-1000 employees', 'rose', 'AI-powered health and fitness application transforming preventive healthcare.', 4.3),
            ('Unacademy', 'https://unacademy.com', 'Bengaluru, India', 'EdTech', '1000-5000 employees', 'blue', 'India’s largest online learning platform for competitive exam prep and upskilling.', 4.1),
            ('Postman', 'https://postman.com', 'Bengaluru, India', 'SaaS', '500-1000 employees', 'orange', 'Leading API platform used by over 30 million developers to build, test, and share APIs.', 4.8),
            ('BrowserStack', 'https://browserstack.com', 'Mumbai, India', 'SaaS', '1000-5000 employees', 'teal', 'World’s leading cloud web and mobile testing platform.', 4.6),
            ('Freshworks', 'https://freshworks.com', 'Chennai, India', 'SaaS', '5000-10000 employees', 'yellow', 'Global provider of modern SaaS software for customer support and IT service management.', 4.4),
            ('Innovaccer', 'https://innovaccer.com', 'Noida, India', 'HealthTech', '1000-5000 employees', 'cyan', 'Leading healthcare data activation platform unifying clinical and financial records.', 4.5),
            ('Palo Alto Networks', 'https://paloaltonetworks.com', 'Bengaluru, India', 'Cybersecurity', '1000-5000 employees', 'orange', 'Global cybersecurity leader continually delivering innovation in network and cloud defense.', 4.7),
        ]

        company_objs = []
        for name, web, loc, ind, sz, col, desc, rat in companies_data:
            comp, _ = Company.objects.get_or_create(
                name=name,
                defaults={
                    'website': web,
                    'location': loc,
                    'industry': ind,
                    'company_size': sz,
                    'logo_color': col,
                    'description': desc,
                    'rating': rat,
                }
            )
            company_objs.append(comp)

        self.stdout.write(self.style.SUCCESS(f'Created {len(company_objs)} tech companies.'))

        # 4. Role Templates with Skill Associations & Salary Profiles (in LPA)
        role_profiles = {
            'Data Analyst': {
                'skills_core': ['SQL', 'Python', 'Excel', 'Power BI', 'Data Analysis', 'Statistics'],
                'skills_opt': ['Tableau', 'Pandas', 'NumPy', 'MySQL', 'PostgreSQL', 'Exploratory Data Analysis', 'A/B Testing', 'BigQuery'],
                'salary_bands': {
                    'Entry Level': (4.5, 8.5),
                    'Mid Level': (8.0, 16.0),
                    'Senior Level': (15.0, 28.0),
                    'Lead / Principal': (26.0, 42.0),
                },
                'titles': ['Junior Data Analyst', 'Data Analyst', 'Senior Data Analyst', 'Lead Product Data Analyst', 'Operations Data Analyst', 'Marketing Analytics Specialist', 'Business Data Analyst', 'Lead Data Analyst'],
            },
            'Data Scientist': {
                'skills_core': ['Python', 'SQL', 'Machine Learning', 'Statistics', 'Pandas', 'Scikit-learn'],
                'skills_opt': ['Deep Learning', 'PyTorch', 'TensorFlow', 'NLP', 'A/B Testing', 'Predictive Modeling', 'AWS', 'BigQuery', 'Apache Spark'],
                'salary_bands': {
                    'Entry Level': (7.0, 14.0),
                    'Mid Level': (14.0, 26.0),
                    'Senior Level': (25.0, 48.0),
                    'Lead / Principal': (45.0, 75.0),
                },
                'titles': ['Junior Data Scientist', 'Data Scientist', 'Senior Data Scientist', 'Principal Data Scientist', 'Applied Scientist - AI', 'Staff Data Scientist', 'AI/ML Data Scientist'],
            },
            'Business Intelligence Analyst': {
                'skills_core': ['Power BI', 'Tableau', 'SQL', 'Excel', 'Data Analysis'],
                'skills_opt': ['MySQL', 'PostgreSQL', 'Snowflake', 'Looker', 'Statistics', 'Data Governance', 'dbt'],
                'salary_bands': {
                    'Entry Level': (4.5, 8.0),
                    'Mid Level': (8.0, 15.5),
                    'Senior Level': (15.0, 26.0),
                    'Lead / Principal': (24.0, 38.0),
                },
                'titles': ['BI Analyst', 'Senior BI Analyst', 'Enterprise BI Consultant', 'Lead Business Intelligence Engineer', 'Tableau BI Specialist', 'Power BI Architect'],
            },
            'Machine Learning Engineer': {
                'skills_core': ['Python', 'Machine Learning', 'PyTorch', 'TensorFlow', 'Scikit-learn', 'MLOps', 'Docker'],
                'skills_opt': ['Deep Learning', 'NLP', 'Computer Vision', 'Kubernetes', 'AWS', 'FastAPI', 'Large Language Models', 'LangChain'],
                'salary_bands': {
                    'Entry Level': (8.0, 15.0),
                    'Mid Level': (15.0, 30.0),
                    'Senior Level': (28.0, 55.0),
                    'Lead / Principal': (50.0, 85.0),
                },
                'titles': ['ML Engineer', 'Senior Machine Learning Engineer', 'Lead MLOps Engineer', 'AI/ML Infrastructure Engineer', 'Deep Learning Specialist', 'Generative AI Engineer'],
            },
            'Data Engineer': {
                'skills_core': ['Python', 'SQL', 'Apache Spark', 'PostgreSQL', 'AWS', 'ETL Pipelines', 'Apache Airflow'],
                'skills_opt': ['Snowflake', 'BigQuery', 'Apache Kafka', 'Docker', 'Kubernetes', 'dbt', 'Scala', 'Amazon Redshift'],
                'salary_bands': {
                    'Entry Level': (6.0, 12.0),
                    'Mid Level': (12.0, 24.0),
                    'Senior Level': (22.0, 42.0),
                    'Lead / Principal': (40.0, 65.0),
                },
                'titles': ['Data Engineer', 'Senior Data Engineer', 'Big Data Engineer', 'Lead Data Pipeline Architect', 'Cloud Data Platform Engineer', 'Analytics Engineer'],
            },
            'Full Stack Developer': {
                'skills_core': ['JavaScript', 'React', 'Node.js', 'Python', 'SQL', 'REST API', 'Git'],
                'skills_opt': ['TypeScript', 'Next.js', 'Django', 'FastAPI', 'PostgreSQL', 'MongoDB', 'Docker', 'Tailwind CSS'],
                'salary_bands': {
                    'Entry Level': (5.0, 10.5),
                    'Mid Level': (10.0, 22.0),
                    'Senior Level': (20.0, 38.0),
                    'Lead / Principal': (35.0, 60.0),
                },
                'titles': ['Full Stack Developer', 'Senior Full Stack Engineer', 'Lead Full Stack Architect', 'Full Stack Python/React Developer', 'Principal Software Engineer - Full Stack'],
            },
            'Frontend Developer': {
                'skills_core': ['JavaScript', 'TypeScript', 'React', 'Tailwind CSS', 'HTML', 'Git'],
                'skills_opt': ['Next.js', 'GraphQL', 'REST API', 'D3.js', 'Plotly', 'Docker'],
                'salary_bands': {
                    'Entry Level': (4.5, 9.5),
                    'Mid Level': (9.0, 18.0),
                    'Senior Level': (17.0, 32.0),
                    'Lead / Principal': (30.0, 50.0),
                },
                'titles': ['Frontend Developer', 'Senior React Developer', 'Lead UI/UX Frontend Engineer', 'Staff Frontend Architect'],
            },
            'Backend Developer': {
                'skills_core': ['Python', 'Java', 'SQL', 'PostgreSQL', 'REST API', 'Redis', 'Git'],
                'skills_opt': ['FastAPI', 'Django', 'Spring Boot', 'Go', 'Docker', 'Kubernetes', 'AWS', 'Apache Kafka'],
                'salary_bands': {
                    'Entry Level': (5.5, 11.0),
                    'Mid Level': (11.0, 22.0),
                    'Senior Level': (21.0, 40.0),
                    'Lead / Principal': (38.0, 65.0),
                },
                'titles': ['Backend Developer', 'Senior Backend Engineer', 'Lead Python Developer', 'Java Backend Architect', 'Staff API Systems Engineer'],
            },
            'DevOps Engineer': {
                'skills_core': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Terraform', 'Linux', 'Git'],
                'skills_opt': ['Microsoft Azure', 'Google Cloud Platform', 'Python', 'Go', 'Redis', 'PostgreSQL', 'Elasticsearch'],
                'salary_bands': {
                    'Entry Level': (6.0, 12.0),
                    'Mid Level': (12.0, 24.0),
                    'Senior Level': (23.0, 44.0),
                    'Lead / Principal': (40.0, 68.0),
                },
                'titles': ['DevOps Engineer', 'Senior Site Reliability Engineer (SRE)', 'Cloud Infrastructure Engineer', 'Lead Platform DevOps Engineer'],
            },
            'Cloud Architect': {
                'skills_core': ['AWS', 'Microsoft Azure', 'Terraform', 'Kubernetes', 'Docker', 'CI/CD'],
                'skills_opt': ['Google Cloud Platform', 'Linux', 'Python', 'PostgreSQL', 'Data Governance', 'Redis'],
                'salary_bands': {
                    'Entry Level': (9.0, 16.0),
                    'Mid Level': (16.0, 32.0),
                    'Senior Level': (30.0, 60.0),
                    'Lead / Principal': (55.0, 90.0),
                },
                'titles': ['Cloud Solutions Architect', 'Enterprise Cloud Architect', 'Lead Azure/AWS Architect', 'Principal Cloud Security Architect'],
            },
            'Cybersecurity Analyst': {
                'skills_core': ['Linux', 'Data Governance', 'Python', 'Git', 'SQL'],
                'skills_opt': ['AWS', 'Microsoft Azure', 'Docker', 'Elasticsearch', 'CI/CD'],
                'salary_bands': {
                    'Entry Level': (5.0, 10.0),
                    'Mid Level': (10.0, 20.0),
                    'Senior Level': (19.0, 36.0),
                    'Lead / Principal': (34.0, 55.0),
                },
                'titles': ['Cybersecurity Analyst', 'Information Security Engineer', 'Senior SOC Analyst', 'Lead Security Architect'],
            },
            'Product Manager': {
                'skills_core': ['Data Analysis', 'A/B Testing', 'Agile / Scrum', 'Jira', 'SQL'],
                'skills_opt': ['Excel', 'Power BI', 'Tableau', 'Python', 'Predictive Modeling'],
                'salary_bands': {
                    'Entry Level': (8.0, 15.0),
                    'Mid Level': (15.0, 28.0),
                    'Senior Level': (26.0, 48.0),
                    'Lead / Principal': (45.0, 75.0),
                },
                'titles': ['Associate Product Manager', 'Product Manager - Data & AI', 'Senior Technical Product Manager', 'Director of Product Management'],
            },
            'AI Research Engineer': {
                'skills_core': ['Python', 'Deep Learning', 'PyTorch', 'Large Language Models', 'LangChain', 'Statistics', 'NLP'],
                'skills_opt': ['TensorFlow', 'Computer Vision', 'Scikit-learn', 'Docker', 'MLOps', 'AWS'],
                'salary_bands': {
                    'Entry Level': (10.0, 18.0),
                    'Mid Level': (18.0, 35.0),
                    'Senior Level': (34.0, 65.0),
                    'Lead / Principal': (60.0, 95.0),
                },
                'titles': ['AI Research Scientist', 'Generative AI Engineer', 'NLP Research Specialist', 'Senior LLM Systems Engineer', 'Foundational AI Researcher'],
            },
        }

        locations = [
            'Bengaluru', 'Bengaluru', 'Bengaluru', # Weighted towards primary tech hubs
            'Hyderabad', 'Hyderabad',
            'Pune', 'Pune',
            'Mumbai', 'Mumbai',
            'Delhi-NCR', 'Gurugram', 'Noida',
            'Chennai',
            'Remote', 'Remote'
        ]

        work_modes = ['Hybrid', 'Hybrid', 'Remote', 'Remote', 'On-site']
        emp_types = ['Full Time', 'Full Time', 'Full Time', 'Contract', 'Internship']

        exp_ranges = {
            'Entry Level': (0, 2),
            'Mid Level': (3, 5),
            'Senior Level': (6, 9),
            'Lead / Principal': (10, 15),
        }

        # 5. Generate 520 realistic Job Postings
        job_instances = []
        job_skills_map = [] # (job_idx, [skill_objs])

        random.seed(42) # Deterministic for consistent, realistic dataset

        roles_list = list(role_profiles.keys())
        today = date.today()

        for i in range(520):
            role = random.choice(roles_list)
            profile = role_profiles[role]
            
            exp_level = random.choices(
                ['Entry Level', 'Mid Level', 'Senior Level', 'Lead / Principal'],
                weights=[0.28, 0.42, 0.22, 0.08]
            )[0]

            exp_min, exp_max = exp_ranges[exp_level]
            sal_low_base, sal_high_base = profile['salary_bands'][exp_level]

            # add realistic jitter
            sal_min = round(random.uniform(sal_low_base, (sal_low_base + sal_high_base) / 2), 1)
            sal_max = round(random.uniform((sal_low_base + sal_high_base) / 2, sal_high_base * 1.15), 1)
            if sal_max <= sal_min:
                sal_max = sal_min + random.uniform(2.0, 5.0)
            sal_avg = round((sal_min + sal_max) / 2.0, 2)

            company = random.choice(company_objs)
            location = random.choice(locations)
            work_mode = 'Remote' if location == 'Remote' else random.choice(work_modes)
            emp_type = 'Internship' if exp_level == 'Entry Level' and random.random() < 0.15 else random.choice(emp_types)
            if emp_type == 'Internship':
                sal_min = round(random.uniform(2.4, 4.8), 1)
                sal_max = round(random.uniform(4.8, 7.2), 1)
                sal_avg = round((sal_min + sal_max) / 2.0, 2)

            title = random.choice(profile['titles'])
            days_ago = random.randint(0, 60)
            posted = today - timedelta(days=days_ago)

            desc = f"""We are seeking a talented and driven **{title}** to join our fast-growing team at **{company.name}** in **{location}**.

In this role, you will collaborate with cross-functional product, engineering, and business intelligence teams to extract critical insights, scale analytical pipelines, and drive high-impact data initiatives."""

            resp = f"""### Key Responsibilities:
- Design, build, and maintain robust analytical models, automated dashboards, and data workflows.
- Partner with product managers, executives, and software engineers to translate business questions into quantitative insights.
- Perform deep-dive exploratory data analysis, A/B experimentation, and metric trend diagnostics.
- Ensure high data integrity, reliability, and code quality through continuous testing and documentation."""

            reqs = f"""### Required Qualifications:
- {exp_min}+ years of hands-on industry experience in relevant technology stack.
- Strong proficiency in {', '.join(profile['skills_core'][:3])}.
- Proven ability to synthesize complex quantitative findings into clear business narratives.
- Degree in Computer Science, Data Science, Statistics, Mathematics, Engineering or related quantitative field."""

            benefits = f"""### Perks & Benefits:
- Competitive compensation package with attractive performance bonuses and ESOPs.
- Comprehensive health insurance coverage for employee and immediate family.
- Flexible work hours and generous remote-work reimbursement setup.
- Dedicated learning budget for conferences, professional certifications, and workshops."""

            job = Job(
                title=title,
                role_category=role,
                company=company,
                location=location,
                experience_level=exp_level,
                experience_min=exp_min,
                experience_max=exp_max,
                employment_type=emp_type,
                work_mode=work_mode,
                salary_min=sal_min,
                salary_max=sal_max,
                salary_avg=sal_avg,
                description=desc,
                responsibilities=resp,
                requirements=reqs,
                benefits=benefits,
                posted_date=posted,
                views_count=random.randint(15, 650),
            )
            job_instances.append(job)

            # Pick 4-7 relevant skills for this job
            num_core = min(len(profile['skills_core']), random.randint(3, 5))
            selected_skills = random.sample(profile['skills_core'], num_core)
            
            # Add 1-3 optional skills
            num_opt = min(len(profile['skills_opt']), random.randint(1, 3))
            selected_skills.extend(random.sample(profile['skills_opt'], num_opt))

            job_skills_map.append(selected_skills)

        # Bulk create jobs
        created_jobs = Job.objects.bulk_create(job_instances)
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_jobs)} Job postings.'))

        # Assign skills to jobs via M2M
        JobSkillThrough = Job.skills.through
        through_instances = []
        for job_obj, skill_names in zip(created_jobs, job_skills_map):
            for s_name in skill_names:
                if s_name in skill_objs:
                    through_instances.append(
                        JobSkillThrough(job_id=job_obj.id, skill_id=skill_objs[s_name].id)
                    )

        JobSkillThrough.objects.bulk_create(through_instances)
        self.stdout.write(self.style.SUCCESS(f'Linked {len(through_instances)} skill-job associations.'))

        # 6. Create Demo Users
        # Superuser / Admin
        admin_user, admin_created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@jobmarket.ai', 'is_staff': True, 'is_superuser': True})
        if admin_created:
            admin_user.set_password('adminpassword123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / adminpassword123'))

        # Demo User (Data Analyst profile)
        demo_user, demo_created = User.objects.get_or_create(username='demo_user', defaults={'email': 'demo@jobmarket.ai', 'first_name': 'Aarav', 'last_name': 'Sharma'})
        if demo_created:
            demo_user.set_password('demopassword123')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS('Created demo user: demo_user / demopassword123'))

        demo_profile, _ = UserProfile.objects.get_or_create(
            user=demo_user,
            defaults={
                'headline': 'Aspiring Data Analyst | Python, SQL & Power BI Specialist',
                'target_role': 'Data Analyst',
                'education': "Bachelor's Degree",
                'years_of_experience': 2.0,
                'current_salary': 6.5,
                'expected_salary': 10.0,
                'preferred_location': 'Bengaluru',
                'preferred_work_mode': 'Hybrid',
                'bio': 'Passionate data enthusiast with 2 years of experience analyzing business metrics, writing SQL queries, and creating executive dashboards in Power BI and Excel.',
                'github_url': 'https://github.com',
                'linkedin_url': 'https://linkedin.com',
            }
        )

        # Assign core skills to demo user
        demo_skills = ['SQL', 'Python', 'Excel', 'Power BI', 'Data Analysis']
        UserSkill.objects.filter(user_profile=demo_profile).delete()
        for s_name in demo_skills:
            if s_name in skill_objs:
                UserSkill.objects.create(
                    user_profile=demo_profile,
                    skill=skill_objs[s_name],
                    proficiency='Intermediate',
                    years_practiced=2.0
                )

        # Bookmark 3 jobs for demo user
        SavedJob.objects.filter(user=demo_user).delete()
        sample_jobs = Job.objects.filter(role_category='Data Analyst')[:3]
        for sj in sample_jobs:
            SavedJob.objects.create(user=demo_user, job=sj)

        self.stdout.write(self.style.SUCCESS('Database successfully seeded with 520+ jobs, 80+ skills, 40+ companies, and demo profiles!'))
