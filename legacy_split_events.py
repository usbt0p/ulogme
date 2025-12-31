from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Configuration
ROOT = Path(__file__).parent.resolve()  # Get directory of this script
LOGS_DIR = ROOT / 'logs'
RENDER_DIR = ROOT / 'render'

def get_day_start_timestamp(ts: int) -> int:
    """
    Returns the unix timestamp of 7:00 AM for the day associated with the given timestamp.
    If the time is before 7:00 AM, it counts as the previous day (ulogme logic).
    """
    dt = datetime.fromtimestamp(ts)
    if dt.hour < 7:
        dt = dt - timedelta(days=1)
    
    # Create new datetime at 7 AM of that day
    day_start = datetime(dt.year, dt.month, dt.day, 7)
    return int(day_start.timestamp())

def parse_and_bucket_file(filepath: Path):
    """
    Reads a legacy ulogme file, parses lines, and groups them by their 
    7AM split timestamp.
    Returns: dict { day_timestamp: [ (event_ts, content_string) ] }
    """
    buckets = defaultdict(list)
    
    if not filepath.exists():
        print(f"Warning: {filepath.name} not found. Skipping.")
        return buckets

    print(f"Processing {filepath.name}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                
                # Split only once at the first space
                parts = line.split(' ', 1)
                if len(parts) < 2: continue
                
                try:
                    ts = int(parts[0])
                    content = parts[1]
                    
                    # Calculate which file this belongs to
                    bucket_ts = get_day_start_timestamp(ts)
                    buckets[bucket_ts].append((ts, content))
                except ValueError:
                    continue # Skip malformed lines
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

    return buckets

def write_split_logs(buckets, prefix):
    """
    Writes the bucketed data into separate files.
    """
    if not buckets:
        return

    # Ensure logs directory exists
    LOGS_DIR.mkdir(exist_ok=True)

    for bucket_ts, events in buckets.items():
        # Sort events by time within the day (good practice)
        events.sort(key=lambda x: x[0])
        
        filename = f"{prefix}_{bucket_ts}.txt"
        out_path = LOGS_DIR / filename
        
        try:
            with open(out_path, 'w', encoding='utf-8') as f:
                for ts, content in events:
                    f.write(f"{ts} {content}\n")
            print(f"  -> Wrote {filename} ({len(events)} events)")
        except Exception as e:
            print(f"Error writing {filename}: {e}")

def main():
    print("--- Starting Legacy Event Converter ---")

    # 1. Process Windows
    win_buckets = parse_and_bucket_file(LOGS_DIR / 'activewin.txt')
    write_split_logs(win_buckets, 'window')

    # 2. Process Keys
    key_buckets = parse_and_bucket_file(LOGS_DIR / 'keyfreq.txt')
    write_split_logs(key_buckets, 'keyfreq')

    # 3. Process Notes
    note_buckets = parse_and_bucket_file(LOGS_DIR / 'notes.txt')
    write_split_logs(note_buckets, 'notes')

    print("--- Conversion Complete ---")

if __name__ == "__main__":
    main()