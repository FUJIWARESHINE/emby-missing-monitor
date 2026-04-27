import json
import time
import logging
from datetime import datetime
from emby_api import EmbyAPI
from notification_sender import NotificationSender

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Config file not found. Please create config.json")
        return None

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()
    logging.info("Starting Emby Missing Episodes Monitor...")
    
    config = load_config()
    if not config:
        return
    
    emby = EmbyAPI(config['emby_url'], config['api_key'])
    notifier = NotificationSender(config['webhook_url'], config['notification_type'])
    
    while True:
        try:
            logging.info("Checking for missing episodes...")
            
            # Get all TV libraries
            libraries = emby.get_tv_libraries()
            
            for library in libraries:
                logging.info(f"Scanning library: {library}")
                
                # Get missing episodes
                missing_episodes = emby.get_missing_episodes(library)
                
                if missing_episodes:
                    logging.info(f"Found {len(missing_episodes)} missing episodes in {library}")
                    
                    # Send notification
                    message = f"Found {len(missing_episodes)} missing episodes in {library}"
                    notifier.send_notification(message)
                else:
                    logging.info(f"No missing episodes found in {library}")
        
        except Exception as e:
            logging.error(f"Error during scan: {e}")
        
        # Wait before next check
        logging.info(f"Waiting {config['check_interval_minutes']} minutes until next check...")
        time.sleep(config['check_interval_minutes'] * 60)

if __name__ == "__main__":
    main()