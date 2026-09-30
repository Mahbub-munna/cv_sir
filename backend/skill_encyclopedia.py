# -----------------------------------
# Skill Encyclopedia - MASSIVE EXPANSION
# -----------------------------------

SKILL_DATA = {
    # LANGUAGES
    "python": {
        "description": "A versatile high-level programming language used in backend development, data science, and AI.",
        "importance": "Industry standard for modern automation, data processing, and scalable backend services.",
        "learning": "Check out 'Automate the Boring Stuff with Python' or Coursera's Python Specializations.",
        "tip": "Highlight projects where you used Python to solve real-world problems.",
        "priority": "Highest",
        "path": ["Python Syntax Basics", "Data Structures & Control Flow", "Functions & Decorators", "Scalable Projects Frameworks"]
    },
    "javascript": {
        "description": "The core language of the web, used for creating interactive and dynamic content.",
        "importance": "98% of the web's frontend runs on JavaScript. It is essential for modern web development.",
        "learning": "MDN Web Docs or freeCodeCamp's JavaScript Algorithm certifications.",
        "tip": "Combine this with a framework mention like React to show professional depth.",
        "priority": "Highest",
        "path": ["Variables & Selectors", "ES6+ Modern Features", "Asynchronous Logic (Promises/Fetch)", "Modern SPA Frameworks"]
    },
    "typescript": {
        "description": "A strongly typed superset of JavaScript that scales to large applications.",
        "importance": "TypeScript caught 15% of bugs in a large-scale study. It's the standard for professional frontend development.",
        "learning": "TypeScript's official Handbook (typescriptlang.org).",
        "tip": "Showcase your ability to define complex interfaces and types in your CV.",
        "priority": "High",
        "path": ["Modern JavaScript", "Type Annotations & Interfaces", "Generics & Advanced Types", "TypeScript React/Node Integration"]
    },
    "rust": {
        "description": "A systems programming language focused on safety, speed, and concurrency.",
        "importance": "Rust has been the 'most loved' language on Stack Overflow for years, key for performance-critical logic.",
        "learning": "The Rust Programming Language (The Book).",
        "tip": "Highlight any systems-level projects or performance optimizations you've built.",
        "priority": "Medium",
        "path": ["Rust Syntax & Tools", "Ownership & Borrowing", "Structuring Large Projects", "Concurrent Systems Programming"]
    },
    "go": {
        "description": "An open-source programming language that makes it easy to build simple, reliable, and efficient software.",
        "importance": "Preferred for cloud-native infrastructure, microservices, and high-performance backends.",
        "learning": "A Tour of Go (tour.golang.org).",
        "tip": "Mention any microservices or distributed systems built with Go.",
        "priority": "High",
        "path": ["Go Basics & Tooling", "Methods & Interfaces", "Goroutines & Channels", "Cloud Native API Services"]
    },

    # FRONTEND
    "react": {
        "description": "A popular JavaScript library for building modern user interfaces.",
        "importance": "Component-based architecture leads to faster development and highly responsive user experiences.",
        "learning": "The official React documentation (react.dev) is the best starting point.",
        "tip": "Showcase complex state management or custom hooks you've developed.",
        "priority": "High",
        "path": ["JavaScript Essentials", "Component Basics & Props", "Hooks (useState/useEffect)", "State Management (Redux/Context)"]
    },
    "next.js": {
        "description": "The React framework for the web, enabling SSR and static site generation.",
        "importance": "Vital for SEO-friendly and mission-critical high-performance web applications.",
        "learning": "Next.js Learn (nextjs.org/learn).",
        "tip": "Describe your experience with Server Components and API Routes.",
        "priority": "High",
        "path": ["Advanced React", "App Router & File-based Routing", "Data Fetching Strategies (SSR/SSG)", "Vercel Deployment & Optimization"]
    },
    "tailwind css": {
        "description": "A utility-first CSS framework for rapid UI development.",
        "importance": "Speed up frontend styling by writing CSS directly in your HTML with utility classes.",
        "learning": "Tailwind Labs' YouTube channel or the official documentation.",
        "tip": "Mention projects where you optimized CSS bundle sizes with Tailwind's JIT mode.",
        "priority": "Medium",
        "path": ["CSS Box Model & Flexbox", "Tailwind Configuration", "Responsive Design Patterns", "Custom Components & Theming"]
    },
    "redux": {
        "description": "A predictable state container for JavaScript apps.",
        "importance": "Centralizes application state for better debugging and consistent UI updates across complex components.",
        "learning": "Redux Toolkit documentation (official and recommended).",
        "tip": "Explain how you managed global app state for user auth or complex data filters.",
        "priority": "Medium",
        "path": ["React State Management", "Immutability & Flux Architecture", "Redux Toolkit (Slices/Thunks)", "RTK Query for API Management"]
    },
    "vue.js": {
        "description": "A progressive framework for building user interfaces.",
        "importance": "Acclaimed for its approachable design and high performance in modern single-page apps.",
        "learning": "Vuejs.org's official guides and documentation.",
        "tip": "Highlight any migration projects from legacy systems to Vue.",
        "priority": "Medium",
        "path": ["JS Essentials", "Templates & Directives", "Composition API", "Vuex/Pinia State Management"]
    },

    # BACKEND
    "node.js": {
        "description": "An asynchronous event-driven JavaScript runtime built for scalable network applications.",
        "importance": "Allows developers to use JavaScript for both frontend and backend (Full Stack consistently).",
        "learning": "Node.js documentation or 'Node.js Design Patterns' book.",
        "tip": "Highlight any Real-time applications (WebSockets) or CLI tools built with Node.",
        "priority": "High",
        "path": ["Asynchronous JS Hub", "Event Loop & File System", "Asynchronous API Design", "Scaling & Microservices"]
    },
    "express": {
        "description": "A fast, unopinionated, minimalist web framework for Node.js.",
        "importance": "The most widely-used framework for building RESTful APIs in the Node ecosystem.",
        "learning": "Expressjs.com's getting started guides.",
        "tip": "Discuss middleware implementation for auth, logging, and error handling.",
        "priority": "High",
        "path": ["Node.js Fundementals", "Route Handling & Middleware", "RESTful Principles", "Backend Security Integrations"]
    },
    "django": {
        "description": "A high-level Python web framework that encourages rapid development and clean, pragmatic design.",
        "importance": "Famous for its 'batteries-included' philosophy—security and database management are built-in.",
        "learning": "Django Project's official tutorial (The 'Polls' app).",
        "tip": "Highlight your use of the Django REST Framework (DRF) for modern web APIs.",
        "priority": "High",
        "path": ["Python Logic Mastery", "Django ORM & Models", "Authentication & Views", "REST APIs with DRF"]
    },
    "fastapi": {
        "description": "A modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.",
        "importance": "One of the fastest Python frameworks available, perfect for AI/ML deployments.",
        "learning": "FastAPI's interactive documentation (it is excellent).",
        "tip": "Emphasize your ability to build high-performance APIs with automatic validation.",
        "priority": "Medium",
        "path": ["Python Type-Hinting", "Pydantic Schemas", "Asynchronous Request Handling", "Background Tasks & Security"]
    },
    "spring boot": {
        "description": "An open-source Java-based framework used to create microservices.",
        "importance": "Standard for large enterprise applications due to its robustness and vast ecosystem.",
        "learning": "Spring.io's official guides and Baeldung tutorials.",
        "priority": "High",
        "path": ["Java Core Proficiency", "Dependency Injection", "Spring Data JPA", "Enterprise Cloud Microservices"]
    },

    # DATABASES
    "sql": {
        "description": "Standard language for managing and querying relational databases.",
        "importance": "Knowing SQL allows you to fetch, store, and analyze data directly.",
        "learning": "Try SQLZoo.net or the SQL courses on DataCamp.",
        "priority": "Highest",
        "path": ["Relational Database Basics", "SELECT & JOIN Queries", "Advanced Aggregations", "Database Design & Normalization"]
    },
    "postgresql": {
        "description": "The world's most advanced open-source relational database.",
        "importance": "Highly extensible and reliable; used for complex, mission-critical data systems.",
        "learning": "The PostgreSQL Tutorial or official documentation.",
        "tip": "Discuss your experience with indexes, transactions, or JSONB storage.",
        "priority": "High",
        "path": ["Core SQL Logic", "Postgres-specific Functions", "Normalization & Performance Tuning", "Advanced Triggers & Procedures"]
    },
    "mongodb": {
        "description": "A widely-used document-based NoSQL database for flexible and scalable data storage.",
        "importance": "Great for handling unstructured data and rapid horizontal scaling.",
        "learning": "MongoDB University's free certification courses.",
        "tip": "Discuss high-volume data horizontal scaling capabilities.",
        "priority": "Medium",
        "path": ["NoSQL Document Concepts", "CRUD Operations & Aggregations", "Data Modeling (Embedding vs Referencing)", "Cluster Management & Indexing"]
    },

    # DEVOPS & CLOUD
    "docker": {
        "description": "A platform for containerizing applications.",
        "importance": "Vital for modern DevOps, ensuring applications run identically across environments.",
        "learning": "Docker's official 'Getting Started' guide.",
        "priority": "High",
        "path": ["Linux CLI Basics", "Docker Containers & Images", "Dockerfile & Optimization", "Docker Compose Orchestration"]
    },
    "kubernetes": {
        "description": "An open-source system for automating deployment, scaling, and management of containerized applications.",
        "importance": "The gold standard for container orchestration in production environments.",
        "learning": "Google's K8s Engine tutorials or 'Kubernetes the Hard Way'.",
        "tip": "Explain your experience with Pods, Deployments, and Ingress controllers.",
        "priority": "High",
        "path": ["Docker Container Mastery", "Kubernetes Architecture", "Pod Scheduling & Scaling", "Cloud-Native Infrastructure"]
    },
    "aws": {
        "description": "Amazon Web Services is a comprehensive cloud computing platform.",
        "importance": "Most modern companies host their infrastructure on clouds like AWS.",
        "learning": "AWS Cloud Practitioner Essentials (Free from Amazon).",
        "priority": "High",
        "path": ["Cloud Fundamentals", "Identity & Access Management (IAM)", "EC2 & S3 Core Services", "Serverless Architecture (Lambda)"]
    },
    "ci/cd": {
        "description": "Continuous Integration and Continuous Deployment/Delivery practices.",
        "importance": "Automating the testing and deployment cycle is key to shipping reliable software faster.",
        "learning": "GitLab CI or GitHub Actions documentation.",
        "tip": "Mention any automated workflows you've set up for tests or deployments.",
        "priority": "High",
        "path": ["Git & Version Control", "Automated Testing Logic", "Pipeline Scripting (YAML)", "Production Deployment Gates"]
    },
    "git": {
        "description": "The most widely-used version control system for tracking changes in source code.",
        "importance": "Essential for collaboration in any modern software engineering team.",
        "learning": "Pro Git book or GitHub's interactive guides.",
        "priority": "Highest",
        "path": ["Commits & Status", "Branching & Merging", "Merge Conflicts & Rebase", "Pull Requests & Code Review"]
    },

    # TESTING
    "jest": {
        "description": "A delightful JavaScript Testing Framework with a focus on simplicity.",
        "importance": "The standard tool for testing React and modern JS applications.",
        "learning": "Jestjs.io's official documentation.",
        "priority": "High",
        "path": ["JS Essentials", "Assertion & Matchers", "Mocking & Spies", "Test-Driven Development (TDD)"]
    },
    "cypress": {
        "description": "Fast, easy and reliable testing for anything that runs in a browser.",
        "importance": "Crucial for End-to-End testing that ensures the entire user journey works perfectly.",
        "learning": "Cypress.io/learn or Kent C. Dodds' testing courses.",
        "priority": "Medium",
        "path": ["Frontend Fundamentals", "E2E Testing Logic", "Cypress Commands & Selectors", "CI Integration for UI Tests"]
    },

    # DESIGN
    "figma": {
        "description": "A collaborative interface design tool for teams.",
        "importance": "The industry standard for building prototypes, design systems, and developer-ready UI designs.",
        "learning": "Figma's official YouTube channel and community templates.",
        "priority": "High",
        "path": ["Design Basics", "Interface Components", "Prototyping & Flow", "Design Systems & Collaboration"]
    },
    "ui/ux": {
        "description": "User Interface and User Experience design principles.",
        "importance": "Ensures that products are not only beautiful but intuitive and user-friendly.",
        "learning": "Nielsen Norman Group reports or Google UX Design Certificate.",
        "priority": "High",
        "path": ["User Research", "Wireframing & Lo-Fi Design", "Cognitive Design Principles", "Hi-Fi Prototyping & Usability Testing"]
    },

    # MANAGEMENT
    "agile": {
        "description": "Iterative approach to software development and project management.",
        "importance": "Vital for fast-paced software teams to deliver value rapidly and adapt to change.",
        "learning": "Atlassian's Agile Coach guides.",
        "priority": "High",
        "path": ["Agile Manifesto Principles", "Ceremonies & Artifacts", "Backlog & Velocity Tracking", "Scaled Agile Frameworks"]
    },
    "scrum": {
        "description": "A framework within which people can address complex adaptive problems.",
        "importance": "Most common Agile framework; mastering it prepares you for modern dev roles.",
        "learning": "Scrum.org's official Scrum Guide.",
        "priority": "High",
        "path": ["Scrum Values", "Roles (PO/SM/Dev)", "Sprints & Daily Standups", "Process Improvement (Retros)"]
    },
    "jira": {
        "description": "A project management tool for software teams.",
        "importance": "Industry standard for tracking tasks, bugs, and project progress.",
        "learning": "Atlassian University's Jira tutorials.",
        "priority": "Medium",
        "path": ["Task Creation & Status", "Sprint Planning & Boards", "Reporting & Dashboards", "Advanced Configurations"]
    },

    # DATA & ML
    "machine learning": {
        "description": "A branch of AI that allows systems to learn from experience.",
        "importance": "Used for everything from personalization to predictive analytics and automation.",
        "learning": "Andrew Ng's Machine Learning Specialization on Coursera.",
        "priority": "Medium",
        "path": ["Linear Algebra & Statistics", "Supervised Learning Algorithms", "Model Evaluation & Metrics", "Model Deployment (MLOps)"]
    },
    "data analysis": {
        "description": "Extracting meaningful insights from data to guide business decisions.",
        "importance": "Drives strategy and optimization across every modern industry.",
        "learning": "Google's Data Analytics Professional Certificate.",
        "priority": "Medium",
        "path": ["Statistics & Probability", "Excel/SQL Queries", "EDA (Exploratory Data Analysis)", "Storytelling with Visualization"]
    }
}

