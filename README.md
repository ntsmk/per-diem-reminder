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

Create a `.env` file and place it in the `\per-diem\app\` directory.

Add the following lines to the `.env` file, replacing the placeholders with your actual credentials:

- `public_key=[YOUR_PUBLIC_KEY]`
- `private_key=[YOUR_PRIVATE_KEY]`
- `client_id=[YOUR_CLIENT_ID]`
- `company_id=[YOUR_COMPANY_ID]`
- `manage_url=[YOUR_MANAGE_URL]`

### 3. Deploy the Application

Run the PowerShell deployment script:

`.\deploy.ps1`

This script will:

- Set up the environment.
- Launch the application using the credentials and configuration from your `.env` file.

If everything is configured correctly, the script will begin checking time entries and sending notification emails as needed.

---

## Notes

- Ensure Python and required dependencies are installed on your system.
- For automation, you can schedule the script using Task Scheduler (Windows) or `cron` (Linux/macOS).
