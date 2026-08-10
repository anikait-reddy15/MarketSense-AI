import os
import json
from ddgs import DDGS

class TrendIngestionEngine:
    def __init__(self):
        """Initializes the keyless DuckDuckGo Search client."""
        self.client = DDGS()

    def fetch_web_trends(self, query, region="in-en", max_results=10):
        """
        Fetches live search results for a given consumer query.
        region="in-en" ensures the results are localized to India in English.
        """
        print(f"[INFO] Fetching top {max_results} web signals for: '{query}'...")
        scraped_data = []

        try:
            # Using the text() method to pull web and forum results
            results = self.client.text(
                query, 
                region=region, 
                safesearch="moderate", 
                max_results=max_results
            )
            
            for index, result in enumerate(results):
                post_data = {
                    "id": f"ddg_{index}",
                    "title": result.get('title', ''),
                    "url": result.get('href', ''),
                    "text": result.get('body', ''), # The snippet containing the consumer context
                    "source": "Web/DuckDuckGo"
                }
                scraped_data.append(post_data)
                
            print(f"[SUCCESS] Extracted {len(scraped_data)} data points for '{query}'.")
            return scraped_data
            
        except Exception as e:
            print(f"[ERROR] Failed to fetch data: {str(e)}")
            return []

    def save_to_json(self, data, filename="raw_trend_data.json"):
        """Saves the structured dictionary to the data/raw/ directory as JSON."""
        # Navigate to the root directory, then into data/raw/
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            
        print(f"[INFO] Data successfully saved to {filepath}")

if __name__ == "__main__":
    scraper = TrendIngestionEngine()
    
    # Example 1: Indian Skincare complaints and trends
    skincare_query = "Indian skincare sunscreen complaints sticky white cast"
    skincare_data = scraper.fetch_web_trends(skincare_query, max_results=15)
    scraper.save_to_json(skincare_data, "skincare_trends.json")
    
    # Example 2: Emerging ingredient trends in India
    ingredient_query = "ashwagandha matcha focus drink trends India"
    ingredient_data = scraper.fetch_web_trends(ingredient_query, max_results=10)
    scraper.save_to_json(ingredient_data, "ingredient_trends.json")