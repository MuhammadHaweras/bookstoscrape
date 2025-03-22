# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Process the 'availability' field
        if 'availability' in adapter and adapter['availability']:
            # Extract the numeric value and text (e.g., "22 available") using regex
            match = re.search(r'\((\d+ available)\)', adapter['availability'])
            if match:
                adapter['availability'] = match.group(1)  # Set the cleaned value

        # Process the 'stars' field
        if 'stars' in adapter and adapter['stars']:
            # Extract the rating word (e.g., "three") and convert it to a digit
            match = re.search(r'star-rating (\w+)', adapter['stars'], re.IGNORECASE)
            if match:
                stars_map = {
                    'one': 1,
                    'two': 2,
                    'three': 3,
                    'four': 4,
                    'five': 5
                }
                rating_word = match.group(1).lower()  # Convert to lowercase for mapping
                adapter['stars'] = stars_map.get(rating_word, 0)  # Default to 0 if not found
        
        return item