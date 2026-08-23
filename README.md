🛡️ AgentShield
AI Agent Reliability Engineering Platform
Team Nawab_Coders · OOSC 4.0 Hackathon · IIIT Allahabad

Table of Contents
Overview
Problem Statement
The Problem We Solve
Our Solution
Key Features
Innovation
Architecture
Tech Stack
Installation Guide
Usage Guide
API Reference
Project Structure
Team
License

1. Overview
AgentShield is an active reliability engineering platform for AI agents. It automatically generates adversarial test scenarios, blocks destructive actions with a real-time firewall, traces root causes, recommends fixes, and verifies improvements—all before deployment.

Philosophy: Attack. Block. Fix. Verify.

Team: Nawab_Coders

Suryanshu Singh - Team Lead, Full Stack Developer

Surya Pratap Singh - Backend, AI Engineer

Raj Nath Pandey - Frontend, UI/UX Designer

2. Problem Statement
PS4: AI Agent Evaluation and Reliability Engine
Build an AI-powered platform that:

Generates realistic and adversarial test scenarios

Runs tests in a sandboxed environment

Detects failure modes

Produces a reliability report

Requirements
Requirement	Description
Scenario Generation	Automatic adversarial test creation
Sandboxed Execution	Safe test environment
Failure Detection	Identify tool loops, hallucinations, unsafe actions
Destructive Testing	Test irreversible actions
Reliability Scorecard	Track reliability across versions
3. The Problem We Solve
The Reality
70% of AI agents fail when deployed on real-world tasks.

Teams test with manual prompts and miss critical failures until deployment.

Four Critical Failure Modes
Failure Mode	Description	Impact
Tool-call loops	Agents stuck in infinite loops	Wasted compute, API costs
Hallucinated confidence	Agents wrong but 100% certain	Incorrect decisions
Unsafe destructive actions	Irreversible actions without confirmation	Data loss, financial damage
Silent goal drift	Agents deviating from user intent	Misaligned outcomes
The Gap
Existing tools tell you something broke after deployment. AgentShield tells you what is about to break before deployment.

4. Our Solution
The AgentShield Flow
Step 1: Attack
Generate adversarial test scenarios automatically

Step 2: Block
Action Firewall intercepts and blocks dangerous actions

Step 3: Root Cause
Trace exactly why the failure happened

Step 4: Fix
Recommend precise, actionable fixes

Step 5: Verify
Re-run tests to prove the fix worked

Results
Metric	Before	After	Improvement
Reliability	61%	94%	+33%
Critical Failures	4	0	-100%
Unsafe Actions	3	0	-100%
Tool Loops	2	0	-100%
5. Key Features
5.1 Action Firewall
Real-time risk scoring and blocking of destructive tool calls.

How It Works:

Calculates risk score (0-100)

Shows blast radius impact

Makes three decisions: Allow, Require Approval, Block

Example:
Tool: delete_account()
Risk Score: 100/100 CRITICAL
Blast Radius: 5 orders, 3 refunds, 2 support tickets
Decision: BLOCKED

5.2 Feral Agent
A secondary AI that actively tries to break your primary agent.

How It Works:

Generates novel attack strategies

Learns from successful attacks

Mutates attacks to find new variants

Evolves its strategy over time

5.3 Self-Evolving Tests
Tests that get smarter over time.

How It Works:

Monitors production failures

Analyzes what went wrong

Generates new regression tests

Adds to test suite automatically

5.4 Root Cause Graph
Visual chain showing exactly why a failure happened.

Example Chain:
User Input
Intent: Account deletion request
Agent Selected: delete_account()
Missing: Confirmation step
Failure: Irreversible action without confirmation

5.5 Canary Testing
Data exfiltration detection with canary tokens.

How It Works:

Creates fake data (canary tokens)

Plants them in the system

Monitors if agent accesses them

Alerts if exfiltration detected

5.6 Cost Analytics
Track test costs in USD and INR.

Metrics Tracked:

Total Cost

Cost Per Test

Cost Per Pass

Cost Per Failure

API Calls

Tokens Used

Example:
USD: $0.0047 total, $0.0002 per test
INR: ₹0.39 total, ₹0.02 per test

6. Innovation
What Makes AgentShield Different
Dimension	AgentShield	Competitors
Approach	Active testing	Passive observation
Timing	Pre-deployment	Post-deployment
Workflow	Attack Block Fix Verify	Report only
Cost Tracking	USD + INR	USD only
CI/CD	Integrated	Manual
Standards	OWASP/MITRE	Proprietary
Competitive Advantages
1. Active, Not Passive
We actively attack, simulate, and break agents to find failures before deployment.

2. Complete Loop
Only platform offering end-to-end workflow: Attack Block Fix Verify.

3. Industry Standards
Aligned with OWASP and MITRE ATT&CK frameworks.

4. Localized Cost Tracking
Track costs in both USD and INR.

5. CI/CD Ready
GitHub Actions runs tests automatically on every pull request.

6. Built for Vibe Coders
Lightweight, git-native, rapid iteration.

