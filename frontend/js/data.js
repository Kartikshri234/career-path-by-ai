// ── SKILL LIST ───────────────────────────────────────────────────────────────
const SKILLS = [
  "Python","Java","C++","JavaScript","SQL","HTML/CSS","React","Node.js",
  "Machine Learning","Deep Learning","Data Analysis","Statistics",
  "Docker","Kubernetes","AWS","Git","Linux","Networking",
  "DSA","System Design","Figma","MongoDB","REST APIs",
  "R","MATLAB","Ethical Hacking","Microcontrollers","Excel","Power BI"
];

// ── CAREER DATA ───────────────────────────────────────────────────────────────
const CAREERS = [
  {
    id: "sde",
    icon: "💻",
    name: "Software Development Engineer",
    desc: "Build scalable applications and systems. Highest demand across all sectors.",
    need: ["DSA","System Design","Java","Python","Git","REST APIs","SQL"],
    roadmap: [
      { w:"Week 1–2",  t:"DSA Fundamentals",     d:"Arrays, Strings, Linked Lists on LeetCode. Aim for 30+ easy problems.", rs:["LeetCode","GeeksForGeeks","Striver SDE Sheet"] },
      { w:"Week 3–4",  t:"Core CS Concepts",      d:"OS, DBMS, Computer Networks basics — essential for all tech interviews.", rs:["Gate Smashers","YouTube"] },
      { w:"Week 5–7",  t:"Full-Stack Project",    d:"Build a CRUD app with React + Node.js + MongoDB, deploy on Vercel.", rs:["Traversy Media","The Odin Project"] },
      { w:"Week 8–10", t:"System Design Basics",  d:"Scalability, load balancing, caching, and database design patterns.", rs:["ByteByteGo","Grokking SD"] },
      { w:"Week 11–12",t:"Mock Interviews & Apply",d:"Do 5+ mock interviews. Apply to 20+ companies simultaneously.", rs:["Pramp","InterviewBit"] }
    ],
    salary: [
      { c:"Bangalore", r:"₹8–35 LPA",  e:"0–5 yrs" },
      { c:"Hyderabad", r:"₹7–28 LPA",  e:"0–5 yrs" },
      { c:"Pune",      r:"₹6–22 LPA",  e:"0–5 yrs" },
      { c:"Mumbai",    r:"₹9–40 LPA",  e:"0–5 yrs" },
      { c:"Chennai",   r:"₹6–20 LPA",  e:"0–5 yrs" },
      { c:"Remote",    r:"₹12–60 LPA", e:"2+ yrs"  }
    ],
    radarLabels: ["Coding","System Design","CS Basics","Problem Solving","Communication","Projects"],
    radarRequired: [9, 7, 8, 9, 6, 7]
  },
  {
    id: "ds",
    icon: "🤖",
    name: "Data Scientist / ML Engineer",
    desc: "Extract insights and build intelligent models from large datasets.",
    need: ["Python","Machine Learning","Deep Learning","Statistics","SQL","Data Analysis","Power BI"],
    roadmap: [
      { w:"Week 1–2",  t:"Python & Statistics",  d:"NumPy, Pandas, Matplotlib. Descriptive stats and probability.", rs:["Kaggle Learn","CS50P"] },
      { w:"Week 3–5",  t:"ML Core",              d:"Regression, Classification, Clustering with Scikit-learn.", rs:["Andrew Ng ML","Hands-On ML Book"] },
      { w:"Week 6–8",  t:"Deep Learning & NLP",  d:"Neural nets, CNNs, Transformers basics with PyTorch.", rs:["Fast.ai","d2l.ai"] },
      { w:"Week 9–10", t:"Kaggle Competitions",  d:"Participate in 2 competitions, focus on feature engineering.", rs:["Kaggle","Towards Data Science"] },
      { w:"Week 11–12",t:"End-to-End ML Project",d:"Build, deploy and document a complete ML pipeline on the cloud.", rs:["MLflow","Streamlit","HuggingFace"] }
    ],
    salary: [
      { c:"Bangalore", r:"₹10–45 LPA", e:"0–5 yrs" },
      { c:"Hyderabad", r:"₹9–35 LPA",  e:"0–5 yrs" },
      { c:"Mumbai",    r:"₹11–50 LPA", e:"0–5 yrs" },
      { c:"Pune",      r:"₹8–30 LPA",  e:"0–5 yrs" },
      { c:"Delhi NCR", r:"₹9–38 LPA",  e:"0–5 yrs" },
      { c:"Remote US", r:"$80–150K",   e:"2+ yrs"  }
    ],
    radarLabels: ["Python","Statistics","ML Knowledge","Data Viz","Research","Problem Solving"],
    radarRequired: [9, 8, 9, 7, 8, 8]
  },
  {
    id: "cloud",
    icon: "☁️",
    name: "Cloud / DevOps Engineer",
    desc: "Build cloud infrastructure, CI/CD pipelines, and a strong DevOps culture.",
    need: ["AWS","Docker","Kubernetes","Linux","Git","Python","Networking"],
    roadmap: [
      { w:"Week 1–2",  t:"Linux & Networking",   d:"Shell scripting, TCP/IP, DNS. Practice on Linux VMs.", rs:["Linux Journey","NetworkChuck"] },
      { w:"Week 3–4",  t:"Docker & Containers",  d:"Containerize apps, write Dockerfiles, use Docker Compose.", rs:["Docker Docs","TechWorld Nana"] },
      { w:"Week 5–7",  t:"AWS Fundamentals",     d:"EC2, S3, RDS, VPC, IAM. Prep for AWS Solutions Architect cert.", rs:["Adrian Cantrill","AWS Free Tier"] },
      { w:"Week 8–10", t:"Kubernetes & CI/CD",   d:"K8s deployments, GitHub Actions, Jenkins pipelines.", rs:["K8s Docs","DevOps Mumshad"] },
      { w:"Week 11–12",t:"Certify & Build Portfolio",d:"Get AWS SAA cert. Deploy a 3-tier app with full CI/CD.", rs:["ExamPro","Udemy"] }
    ],
    salary: [
      { c:"Bangalore", r:"₹9–40 LPA",  e:"0–5 yrs" },
      { c:"Hyderabad", r:"₹8–32 LPA",  e:"0–5 yrs" },
      { c:"Pune",      r:"₹7–28 LPA",  e:"0–5 yrs" },
      { c:"Mumbai",    r:"₹10–45 LPA", e:"0–5 yrs" },
      { c:"Chennai",   r:"₹7–25 LPA",  e:"0–5 yrs" },
      { c:"Remote",    r:"₹15–70 LPA", e:"3+ yrs"  }
    ],
    radarLabels: ["Linux","Cloud Platforms","Scripting","Networking","CI/CD","Security"],
    radarRequired: [8, 9, 7, 8, 8, 7]
  },
  {
    id: "cyber",
    icon: "🔐",
    name: "Cybersecurity Engineer",
    desc: "Protect systems and networks. One of the fastest growing fields in tech.",
    need: ["Networking","Linux","Ethical Hacking","Python","Git","SQL"],
    roadmap: [
      { w:"Week 1–2",  t:"Networking Fundamentals",d:"OSI model, TCP/IP, DNS, firewalls. TryHackMe beginner rooms.", rs:["TryHackMe","CompTIA Net+"] },
      { w:"Week 3–4",  t:"Linux & Bash Scripting", d:"File permissions, cron, log analysis. Automate tasks in Bash.", rs:["OverTheWire","Linux Journey"] },
      { w:"Week 5–7",  t:"Ethical Hacking Basics", d:"Reconnaissance, vulnerability scanning, Metasploit intro.", rs:["Hack The Box","TCM Security"] },
      { w:"Week 8–10", t:"Web App Security",        d:"OWASP Top 10, SQL injection, XSS, Burp Suite.", rs:["PortSwigger Academy","OWASP"] },
      { w:"Week 11–12",t:"Certify & CTF Practice",  d:"Attempt CEH or CompTIA Security+. Join CTF competitions.", rs:["CTFtime.org","TryHackMe"] }
    ],
    salary: [
      { c:"Bangalore", r:"₹8–32 LPA",  e:"0–5 yrs" },
      { c:"Hyderabad", r:"₹7–28 LPA",  e:"0–5 yrs" },
      { c:"Mumbai",    r:"₹9–35 LPA",  e:"0–5 yrs" },
      { c:"Pune",      r:"₹7–25 LPA",  e:"0–5 yrs" },
      { c:"Delhi NCR", r:"₹8–30 LPA",  e:"0–5 yrs" },
      { c:"Remote",    r:"₹12–55 LPA", e:"2+ yrs"  }
    ],
    radarLabels: ["Networking","Linux","Ethical Hacking","Scripting","Web Security","Forensics"],
    radarRequired: [9, 8, 9, 7, 8, 6]
  }
];
