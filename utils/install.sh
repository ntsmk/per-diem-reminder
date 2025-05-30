#!/usr/bin/env sh
set -e  # Exit script if any command fails

# Navigate to the app directory
cd /root/per-diem/app/

# Set permissions for .env file
chmod 600 .env

# Create and activate a virtual environment (only if it doesn't already exist)
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install required dependencies
pip3 install -r requirements.txt

# Set environment variables and add the cron job (overwrite existing crontab) runs on the 1st of every month at midnight
echo "0 0 1 * * cd /root/per-diem/app && source /root/per-diem/app/.env && /root/per-diem/app/venv/bin/python /root/per-diem/app/main.py >> /root/per-diem/cron.log 2>&1" | crontab -

# Print confirmation message
echo "Cron set completed!"