7. Architecture
High-Level Architecture
User Experience:
Landing Page → Streamlit App (Frontend)

Frontend (Streamlit):

Interactive Dashboard

Live Test Execution

Real-time Reports

Cost Tracking

Backend (FastAPI on Render):

API Routes

Agent Evaluator

Action Firewall

Attack Generator

Feral Agent

Cost Tracker

External Services:

LLM APIs (Groq/OpenAI)

Vector DB (ChromaDB)

GitHub Actions (CI/CD)

Deployment Architecture
GitHub Repository:

Source Code

Workflows

GitHub Actions (CI/CD):

Run tests on PR

Build and deploy

Render (Backend Hosting):

FastAPI app

Public API endpoint

Streamlit Cloud (Frontend Hosting):

Streamlit app

Public dashboard

8. Tech Stack
Frontend
Technology	Version	Purpose
Streamlit	1.29.0	Interactive dashboard
Plotly	5.18.0	Data visualization
Pandas	2.1.3	Data processing
Custom CSS	-	Premium UI/UX
Backend
Technology	Version	Purpose
FastAPI	0.104.1	REST API framework
Python	3.11	Core language
Uvicorn	0.24.0	ASGI server
Pydantic	2.5.0	Data validation
AI & ML
Technology	Version	Purpose
Groq	0.4.0	Fast LLM inference
OpenAI	1.6.0	LLM API (fallback)
ChromaDB	0.4.22	Vector database
Sentence-Transformers	2.2.2	Embeddings
DevOps
Technology	Purpose
Render	Backend hosting
Streamlit Cloud	Frontend hosting
GitHub Actions	CI/CD pipeline
Git	Version control
Dependencies
Backend (backend/requirements.txt):
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
pydantic==2.5.0
httpx==0.25.0
requests==2.31.0
pandas==2.1.3
plotly==5.18.0
numpy==1.26.2
pyyaml==6.0

Frontend (frontend/requirements.txt):
streamlit==1.29.0
pandas==2.1.3
plotly==5.18.0
numpy==1.26.2
requests==2.31.0
pyyaml==6.0

9. Installation Guide
Prerequisites
Python 3.11+
Git
API keys for Groq/OpenAI (optional)

Step 1: Clone Repository
git clone https://github.com/YOUR_USERNAME/agentshield.git
cd agentshield

Step 2: Create Virtual Environment
macOS/Linux:
python3 -m venv venv
source venv/bin/activate

Windows:
python -m venv venv
venv\Scripts\activate

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Set Environment Variables
Create .env file:
AGENTSHIELD_API_URL=http://localhost:8000
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key

Step 5: Run Backend
cd backend
uvicorn app:app --reload

Step 6: Run Frontend
cd frontend
streamlit run app.py

Step 7: Access Application
Frontend: http://localhost:8501
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs

Deployment
Backend on Render:

Push code to GitHub

Create Web Service on Render

Connect GitHub repository

Root Directory: backend/

Build Command: pip install -r requirements.txt

Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT

Frontend on Streamlit Cloud:

Push code to GitHub

Go to share.streamlit.io

Connect GitHub repository

Main file: frontend/app.py

10. Usage Guide
Quick Start
Click "Test Connection" to verify backend

Click "Generate Tests" (20 scenarios)

Click "Run Tests" to execute

View the reliability report

Click "Apply Fixes" to see improvement

Dashboard Overview
Metrics Display:

Reliability Score

Safety Score

Tests Passed

Consistency Score

Controls:

Test Connection

Generate Tests

Run Tests

Chaos Mode

Apply Fixes

Sections:

Performance Metrics Chart

Attack Type Breakdown

Fix Recommendations

Before/After Comparison

Advanced Features
Chaos Mode:
Toggle to inject failures and test agent recovery

Feral Agent:
Click "Launch Attack" to test AI vs AI

Cost Tracking:
Click "Refresh Cost Summary" to see USD/INR costs

Dataset Loader:
Load OWASP, MITRE, or custom datasets

Per-Turn Evaluation:
Enter user input and see real-time analysis

Canary Testing:
Create canary tokens and check for exfiltration

Fix Generation:
Generate code fixes for failures

11. API Reference
Health Check
GET /
Response: {"message": "AgentShield API", "status": "running"}

GET /health
Response: {"status": "healthy", "api_version": "3.0.0"}

Tools
GET /tools
Response: {"tools": [{"name": "get_customer_profile", ...}]}

Test Generation
POST /generate-tests
Body: {"count": 20}
Response: {"count": 20, "scenarios": [...]}

Test Execution
POST /run-tests
Response: {"passed": 18, "report": {...}}

Report
GET /report
Response: {"overall_reliability": 87, ...}

Fix Application
POST /apply-fix
Body: {"recommendations": ["Add confirmation gate"]}
Response: {"status": "fixes_applied", "new_reliability": 94}

Chaos Mode
POST /chaos-mode?enable=true
Response: {"chaos_enabled": true}

Feral Agent
POST /feral-attack
Response: {"attack": {...}, "result": {...}}

