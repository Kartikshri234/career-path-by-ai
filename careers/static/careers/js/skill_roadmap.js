/**
 * skill_roadmap.js — Skill Roadmap Planner
 * All logic for the 3-step wizard: skill picker, timeline, roadmap generator
 */

/* ═══════════════════════════════════════════════════
   SKILL DATABASE
═══════════════════════════════════════════════════ */
const SKILL_DB = {
  "Programming":{ icon:"💻", color:"#818cf8", skills:{
    "Python":     {icon:"🐍", salary:"₹5–30 LPA", demand:"Very High", roles:["Backend Dev","Data Scientist","ML Engineer"],
      why:"Python is the most in-demand language globally. It powers AI, web, automation, and data.",
      resources:[{name:"Python.org Docs",type:"free",note:"Official reference"},{name:"CS50P (Harvard)",type:"free",note:"Best free Python course"},{name:"Automate Boring Stuff",type:"free",note:"Practical projects"},{name:"Python Bootcamp Udemy",type:"paid",note:"Most popular paid course"}],
      milestone:"Build a CLI tool that reads a CSV, processes data, and outputs a report",
      tip:"Build something real every week — a script, a bot, a scraper. Python clicks fastest through practice.",
      tasks:[{t:"Install Python 3 + VS Code, learn variables, loops, functions",d:"Write your first 3 scripts from scratch without tutorials"},{t:"Learn lists, dicts, sets — build a grade tracker",d:"Real data structures, not just reading about them"},{t:"Learn OOP: classes, inheritance, methods",d:"Build a BankAccount class with deposit/withdraw/balance"},{t:"File I/O, JSON, error handling",d:"Build an expense tracker that saves to a JSON file"},{t:"Install packages with pip, use requests to hit an API",d:"Fetch weather data and print it neatly"}]},
    "JavaScript":{icon:"🟨", salary:"₹5–28 LPA", demand:"Very High", roles:["Frontend Dev","Full-Stack Dev","React Dev"],
      why:"JavaScript is the only language that runs in browsers. Every website uses it.",
      resources:[{name:"javascript.info",type:"free",note:"Best JS tutorial online"},{name:"The Odin Project",type:"free",note:"Free full-stack curriculum"},{name:"FreeCodeCamp JS",type:"free",note:"Interactive exercises"},{name:"You Don't Know JS",type:"free",note:"Deep-dive book series"}],
      milestone:"Build a weather app using a real API, deployed on GitHub Pages",
      tip:"Open DevTools console right now and start typing. Fastest way to learn JS is to run it instantly.",
      tasks:[{t:"Variables (let/const), types, operators, scope",d:"Never use var — understand why let and const exist"},{t:"DOM: querySelector, addEventListener, innerHTML",d:"Build an interactive to-do list from scratch"},{t:"ES6+: arrow functions, destructuring, spread, template literals",d:"Rewrite your to-do list using only ES6 syntax"},{t:"Async JS: Promises → async/await + Fetch API",d:"Fetch from a public API, handle loading and errors"},{t:"Modules (import/export) + bundle with Vite",d:"Split your project into multiple files cleanly"}]},
    "Java":       {icon:"☕", salary:"₹6–32 LPA", demand:"High", roles:["Backend Dev","Android Dev","SDE at FAANG"],
      why:"Java powers enterprise software and Android. Most top companies use Java for large-scale systems.",
      resources:[{name:"Java Brains YouTube",type:"free",note:"Excellent free Java + Spring"},{name:"GeeksForGeeks Java",type:"free",note:"Best concept reference"},{name:"Spring Boot – Amigoscode",type:"free",note:"Free YouTube Spring series"},{name:"Effective Java (Book)",type:"paid",note:"Must-read for professional Java"}],
      milestone:"Build a REST API with Spring Boot that does full CRUD with a database",
      tip:"Java is verbose but consistent. Understand WHY OOP works — it makes every other OOP language easier.",
      tasks:[{t:"Setup JDK 17 + IntelliJ, write Hello World",d:"Understand compilation (javac) vs running (java)"},{t:"OOP: classes, interfaces, inheritance, polymorphism",d:"Build a Shape hierarchy with area() method"},{t:"Collections: ArrayList, HashMap, HashSet",d:"Solve 15 LeetCode problems using Java collections"},{t:"Exceptions and File I/O",d:"Build a CSV reader with proper error handling"},{t:"Spring Boot REST API with GET/POST/PUT/DELETE",d:"Test all endpoints with Postman"}]},
    "C++":        {icon:"⚙️", salary:"₹6–35 LPA", demand:"High", roles:["Systems Engineer","Game Dev","Competitive Programmer"],
      why:"C++ gives direct memory control. Used in game engines, OS, compilers, and HFT.",
      resources:[{name:"LearnCPP.com",type:"free",note:"Most comprehensive free tutorial"},{name:"CP Handbook (Laaksonen)",type:"free",note:"Free competitive programming book"},{name:"Codeforces",type:"free",note:"Best platform for C++ practice"},{name:"C++ Primer (Book)",type:"paid",note:"Classic definitive reference"}],
      milestone:"Implement BFS, DFS, and Dijkstra and pass all test cases on Codeforces",
      tip:"Start with competitive programming — it forces you to understand C++ deeply and fast.",
      tasks:[{t:"Syntax, variables, loops, functions",d:"Write a calculator, guessing game, and fibonacci"},{t:"Pointers and memory management",d:"Allocate with new[], free with delete[]. Draw stack vs heap"},{t:"STL: vector, map, set, queue, priority_queue",d:"Solve 20 LeetCode problems using only STL"},{t:"OOP: classes, operator overloading",d:"Build a Matrix class with +, * operators"},{t:"Solve 50 Codeforces Div 3 problems",d:"Join virtual contests every weekend"}]},
    "TypeScript": {icon:"🔷", salary:"₹8–35 LPA", demand:"Growing Fast", roles:["Frontend Dev","Full-Stack Dev","React + TS Dev"],
      why:"TypeScript catches bugs at compile time. It's now the standard in professional React/Node projects.",
      resources:[{name:"TypeScript Official Docs",type:"free",note:"Handbook is excellent"},{name:"Matt Pocock TS Course",type:"free",note:"Best modern TS course, free"},{name:"Total TypeScript",type:"paid",note:"Deep dive into advanced TS"},{name:"Execute Program TS",type:"paid",note:"Interactive TypeScript learning"}],
      milestone:"Migrate a JavaScript project to strict TypeScript with zero any types",
      tip:"Don't avoid 'any' — understand WHY it's dangerous. The goal is strict TypeScript.",
      tasks:[{t:"Types, type inference, type aliases",d:"Annotate an existing JS file with proper TypeScript"},{t:"Interfaces vs types, optional and readonly props",d:"Model User, Product, ApiResponse types"},{t:"Union, intersection types, type narrowing",d:"Write a function handling string | number correctly"},{t:"Generics: functions, classes, utility types",d:"Build a typed API response wrapper"},{t:"Strict mode tsconfig + apply to a real project",d:"Enable strict, noImplicitAny, strictNullChecks"}]},
    "Go":         {icon:"🐹", salary:"₹10–40 LPA", demand:"High", roles:["Backend Engineer","Cloud Engineer","SRE"],
      why:"Go powers Docker, Kubernetes, and Terraform. Fast, simple, and built for concurrency.",
      resources:[{name:"Tour of Go (official)",type:"free",note:"Start here — interactive"},{name:"Go by Example",type:"free",note:"Concise real examples"},{name:"TechWorld Nana Go",type:"free",note:"Hands-on for backend devs"},{name:"The Go Programming Language",type:"paid",note:"Definitive Go reference"}],
      milestone:"Build a REST API with JWT auth, a database, and proper error handling",
      tip:"Go forces explicit error handling. Embrace it — it's what makes Go programs reliable in production.",
      tasks:[{t:"Syntax: variables, types, functions, control flow",d:"Complete Tour of Go in one sitting"},{t:"Structs and methods",d:"Build a User struct with Greet() and Validate() methods"},{t:"Interfaces and error handling (no exceptions in Go)",d:"Propagate errors correctly up the call stack"},{t:"Goroutines and channels — Go's killer feature",d:"Build a concurrent file downloader with WaitGroup"},{t:"HTTP server + PostgreSQL + unit tests",d:"80%+ test coverage on your handler functions"}]},
  }},
  "Web Dev":{ icon:"🌐", color:"#22d3ee", skills:{
    "HTML/CSS":  {icon:"🎨",salary:"₹3–18 LPA",demand:"Essential",roles:["Frontend Dev","UI Developer","Full-Stack Dev"],why:"HTML and CSS are the foundation of every website.",resources:[{name:"MDN Web Docs",type:"free",note:"The ultimate reference"},{name:"Kevin Powell YouTube",type:"free",note:"Best CSS teacher on YouTube"},{name:"CSS Tricks",type:"free",note:"Practical CSS guides"},{name:"Scrimba HTML/CSS",type:"free",note:"Interactive browser learning"}],milestone:"Build a fully responsive portfolio site deployed on GitHub Pages",tip:"Use Chrome DevTools constantly. Inspect every website you visit.",tasks:[{t:"Semantic HTML: header, nav, main, article, section, footer",d:"Rebuild a Wikipedia article using only semantic tags"},{t:"CSS Flexbox — navbars, card rows, centering",d:"Build a navbar, 3-card row, and hero section"},{t:"CSS Grid — 2D page layouts",d:"Build a dashboard with sidebar + header + content"},{t:"Responsive design + media queries",d:"Mobile-first: start at 320px, scale up to 1440px"},{t:"CSS animations + transitions + custom properties",d:"Add hover effects, loading spinners, entrance animations"}]},
    "React":     {icon:"⚛️",salary:"₹7–35 LPA",demand:"Very High",roles:["Frontend Dev","React Dev","Full-Stack Dev"],why:"React is used by Facebook, Airbnb, Netflix. It's #1 in job listings.",resources:[{name:"React Official Docs",type:"free",note:"New react.dev is excellent"},{name:"Scrimba React Course",type:"free",note:"Free interactive React"},{name:"Jack Herrington YouTube",type:"free",note:"Advanced React patterns"},{name:"Epic React (Kent C. Dodds)",type:"paid",note:"Most thorough React course"}],milestone:"Build a full CRUD task manager with filtering, sorting, and localStorage",tip:"Stop following tutorials after a point. Build something real.",tasks:[{t:"JSX, functional components, and props",d:"Build a ProfileCard component with 3 different instances"},{t:"useState and event handling",d:"Build a counter, form input, and toggle button"},{t:"useEffect and data fetching",d:"Fetch from PokeAPI, show loading spinner, handle errors"},{t:"Context API for global state",d:"Add dark/light theme toggle with createContext"},{t:"React Router v6 + full project",d:"Build a task manager with filtering and local storage"}]},
    "Node.js":   {icon:"🟩",salary:"₹7–32 LPA",demand:"High",roles:["Backend Dev","Full-Stack Dev","API Dev"],why:"Node.js lets JavaScript run on servers.",resources:[{name:"Node.js Official Docs",type:"free",note:"Essential reference"},{name:"Traversy Media Node.js",type:"free",note:"Free practical crash course"},{name:"Dave Gray Node.js",type:"free",note:"Full series from scratch"},{name:"NodeJS Complete Guide Udemy",type:"paid",note:"Most comprehensive paid course"}],milestone:"Build a REST API with JWT auth, MongoDB, and CRUD — deploy on Render",tip:"Understand the event loop before complex async code.",tasks:[{t:"Node architecture: event loop, non-blocking I/O",d:"Read 3 files concurrently — observe the async behavior"},{t:"Express.js REST API: GET, POST, PUT, DELETE",d:"Create a books API with in-memory data first"},{t:"MongoDB + Mongoose schemas, models, queries",d:"Replace in-memory storage with MongoDB Atlas"},{t:"JWT authentication: register, login, protected routes",d:"Hash passwords with bcrypt, check tokens in middleware"},{t:"Deploy to Render + Postman documentation",d:"Write a Postman collection for every endpoint"}]},
    "REST APIs": {icon:"🔌",salary:"₹6–30 LPA",demand:"High",roles:["Backend Dev","API Engineer","Integration Dev"],why:"REST APIs are how every modern app communicates.",resources:[{name:"REST API Tutorial",type:"free",note:"Clear REST concepts"},{name:"Postman Learning Center",type:"free",note:"Best testing tool"},{name:"HTTP Status Dogs",type:"free",note:"Fun way to learn HTTP codes"},{name:"API Design Patterns",type:"paid",note:"Advanced production patterns"}],milestone:"Design and build a fully documented REST API with Swagger/OpenAPI spec",tip:"Design your API before coding it.",tasks:[{t:"HTTP methods: GET, POST, PUT, PATCH, DELETE",d:"Know exactly when to use each one"},{t:"HTTP status codes: 200, 201, 400, 401, 403, 404, 500",d:"Return the correct status for every scenario"},{t:"RESTful URL design and resource naming",d:"/users/:id/posts is correct — /getPostsByUserId is wrong"},{t:"JWT authentication for protected endpoints",d:"Add Bearer token middleware to your routes"},{t:"Pagination, filtering, sorting on list endpoints",d:"GET /products?page=2&limit=10&sort=price&order=asc"}]},
    "MongoDB":   {icon:"🍃",salary:"₹6–28 LPA",demand:"High",roles:["Backend Dev","Full-Stack Dev","Data Engineer"],why:"MongoDB is the most popular NoSQL database.",resources:[{name:"MongoDB University",type:"free",note:"Official free courses — M001 first"},{name:"Mongoose Docs",type:"free",note:"Essential for Node.js + MongoDB"},{name:"Fireship MongoDB",type:"free",note:"Quick visual explanations"},{name:"MongoDB Complete Bootcamp",type:"paid",note:"Practical end-to-end course"}],milestone:"Build a blog with users, posts, comments, and aggregation analytics",tip:"Learn indexing early — a missing index on 1M records will crash your app.",tasks:[{t:"Documents, collections, and flexible schema model",d:"CRUD with MongoDB Compass first, then code"},{t:"Query operators: $gt, $lt, $in, $regex, $exists",d:"Write 10 real queries using these operators"},{t:"Mongoose schemas: required, default, validators",d:"Create User and Post schemas with proper validation"},{t:"Aggregation Pipeline: $match, $group, $lookup",d:"Calculate average comments per post by author"},{t:"Indexes: single field, compound, text",d:"Use .explain() and verify index usage"}]},
  }},
  "Data & AI":{ icon:"🤖", color:"#fbbf24", skills:{
    "Machine Learning":{icon:"🧠",salary:"₹10–45 LPA",demand:"Very High",roles:["ML Engineer","Data Scientist","AI Researcher"],why:"ML is transforming every industry.",resources:[{name:"Andrew Ng ML Specialisation",type:"free",note:"Best ML course ever, free to audit"},{name:"Kaggle Learn ML",type:"free",note:"Quick practical micro-courses"},{name:"Fast.ai Practical ML",type:"free",note:"Top-down, build first"},{name:"Hands-On ML (Géron)",type:"paid",note:"The practical ML bible"}],milestone:"End-to-end ML project: data cleaning → training → evaluation → prediction",tip:"Every algorithm you learn, implement it by hand first.",tasks:[{t:"NumPy + Pandas fundamentals",d:"Load Titanic dataset, inspect types, handle nulls"},{t:"Supervised learning: linear + logistic regression",d:"Implement gradient descent from scratch in NumPy"},{t:"Decision trees, random forests, evaluation metrics",d:"Build a spam classifier, evaluate with F1 score"},{t:"Model evaluation: cross-validation, confusion matrix",d:"Learn WHEN to use each metric — accuracy is often wrong"},{t:"Feature engineering + Kaggle competition",d:"Improve your model 10% through features only"}]},
    "Deep Learning":{icon:"🔬",salary:"₹12–50 LPA",demand:"High",roles:["DL Engineer","Computer Vision Dev","NLP Engineer"],why:"Deep Learning powers GPT, image recognition, and autonomous vehicles.",resources:[{name:"Fast.ai Deep Learning",type:"free",note:"Free practical-first course"},{name:"d2l.ai",type:"free",note:"Free book with code"},{name:"Andrew Ng DL Specialisation",type:"free",note:"Audit free"},{name:"PyTorch Official Tutorials",type:"free",note:"Best way to learn PyTorch"}],milestone:"Fine-tune a pre-trained model on your own dataset and deploy as an API",tip:"Start with PyTorch over TensorFlow. More Pythonic, easier to debug.",tasks:[{t:"Neural networks from scratch in NumPy",d:"Implement forward + backprop manually"},{t:"PyTorch basics: Dataset, DataLoader, nn.Module",d:"Redo your NumPy net in PyTorch"},{t:"CNNs for image classification on CIFAR-10",d:"Beat 80% accuracy, visualise feature maps"},{t:"Transfer learning: fine-tune ResNet on custom data",d:"Compare vs training from scratch"},{t:"Deploy model as a FastAPI REST endpoint",d:"Add a simple HTML frontend for image upload"}]},
    "Data Analysis":{icon:"📊",salary:"₹6–28 LPA",demand:"High",roles:["Data Analyst","Business Analyst","Product Analyst"],why:"Data analysis bridges raw data and business decisions.",resources:[{name:"Kaggle Learn Pandas",type:"free",note:"Best structured Pandas course"},{name:"Towards Data Science",type:"free",note:"Hundreds of EDA walkthroughs"},{name:"Real Python Data Science",type:"free",note:"Clear tutorials per tool"},{name:"Python for Data Analysis",type:"paid",note:"Written by Pandas creator"}],milestone:"Full EDA on a 50,000+ row dataset, published as a Jupyter notebook",tip:"Find a dataset you actually care about.",tasks:[{t:"Pandas: DataFrames, indexing, loc/iloc, filtering",d:"Load a CSV, inspect dtypes, filter rows, rename columns"},{t:"Data cleaning: nulls, types, duplicates, outliers",d:"Take a messy Kaggle dataset and make it analysis-ready"},{t:"GroupBy + aggregations",d:"Answer 10 business questions about a sales dataset"},{t:"Merge/join datasets, pivot tables",d:"Combine 3 datasets, create a monthly sales by region pivot"},{t:"Visualise with Matplotlib + Seaborn",d:"Every insight needs a chart"}]},
    "SQL":       {icon:"🗄️",salary:"₹5–25 LPA",demand:"Very High",roles:["Data Analyst","Backend Dev","Data Engineer"],why:"SQL is the most used data skill in the world.",resources:[{name:"SQLZoo",type:"free",note:"Interactive SQL in browser"},{name:"Mode Analytics SQL Tutorial",type:"free",note:"Real analytics SQL patterns"},{name:"DataLemur",type:"free",note:"Real interview questions from FAANG"},{name:"SQL for Data Analysis",type:"paid",note:"Advanced analytics techniques"}],milestone:"Solve 50 SQL problems on DataLemur including window functions and complex JOINs",tip:"Write SQL every day, even 15 minutes.",tasks:[{t:"SELECT, WHERE, ORDER BY, LIMIT, DISTINCT",d:"Write 30 queries on a sample database"},{t:"All JOINs: INNER, LEFT, RIGHT, FULL OUTER, SELF",d:"Draw the Venn diagram and write an example for each"},{t:"GROUP BY, HAVING, aggregate functions",d:"Find average order value per customer per month"},{t:"CTEs (WITH clause) and subqueries",d:"Rewrite a complex subquery as a CTE"},{t:"Window functions: ROW_NUMBER, RANK, LAG, SUM OVER",d:"Find each customer's most recent order"}]},
  }},
  "DevOps":{ icon:"☁️", color:"#34d399", skills:{
    "Docker":    {icon:"🐳",salary:"₹8–35 LPA",demand:"Very High",roles:["DevOps Engineer","Backend Dev","Cloud Engineer"],why:"Docker solves 'it works on my machine'. Every modern deployment uses containers.",resources:[{name:"Docker Official Docs",type:"free",note:"Get Started section is excellent"},{name:"TechWorld Nana Docker",type:"free",note:"Best free DevOps YouTube"},{name:"Play with Docker",type:"free",note:"Free browser-based Docker"},{name:"Docker Deep Dive (Book)",type:"paid",note:"Short, clear, practical"}],milestone:"Containerise a full-stack app (frontend + backend + DB) with Docker Compose",tip:"Containerise every project you build from now on.",tasks:[{t:"Images vs containers vs registries",d:"Pull nginx, run it, inspect it, stop and remove it"},{t:"Write a Dockerfile for a Node.js or Python app",d:"Use .dockerignore and multi-stage build"},{t:"Docker Compose for multi-container apps",d:"web app + MongoDB + Redis in one compose.yml"},{t:"Volumes + networking",d:"Make DB data persist across container restarts"},{t:"Push to Docker Hub, pull on another machine",d:"Build, tag, push, pull — the full CI/CD cycle"}]},
    "AWS":       {icon:"☁️",salary:"₹10–45 LPA",demand:"Very High",roles:["Cloud Engineer","DevOps Engineer","Solutions Architect"],why:"AWS has 33% of the cloud market.",resources:[{name:"AWS Free Tier",type:"free",note:"12 months free — use it now"},{name:"Cloud Quest (AWS)",type:"free",note:"Official gamified learning"},{name:"AWS Skill Builder",type:"free",note:"Official platform, many free courses"},{name:"Adrian Cantrill AWS SAA",type:"paid",note:"Best Solutions Architect course"}],milestone:"Deploy a 3-tier app: React on S3, Node on EC2, data on RDS, with proper IAM",tip:"Use the Free Tier aggressively. Build something in AWS every week.",tasks:[{t:"Regions, AZs, free tier — set billing alert at $5",d:"Explore the console for 30 minutes after setup"},{t:"Launch EC2 Ubuntu, SSH in, deploy a web app",d:"Make it accessible from the internet"},{t:"S3 static website hosting + CloudFront CDN",d:"Deploy your React app on S3"},{t:"IAM: users, roles, policies (least privilege)",d:"Create a role for EC2 that can only read from one S3 bucket"},{t:"RDS PostgreSQL in a private subnet",d:"Never expose your database to the public internet"}]},
    "Linux":     {icon:"🐧",salary:"₹7–32 LPA",demand:"Essential",roles:["DevOps Engineer","SRE","Backend Dev"],why:"Every server in the world runs Linux.",resources:[{name:"Linux Journey",type:"free",note:"Best interactive Linux site"},{name:"The Linux Command Line",type:"free",note:"Free online — most complete book"},{name:"OverTheWire Bandit",type:"free",note:"Learn Linux by solving challenges"},{name:"Linux Foundation Courses",type:"paid",note:"Official Linux Foundation content"}],milestone:"Write a Bash script that automates server setup",tip:"Install Ubuntu on WSL2 right now. The only way to learn Linux is to live in the terminal daily.",tasks:[{t:"Navigate filesystem: ls, cd, pwd, find, locate",d:"Find all .log files modified in the last 7 days"},{t:"Permissions: chmod, chown, tar, gzip",d:"Create a backup script"},{t:"Process management: ps, top, kill, systemctl",d:"Find the process using the most CPU and kill it"},{t:"Write Bash scripts: variables, loops, functions, args",d:"Automate your dev environment setup in one script"},{t:"Nginx reverse proxy + SSL with Let's Encrypt",d:"Serve your app on HTTPS"}]},
    "Git":       {icon:"🌿",salary:"₹5–25 LPA",demand:"Essential",roles:["Every developer role","Open Source Contributor"],why:"Git is how all software is built collaboratively.",resources:[{name:"Oh My Git! (game)",type:"free",note:"Learn Git by playing"},{name:"Atlassian Git Tutorial",type:"free",note:"Clearest written tutorial"},{name:"Learn Git Branching",type:"free",note:"Visual interactive game"},{name:"Git Docs (official)",type:"free",note:"Reference for every command"}],milestone:"Contribute a real pull request to an open-source project on GitHub",tip:"Never force push to main. Understand git rebase --interactive.",tasks:[{t:"init, add, commit, status, log — 80% of daily Git",d:"Make 10 commits with meaningful messages"},{t:"Branching: branch, checkout, merge, resolve conflicts",d:"Create a feature branch, merge back, resolve a conflict"},{t:"Remote: clone, push, pull, fetch, GitHub",d:"Push a project to GitHub, clone it on another machine"},{t:"Interactive rebase: squash, fixup, reword",d:"Clean up 5 messy commits into 1 meaningful one"},{t:"GitHub Actions: automated test on every push",d:"A basic CI workflow is enough to start"}]},
  }},
  "Security":{ icon:"🔐", color:"#f87171", skills:{
    "Ethical Hacking":{icon:"🕵️",salary:"₹8–40 LPA",demand:"Growing Fast",roles:["Penetration Tester","Red Team","Bug Bounty Hunter"],why:"Cybersecurity jobs grow 3x faster than average.",resources:[{name:"TryHackMe",type:"free",note:"Best platform to start"},{name:"Hack The Box",type:"free",note:"More advanced real challenges"},{name:"TCM Security Courses",type:"paid",note:"Best practical hacking courses"},{name:"PortSwigger Web Academy",type:"free",note:"Free web app security labs"}],milestone:"Complete TryHackMe Jr Penetration Tester path and hack your first HTB machine",tip:"Document everything. Write a professional pentest report for every machine.",tasks:[{t:"Networking: OSI model, TCP/IP, ports, protocols",d:"Capture and analyse HTTP + DNS traffic with Wireshark"},{t:"Linux commands for hacking: nmap, netcat, grep, find",d:"Scan your home network with nmap"},{t:"Complete TryHackMe Pre-Security + Beginner paths",d:"Earn the certificates"},{t:"Web vulnerabilities: SQLi, XSS, IDOR (OWASP Top 10)",d:"Complete PortSwigger SQLi and XSS labs for free"},{t:"Set up home lab: Kali + Metasploitable2, write writeups",d:"Hack Metasploitable2 fully, document every step"}]},
    "Cybersecurity":{icon:"🛡️",salary:"₹8–38 LPA",demand:"Very High",roles:["SOC Analyst","Security Engineer","Cloud Security"],why:"Cybercrime costs $8 trillion/year.",resources:[{name:"CompTIA Security+ Guide",type:"paid",note:"Gold standard entry cert"},{name:"OWASP Top 10",type:"free",note:"Essential web security reference"},{name:"CyberDefenders",type:"free",note:"Blue team SOC challenges"},{name:"Blue Team Labs Online",type:"free",note:"Free defensive security labs"}],milestone:"Pass CompTIA Security+ and complete 10 blue team labs on CyberDefenders",tip:"Learn both offense and defense. You can't defend what you can't attack.",tasks:[{t:"CIA triad, attack types: phishing, ransomware, DDoS",d:"For each attack, write one defensive control"},{t:"Cryptography: symmetric, asymmetric, hashing, TLS",d:"Explain how HTTPS works end-to-end"},{t:"SIEM + log analysis with Splunk Free or ELK Stack",d:"Write a detection rule for failed SSH logins"},{t:"Incident response: identify, contain, eradicate, recover",d:"Write an IR playbook for a ransomware scenario"},{t:"CompTIA Security+ certification exam",d:"Use Professor Messer's free course + practice exams"}]},
  }},
  "Design":{ icon:"🎨", color:"#a78bfa", skills:{
    "Figma":  {icon:"🖌️",salary:"₹6–28 LPA",demand:"High",roles:["UI Designer","UX Designer","Product Designer"],why:"Figma is the industry-standard design tool.",resources:[{name:"Figma Official Learn",type:"free",note:"Official tutorials — start here"},{name:"DesignCourse YouTube",type:"free",note:"Free UI/UX Figma tutorials"},{name:"Scrimba Figma Course",type:"free",note:"Interactive browser-based"},{name:"Refactoring UI (Book)",type:"paid",note:"Best UI design book ever"}],milestone:"Design a complete mobile app (10+ screens) with a component library and prototype",tip:"Copy great designs before making originals. Recreate an Airbnb screen.",tasks:[{t:"Frames, layers, shapes, typography, colour styles",d:"Recreate a simple landing page pixel-by-pixel"},{t:"Auto Layout for responsive components",d:"Build a button that resizes correctly with different text"},{t:"Components with variants: primary, secondary, disabled",d:"Build a button with 4 states"},{t:"Design a 10-screen mobile app",d:"Onboarding, home, detail, settings, empty states"},{t:"Interactive prototype + get feedback from non-designers",d:"Link all screens, present to 3 people"}]},
    "UI/UX":  {icon:"✏️",salary:"₹6–25 LPA",demand:"High",roles:["UX Designer","Product Designer","UX Researcher"],why:"Understanding users separates good from great products.",resources:[{name:"Nielsen Norman Group",type:"free",note:"The authoritative UX resource"},{name:"Google UX Design Coursera",type:"free",note:"Free to audit, comprehensive"},{name:"Laws of UX",type:"free",note:"Design principles explained visually"},{name:"Don't Make Me Think",type:"paid",note:"Classic UX book — short and essential"}],milestone:"Design a product from user research through prototype, with usability test evidence",tip:"Watch real users use your design. 5 user tests reveal 85% of usability problems.",tasks:[{t:"Study Gestalt principles and visual hierarchy",d:"Audit 3 apps you use daily"},{t:"Conduct 3 user interviews for a problem space",d:"Listen more than you talk"},{t:"Build low-fidelity wireframes for your solution",d:"Paper or Figma — speed matters here"},{t:"Run a usability test on your prototype",d:"5 participants minimum, record sessions"},{t:"Present a UX case study: problem → research → solution",d:"Publish on Behance or your portfolio site"}]},
  }},
  "CS Fundamentals":{ icon:"📚", color:"#4ade80", skills:{
    "DSA":         {icon:"🧩",salary:"₹10–60 LPA",demand:"Essential for top companies",roles:["SDE at FAANG","Competitive Programmer","Senior Backend"],why:"DSA is the gatekeeper to top tech companies.",resources:[{name:"Striver A2Z Sheet",type:"free",note:"Best structured DSA roadmap for India"},{name:"NeetCode.io",type:"free",note:"150 curated problems with solutions"},{name:"Strivers SDE Sheet",type:"free",note:"180 problems covering every pattern"},{name:"CLRS (Intro to Algorithms)",type:"paid",note:"The academic bible for deep theory"}],milestone:"Solve 200 LeetCode problems across all major topics and pass a mock interview",tip:"Don't grind randomly. Follow Striver's A2Z.",tasks:[{t:"Arrays + Strings: two pointers, sliding window, prefix sum",d:"Solve 30 easy+medium — at least 5 of each pattern"},{t:"Linked Lists: reverse, cycle detection, merge, LRU",d:"Implement singly + doubly linked lists from scratch"},{t:"Trees + BST: traversals, height, LCA, serialisation",d:"Implement all 4 traversals iteratively"},{t:"Graphs: BFS, DFS, topo sort, Dijkstra, Union-Find",d:"Solve 20 graph problems including 3 grid problems"},{t:"DP: memoisation → tabulation, knapsack, LCS, LIS",d:"Solve Blind 75 DP problems — watch NeetCode for patterns"}]},
    "System Design":{icon:"🏗️",salary:"₹20–80 LPA",demand:"Critical for senior roles",roles:["Senior SDE","Staff Engineer","Solutions Architect"],why:"System Design separates junior from senior engineers.",resources:[{name:"ByteByteGo (Alex Xu)",type:"free",note:"Best system design YouTube"},{name:"System Design Interview Vol 1+2",type:"paid",note:"Standard books for SD interviews"},{name:"DDIA (Designing Data-Intensive Apps)",type:"paid",note:"Most important tech book of the decade"},{name:"Grokking SD Interview",type:"paid",note:"Structured course with common questions"}],milestone:"Design URL shortener, Instagram, and WhatsApp — articulate every trade-off clearly",tip:"Every SD answer: requirements → capacity estimation → high-level design → deep dive → trade-offs.",tasks:[{t:"Scalability: vertical vs horizontal, load balancers",d:"Design a system that handles 10x traffic"},{t:"Caching: Redis, CDN, cache invalidation strategies",d:"Design a caching layer for a Twitter home timeline"},{t:"Databases: SQL vs NoSQL, sharding, replication, CAP",d:"Choose and justify a database for 5 different use cases"},{t:"Message queues: Kafka, pub/sub, async processing",d:"Design an order system with event-driven architecture"},{t:"Design URL shortener end-to-end in 45 minutes",d:"Cover hashing, DB schema, redirect, analytics, scale"}]},
  }},
};

