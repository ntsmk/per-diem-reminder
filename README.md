Per-Diem Email Notification

Description

This project automates email notifications for employees whose time entries exceed a customizable threshold (default: 2 hours). The system alerts them that they may need to submit a per-diem request. 
The project primarily utilizes Python and the ConnectWise API.

Installation

Follow these steps to set up the project locally:

1. Modify Deployment Script

Edit deploy.ps1 to update the file path and server domain name.

Currently, the script is set to use a local folder path and a local VM IP address.

2. Configure Environment Variables

Create a .env file and add the required API credentials. Place .env file **under \per-diem\app**:

public_key=[YOUR_PUBLIC_KEY]

private_key=[YOUR_PRIVATE_KEY]

client_id=[YOUR_CLIENT_ID]

company_id=[YOUR_COMPANY_ID]

manage_url=[MANAGE_URL]

3. Run the Application

Execute the deployment script:

.\deploy.ps1

