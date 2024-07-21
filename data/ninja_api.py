import requests

def format_event(event):
    if event.get('published', False):  # Only format the event if it's published
        return {
            "title": event['title'],
            "start": event['start'],
            "end": event['end'],
            "className": event['className'],
            "context": event['context']
        }
    return None


def get_events_by_category(category):
    url_events = f"https://geomapindex.com/api/events/category/{category}"
    response = requests.get(url_events)
    if response.status_code == 200:
        events_data = response.json()
        formatted_events = [format_event(event) for event in events_data]
        return formatted_events
    else:
        return f"Error: {response.status_code}, {response.text}"


if __name__ == "__main__":
    # Testing API
    print("Testing API")
    events_by_category = get_events_by_category("plotly")
    print(events_by_category)