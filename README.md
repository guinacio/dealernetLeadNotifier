# DealerNet Web Leads Notifier

## Overview

This Python script is designed to notify a WhatsApp user or group about new web leads from the DealerNet system for automotive dealerships in Brazil. DealerNet doesn't have a built-in notification system, so this script serves as a workaround to keep users informed about new leads.

## Setup

1. Clone this repository:

```bash
git clone https://github.com/guinacio/dealernetLeadNotifier.git
cd dealernetLeadNotifier
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```

3. Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

4. Create a `credentials.env` file with your DealerNet and WhatsApp API credentials:

```env
USERNAME_CR=<Your_DealerNet_Username>
PASSWORD_CR=<Your_DealerNet_Password>
API_KEY=<Your_WhatsApp_API_Key>
```

Replace `<Your_DealerNet_Username>`, `<Your_DealerNet_Password>`, and `<Your_WhatsApp_API_Key>` with your actual credentials. Or you can edit the example .env file manually.

## Configuration

- Adjust constants in the script such as `WAIT_TIME`, `LOGIN_URL`, `DEALERNET_USERNAME`, `DEALERSHIP`, and `url` according to your setup.

## Running the Script

Run the script:

```bash
python lead_notifier.py
```

The script will run continuously, checking for new leads at the specified intervals.

## Notes

- The script logs errors in the `playwright_errors.log` file.
- Adjust the `NOTIFY_ERROR` variable to control error notifications.

## Screenshot
<img src="https://github.com/guinacio/dealernetLeadNotifier/assets/2325925/044d93d1-f0d7-429d-96f6-45cd0b031fe5)" width="300" />
