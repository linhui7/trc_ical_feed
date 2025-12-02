import requests
from copy import deepcopy
from icalendar import Calendar, Event

# URLs for the 4 gym locations + their display names
FEEDS = [
    {
        "url": "https://app.rockgympro.com/ical/public/0d6c7fa257084fd3b9628ca1759d88eb",
        "prefix": "TRC Durham",
    },
    {
        "url": "https://app.rockgympro.com/ical/public/ff72f7c8859742ada90d47dfdf1bbb97",
        "prefix": "TRC Morrisville",
    },
    {
        "url": "https://app.rockgympro.com/ical/public/7fa510dd88f746378b4e0d79da753e70",
        "prefix": "TRC Raleigh",
    },
    {
        "url": "https://app.rockgympro.com/ical/public/8a61329b24414b9e9f5313d64661c0c8",
        "prefix": "TRC Salvage Yard",
    },
]

# Event titles we care about
TARGET_TITLES = {
    "Member Guest Hours",
    "Climbing Connections",
}

OUTPUT_FILE = "trc_filtered.ics"


def fetch_calendar(url: str) -> Calendar:
    """Download an .ics file from a URL and parse it into an icalendar.Calendar."""
    resp = requests.get(url)
    resp.raise_for_status()
    return Calendar.from_ical(resp.content)


def build_filtered_calendar() -> Calendar:
    """
    Fetch all source calendars, filter to target events,
    and return a new merged Calendar object with prefixed titles.
    """
    merged_cal = Calendar()
    merged_cal.add("prodid", "-//TRC Filtered Feed//lin-hui//EN")
    merged_cal.add("version", "2.0")
    merged_cal.add("X-WR-CALNAME", "TRC - Member Guest + Climbing Connections")

    total_events = 0
    kept_events = 0

    for feed in FEEDS:
        url = feed["url"]
        prefix = feed["prefix"]

        cal = fetch_calendar(url)
        print(f"Fetched calendar from {url} ({prefix})")

        for component in cal.walk():
            if component.name != "VEVENT":
                continue

            total_events += 1
            summary = str(component.get("summary"))

            if summary in TARGET_TITLES:
                # Make a copy so we don't mutate the original event
                new_event: Event = deepcopy(component)
                new_event["summary"] = f"{prefix} - {summary}"
                merged_cal.add_component(new_event)
                kept_events += 1

    print(f"Total events seen across all feeds: {total_events}")
    print(f"Events kept (matching target titles): {kept_events}")

    return merged_cal


def main():
    merged_cal = build_filtered_calendar()

    # Write to an .ics file
    with open(OUTPUT_FILE, "wb") as f:
        f.write(merged_cal.to_ical())

    print(f"Filtered calendar written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