/* ═══════════════════════════════════════════════════
   LEARN FLOW DATA
═══════════════════════════════════════════════════ */
const LEARN_FLOW = {
  "Python":[{topic:"1. Setup & Basics",why:"You need a working environment before writing a single line.",doThis:"Install Python 3 + VS Code. Write first script: variables, print, input, if/else.",time:"Days 1–3"},{topic:"2. Loops, Functions & Lists",why:"These three things make up 70% of all Python programs.",doThis:"Build a number-guessing game with while loop. Write 5 reusable functions.",time:"Days 4–7"},{topic:"3. Dicts, Sets & Tuples",why:"Real programs store data in these structures constantly.",doThis:"Build a student grade tracker using a dict.",time:"Week 2"},{topic:"4. Object-Oriented Programming",why:"OOP lets you model real-world things as objects.",doThis:"Build a BankAccount class: deposit(), withdraw(), balance.",time:"Week 2–3"},{topic:"5. File I/O, JSON & Error Handling",why:"Every real app reads/writes files and handles crashes.",doThis:"Build an expense tracker that saves/loads from a JSON file.",time:"Week 3"},{topic:"6. Modules, pip & venv",why:"Third-party libraries are essential.",doThis:"Install requests, fetch weather from an API. Set up venv.",time:"Week 4"},{topic:"7. Build & Ship a Real Project",why:"Projects cement everything.",doThis:"Build a CLI expense tracker OR a web scraper OR a Telegram bot.",time:"Week 4–5"}],
  "JavaScript":[{topic:"1. Variables, Types & Operators",why:"JavaScript has quirks. Learn them now to avoid mysterious bugs later.",doThis:"Open browser console. Experiment with let, const, var. Test == vs ===.",time:"Days 1–2"},{topic:"2. Functions & Scope",why:"Functions are the building block of all JS code.",doThis:"Rewrite 5 regular functions as arrow functions. Build a counter using a closure.",time:"Days 3–5"},{topic:"3. DOM Manipulation",why:"This is what makes web pages interactive.",doThis:"Build a to-do list: add, delete, mark-complete. Vanilla JS + DOM only.",time:"Week 2"},{topic:"4. Arrays & Objects (ES6+)",why:"map, filter, reduce, destructuring — used in every modern codebase.",doThis:"Take an array of user objects and chain .filter().map().reduce().",time:"Week 2–3"},{topic:"5. Async: Promises → Async/Await",why:"Without async knowledge you can't fetch data from any API.",doThis:"Fetch from OpenWeatherMap. First with .then(), then rewrite with async/await.",time:"Week 3"},{topic:"6. Modules & Tooling",why:"Real apps split code into files.",doThis:"Split your to-do app into 3 files using import/export. Bundle with Vite.",time:"Week 4"},{topic:"7. Deploy a Project",why:"Deployment separates learners from builders.",doThis:"Build a weather app or quiz app. Deploy on GitHub Pages or Vercel.",time:"Week 4–5"}],
  "DSA":[{topic:"1. Arrays & Strings",why:"Foundation of every other data structure.",doThis:"25 problems: two pointers, sliding window, prefix sums.",time:"Week 1–2"},{topic:"2. Linked Lists",why:"Teach pointer manipulation.",doThis:"Implement singly + doubly from scratch. Reverse, cycle detection.",time:"Week 2"},{topic:"3. Trees & BST",why:"Power databases, file systems, expression parsers.",doThis:"BST insert/search/delete. All 4 traversals iteratively.",time:"Week 2–3"},{topic:"4. Graphs: BFS, DFS, Dijkstra",why:"Appear in 30%+ of hard interview questions.",doThis:"Number of islands, course schedule (topo), shortest path.",time:"Week 3–4"},{topic:"5. Dynamic Programming",why:"Separates good candidates from great.",doThis:"30 DP problems: memoisation then tabulation.",time:"Week 4–5"},{topic:"6. Mock Interviews",why:"Interviews are a skill separate from DSA knowledge.",doThis:"10 mock interviews on Pramp. 2 mediums in 45 min while explaining aloud.",time:"Week 5–6"}],
};

