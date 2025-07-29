import subprocess
import pandas as pd
import json

def get_wifi_profiles():
    # command : netsh wlan show profiles
    try:
        command = "netsh wlan show profiles"
        result = subprocess.run(
            # ["netsh", "wlan", "show", "profiles"],
            command,
            capture_output=True,
            text=True,
            shell=True,
            check=True
        )
        output = result.stdout
        return output

    except subprocess.CalledProcessError as e:
        # print(f"Command failed with error: {e}")
        return None
    

def get_wifi_info(wifi_name):
    # command : netsh wlan show profile name="WiFiName" key=clear
    try:
        command = f'netsh wlan show profile name="{wifi_name}" key=clear'
        result = subprocess.run(
            # ["netsh", "wlan", "show", "profile",f'name="{wifi_name}"' , "key=clear"],
            command,
            capture_output=True,
            text=True,
            shell=True,
            check=True
        )
        output = result.stdout
        return output
    except subprocess.CalledProcessError as e:
        # print(f"Command failed with error: {e}")
        return None
    

def extract_wifi_password(lines):
    for line in lines.splitlines():
        line = line.strip()
        if line.startswith("Key Content"):
            return line.split(":", 1)[1].strip()
            # return list(line.split(":", 1))[1][1:]
    return None


def wifi_profiles():
    wifi = {}
    wifi_profiles_text = get_wifi_profiles()
    if not wifi_profiles_text:
        print("No Wi-Fi profiles found or command failed.")
        return wifi

    for line in wifi_profiles_text.splitlines():
        line = line.strip()
        if line.startswith("All User Profile"):
            wifi_name = line.split(":", 1)[1].strip()
            data = get_wifi_info(wifi_name)
            if data:
                password = extract_wifi_password(data)
                wifi[wifi_name] = password if password else None
    return wifi


def display_wifi_table(wifi_dict):
    df = pd.DataFrame([
        {"SSID": ssid, "Password": pwd if pwd else "(Open/Not Found)"}
        for ssid, pwd in wifi_dict.items()
    ])
    
    print(df.to_string(index=False))


def save_wifi_to_json(wifi_dict, filename="wifi_passwords.json"):
    try:
        with open (filename, "w", encoding="utf-8") as f:
            json.dump(wifi_dict, f, ensure_ascii=False, indent=4)
        print(f"Wi-Fi data saved to {filename}")
    except Exception as e:
        print(f"Failed to save JSON: {e}")


if __name__ == "__main__":
    wifi = wifi_profiles()
    display_wifi_table(wifi)
    save_wifi_to_json(wifi)

