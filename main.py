import requests
import os
from decouple import config


API_URL = "https://fortnite-api.com/v2/stats/br/v2"
API_KEY = config('API_KEY')

def format_and_print_stats(stats):
    formatted_stats = ""
    for mode, data in stats.items():
        formatted_stats += f"{mode.capitalize()} Stats:\n"
        if data is None:
            formatted_stats += "No data available for this mode.\n"
        else:
            for stat_name, stat_value in data.items():
                if isinstance(stat_value, dict):
                    formatted_stats += f"{stat_name.capitalize()}:\n"
                    for key, value in stat_value.items():
                        formatted_stats += f"  {key.capitalize()}: {value}\n"
            formatted_stats += "\n"
    return formatted_stats

def export_to_txt(player_name, stats):
    file_name = f"{player_name}.txt"
    with open(file_name, 'w') as file:
        file.write(f"Fortnite Stats for {player_name}\n\n")
        file.write(stats)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    name = input("Enter your Fortnite account name: ")

    account_type = input("Enter your account type (epic/psn/xbl): ").lower()

    time_window = input("Enter the time window (season/lifetime): ").lower()

    image = input("Enter the platform for the generated image (all/keyboardMouse/gamepad/touch/none): ").lower()

    params = {
        "name": name,
        "accountType": account_type,
        "timeWindow": time_window,
        "image": image
    }

    headers = {
        "Authorization": API_KEY
    }

    response = requests.get(API_URL, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Fortnite BR Stats for", name)
        print("Account Type:", account_type)
        print("Time Window:", time_window)
        print("Image Platform:", image)
        print()
        stats = format_and_print_stats(data['data']['stats'])
        print(stats)
        
        export_choice = input("Do you want to export this information to a text file (y/n)?: ")
        if export_choice.lower() == 'y':
            export_to_txt(name, stats)
            print(f"Data exported to {name}.txt")
        
        input("Press any key to exit...")
    else:
        print(f"Error: {response.status_code} - Unable to fetch data")
        input("Press any key to exit...")

if __name__ == "__main__":
    main()