/* ═══════════════════════════════════════════════════
   STATE
═══════════════════════════════════════════════════ */
let sel = [], dur = 12, lvl = 'beginner', taskState = {};

/* ═══════════════════════════════════════════════════
   INIT
═══════════════════════════════════════════════════ */
(function init() {
  const catGrid  = document.getElementById('cat-grid');
  const sections = document.getElementById('skill-sections');

  Object.entries(SKILL_DB).forEach(([cat, data]) => {
    const count = Object.keys(data.skills).length;

    const cc = document.createElement('div');
    cc.className = 'cat-card';
    cc.innerHTML = `<div class="ci">${data.icon}</div><div class="cn">${cat}</div><div class="cc">${count} skills</div>`;
    cc.onclick = () => {
      document.querySelectorAll('.cat-card').forEach(c => c.classList.remove('active'));
      cc.classList.add('active');
      document.getElementById(`sec-${slugify(cat)}`).scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
    catGrid.appendChild(cc);

    const sec = document.createElement('div');
    sec.className = 'skill-section';
    sec.id = `sec-${slugify(cat)}`;
    sec.innerHTML = `<div class="skill-section-head"><span style="background:${data.color}20;color:${data.color};padding:3px 10px;border-radius:6px;font-size:.78rem;font-weight:700;">${data.icon} ${cat}</span></div><div class="skill-chips"></div>`;
    const chipsDiv = sec.querySelector('.skill-chips');
    Object.entries(data.skills).forEach(([skill, info]) => {
      const chip = document.createElement('div');
      chip.className = 'sk-chip';
      chip.dataset.skill = skill;
      chip.textContent = info.icon + ' ' + skill;
      chip.onclick = () => toggleSkill(skill, chip);
      chipsDiv.appendChild(chip);
    });
    sections.appendChild(sec);
  });
})();

/* ═══════════════════════════════════════════════════
   HELPERS
═══════════════════════════════════════════════════ */
function slugify(s) { return s.replace(/\s+/g, '_'); }
function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

function findSkill(name) {
  for (const cat of Object.values(SKILL_DB)) {
    if (cat.skills[name]) return cat.skills[name];
  }
  return null;
}

/* ═══════════════════════════════════════════════════
   SKILL TOGGLE + TRAY
═══════════════════════════════════════════════════ */
function toggleSkill(skill, el) {
  if (sel.includes(skill)) {
    sel = sel.filter(s => s !== skill);
    el.classList.remove('picked');
  } else {
    if (sel.length >= 8) { alert('Max 8 skills! Remove one first — focus is key.'); return; }
    sel.push(skill);
    el.classList.add('picked');
  }
  updateTray();
}

function updateTray() {
  const chipsEl = document.getElementById('tray-chips');
  const emptyEl = document.getElementById('tray-empty');
  const trayEl  = document.getElementById('skill-tray');
  const numEl   = document.getElementById('tray-num');
  const fillEl  = document.getElementById('tray-fill');
  const countEl = document.getElementById('tray-count');

  numEl.textContent = sel.length;
  countEl.classList.remove('bump');
  void countEl.offsetWidth;
  countEl.classList.add('bump');

  fillEl.style.width = (sel.length / 8 * 100) + '%';
  countEl.style.background  = sel.length >= 8 ? 'var(--amber-soft)' : 'var(--indigo-soft)';
  countEl.style.color       = sel.length >= 8 ? 'var(--amber)'      : 'var(--indigo)';
  countEl.style.borderColor = sel.length >= 8 ? 'var(--amber)'      : 'var(--border-i)';

  if (!sel.length) {
    emptyEl.style.display = '';
    chipsEl.style.display = 'none';
    trayEl.classList.remove('has-items');
  } else {
    emptyEl.style.display = 'none';
    chipsEl.style.display = '';
    trayEl.classList.add('has-items');

    const existing = new Set([...chipsEl.querySelectorAll('.tray-chip')].map(c => c.dataset.skill));
    [...chipsEl.querySelectorAll('.tray-chip')].forEach(c => {
      if (!sel.includes(c.dataset.skill)) c.remove();
    });
    sel.forEach(skill => {
      if (existing.has(skill)) return;
      const info = findSkill(skill);
      const c = document.createElement('div');
      c.className = 'tray-chip';
      c.dataset.skill = skill;
      c.innerHTML = `
        <span class="tray-chip-icon">${info?.icon || '📌'}</span>
        <span class="tray-chip-name">${skill}</span>
        <button class="tray-chip-remove" onclick="removeSkill('${skill}')" title="Remove ${skill}">×</button>`;
      chipsEl.appendChild(c);
    });
  }
  document.getElementById('btn-next1').disabled = !sel.length;
}

function removeSkill(skill) {
  sel = sel.filter(s => s !== skill);
  document.querySelectorAll('.sk-chip').forEach(c => { if (c.dataset.skill === skill) c.classList.remove('picked'); });
  updateTray();
}

function clearAll() {
  sel = [];
  document.querySelectorAll('.sk-chip').forEach(c => c.classList.remove('picked'));
  updateTray();
}

/* ═══════════════════════════════════════════════════
   STEP 2 CONTROLS
═══════════════════════════════════════════════════ */
function setDur(w, el) { dur = w; document.querySelectorAll('.dur-card').forEach(c => c.classList.remove('sel')); el.classList.add('sel'); }
function setLvl(l, el) { lvl = l; document.querySelectorAll('.lvl-card').forEach(c => c.classList.remove('sel')); el.classList.add('sel'); }

/* ═══════════════════════════════════════════════════
   NAVIGATION
═══════════════════════════════════════════════════ */
function goTo(step) {
  if (step === 2 && !sel.length) return;
  [1,2,3].forEach(i => {
    document.getElementById(`panel-${i}`).classList.toggle('active', i === step);
    const wz = document.getElementById(`wz${i}`);
    wz.classList.toggle('active', i === step);
    wz.classList.toggle('done', i < step);
  });
  [1,2].forEach(i => document.getElementById(`wl${i}`).classList.toggle('done', i < step));
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ═══════════════════════════════════════════════════
   LEARN FLOW BUILDER
═══════════════════════════════════════════════════ */
const LNF_VARIANTS = ['','v2','v3','v4','v5','v6','v2','v3'];

function buildLearnFlow(skill) {
  const steps = LEARN_FLOW[skill];
  if (!steps || !steps.length) return '';
  const show = lvl === 'beginner' ? steps.slice(0,4) : lvl === 'intermediate' ? steps.slice(0,6) : steps;
  const stepsHtml = show.map((s,i) => {
    const v = LNF_VARIANTS[i % LNF_VARIANTS.length];
    const isLast = i === show.length - 1;
    return `<div class="lnf-row ${v}">
      <div class="lnf-left"><div class="lnf-num">${i+1}</div>${!isLast ? '<div class="lnf-line"></div>' : ''}</div>
      <div class="lnf-content">
        <div class="lnf-step-lbl">Step ${i+1} of ${show.length}</div>
        <div class="lnf-topic">${s.topic}</div>
        <div class="lnf-why">${s.why}</div>
        <div class="lnf-do-label">👉 What to do</div>
        <div class="lnf-do">${s.doThis}</div>
        <span class="lnf-time">⏱ ${s.time}</span>
      </div></div>`;
  }).join('');
  return `<div class="lnf-block"><div class="lnf-header">📚 Learn in This Order <em>${show.length} steps</em></div><div class="lnf-steps">${stepsHtml}</div></div>`;
}

/* ═══════════════════════════════════════════════════
   ROADMAP GENERATOR
═══════════════════════════════════════════════════ */
function generate() {
  goTo(3);
  const hpw = { beginner:8, intermediate:12, advanced:16 }[lvl];
  const totalH = dur * hpw;
  const phases = buildPhases();
  const totalTasks = phases.reduce((s,p) => s + p.tasks.length, 0);

  document.getElementById('rm-subtitle').textContent = `${sel.length} skill${sel.length>1?'s':''} · ${dur} weeks · ${cap(lvl)} level`;
  document.getElementById('rm-badges').innerHTML = `<span class="rm-badge rm-badge-purple">${sel.length} Skills</span><span class="rm-badge rm-badge-teal">${dur} Weeks</span><span class="rm-badge rm-badge-yellow">~${totalH}h total</span>`;
  document.getElementById('rm-stats').innerHTML = `
    <div class="rm-stat"><div class="rm-stat-val">${sel.length}</div><div class="rm-stat-lbl">Skills</div></div>
    <div class="rm-stat"><div class="rm-stat-val">${dur}</div><div class="rm-stat-lbl">Weeks</div></div>
    <div class="rm-stat"><div class="rm-stat-val">${phases.length}</div><div class="rm-stat-lbl">Phases</div></div>
    <div class="rm-stat"><div class="rm-stat-val">${totalTasks}</div><div class="rm-stat-lbl">Tasks</div></div>
    <div class="rm-stat"><div class="rm-stat-val">~${totalH}h</div><div class="rm-stat-lbl">Est. Hours</div></div>`;

  const pillsEl = document.getElementById('skill-pills');
  pillsEl.innerHTML = '';
  sel.forEach(skill => {
    const info = findSkill(skill);
    const pill = document.createElement('div');
    pill.className = 'sk-pill';
    pill.innerHTML = `<span>${info?.icon||'📌'}</span><span>${skill}</span>
      <svg width="20" height="20" viewBox="0 0 20 20">
        <circle cx="10" cy="10" r="7" fill="none" stroke="var(--border)" stroke-width="2.5"/>
        <circle cx="10" cy="10" r="7" fill="none" stroke="var(--indigo)" stroke-width="2.5"
          stroke-dasharray="43.98" stroke-dashoffset="43.98" class="pill-arc" data-skill="${skill}" stroke-linecap="round"/>
      </svg>`;
    pillsEl.appendChild(pill);
  });

  const infoSec = document.getElementById('info-sec');
  const infoStrip = document.getElementById('info-strip');
  infoSec.style.display = '';
  infoStrip.style.display = '';
  infoStrip.innerHTML = '';
  sel.forEach(skill => {
    const info = findSkill(skill);
    if (!info) return;
    const block = document.createElement('div');
    block.className = 'info-block';
    block.innerHTML = `<div class="ib-name">${info.icon} ${skill}</div><div class="ib-why">${info.why}</div>
      <div class="ib-tags">${(info.roles||[]).map(r=>`<span class="ib-tag ib-tag-role">${r}</span>`).join('')}
      <span class="ib-tag ib-tag-sal">💰 ${info.salary||'Market rate'}</span>
      <span class="ib-tag ib-tag-dem">📈 ${info.demand||'High'}</span></div>`;
    infoStrip.appendChild(block);
  });

  const container = document.getElementById('rm-phases');
  container.innerHTML = '';
  const pcColors = ['pc1','pc2','pc3','pc4','pc5','pc6','pc1','pc2'];
  const diffLabel = {beginner:'Easy',intermediate:'Medium',advanced:'Hard'}[lvl];
  const diffClass = {Easy:'easy',Medium:'medium',Hard:'hard'}[diffLabel];

  phases.forEach((phase, idx) => {
    const pc = pcColors[idx % pcColors.length];
    const card = document.createElement('div');
    card.className = `phase-card ${pc}`;
    card.dataset.idx = idx;
    const skillChips = (phase.skills||[]).map(s=>`<span class="ph-skill">${findSkill(s)?.icon||'📌'} ${s}</span>`).join('');
    const resHtml = (phase.resources||[]).map(r=>`<div class="res-card"><div class="res-type ${r.type}">${r.type==='free'?'✅ Free':'💳 Paid'}</div><div class="res-name">${r.name}</div><div class="res-note">${r.note}</div></div>`).join('');
    const taskHtml = phase.tasks.map((t,ti) => {
      const key = `${idx}-${ti}`;
      const on = taskState[key] ? 'on' : '';
      const done = taskState[key] ? 'done' : '';
      return `<div class="task-row ${done}" onclick="toggleTask(${idx},${ti},this)">
        <div class="task-cb ${on}"></div><span class="task-num">${ti+1}.</span>
        <div class="task-info"><div class="task-t">${t.t}</div>${t.d?`<div class="task-d">${t.d}</div>`:''}</div></div>`;
    }).join('');
    const learnFlow = buildLearnFlow((phase.skills||[])[0]);
    card.innerHTML = `
      <div class="phase-hdr" onclick="togglePhase(this)">
        <div class="phase-hdr-left">
          <div class="phase-week">${phase.week}</div>
          <div class="phase-name">${phase.title}</div>
          <div class="phase-sub">${phase.subtitle}</div>
          <div class="phase-badges2">
            <span class="ph-badge2 ${diffClass}">${diffLabel}</span>
            <span class="ph-badge2">⏱ ${phase.hours}</span>
            <span class="ph-badge2">📝 ${phase.tasks.length} tasks</span>
            ${phase.isIntegration?'<span class="ph-badge2" style="background:var(--emerald-soft);color:var(--emerald);border:none">🏁 Final Project</span>':''}
          </div>
        </div>
        <div class="phase-hdr-right">
          <div class="phase-mini">
            <div class="mini-track"><div class="mini-fill" style="width:0%"></div></div>
            <span class="mini-count">0 / ${phase.tasks.length}</span>
          </div>
          <span class="phase-chevron">▼</span>
        </div>
      </div>
      <div class="phase-body${idx===0?'':' collapsed'}">
        <div class="phase-desc-block"><p class="phase-desc">${phase.desc}</p></div>
        ${learnFlow}
        ${phase.milestone?`<div class="phase-milestone"><span class="ms-icon">🏆</span><div><div class="ms-main">${phase.milestone}</div><div class="ms-sub">This is your goal — ship it before moving on</div></div></div>`:''}
        ${phase.tip?`<div class="phase-tip"><span>💡</span><span class="tip-text"><strong>Pro tip:</strong> ${phase.tip}</span></div>`:''}
        ${skillChips?`<div class="ph-skills-row">${skillChips}</div>`:''}
        ${resHtml?`<div class="phase-res"><div class="phase-res-label">📚 Curated Resources</div><div class="res-grid">${resHtml}</div></div>`:''}
        <div class="phase-tasks"><div class="tasks-label">✅ Step-by-Step Tasks</div>${taskHtml}</div>
      </div>`;
    container.appendChild(card);
  });

  const firstCard = container.querySelector('.phase-card');
  if (firstCard) firstCard.classList.add('open');
  updateProgress();
}

/* ═══════════════════════════════════════════════════
   PHASE BUILDER
═══════════════════════════════════════════════════ */
function buildPhases() {
  const phases = [];
  const wps = Math.max(1, Math.floor(dur / sel.length));
  const hpw = {beginner:8,intermediate:12,advanced:16}[lvl];
  const levelDesc = {
    beginner:     'Build solid foundations — set up tools, learn core syntax, and ship your first real project.',
    intermediate: 'Go beyond tutorials — write production-quality code and build something portfolio-worthy.',
    advanced:     'Reach expert level — tackle complex problems, optimise for scale, lead real projects.'
  };
  const levelSuffix = {beginner:'— Foundations',intermediate:'— Deep Dive',advanced:'— Mastery'};
  let cur = 1;

  sel.forEach(skill => {
    const info = findSkill(skill) || {};
    const weekEnd = cur + wps - 1;
    const weekLabel = wps===1 ? `Week ${cur}` : `Week ${cur}–${weekEnd}`;
    const totalH = wps * hpw;
    const rawTasks = info.tasks || [];
    const tasks = lvl==='beginner' ? rawTasks.slice(0,4) : lvl==='intermediate' ? rawTasks.slice(0,5) : rawTasks;
    const finalTasks = tasks.length ? tasks : [
      {t:`Set up your ${skill} environment`,d:'Install required tools and configure your workspace'},
      {t:`Complete the official ${skill} getting-started tutorial`,d:'Official docs are always the most accurate'},
      {t:`Build a small project with what you've learned`,d:'Small and complete beats large and unfinished'},
    ];
    phases.push({
      week: weekLabel, title: `${info.icon||'📌'} ${skill}`, subtitle: levelSuffix[lvl],
      desc: levelDesc[lvl] + ` This phase is dedicated entirely to ${skill}.`,
      skills: [skill], tasks: finalTasks,
      resources: info.resources || [{name:'Official Documentation',type:'free',note:'Always the most accurate source'}],
      milestone: info.milestone || null, tip: info.tip || null, hours: `~${totalH}h`, isIntegration: false,
    });
    cur = weekEnd + 1;
  });

  if (cur <= dur) {
    const rem = dur - cur + 1;
    phases.push({
      week: `Week ${cur}–${dur}`, title: '🏁 Integration & Portfolio Project', subtitle: '— Combine Everything',
      desc: `Bring it all together. Build one complete, real-world project showcasing all ${sel.length} skills.`,
      skills: sel.slice(0,4),
      tasks: [
        {t:'Define project scope: problem, features, target users',d:'A focused app done well beats a sprawling one half-done'},
        {t:'Set up the repository with a proper README',d:'What it is, why you built it, how to run it, tech stack'},
        {t:'Build core features one by one with clear commits',d:'Small commits with clear messages show your process'},
        {t:'Write tests for the critical parts',d:'Even 20% coverage on important logic is better than zero'},
        {t:'Deploy publicly (Vercel, Render, Railway)',d:'It must be live — a GitHub link alone is not enough'},
        {t:'Record a 2-minute demo video',d:'A video in your README gets 5x more attention'},
      ],
      resources: [
        {name:'GitHub',type:'free',note:'Host code — clean commit history matters'},
        {name:'Vercel / Netlify',type:'free',note:'Free frontend hosting'},
        {name:'Render / Railway',type:'free',note:'Free backend + database hosting'},
      ],
      milestone: "A live, deployed, documented project you're proud to share",
      tip: 'Quality over features. A clean 3-feature app gets you further than a messy 10-feature one.',
      hours: `~${rem*10}h`, isIntegration: true,
    });
  }
  return phases;
}

/* ═══════════════════════════════════════════════════
   ACCORDION + TASKS
═══════════════════════════════════════════════════ */
function togglePhase(hdr) {
  const card = hdr.closest('.phase-card');
  const body = card.querySelector('.phase-body');
  const open = card.classList.contains('open');
  card.classList.toggle('open', !open);
  body.classList.toggle('collapsed', open);
}
function expandAll()   { document.querySelectorAll('#rm-phases .phase-card').forEach(c => { c.classList.add('open');    c.querySelector('.phase-body').classList.remove('collapsed'); }); }
function collapseAll() { document.querySelectorAll('#rm-phases .phase-card').forEach(c => { c.classList.remove('open'); c.querySelector('.phase-body').classList.add('collapsed'); }); }

function toggleTask(pi, ti, row) {
  const key = `${pi}-${ti}`;
  taskState[key] = !taskState[key];
  row.querySelector('.task-cb').classList.toggle('on', taskState[key]);
  row.classList.toggle('done', taskState[key]);
  const card = row.closest('.phase-card');
  const allT = card.querySelectorAll('.task-row'), doneT = card.querySelectorAll('.task-row.done');
  const pp = allT.length ? Math.round(doneT.length / allT.length * 100) : 0;
  card.querySelector('.mini-fill').style.width = pp + '%';
  card.querySelector('.mini-count').textContent = `${doneT.length} / ${allT.length}`;
  updateProgress();
}

function updateProgress() {
  const all = document.querySelectorAll('#rm-phases .task-row');
  const done = document.querySelectorAll('#rm-phases .task-row.done');
  const pct = all.length ? Math.round(done.length / all.length * 100) : 0;
  document.getElementById('prog-pct').textContent = pct + '%';
  document.getElementById('prog-fill').style.width = pct + '%';
  document.getElementById('prog-done').textContent = `${done.length} of ${all.length} tasks`;
  const C = 43.98;
  sel.forEach(skill => {
    const phases = [...document.querySelectorAll('#rm-phases .phase-card')].filter(c =>
      [...c.querySelectorAll('.ph-skill')].some(s => s.textContent.includes(skill))
    );
    let sA = 0, sD = 0;
    phases.forEach(c => { sA += c.querySelectorAll('.task-row').length; sD += c.querySelectorAll('.task-row.done').length; });
    const arc = document.querySelector(`.pill-arc[data-skill="${skill}"]`);
    if (arc) arc.style.strokeDashoffset = sA ? C - (sD / sA * C) : C;
  });
}

/* ═══════════════════════════════════════════════════
   COPY + RESET
═══════════════════════════════════════════════════ */
function copyRoadmap() {
  const lines = [`📍 CareerCompass Skill Roadmap\n`, `Skills: ${sel.join(', ')}`, `Duration: ${dur} weeks | Level: ${cap(lvl)}\n`];
  document.querySelectorAll('#rm-phases .phase-card').forEach(c => {
    lines.push(`${c.querySelector('.phase-week').textContent.trim()} — ${c.querySelector('.phase-name').textContent.trim()}`);
    c.querySelectorAll('.task-t').forEach(t => lines.push(`  • ${t.textContent}`));
    lines.push('');
  });
  navigator.clipboard.writeText(lines.join('\n')).then(() => alert('✅ Roadmap copied! Paste into Notion, Notes, or anywhere.'));
}

function resetAll() {
  sel = []; dur = 12; lvl = 'beginner'; taskState = {};
  document.querySelectorAll('.sk-chip').forEach(c => c.classList.remove('picked'));
  updateTray();
  document.querySelectorAll('.dur-card').forEach(c => c.classList.remove('sel'));
  document.querySelectorAll('.dur-card')[2].classList.add('sel');
  document.querySelectorAll('.lvl-card').forEach(c => c.classList.remove('sel'));
  document.querySelectorAll('.lvl-card')[0].classList.add('sel');
  document.getElementById('info-strip').style.display = 'none';
  document.getElementById('info-sec').style.display   = 'none';
  goTo(1);
}
