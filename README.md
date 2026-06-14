# Automated QA & Data Ingestion Pipeline
**Role:** Technical Execution Personnel | **Ecosystem:** MyRabbAI Platform

## 📌 Project Overview
This repository contains a custom-built, Python-based automation architecture designed to maintain 100% platform accessibility and automate bulk data entry tasks. It eliminates manual regression testing and secures data fidelity for cloud-based educational infrastructure. 

## 🚀 Key Features

* **Automated Regression Sentinel:** A headless Selenium script that validates platform authentication daily via Windows Task Scheduler.
* **Proactive Latency Monitoring:** Tracks backend server response times during login sequences to identify application bottlenecks before system failure.
* **Automated Incident Alerting:** Integrates Python's `smtplib` to dispatch real-time email warnings to QA engineers if UI load times exceed the 10-second threshold or if authentication fails.
* **Bulk Data Ingestion Engine:** Automates the migration of hundreds of structured assets (text and localized image paths) from CSV databases directly into the web platform, bypassing human error.
* **Self-Updating Analytics Log:** Automatically appends daily test metrics (Timestamp, Status, Latency) into a localized CSV dataset for weekly KPI reporting.

## 🛠️ Technology Stack
* **Language:** Python 3.x
* **Browser Automation:** Selenium WebDriver (Edge, Headless)
* **Alerting/Networking:** Built-in `smtplib`, `email.mime`
* **Data Handling:** `csv`, `os`, `datetime`
* **Orchestration:** Windows Task Scheduler, Batch Scripting

## 🔐 Security Note
For security and compliance, sensitive credentials (emails, passwords, and SMTP App Passwords) have been removed from this public repository and replaced with placeholder variables to simulate a production environment utilizing secure secrets management.
