import subprocess
import time
import re

BATTERY_LIMIT = 25
CHECK_INTERVAL = 15


def get_battery_status():
    result = subprocess.run(
        ["pmset", "-g", "batt"],
        capture_output=True,
        text=True,
        check=True
    )

    output = result.stdout

    percentage_match = re.search(r"(\d+)%", output)

    if percentage_match is None:
        return None, False

    percentage = int(percentage_match.group(1))
    is_charging = "AC Power" in output

    return percentage, is_charging


def send_alert():
    message = (
        "Your MacBook battery has reached 80%. "
        "You can unplug your charger now."
    )

    subprocess.run([
        "osascript",
        "-e",
        f'display notification "{message}" '
        'with title "Battery Alarm" '
        'sound name "Glass"'
    ])

    print("🔔 Battery reached 80%! Unplug your charger.")

    subprocess.run([
        "afplay",
        "/System/Library/Sounds/Glass.aiff"
    ])


def main():
    print("================================")
    print("   MACBOOK BATTERY ALARM")
    print("================================")
    print(f"Alert threshold: {BATTERY_LIMIT}%")
    print(f"Checking every {CHECK_INTERVAL} seconds.")
    print("Press Ctrl+C to stop.\n")

    already_alerted = False

    try:
        while True:
            percentage, is_charging = get_battery_status()

            if percentage is None:
                print("Unable to read battery status.")
                time.sleep(CHECK_INTERVAL)
                continue

            print(
                f"Battery: {percentage}% | "
                f"Charging: {'Yes' if is_charging else 'No'}"
            )

            if not is_charging:
                already_alerted = False

            elif percentage >= BATTERY_LIMIT and not already_alerted:
                send_alert()
                already_alerted = True

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\nBattery Alarm stopped.")


if __name__ == "__main__":
    main()
