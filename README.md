# Per-Diem Email Reminder

## Overview

This project automates email alerts for employees whose time entries exceed a configurable threshold (default: **2 hours**). When this threshold is passed, the system notifies employees that a per-diem request may be required.

The application is built using **Python** and integrates with the **ConnectWise API**.

---

## Installation

Follow the steps below to set up the project locally:

### 1. Update the Deployment Script

Modify `deploy.ps1` to reflect your local environment:

- Update the folder path.
- Replace the local VM IP with your server's domain or IP address.

### 2. Set Environment Variables

Create a `.env` file and place it in the following directory:

