import csv
import json
import logging
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

import feedparser
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import CONFIG
from slack_notifier import SlackNotifier

class MaradminProcessor:
    def __init__(self):
        load_dotenv()
        self.config = CONFIG  # Set config first since other methods depend on it
        self.setup_logging()
        self.contacts = []
        self.processed_maradmins = self.load_processed_maradmins()
        self.driver = None
        self.mcc_lookup = self.load_mcc_lookup()

        slack_webhook_url = os.getenv('MARADMIN_SLACK_WEBHOOK_URL')
        self.slack_notifier = None
        if slack_webhook_url:
            try:
                self.slack_notifier = SlackNotifier(slack_webhook_url, self)
                self.logger.info("Slack notifier initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize Slack notifier: {str(e)}")

    def setup_logging(self):
        log_dir = Path(CONFIG['log_dir'])
        log_dir.mkdir(exist_ok=True)
        log_filename = log_dir / f"maradmin-alert{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_driver(self):
        try:
            options = uc.ChromeOptions()
            options.headless = True
            options.add_argument('--window-size=1920,1080')
            options.binary_location = /usr/bin/chromium
            self.driver = uc.Chrome(options=options)
            self.logger.info("Chrome driver initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to setup Chrome driver: {str(e)}")
            raise

    def cleanup_driver(self):
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("Chrome driver closed")
            except OSError as e:
                # Suppress WinError 6: The handle is invalid
                if e.winerror == 6:
                    self.logger.info("Suppressed WinError 6 during Chrome driver cleanup")
                else:
                    self.logger.warning(f"Exception during Chrome driver cleanup: {str(e)}")
            except Exception as e:
                self.logger.warning(f"Exception during Chrome driver cleanup: {str(e)}")

    def load_contacts(self, custom_csv_path=None) -> List[Dict[str, str]]:
        contacts = []
        try:
            csv_path = custom_csv_path if custom_csv_path else self.config['contacts_file']
            with open(csv_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if row['first_name'].strip() and row['last_name'].strip():
                        contacts.append({
                            'first_name': row['first_name'].strip().upper(),
                            'last_name': row['last_name'].strip().upper(),
                            'full_name': f"{row['last_name'].strip().upper()}, {row['first_name'].strip().upper()}",
                            'group': row.get('group', '').strip(),
                            'mos': row.get('mos', '').strip().upper() if 'mos' in row else ''
                        })
            self.logger.info(f"Successfully loaded {len(contacts)} contacts")
            return contacts
        except Exception as e:
            self.logger.error(f"Error loading contacts: {str(e)}")
            return []
    
    def load_mcc_lookup(self) -> Dict[str, str]:
        mcc_lookup = {}
        try:
            with open('MCC Codes.csv', 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if len(row) >= 4:
                        code = row[0].strip().upper()
                        command_name = row[3].strip()
                        mcc_lookup[code] = command_name
            self.logger.info(f"Loaded {len(mcc_lookup)} MCC codes from MCC.csv")
        except Exception as e:
            self.logger.error(f"Error loading MCC lookup: {str(e)}")
        return mcc_lookup

    def get_command_name_from_mcc(self, mcc_code: str) -> str:
        return self.mcc_lookup.get(mcc_code.upper(), "Unknown Command")

    def load_processed_maradmins(self) -> Dict:
        try:
            archive_path = Path(self.config['archive_file'])
            if not archive_path.exists():
                self.logger.info("No processed MARADMINs file found, creating new one")
                with open(archive_path, 'w') as file:
                    json.dump({}, file)
                return {}
            with open(archive_path, 'r') as file:
                data = json.load(file)
                self.logger.info(f"Loaded {len(data)} processed MARADMINs")
                return data
        except json.JSONDecodeError:
            self.logger.warning("Invalid JSON in processed MARADMINs file, creating new one")
            with open(archive_path, 'w') as file:
                json.dump({}, file)
            return {}
        except Exception as e:
            self.logger.error(f"Error loading processed MARADMINs: {str(e)}")
            return {}

    def save_processed_maradmins(self):
        try:
            with open(CONFIG['archive_file'], 'w') as file:
                json.dump(self.processed_maradmins, file, indent=2)
            self.logger.info("Processed MARADMINs saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving processed MARADMINs: {str(e)}")

    def extract_page_text(self, url: str) -> Optional[str]:
        try:
            self.logger.info(f"Loading page: {url}")
            self.driver.get(url)
            wait = WebDriverWait(self.driver, CONFIG['page_timeout'])
            content_selectors = [
                '.body-text',
                '.article-content',
                '.content-body',
                '[class*="body"]',
                '[class*="content"]'
            ]
            content_element = None
            for selector in content_selectors:
                try:
                    content_element = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            if content_element is None:
                content_element = self.driver.find_element(By.TAG_NAME, 'body')
            text_content = content_element.text
            self.logger.info(f"Successfully extracted {len(text_content)} characters from page")
            return text_content
        except Exception as e:
            self.logger.error(f"Error extracting text from {url}: {str(e)}")
            return None

    def search_1stlt_promotions(self, text: str, contacts: List[Dict]) -> List[Dict]:
        matches = []
        text_upper = text.upper()
        sections = text_upper.split('\n\n')
        promotion_sections = []
        for section in sections:
            if "THE FOLLOWING" in section and any(title in section for title in ["1STLT", "OFFICER"]):
                promotion_sections.append(section)
        if not promotion_sections:
            self.logger.warning("Could not find promotion section in MARADMIN")
            return matches

        # Compile regex patterns for all contacts once for efficiency
        compiled_patterns = []
        for contact in contacts:
            last_name = contact['last_name']
            first_name = contact['first_name']
            pattern = re.compile(
                rf"^{first_name}\s+(?:[A-Z]\s*\.\s+)?{last_name}(?:\s+(?:II|III|JR|SR))?\b",
                re.IGNORECASE
            )
            compiled_patterns.append((contact, pattern))

        for promotion_section in promotion_sections:
            for line in promotion_section.split('\n'):
                line = line.strip()
                if not line or len(line) < 5:
                    continue
                for contact, pattern in compiled_patterns:
                    if pattern.search(line):
                        match_info = {
                            'contact': contact,
                            'matched_text': line,
                            'confidence': 100,
                            'name_format': f"{contact['last_name']}, {contact['first_name']}"
                        }
                        matches.append(match_info)
                        self.logger.info(
                            f"Match found: {contact['full_name']} "
                            f"(confidence: 100%) "
                            f"matched with: {line}"
                        )
                        break
        return matches

    def process_maradmin(self, entry: Dict) -> List[Dict]:
        self.logger.info(f"Processing MARADMIN: {entry['title']}")
        page_text = self.extract_page_text(entry['link'])
        if not page_text:
            self.logger.error(f"Could not extract text from {entry['link']}")
            return []
        self.logger.info(f"Extracted text length: {len(page_text)}")
        normalized_title = entry['title'].strip().upper()
        self.logger.info(f"Normalized MARADMIN title: {normalized_title}")
        # Determine if this is an enlisted promotion MARADMIN using regex matching
        enlisted_titles = CONFIG.get('enlisted_promotion_titles', [])
        officer_titles = CONFIG.get('officer_promotion_titles', [])
        enlisted_match = False
        for title in enlisted_titles:
            pattern = rf"\b{re.escape(title.strip().upper())}\b"
            self.logger.info(f"Checking regex pattern '{pattern}' against MARADMIN title")
            if re.search(pattern, normalized_title):
                enlisted_match = True
                break
        if enlisted_match:
            self.logger.info("Using search_enlisted_promotions")
            matches = self.search_enlisted_promotions(page_text, self.contacts)
        else:
            officer_match = False
            for title in officer_titles:
                pattern = rf"\b{re.escape(title.strip().upper())}\b"
                self.logger.info(f"Checking regex pattern '{pattern}' against MARADMIN title")
                if re.search(pattern, normalized_title):
                    officer_match = True
                    break
            if officer_match:
                self.logger.info("Using search_1stlt_promotions")
                matches = self.search_1stlt_promotions(page_text, self.contacts)
            else:
                self.logger.info("No matching promotion type found")
                matches = []
        self.processed_maradmins[entry['id']] = {
            'title': entry['title'],
            'link': entry['link'],
            'processed_date': datetime.now().isoformat(),
            'matches_found': len(matches),
            'match_details': [
                {
                    'name': match['full_name'] if 'full_name' in match else match['contact']['full_name'],
                    'confidence': match.get('confidence', 100),
                    'matched_text': match.get('matched_text', '')
                }
                for match in matches
            ]
        }
        if matches and self.slack_notifier:
            self.slack_notifier.send_promotion_notification(matches, entry['title'], entry['link'])
        return matches

    def check_rss_feed(self) -> List[Dict]:
        self.logger.info("Checking RSS feed for new MARADMINs")
        try:
            feed = feedparser.parse(CONFIG['rss_url'])
            if not feed.entries:
                self.logger.warning("No entries found in RSS feed")
                return []
            self.logger.info(f"Found {len(feed.entries)} entries in RSS feed")
            self.logger.info("Available MARADMINs in feed:")
            for entry in feed.entries:
                self.logger.info(f"- {entry.title}")
            new_entries = []
            for entry in feed.entries:
                if any(title in entry.title.upper() for title in CONFIG['officer_promotion_titles']):
                    if entry.id not in self.processed_maradmins:
                        new_entries.append(entry)
            self.logger.info(f"Found {len(new_entries)} new promotion MARADMINs to process")
            return new_entries
        except Exception as e:
            self.logger.error(f"Error checking RSS feed: {str(e)}")
            return []

    def run(self):
        self.logger.info("Starting MARADMIN Alert System v2.0")
        try:
            self.contacts = self.load_contacts()
            if not self.contacts:
                self.logger.error("No contacts loaded, exiting")
                return
            self.setup_driver()
            new_entries = self.check_rss_feed()
            if not new_entries:
                self.logger.info("No new promotion MARADMINs found")
                if self.slack_notifier:
                    self.slack_notifier.send_promotion_notification([], "No New Promotions", "")
                return
            for entry in new_entries:
                matches = self.process_maradmin(entry)
                if matches:
                    group_to_matches = {
                        'Delta': [],
                        'MFCC': [],
                        'Personal': []
                    }
                    for match in matches:
                        group = match['contact'].get('group', '').strip()
                        if group == 'Delta':
                            group_to_matches['Delta'].append(match)
                        elif group == 'MFCC':
                            group_to_matches['MFCC'].append(match)
                        else:
                            group_to_matches['Personal'].append(match)
                    # Cache webhook URLs once per group
                    webhook_urls = {}
                    for group in group_to_matches.keys():
                        webhook_env_var = f"{group.upper()}_SLACK_WEBHOOK_URL"
                        webhook_urls[group] = os.getenv(webhook_env_var)
                        self.logger.info(f"Group '{group}' uses env var '{webhook_env_var}' with webhook URL: {'FOUND' if webhook_urls[group] else 'NOT FOUND'}")
                    for group, group_matches in group_to_matches.items():
                        webhook_url = webhook_urls.get(group)
                        if webhook_url and group_matches:
                            notifier = SlackNotifier(webhook_url, self)
                            notifier.send_promotion_notification(group_matches, f"{entry['title']} - {group} Promotions", entry['link'])
                        else:
                            self.logger.warning(f"No Slack webhook URL found for group '{group}' or no matches to send")
                time.sleep(2)
            self.save_processed_maradmins()
            self.logger.info(f"Processing complete:")
            self.logger.info(f"- Processed {len(new_entries)} new MARADMINs")
        except Exception as e:
            self.logger.critical(f"Critical error in main execution: {str(e)}")
        finally:
            self.cleanup_driver()

    def search_enlisted_promotions(self, text: str, contacts: List[Dict]) -> List[Dict]:
        matches = []
        lines = text.splitlines()
        for line in lines:
            # Each line may contain two columns of enlisted promotions
            print(f"Processing line: {line}")
            columns = [line[:40].strip(), line[40:].strip()]
            print(f"Split into columns: {columns}")
            for col in columns:
                if not col:
                    continue
                print(f"Checking column: {col}")
                # Match pattern: LASTNAME  FI MI MOS/number/MCCCODE
                m = re.match(r"([A-Z]+)\s+([A-Z]{1,2})\s+([\w/ ]+)", col)
                if m:
                    last_name = m.group(1)
                    initials = m.group(2)
                    rest = m.group(3)
                    print(f"Parsed last_name: {last_name}, initials: {initials}, rest: {rest}")
                    for contact in contacts:
                        # Match last name exactly and first initial of first name
                        if contact['last_name'] == last_name and contact['first_name'].startswith(initials[0]):
                            match_info = {
                                'contact': contact,
                                'matched_text': col,
                                'confidence': 90,
                                'name_format': f"{contact['last_name']}, {contact['first_name']}"
                            }
                            matches.append(match_info)
                            self.logger.info(f"Enlisted match found: {contact['full_name']} matched with: {col}")
                            print(f"Match found: {contact['full_name']} matched with: {col}")
                            break
        return matches
