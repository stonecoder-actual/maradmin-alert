# MARADMIN Alert System

This project is an automated alert system for MARADMIN (Marine Administrative Messages) promotions. It scrapes MARADMIN RSS feeds, processes promotion announcements, matches them against a contact list, and sends notifications to Slack channels.

## Features

- Uses Selenium with undetected-chromedriver for reliable web scraping.
- Fuzzy name matching to identify promotions.
- Supports multiple Slack channels for different groups.
- Maintains a processed archive to avoid duplicate notifications.
- Configurable via environment variables and config file.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser installed
- Slack workspace with incoming webhook URLs for notification channels

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd Maradmin-Alert
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

4. Create a `.env` file in the `Maradmin-Alert` directory with the following environment variables:

```env
MARADMIN_SLACK_WEBHOOK_URL=<your-main-slack-webhook-url>
DELTA_SLACK_WEBHOOK_URL=<slack-webhook-url-for-delta-group>
MFCC_SLACK_WEBHOOK_URL=<slack-webhook-url-for-mfcc-group>
PERSONAL_SLACK_WEBHOOK_URL=<slack-webhook-url-for-personal-group>
```

Replace the placeholder URLs with your actual Slack webhook URLs. For testing, you can point all to a test Slack channel.

### Configuration

- `config.py` contains configuration constants such as RSS feed URL, file paths, titles of interest, and timeouts.
- `contacts.csv` should contain your contact list with columns: `first_name`, `last_name`, and optionally `group`.
- `MCC Codes.csv` contains MCC codes and corresponding command names for lookup.

### Running the Alert System

Run the main script:

```bash
python main.py
```

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
