import logging
import requests
from typing import List, Dict, Optional

class SlackNotifier:
    def __init__(self, webhook_url: str, processor=None):
        self.webhook_url = webhook_url
        self.processor = processor

    def format_name(self, full_name: str, matched_text: str) -> str:
        """
        Format name as 'First MI Last' from full_name 'LAST, FIRST' and matched_text line.
        matched_text example: 'MICHAEL A. YURECKO              09JUN25      K03'
        """
        parts = matched_text.strip().split()
        if len(parts) >= 2:
            first = parts[0].capitalize()
            middle = ''
            last = ''
            if len(parts[1]) == 2 and parts[1].endswith('.'):
                middle = parts[1].capitalize()
                if len(parts) >= 3:
                    last = parts[2].capitalize()
            else:
                last = parts[1].capitalize()
            if not last:
                last_first = full_name.split(',')
                if len(last_first) == 2:
                    last = last_first[0].capitalize()
                    first = last_first[1].strip().capitalize()
            if middle:
                return f"{first} {middle} {last}".strip()
            else:
                return f"{first} {last}".strip()
        else:
            last_first = full_name.split(',')
            if len(last_first) == 2:
                first = last_first[1].strip().capitalize()
                last = last_first[0].capitalize()
                return f"{first} {last}"
            return full_name

    def send_promotion_notification(self, matches: List[Dict], maradmin_title: str, maradmin_link: str):
        if not matches:
            return

        message_lines = [
            f"*MARADMIN Alert: New Matches Found in {maradmin_title}*",
            ""
        ]

        for match in matches:
            name = self.format_name(match['contact']['full_name'], match['matched_text'])
            mcc_code = match['matched_text'].split()[-1]
            command_name = "Unknown Command"
            if self.processor:
                command_name = self.processor.get_command_name_from_mcc(mcc_code)
            message_lines.append(f"• {name}  Command: {command_name}")

        message_lines.append("")
        message_lines.append(f"<{maradmin_link}|View MARADMIN>")
        message_lines.append("")
        message_lines.append("_This is an automated notification from the MARADMIN Alert System. Confirm important information by referenceing the MARADMIN_")

        payload = {
            "text": "\n".join(message_lines)
        }

        try:
            response = requests.post(self.webhook_url, json=payload)
            if response.status_code == 200:
                logging.info("Sent Slack notification successfully")
            else:
                logging.error(f"Failed to send Slack notification: {response.status_code} {response.text}")
        except Exception as e:
            logging.error(f"Exception sending Slack notification: {str(e)}")
