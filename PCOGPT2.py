import requests
import json
from datetime import datetime
from collections import defaultdict

# Replace with your Planning Center API credentials
APP_ID = #"Enter APP ID"
APP_SECRET = #"Enter APP Secret"
BASE_URL = "https://api.planningcenteronline.com/services/v2"

# Function to authenticate and fetch data from Planning Center
def get_planning_center_data(endpoint):
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        auth=(APP_ID, APP_SECRET)
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Fetch data for today's second service
def fetch_today_service_data():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Fetching data for today's second service: {today}")

    service_type_id = #"Enter service_type_id"
    plans_endpoint = f"/service_types/{service_type_id}/plans?filter=future&order=sort_date"
    plans_data = get_planning_center_data(plans_endpoint)

    if not plans_data or len(plans_data['data']) == 0:
        print("No upcoming plans found.")
        return None

    # Find the first plan matching today's date or the next available plan
    for plan in plans_data['data']:
        plan_date = datetime.strptime(plan['attributes']['sort_date'], "%Y-%m-%dT%H:%M:%SZ").date()
        if plan_date >= datetime.now().date():  # Look for today's or the next plan
            return plan['id'], plan

    print("No plans found for today or future dates.")
    return None
    # Update Service_type_id in URL
def fetch_songs_and_people(plan_id):
    songs_endpoint = f"/service_types/#Enter service_type_id#/plans/{plan_id}/items"
    people_endpoint = f"/service_types/#Enter service_type_id#/plans/{plan_id}/team_members"

    # Fetch songs
    songs_data = get_planning_center_data(songs_endpoint)
    songs = []
    if songs_data:
        for item in songs_data['data']:
            if item['type'] == "Item" and "title" in item['attributes']:
                song_title = item['attributes']['title']
                
                # Safely fetch song details for additional metadata
                song_id = None
                if 'song' in item['relationships'] and item['relationships']['song']['data'] is not None:
                    song_id = item['relationships']['song']['data']['id']

                if song_id:
                    song_details_endpoint = f"/songs/{song_id}"
                    song_details = get_planning_center_data(song_details_endpoint)

                    # Extract writer credits and copyright information
                    writer_credits = song_details['data']['attributes'].get('author', "N/A")
                    copyright_notice = song_details['data']['attributes'].get('copyright', "N/A")
                else:
                    writer_credits = "N/A"
                    copyright_notice = "N/A"

                songs.append({
                    "title": song_title,
                    "sequence": item['attributes'].get('sequence', None),
                    "length": item['attributes'].get('length', None),
                    "description": item['attributes'].get('description', None),
                    "ccli_number": item['attributes'].get('ccli_number', "N/A"),
                    "writer_credits": writer_credits,
                    "copyright_notice": copyright_notice,
                })
    
    # Fetch people and filter by team
    people_data = get_planning_center_data(people_endpoint)
    teams = defaultdict(list)  # Dictionary to group people by team
    if people_data:
        for person in people_data['data']:
            # Fetch team name from relationships
            team_id = person['relationships']['team']['data']['id']
            team_endpoint = f"/service_types/1048874/teams/{team_id}"
            team_data = get_planning_center_data(team_endpoint)
            team_name = team_data['data']['attributes']['name']

            if team_name in ["Audio/Visual", "Speakers", "Music"]:
                teams[team_name].append({
                    "name": person['attributes']['name'],
                    "position": person['attributes']['team_position_name'],
                })

    # Sort teams alphabetically and people within teams by position
    sorted_teams = {
        team: sorted(members, key=lambda x: x['position'])
        for team, members in sorted(teams.items())
    }

    return songs, sorted_teams


# Main function
def main():
    plan_data = fetch_today_service_data()
    if not plan_data:
        return

    plan_id, plan_details = plan_data
    songs, people = fetch_songs_and_people(plan_id)

    # Prepare output
    output = {
        "service_date": plan_details['attributes']['sort_date'],
        "songs": songs,
        "people": people
    }

    # Save to JSON file
    with open("today_service_data.json", "w") as file:
        json.dump(output, file, indent=4)

    print("Today's service data saved to 'today_service_data.json'.")

if __name__ == "__main__":
    main()
