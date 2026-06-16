# 🚀 IPO Intelligence Platform

A production-grade IPO intelligence platform that continuously monitors official IPO activity from SEC EDGAR, NASDAQ, and NYSE, generates structured intelligence, stores historical events, visualizes company progress, and delivers real-time alerts.

Unlike traditional IPO trackers that rely on news articles and rumors, this platform focuses exclusively on official regulatory filings and exchange announcements.

---

# 📸 Screenshots

## Dashboard

The main monitoring dashboard displaying tracked companies, IPO readiness, latest events, platform health, and watchlist activity.

![Dashboard](screenshots/dashboard.png)

---

## Company Overview

Detailed company intelligence page showing IPO progression, historical event timeline, readiness score, and official filing history.

![Company Overview](screenshots/Company_overview.png)

---

## API Documentation

Interactive FastAPI documentation for exploring platform endpoints and testing IPO intelligence APIs.

![API Documentation](screenshots/API_docs.png)

---

## n8n Automation Workflow

Automated workflow responsible for processing IPO events and triggering downstream notifications.

![n8n Workflow](screenshots/n8n_workflow.png)

---

## Azure Production Deployment

Production environment hosted on Microsoft Azure Virtual Machine with automated services and scheduled IPO monitoring pipelines.

![Azure VM](screenshots/Azure_VM.png)

---

# 🎯 Project Overview

The IPO Intelligence Platform automates the complete IPO monitoring workflow:

* Official filing detection
* Exchange announcement monitoring
* Event classification
* Historical storage
* IPO timeline reconstruction
* Intelligence generation
* Dashboard visualization
* Real-time Telegram alerting

The platform operates continuously on Microsoft Azure using automated systemd services and timers.

---

# ✨ Key Features

## Official IPO Monitoring

Monitors official IPO activity from:

* SEC EDGAR
* NASDAQ IPO Center
* NYSE IPO Center

Supported events:

* Confidential Filing
* Confidential Filing Amendment
* S-1 Filing
* S-1 Amendment
* IPO Pricing
* IPO Priced

---

## Watchlist Tracking

Maintains a dedicated IPO watchlist and automatically monitors all tracked companies.

Current watchlist size:

* 12 high-profile private companies

The platform automatically scans official sources every 15 minutes.

---

## IPO Intelligence Engine

Every detected event is enriched with structured intelligence:

* Importance Level
* IPO Stage
* Readiness Score
* Event Classification
* Timeline Progression
* Executive Intelligence Summary

Example:

```text
Stage: 🔴 Final Stage
Readiness Score: 100
Event: IPO_PRICED
```

---

## Historical Event Storage

Stores all official IPO milestones in PostgreSQL.

Features:

* Event history
* Timeline reconstruction
* Duplicate prevention
* Filing date tracking
* Source tracking
* Structured metadata

---

## Interactive Dashboard

Built with Next.js and Tailwind CSS.

Dashboard capabilities:

* IPO Monitoring Overview
* Watchlist Tracking
* Company Detail Pages
* IPO Timeline Visualization
* Event Intelligence Display
* Platform Health Metrics

---

## Real-Time Telegram Alerts

Automatically delivers alerts whenever new official IPO activity is detected.

Each alert contains:

* Company Name
* Event Type
* Source
* Importance
* Stage
* Intelligence Summary

Duplicate protection ensures alerts are never sent twice.

---

# 🏗️ Architecture

```text
SEC EDGAR
NASDAQ IPO
NYSE IPO
      │
      ▼
run_official_pipeline.py
      │
      ▼
IPO Repository
      │
      ▼
PostgreSQL
      │
      ├────────────► FastAPI API
      │                    │
      │                    ▼
      │             Next.js Dashboard
      │
      └────────────► n8n Workflow
                            │
                            ▼
                     Telegram Alerts
```

---

# ⚙️ Technology Stack

## Backend

* Python 3.12
* FastAPI
* SQLAlchemy

## Database

* PostgreSQL

## Frontend

* Next.js 15
* React
* TypeScript
* Tailwind CSS

## Infrastructure

* Microsoft Azure Virtual Machine
* systemd Services
* systemd Timers

## Automation

* n8n

## Notifications

* Telegram Bot API

---

# 📡 API Endpoints

## Platform Statistics

```http
GET /ipo/stats
```

Returns platform-wide metrics.

---

## Watchlist

```http
GET /ipo/watchlist
```

Returns all tracked companies.

---

## Company Details

```http
GET /ipo/company/{company_name}
```

Returns:

* Company Information
* Event History
* IPO Timeline
* Readiness Score
* Intelligence Summary

---

## Latest Official Event

```http
GET /ipo/check-new-alert
```

Returns:

* Latest Official IPO Event
* Intelligence Assessment
* IPO Stage
* Readiness Score
* Timeline Progress

---

# 🗄️ Database Schema

## ipo_watchlist

Stores tracked companies.

Fields:

* id
* company_name
* active
* created_at

---

## ipo_official_events

Stores official IPO events.

Fields:

* id
* company_name
* source
* event_type
* title
* source_url
* filing_date
* detected_at
* event_metadata

---

## alert_state

Stores alert deduplication state.

Fields:

* company_name
* last_headline

---

# 🤖 Automation

The official monitoring pipeline executes automatically every 15 minutes.

Collectors:

* SEC EDGAR Collector
* NASDAQ IPO Collector
* NYSE IPO Collector

Execution Flow:

```text
ipo-official-pipeline.timer
            │
            ▼
run_official_pipeline.py
            │
            ▼
SEC EDGAR Collector
NASDAQ IPO Collector
NYSE IPO Collector
```

---

# ☁️ Deployment

Hosted on:

* Microsoft Azure Virtual Machine

Production Services:

* ipo-api.service
* ipo-dashboard.service
* ipo-official-pipeline.service
* ipo-official-pipeline.timer

---

# 🔒 Reliability Features

✅ Official Source Monitoring

✅ Automated Data Collection

✅ Historical Event Storage

✅ Duplicate Event Prevention

✅ Telegram Alerting

✅ Reboot-Safe Services

✅ Automated Pipeline Scheduling

✅ Watchlist Tracking

✅ Intelligence Enrichment

✅ Timeline Reconstruction

---

# 🚀 Future Enhancements

* Expanded Watchlist Coverage
* Additional Exchange Support
* Advanced IPO Analytics
* User Authentication
* Email Notifications
* Mobile Notifications
* Docker Deployment
* CI/CD Pipelines
* Multi-User Watchlists

---

# 📈 Why This Project?

Most IPO trackers rely heavily on news articles, rumors, and social media discussions.

This platform focuses exclusively on official sources:

* SEC EDGAR Filings
* NASDAQ IPO Announcements
* NYSE IPO Announcements

This significantly reduces false positives and provides a more reliable view of the IPO lifecycle.

---

# 👨‍💻 Author

**Soumyadutta Dash**

AI Automation Engineer | Data Engineering Enthusiast

Built as a production-grade intelligence platform demonstrating:

* Data Engineering
* Backend Development
* Cloud Deployment
* Automation Engineering
* Event Intelligence Systems
* Full-Stack Development