# DYNAMIC CATEGORY TEMPLATES
# -----------------------------------
FALLBACK_TEMPLATES = {
    "frontend": {
        "priority": "High",
        "steps": ["Core Structural Principles", "Professional Styling & Layouts", "Functional Component Logic", "Performance & State Management"]
    },
    "backend": {
        "priority": "High",
        "steps": ["Logic & Algorithms", "API Architecture Design", "Database Modeling & Interaction", "Scalable Security Protocols"]
    },
    "database": {
        "priority": "High",
        "steps": ["Schema Modeling & Relations", "Efficient Querying & Manipulation", "Optimization & Performance Tuning", "Scaling & Replication Mastery"]
    },
    "devops": {
        "priority": "High",
        "steps": ["Infrastructure & Scripting", "Automation & CI/CD Pipelines", "Containerization Orchestration", "Monitoring & Reliability Strategy"]
    },
    "ai/ml": {
        "priority": "Medium",
        "steps": ["Mathematical & Statistical Foundations", "Data Processing & Feature Engineering", "Model Selection & Architecture", "System Deployment & Deployment"]
    },
    "management": {
        "priority": "High",
        "steps": ["Principles & Strategic Alignment", "Framework Implementation", "Team & Resource Coordination", "Continuous Delivery Optimization"]
    },
    "design": {
        "priority": "Medium",
        "steps": ["Foundational Design Assets", "Interactive Prototyping", "Design System Scalability", "User Collaboration & Testing"]
    },
    "testing": {
        "priority": "High",
        "steps": ["Test Environment Configuration", "Writing Robust Test Logic", "Automated Coverage Strategies", "CI Integration Analysis"]
    },
    "security": {
        "priority": "Highest",
        "steps": ["Threat Modeling & Identification", "Security Protocol Implementation", "Authorization & Encryption Logic", "Continuous Security Compliance"]
    },
    "professional": {
        "priority": "Standard",
        "steps": ["Core Concept Mastery", "Advanced Specialization Logic", "Strategic Real-World Applications", "Peer Mentorship & Leadership"]
    }
}

