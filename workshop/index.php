<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <title>UoM GDG - Agentic Architectures - Dec 2025</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link rel="stylesheet" href="https://bootswatch.com/5/brite/bootstrap.min.css">

  <style>
    html {
      scroll-behavior: smooth;
    }

    body {
      padding-top: 70px;
    }

    .hero {
      padding: 80px 0;
    }

    .hero-subtitle {
      max-width: 600px;
    }

    .section {
      padding: 60px 0;
    }

    footer {
      padding: 30px 0;
    }
  </style>
</head>

<body data-bs-spy="scroll" data-bs-target="#mainNavbar" data-bs-offset="80" tabindex="0">

  <!-- Navbar -->
  <nav id="mainNavbar" class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
    <div class="container">
      <a class="navbar-brand" href="#top">UoM GDG · Agentic Architectures</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarContent">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link" href="#top">Intro</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#presenter">Presenter</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#steps">Steps</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#present">Showcase</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- Hero -->
  <header id="top" class="hero bg-light">
    <div class="container">
      <div class="row align-items-center gy-4">
        <div class="col-lg-7">
          <h1 class="display-4 fw-bold">Agentic Architectures</h1>
          <p class="lead hero-subtitle mt-3">
            Hands-on session exploring the creation of custom agents using tools such as the Agent Development Kit,
            Vertex AI Agent Builder, and the Gemini and GCP command-line interface for rapid prototyping,
            automation, and experiments.
          </p>
          <p class="text-muted mb-4">
            December 2025 &middot; University of Manchester GDG
          </p>
          <a href="https://github.com/nenuadrian/google-agents/tree/main/adk_research_assistant" target="_blank"
            class="btn btn-outline-primary btn-lg">
            GitHub Repository
          </a>
          <br /><br />
          <br /><br />
          <h2>nenuadrian.com/uom/gdg/2025/workshop</h2>
        </div>
        <div class="col-lg-5">
          <div class="card">
            <div class="card-body">
              <div class="fs-5">
                <pre><code>+-----------------------------+
| (START)                     |
|  sequential_pipeline_agent  |
+--------------+--------------+
               |
               v
+-----------------------------+
| Step 1: parallel_research_agent |
+--------------+--------------+
               |
  +------------+------------+
  |                         |
  v                         v
+-----------------+     +----------------------+
|  google_agent   |     | arxiv_research_agent |
+-----------------+     +----------------------+
  |       |                 |        |
  |       v                 |        v
  | [ Google Search ]       |  [ arXiv API ]
  |                         |
  | "google_research_result"| "arxiv_research_result"
  |                         |
  +------------+------------+
               |
               v
+-----------------------------+
| Step 2:      merger_agent     |
+-----------------------------+
               |
               | (Synthesizes results)
               | "Synthesized Report & Subject"
               v
+-----------------------------+
| Step 3:      email_agent      |
+-----------------------------+
               |
               | (Generates & sends HTML email)
               v
+-----------------------------+
|        [ SMTP Server ]        |
+-----------------------------+
               |
               v
+-----------------------------+
|       (END) User's Inbox      |
+-----------------------------+</code></pre>
              </div>
            </div>
          </div>
        </div>
      </div>
  </header>

  <!-- Presenter -->
  <section id="presenter" class="section">
    <div class="container">
      <h2 class="mb-4">Presenter: Adrian Mircea Nenu</h2>
      <div class="row gy-4">
        <div class="col-lg-8">
          <p>
            Originally from Romania, CS BSc with Industrial Experience at UoM, MSc Business Analytics at Uni. of Bath,
            worked at Morgan Stanley (IE + full-time 4 years) as an individual contributor and manager, and at Google.
            Worked in customer-facing, web, and infrastructure (C++) at Google.
          </p>
          <p>
            My PhD work spans from policy-gradient methods and optimisation geometry to GNNs and Graph Transformers, in
            the <a href="https://github.com/agent-lab" target="_blank">AgentLab group</a> with Dr Mingfei Sun and Prof
            Kask.
          </p>
          <a href="https://nenuadrian.com" target="_blank" class="btn btn-outline-primary btn-lg">
            Connect with Adrian
          </a>
        </div>
        <div class="col-lg-4">
          <div class="card">
            <div class="card-header">
              Quick bio
            </div>
            <div class="card-body">
              <ul class="mb-0">
                <li>AI researcher &amp; software engineer</li>
                <li>Works with RL, RLHF, and LLM tooling</li>
                <li>Enjoys clean abstractions &amp; messy experiments</li>
                <li>Hackathon enthusiast</li>
                <li>Knowledge is power</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>


  <section class="section bg-light" id="steps">
    <div class="container">
      <h2 class="mb-4">Step I: Base Agent</h2>
      <div class="row gy-4">
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header">
              Kick off
            </div>
            <div class="card-body">
              <pre class="mb-3"><code># Python Env
python -m venv .venv
source .venv/bin/activate

# OR Conda - feel free to use anything, e.g. Poetry, Pipenv, etc.
conda create -n agents python=3.11 -y
conda activate agents

# Create an API key on https://aistudio.google.com/api-keys

# Create base project: 1) gemini-2.5-flash, 1) Google AI Studio, provide the Key
adk create adk_research_assistant

