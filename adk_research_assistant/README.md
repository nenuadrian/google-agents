# Research assistant

https://nenuadrian.com/uom/gdg/2025/workshop/

![image](./assets/example.png)

## Install

```bash
# Python Env
python -m venv .venv
source .venv/bin/activate

# OR Conda - feel free to use anything, e.g. Poetry, Pipenv, etc.
conda create -n agents python=3.11 -y
conda activate agents

pip install google-adk

# Create an API key on https://aistudio.google.com/api-keys

# Create base project: 1) gemini-2.5-flash, 1) Google AI Studio, provide the Key
adk create adk-research-assistant
cd adk-research-assistant
```

Add to .env the model to use:

```bash
GEMINI_MODEL=gemini-2.5-flash
```

## Simple arxiv agent

```bash
pip install arxiv
```

## Simple email agent

Make an account on [mailersend.com](https://www.mailersend.com/), get SMTP credentials.
Add them to the `.env` file.

```bash
SMTP_DEFAULT_PORT=587
SMTP_HOST="smtp.mailersend.net"
SMTP_USERNAME=""
SMTP_PASSWORD=""
FROM_ADDR="test@DOMAIN_GENERATED"
TO_ADDR="YOUR_EMAIL"
```

```bash
pip install secure-smtplib
```