GET /feral-stats
Response: {"total_attacks": 45, "success_rate": 67}

Root Cause
POST /analyze-failures
Response: {"taxonomy_breakdown": {...}, "failure_chains": [...]}

Cost Tracking
POST /track-cost
Response: {"cost": 0.0047, "total_cost": 0.047}

GET /cost-summary
Response: {"summary": {...}, "suggestions": [...]}

GET /cost-to-fix
Response: {"total_cost_usd": 0.0041, "total_cost_inr": 0.34}

Self-Evolution
POST /self-evolve
Response: {"new_tests": 5, "total_tests": 25}

POST /evolve-tests
Response: {"new_scenarios": 3, "total_scenarios": 23}

Per-Turn Evaluation
POST /evaluate-turn
Body: {"user_input": "Delete my account", "agent_thought": "..."}
Response: {"flags": [...], "is_safe": false}

GET /evaluate-stats
Response: {"total_turns_evaluated": 150, "safety_rate": 92}

Canary Testing
POST /create-canary
Body: {"test_id": "canary_001", "data_type": "customer"}
Response: {"canary_id": "abc123", ...}

POST /check-exfiltration
Body: {"response": {...}, "test_id": "canary_001"}
Response: {"exfiltrated": false}

GET /canary-report
Response: {"total_canaries": 5, "exfiltrated": 0}

Fix Generation
POST /generate-fix
Body: {"failure": {"input": "...", "attack_type": "destructive_action"}}
Response: {"fix_id": "fix_001", "code": "..."}

POST /create-pr
Body: {"fix_id": "fix_001"}
Response: {"fix_id": "fix_001", "status": "open"}

GET /fix-history
Response: {"total_fixes": 10, "applied_fixes": 8}

Dataset Loader
GET /datasets
Response: {"datasets": [...], "summary": {...}}

GET /dataset/{name}
Response: {"dataset": "owasp_top_10", "tests": [...]}

POST /dataset/generate
Body: {"name": "my_dataset", "size": 20, "dataset_type": "owasp"}
Response: {"status": "success", "size": 20}

POST /dataset/import
Body: {"name": "imported", "format": "json", "data": "..."}
Response: {"status": "success", "size": 15}

GET /dataset/{name}/export?format=json
Response: {"name": "owasp_top_10", "items": [...]}

GET /dataset/random?count=5
Response: {"tests": [...], "count": 5}

POST /dataset/merge
Body: {"name1": "owasp_top_10", "name2": "mitre_attacks", "new_name": "combined"}
Response: {"status": "success", "size": 24}

12. Project Structure
agentshield/
├── backend/
│ ├── app.py
│ ├── agent.py
│ ├── firewall.py
│ ├── attack_generator.py
│ ├── chaos_injector.py
│ ├── evaluator.py
│ ├── feral_agent.py
│ ├── self_evolver.py
│ ├── per_turn_evaluator.py
│ ├── canary_tester.py
│ ├── fix_generator.py
│ ├── root_cause.py
│ ├── cost_tracker.py
│ ├── production_analyzer.py
│ ├── dataset_loader.py
│ └── requirements.txt
├── frontend/
│ ├── app.py
│ ├── style.css
│ └── requirements.txt
├── .github/
│ └── workflows/
│ └── agent-tests.yml
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE

File Descriptions
backend/app.py - Main FastAPI application with all routes

backend/agent.py - Customer Support Agent (target agent)

backend/firewall.py - Action Firewall with risk scoring

backend/attack_generator.py - Generates adversarial scenarios

backend/chaos_injector.py - Chaos mode testing

backend/evaluator.py - Test runner and report generator

backend/feral_agent.py - AI vs AI testing

backend/self_evolver.py - Self-evolving tests

backend/per_turn_evaluator.py - Per-turn evaluation

backend/canary_tester.py - Canary testing

backend/fix_generator.py - Fix generation

backend/root_cause.py - Root cause analysis

backend/cost_tracker.py - Cost tracking (USD/INR)

backend/production_analyzer.py - Production log analysis

backend/dataset_loader.py - Dataset management

frontend/app.py - Streamlit dashboard

frontend/style.css - Custom styling

agent-tests.yml - CI/CD pipeline

13. Team Nawab_Coders
Name	Role	Contributions
Suryanshu Singh	Team Lead, Full Stack Developer	Architecture, CI/CD, Integration
Surya Pratap Singh	Backend, AI Engineer	API, Firewall, Feral Agent, AI Logic
Raj Nath Pandey	Frontend, UI/UX Designer	Dashboard, CSS, User Experience
14. License
MIT License

Copyright (c) 2026 Team Nawab_Coders

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

🔗 Links
Live Demo: https://agentshield-username.streamlit.app
Backend API: https://agentshield-api.onrender.com
GitHub: https://github.com/YOUR_USERNAME/agentshield

📧 Contact
Team: Nawab_Coders
Hackathon: OOSC 4.0 · IIIT Allahabad

Built with ❤️ by Team Nawab_Coders for OOSC 4.0 Hackathon