adk run adk_research_assistant
</code></pre>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <p>500 requests / day limit on Free tier.</p>
          <a href="https://aistudio.google.com/api-keys" target="_blank" class="btn btn-outline-primary btn-lg">
            Google AI Studio
          </a>
          <a href="https://google.github.io/adk-docs/get-started/python/" target="_blank"
            class="btn btn-outline-primary btn-lg">
            ADK Docs - Python Getting Started
          </a>
          <br />
          <br />
          <div class="card">
            <div class="card-header">
              Append to .env
            </div>
            <div class="card-body">
              <pre class="mb-3"><code>GEMINI_MODEL=gemini-2.5-flash-preview-09-2025</code></pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <h2 class="mb-4">Step II: arXiv Agent</h2>
      <div class="row gy-4">
        <div class="col-lg-8">
          <p>We will use the arXiv API to gather research papers related to your query.</p>
        </div>
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header">
              arxiv_agent.py
            </div>
            <div class="card-body">
              <pre class="mb-3"><code><?= file_get_contents("../adk_research_assistant/arxiv_agent.py") ?></code></pre>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="card">
            <div class="card-header">
              Dependencies
            </div>
            <div class="card-body">
              <pre class="mb-3"><code>pip install arxiv</code></pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <section class="section bg-light">
    <div class="container">
      <h2 class="mb-4">Step III: Email Agent</h2>
      <div class="row gy-4">
        <div class="col-lg-12">
          <p>We will use MailerSend to send emails with the research report.</p>
          <p>Make an account on <a href="https://www.mailersend.com/" target="_blank">mailersend.com</a>, get SMTP
            credentials.</p>
        </div>
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header">
              email_agent.py
            </div>
            <div class="card-body">
              <pre class="mb-3"><code><?= file_get_contents("../adk_research_assistant/email_agent.py") ?></code></pre>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <a href="https://www.mailersend.com/" target="_blank" class="btn btn-outline-primary btn-lg">
            Create MailerSend Account
          </a>
          <br />
          <br />

          <div class="card">
            <div class="card-header">
              Dependencies
            </div>
            <div class="card-body">
              <pre class="mb-3"><code>pip install secure-smtplib</code></pre>
            </div>
          </div>
          <br />
          <p>Once you have made an account, update your .env file to contain:</p>
          <div class="card">
            <div class="card-header">
              Append to .env
            </div>
            <div class="card-body">
              <pre class="mb-3"><code>SMTP_DEFAULT_PORT=587
SMTP_HOST="smtp.mailersend.net"
SMTP_USERNAME=""
SMTP_PASSWORD=""
FROM_ADDR="test@DOMAIN_GENERATED"
TO_ADDR="YOUR_EMAIL"</code></pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="container">
      <h2 class="mb-4">Bring it all together</h2>
      <div class="row gy-4">
        <div class="col-lg-12">
          <p>This is where we combine all the agents to create a seamless research assistant workflow.</p>
          <p>We will use the Google Search and arXiv agents to gather information, then merge and email the results.</p>
        </div>
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header">
              agent.py
            </div>
            <div class="card-body">
              <pre class="mb-3"><code><?= file_get_contents("../adk_research_assistant/agent.py") ?></code></pre>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="card">
            <div class="card-body">
              <div class="fs-5">
                <pre><code>+-----------------------------+
| (START)                     |
|  sequential_pipeline_agent  |
+--------------+--------------+
               |
               v
+-----------------------------+
| Step 1: parallel_research_agent |
+--------------+--------------+
               |
  +------------+------------+
  |                         |
  v                         v
+-----------------+     +----------------------+
|  google_agent   |     | arxiv_research_agent |
+-----------------+     +----------------------+
  |       |                 |        |
  |       v                 |        v
  | [ Google Search ]       |  [ arXiv API ]
  |                         |
  | "google_research_result"| "arxiv_research_result"
  |                         |
  +------------+------------+
               |
               v
+-----------------------------+
| Step 2:      merger_agent     |
+-----------------------------+
               |
               | (Synthesizes results)
               | "Synthesized Report & Subject"
               v
+-----------------------------+
| Step 3:      email_agent      |
+-----------------------------+
               |
               | (Generates & sends HTML email)
               v
+-----------------------------+
|        [ SMTP Server ]        |
+-----------------------------+
               |
               v
+-----------------------------+
|       (END) User's Inbox      |
+-----------------------------+</code></pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <section id="present" class="section bg-light">
    <div class="container">
      <h2 class="mb-4">Step IV: Present your work?!</h2>
      <div class="row gy-4">
        <div class="col-lg-12">
          <p>
            Let's have a few of you showcase what you have built, challenges you faced in this session and what you
            think you could build next!
          </p>

        </div>


      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer class="bg-dark text-light">
    <div class="container text-center">
      <p class="mb-1">&copy; 2025 UoM GDG · Gemini CLI Workshop</p>
      <p class="mb-0">
        Contact:
        <a href="mailto:contact@nenuadrian.com" class="link-light">
          contact@nenuadrian.com
        </a>
      </p>
    </div>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI"
    crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.min.js"
    integrity="sha384-G/EV+4j2dNv+tEPo3++6LCgdCROaejBqfUeNjuKAiuXbjrxilcCdDz6ZAVfHWe1Y"
    crossorigin="anonymous"></script>
</body>

</html>