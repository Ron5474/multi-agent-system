# Multi-Agent Personal Life OS — Setup Guide

Everything you need to do before running the system for the first time.

---

## 1. Python Environment

```bash
cd multi-agent
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

---

## 2. Discord Server

### 2a. Create the server and channels

1. Open Discord → click **+** (Add a Server) → Create My Own → For me and my friends
2. Name it whatever you like (e.g. "Life OS")
3. Create these **6 text channels** (exact names matter):
   - `general`
   - `morning-brief`
   - `school`
   - `research`
   - `system`
   - `tasks`

### 2b. Create a webhook for each channel

For **each** of the 6 channels:

1. Right-click the channel → **Edit Channel**
2. Go to **Integrations** → **Webhooks** → **New Webhook**
3. Give it a name (e.g. "Agent Bot")
4. Click **Copy Webhook URL** — save it, you'll paste it into `.env`

### 2c. Create the Discord bot

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **New Application** → give it a name (e.g. "Chief of Staff")
3. Go to the **Bot** tab → click **Add Bot**
4. Under **Privileged Gateway Intents**, enable **Message Content Intent**
5. Click **Reset Token** → copy the token — save it for `.env`

### 2d. Invite the bot to your server

1. Still in the developer portal, go to **OAuth2** → **URL Generator**
2. Under **Scopes**, check `bot`
3. Under **Bot Permissions**, check:
   - Send Messages
   - Read Message History
   - View Channels
4. Copy the generated URL → open it in your browser → select your server → Authorize

---

## 3. Environment Variables

```bash
cp .env.example .env
```

Open `.env` and fill in every value:

```
# Your privately hosted Qwen endpoint
LLM_BASE_URL=https://your-hosted-qwen-endpoint
LLM_API_KEY=your-api-key
LLM_MODEL=qwen-3.5

# Discord bot token (from step 2c)
DISCORD_BOT_TOKEN=your-discord-bot-token

# Canvas iCal feed URL (from step 4)
CANVAS_ICAL_URL=https://sjsu.instructure.com/feeds/calendars/user_YOURTOKEN.ics

# Webhook URLs (one per channel, from step 2b)
DISCORD_WEBHOOK_GENERAL=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_MORNING_BRIEF=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_SCHOOL=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_RESEARCH=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_SYSTEM=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_TASKS=https://discord.com/api/webhooks/...
```

---

## 4. Canvas iCal Feed

The Assignment Scout pulls your deadlines from your personal Canvas calendar feed — no API token or IT approval needed.

1. Log into [sjsu.instructure.com](https://sjsu.instructure.com)
2. Click **Calendar** in the left sidebar
3. At the bottom of the page, click **Calendar Feed**
4. Copy the URL that appears (it looks like `https://sjsu.instructure.com/feeds/calendars/user_XXXX.ics`)

Then in `.env`:
```
CANVAS_ICAL_URL=https://sjsu.instructure.com/feeds/calendars/user_YOURTOKEN.ics
```

---

## 5. Running the System

You need two terminals.

**Terminal 1 — Discord bot** (handles your messages in #general):
```bash
cd multi-agent
venv/bin/python3 bot.py
```
You should see: `Chief of Staff online as <bot name>`

**Terminal 2 — Scheduler** (runs agents on their cron schedules):
```bash
cd multi-agent
venv/bin/python3 scheduler.py
```
You should see: `Scheduler starting`

---

## 6. Smoke Tests

### Test the bot responds
Type this in your Discord `#general` channel:
```
hello, who are you?
```
Expected: Chief of Staff replies with a greeting.

### Test a research task
```
research the latest work on AI agents and tool use
```
Expected: Chief of Staff acknowledges and queues the task. Within 30 minutes the Research Analyst picks it up and posts a summary to `#research`.

### Manually trigger the System Monitor
```bash
cd multi-agent
venv/bin/python3 -c "from agents.system_monitor import run_health_check; run_health_check()"
```
Expected: A health report appears in your Discord `#system` channel.

### Manually trigger Assignment Scout
```bash
cd multi-agent
venv/bin/python3 -c "from agents.assignment_scout import run_scan; run_scan()"
```
Expected: Deadline summary posted to `#school` (requires `CANVAS_ICAL_URL` in `.env`).

---

## 7. Cron Schedule Reference

| Time | Agent | Action |
|---|---|---|
| 8:00 AM | Assignment Scout | Fetch Canvas deadlines → `#school` |
| 8:05 AM | Chief of Staff | Morning brief → `#morning-brief` |
| 8:10 AM | System Monitor | Health check → `#system` |
| Every 30 min | Research Analyst | Poll task queue, run pending research |
| 8:00 PM | System Monitor | Evening health check → `#system` |
| 11:00 PM | Chief of Staff | Nightly memory consolidation |

---

## 8. Project Structure Reference

```
multi-agent/
├── core/
│   ├── agent_loop.py       ← bare-metal LLM tool-dispatch loop
│   ├── llm_client.py       ← Qwen API wrapper
│   └── task_queue.py       ← memory/tasks.json read/write
├── agents/
│   ├── chief_of_staff.py   ← orchestrator + Discord brain
│   ├── assignment_scout.py ← deadline scanner
│   ├── research_analyst.py ← web search + summarization
│   └── system_monitor.py   ← health checks
├── tools/
│   ├── memory.py           ← read/write markdown memory files
│   ├── file_reader.py      ← read PDFs and text files
│   ├── canvas.py           ← fetch assignments from Canvas iCal feed
│   ├── web_search.py       ← DuckDuckGo search
│   └── discord_tools.py    ← post to Discord via webhooks
├── prompts/                ← system prompt for each agent
├── memory/                 ← runtime state (gitignored)
├── bot.py                  ← Discord bot entry point
├── scheduler.py            ← APScheduler cron heartbeats
└── .env                    ← your credentials (gitignored)
```
