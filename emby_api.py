import requests
import logging
from typing import List, Dict

class EmbyAPI:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'X-Emby-Token': api_key,
            'Content-Type': 'application/json'
        }
    
    def get_tv_libraries(self) -> List[str]:
        """Get list of TV show library names"""
        try:
            response = requests.get(
                f"{self.base_url}/Library/VirtualFolders",
                headers=self.headers
            )
            response.raise_for_status()
            
            libraries = []
            for folder in response.json():
                if folder.get('ContentType') == 'tvshows':
                    libraries.append(folder['Name'])
            
            return libraries
        except Exception as e:
            logging.error(f"Error getting TV libraries: {e}")
            return []
    
    def get_missing_episodes(self, library_name: str) -> List[Dict]:
        """Get missing episodes in specified library"""
        try:
            # Get items in library
            params = {
                'ParentId': self._get_library_id(library_name),
                'IncludeItemTypes': 'Series',
                'Recursive': 'true',
                'Fields': 'MissingEpisodesCount'
            }
            
            response = requests.get(
                f"{self.base_url}/Items",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            
            series_with_missing = []
            for item in response.json().get('Items', []):
                if item.get('MissingEpisodesCount', 0) > 0:
                    series_with_missing.append(item)
            
            return series_with_missing
        except Exception as e:
            logging.error(f"Error getting missing episodes: {e}")
            return []
    
    def _get_library_id(self, library_name: str) -> str:
        """Get library ID by name"""
        try:
            response = requests.get(
                f"{self.base_url}/Library/VirtualFolders",
                headers=self.headers
            )
            response.raise_for_status()
            
            for folder in response.json():
                if folder['Name'] == library_name:
                    return folder['ItemId']
            return None
        except Exception as e:
            logging.error(f"Error getting library ID: {e}")
            return None