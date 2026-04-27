import requests
import logging
from abc import ABC, abstractmethod

class NotificationSender(ABC):
    @abstractmethod
    def send_notification(self, message: str):
        pass

class DiscordNotificationSender(NotificationSender):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send_notification(self, message: str):
        try:
            payload = {
                "content": message,
                "embeds": [
                    {
                        "title": "Missing Episodes Found!",
                        "description": message,
                        "color": 16711680,  # Red color
                        "timestamp": ""
                    }
                ]
            }
            
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            
            logging.info(f"Discord notification sent successfully: {message}")
        except Exception as e:
            logging.error(f"Error sending Discord notification: {e}")

class TelegramNotificationSender(NotificationSender):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send_notification(self, message: str):
        try:
            # Extract chat_id and bot_token from webhook_url
            # Expected format: https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}
            # For now, we'll assume the full URL is the send_message endpoint
            params = {
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(self.webhook_url, data=params)
            response.raise_for_status()
            
            logging.info(f"Telegram notification sent successfully: {message}")
        except Exception as e:
            logging.error(f"Error sending Telegram notification: {e}")

def NotificationSenderFactory(notification_type: str, webhook_url: str):
    """Factory method to create appropriate notification sender"""
    if notification_type.lower() == 'discord':
        return DiscordNotificationSender(webhook_url)
    elif notification_type.lower() == 'telegram':
        return TelegramNotificationSender(webhook_url)
    else:
        raise ValueError(f"Unsupported notification type: {notification_type}")