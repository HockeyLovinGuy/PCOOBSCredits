import json

print("Begin JSONtoText")
# Load JSON data from file
with open('today_service_data.json', 'r') as file:
    data = json.load(file)

# Prepare output
output_lines = []

# Add 29 blank lines
output_lines.extend([""] * 29)

# Process people data
output_lines.append("CREDITS:\n")
for category, persons in data["people"].items():
    for person in persons:
        output_lines.append(f"{person['name']} - {person['position']}")
output_lines.append("\nSongs:\n")

# Process songs data
for song in data["songs"]:
    if song["writer_credits"] != "N/A" and song["copyright_notice"] != "N/A":
        output_lines.append(
            f"“{song['title']}” words & music by {song['writer_credits']}\n"
            f"© {song['copyright_notice']}\nCCLI License No. 703186\n"
        )

# Update Website and socials for footer
# Add footer
output_lines.append("\nFor more information, please visit {URL}\n")
output_lines.append("Follow us on social media for updates and more:\n")
output_lines.append("Facebook - https://www.facebook.com/{Social}/\n")
output_lines.append("Instagram - https://www.instagram.com/{Social}/\n")
output_lines.append("YouTube - https://www.youtube.com/{Social}")


# Save to text file
output_file = "service_output.txt"
with open(output_file, 'w') as file:
    file.write("\n".join(output_lines))

print(f"Output saved to {output_file}")
