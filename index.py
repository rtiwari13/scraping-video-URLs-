import requests
from bs4 import BeautifulSoup
import re
from collections import Counter

url = 'https://www.youtube.com/c/tseries/videos'
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    video_elements = soup.find_all('a', {'id': 'video-title'})
    start_date = 'August 8, 2023'
    end_date = 'May 22, 2023'

    unique_dates_and_urls = {}
    video_ids = []
    for video_element in video_elements:
        video_url = 'https://www.youtube.com' + video_element['href']
        video_description = video_element.find_next('div', {'id': 'description'}).text
        match = re.search(r'Published on (\w+ \d+, \d+)', video_description)
        if match:
            upload_date = match.group(1)
            if start_date <= upload_date <= end_date:
                video_id_match = re.search(r'v=([A-Za-z0-9_-]+)', video_url)
                if video_id_match:
                    video_id = video_id_match.group(1)
                    video_ids.append(video_id)
                    unique_dates_and_urls[upload_date] = video_url

    for upload_date, video_url in unique_dates_and_urls.items():
        print(f'Upload Date: {upload_date}')
        print(f'Video URL: {video_url}')
    video_id_string = ''.join(video_ids)
    video_id_string = video_id_string.lower() 
    character_counts = Counter(video_id_string)

    if character_counts:
        most_common_character, count = character_counts.most_common(1)[0]
      
        print(f'Most Repeated Character in Video IDs: {most_common_character} ({count} times)')
    else:
        print("No Video IDs found to count.")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