def get_category(skill_name):
    name = skill_name.lower()
    
    # Frontend
    if any(k in name for k in ["ui", "css", "html", "react", "frontend", "web", "layout", "design", "vue", "angular", "sass", "sculpt", "client"]):
        return "frontend"
    # Database
    if any(k in name for k in ["sql", "db", "query", "mongo", "postgres", "redis", "schema", "database", "data", "storage"]):
        return "database"
    # DevOps
    if any(k in name for k in ["docker", "kubernetes", "aws", "cloud", "devops", "linux", "infra", "git", "ci/cd", "deployment", "automation", "azure", "gcp"]):
        return "devops"
    # AI/ML
    if any(k in name for k in ["ai", "machine learning", "neural", "intelligence", "tensor", "model", "prediction", "science", "nlp"]):
        return "ai/ml"
    # Testing
    if any(k in name for k in ["test", "jest", "cypress", "selenium", "qa", "quality", "mocha", "chai", "junit"]):
        return "testing"
    # Design
    if any(k in name for k in ["figma", "sketch", "photoshop", "ux", "ui", "prototype", "wireframe", "color", "typograph"]):
        return "design"
    # Management
    if any(k in name for k in ["agile", "scrum", "manage", "lead", "project", "jira", "kanban", "trello", "coordinator"]):
        return "management"
    # Security
    if any(k in name for k in ["auth", "security", "jwt", "oauth", "password", "encrypt", "privacy", "cyber", "protection"]):
        return "security"
    # Backend
    if any(k in name for k in ["python", "java", "node", "backend", "api", "server", "logic", "django", "express", "fastapi", "spring", "go", "php", "rust"]):
        return "backend"
    
    return "professional"

