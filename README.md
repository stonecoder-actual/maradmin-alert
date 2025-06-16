# MARADMIN Alert System

This project is an automated alert system for MARADMIN (Marine Administrative Messages) promotions. It scrapes MARADMIN RSS feeds, processes promotion announcements, matches them against a contact list, and sends notifications to Slack channels.

## Features

- Uses Selenium with undetected-chromedriver for reliable web scraping.
- Fuzzy name matching to identify promotions.
- Supports multiple Slack channels for different groups.
- Maintains a processed archive to avoid duplicate notifications.
- Configurable via environment variables and config file.

## Setup Instructions

### Quick Setup (Recommended for First-Time Users)

For first-time setup, use the automated setup wizard:

```bash
python setup.py
```

This will launch a GUI that will help you:
- Install required Python packages
- Verify Chrome browser installation
- Configure Slack webhook URLs
- Create template CSV files
- Test your configuration

### Manual Setup (Advanced Users)

If you prefer manual setup or need to troubleshoot:

#### Prerequisites

- Python 3.8 or higher
- Google Chrome browser installed
- Slack workspace with incoming webhook URLs for notification channels

#### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd maradmin-alert
```

2. Create and activate a Python virtual environment (optional but recommended):

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required Python packages:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project directory with the following environment variables:

```env
MARADMIN_SLACK_WEBHOOK_URL=<your-main-slack-webhook-url>
DELTA_SLACK_WEBHOOK_URL=<slack-webhook-url-for-delta-group>
MFCC_SLACK_WEBHOOK_URL=<slack-webhook-url-for-mfcc-group>
```

Replace the placeholder URLs with your actual Slack webhook URLs. For testing, you can point all to a test Slack channel.

#### Configuration Files

- `config.py` contains configuration constants such as RSS feed URL, file paths, titles of interest, and timeouts.
- `contacts.csv` should contain your contact list with columns: `first_name`, `last_name`, `group`, and optionally `mos`.
- `MCC Codes.csv` contains MCC codes and corresponding command names for lookup.

Example `contacts.csv` format:
```csv
first_name,last_name,group,mos
John,Doe,Personal,0311
Jane,Smith,Delta,0651
Bob,Johnson,MFCC,0231
```

### Running the Alert System

You can run the system in several ways:

1. Using the Automated Run Scripts (Recommended for scheduled tasks):

The project includes two automated run scripts that handle virtual environment setup and dependency management:

- For Windows: `run.bat`
- For Linux: `run.sh`

These scripts will:
- Create a Python virtual environment if it doesn't exist
- Install/update required dependencies
- Run the main script with proper error handling
- Provide detailed logging with timestamps

2. GUI Mode (Recommended for manual searches):
```bash
python run_gui.py
```
This will launch the graphical interface where you can:
- Search for specific promotions
- Clear processed MARADMINs
- Access the setup wizard if needed

3. Command Line Mode (Alternative for manual runs):
```bash
python main.py
```

### Automated Scheduling

#### Windows Task Scheduler
1. Open Task Scheduler (Win + R, type "taskschd.msc")
2. Click "Create Basic Task"
3. Name it "MARADMIN Alert" and click Next
4. Choose your trigger (Daily/Weekly/etc) and click Next
5. Set the start time and frequency
6. Select "Start a Program"
7. In "Program/script" enter the full path to run.bat:
   ```
   C:\Path\To\Your\maradmin-alert\run.bat
   ```
8. In "Start in" enter:
   ```
   C:\Path\To\Your\maradmin-alert
   ```
9. Click Next, then Finish
10. Optional: Right-click the task and select Properties to set additional options like "Run with highest privileges"

#### Linux Cron Job
1. Make the run script executable:
```bash
chmod +x run.sh
```

2. Open your crontab:
```bash
crontab -e
```

3. Add one of these lines depending on your desired schedule:
```bash
# Run every hour
0 * * * * /path/to/maradmin-alert/run.sh >> /path/to/maradmin-alert/logs/cron.log 2>&1

# Run daily at 8 AM
0 8 * * * /path/to/maradmin-alert/run.sh >> /path/to/maradmin-alert/logs/cron.log 2>&1

# Run every Monday at 9 AM
0 9 * * 1 /path/to/maradmin-alert/run.sh >> /path/to/maradmin-alert/logs/cron.log 2>&1
```

Note: The run scripts include timestamp logging and error handling, making it easier to troubleshoot scheduled runs. Check the logs directory for detailed execution logs.

The system will:

- Load contacts and MCC codes.
- Check the MARADMIN RSS feed for new promotion entries.
- Scrape and process new entries.
- Send notifications to Slack channels based on contact groups.
- Log activity to the `logs` directory.

### Logs

Logs are saved in the `logs` directory with timestamps for each run.

## Code Structure

- `config.py`: Configuration constants.
- `slack_notifier.py`: SlackNotifier class for sending Slack messages.
- `maradmin_processor.py`: MaradminProcessor class with main processing logic.
- `main.py`: Entry point script to run the alert system.

## Extending the System

- Add new functions or notification channels by creating new modules or extending existing ones.
- Update `contacts.csv` and Slack webhook environment variables to manage groups and channels.
- Modify `config.py` for custom RSS feeds or titles of interest.

## Troubleshooting

- Ensure Chrome browser is installed and compatible with undetected-chromedriver.
- Verify Slack webhook URLs are correct and have permissions.
- Check logs in the `logs` directory for detailed error messages.
- For Selenium issues, ensure network access and page selectors are up to date.

## License

Specify your license here.

## Contact

For questions or support, contact [Your Name] at [Your Email].