def get_skill_info(skill_name):
    """
    Returns dedicated skill information.
    If the skill is not in the library, it generates a custom-sounding 
    roadmap using domain-specific 'Progressive Mastery' logic.
    """
    # Normalize input
    key = skill_name.lower().strip()
    
    # 1. Exact Match Library (Highest Quality)
    if key in SKILL_DATA:
        return SKILL_DATA[key]
    
    # 2. Smart Category Dynamic Generation
    category = get_category(skill_name)
    template = FALLBACK_TEMPLATES[category]
    
    # Create a 'Personalized' roadmap path using the skill name creatively
    # Instead of just "Skill: Step", we create more professional headers
    path = [
        f"Step 1: {skill_name} {template['steps'][0]}",
        f"Step 2: {skill_name} {template['steps'][1]}",
        f"Step 3: {skill_name} {template['steps'][2]}",
        f"Step 4: {skill_name} {template['steps'][3]}",
    ]
    
    return {
        "description": f"{skill_name} is a high-demand professional competency specifically required for your target role in the industry.",
        "importance": f"Mastering {skill_name} enables you to implement structural improvements and professional-grade logic in modern software environments.",
        "learning": f"We recommend diving into the official documentation for {skill_name} and following a certified professional path on Coursera or Udemy.",
        "tip": f"Clearly highlight {skill_name} in your technical summary and describe a specific high-impact scenario where you've studied or applied a similar logic.",
        "priority": template["priority"],
        "path": path
    }
