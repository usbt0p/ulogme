import json
from pathlib import Path

# Paths
ROOT = Path(__file__).parent.resolve()
LOGS_DIR = ROOT / 'logs'
RENDER_DIR = ROOT / 'render'

def load_events(filepath):
    """
    Reads a file with "timestamp string" lines. Returns list of dicts.
    """
    events = []
    if not filepath.exists():
        return events

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                # Split at first space only
                parts = line.split(' ', 1)
                if len(parts) < 2: continue
                
                events.append({
                    't': int(parts[0]), 
                    's': parts[1].strip()
                })
    except Exception as e:
        print(f"Error reading {filepath.name}: {e}")
        
    return events

def get_mtime(filepath):
    """Returns modification time or 0 if missing."""
    return int(filepath.stat().st_mtime) if filepath.exists() else 0

def update_events():
    """
    Scans log files, groups by day, and writes JSONs if source files changed.
    """
    # Ensure output dir exists
    RENDER_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Find all unique timestamps from filenames (e.g., window_12345.txt)
    # We look at all relevant log files to build the master time list
    all_files = list(LOGS_DIR.glob('*_*.txt'))
    timestamps = set()
    
    for p in all_files:
        if p.name.startswith(('keyfreq_', 'window_', 'notes_', 'blog_')):
            try:
                # Extract number between last underscore and .txt
                ts_str = p.stem.split('_')[-1]
                timestamps.add(int(ts_str))
            except ValueError:
                continue

    sorted_ts = sorted(list(timestamps))
    out_list = []

    for t0 in sorted_ts:
        t1 = t0 + 86400 # 24 hrs later
        fname_out = f'events_{t0}.json'
        out_list.append({'t0': t0, 't1': t1, 'fname': fname_out})

        # Define file paths
        f_json = RENDER_DIR / fname_out
        f_win = LOGS_DIR / f'window_{t0}.txt'
        f_key = LOGS_DIR / f'keyfreq_{t0}.txt'
        f_note = LOGS_DIR / f'notes_{t0}.txt'
        f_blog = LOGS_DIR / f'blog_{t0}.txt'

        # Check if we need to regenerate (Cache invalidation)
        do_write = False
        if not f_json.exists():
            do_write = True
        else:
            t_json = get_mtime(f_json)
            # If any source file is newer than the JSON, regenerate
            if any(get_mtime(f) > t_json for f in [f_win, f_key, f_note, f_blog]):
                print(f"Source changed, updating {fname_out}...")
                do_write = True

        if do_write:
            # Load Data
            e_win = load_events(f_win)
            e_key = load_events(f_key)
            e_note = load_events(f_note)
            
            # Convert keyfreq 's' to int
            for k in e_key:
                try:
                    k['s'] = int(k['s'])
                except ValueError: 
                    k['s'] = 0

            # Load Blog
            blog_content = ""
            if f_blog.exists():
                try:
                    with open(f_blog, 'r', encoding='utf-8') as f:
                        blog_content = f.read()
                except Exception as e:
                    print(f"Error reading blog {t0}: {e}")

            # Dump JSON
            data = {
                'window_events': e_win,
                'keyfreq_events': e_key,
                'notes_events': e_note,
                'blog': blog_content
            }
            
            with open(f_json, 'w', encoding='utf-8') as f:
                json.dump(data, f)
            print(f"Wrote {f_json.name}")

    # Write the master list
    f_export = RENDER_DIR / 'export_list.json'
    with open(f_export, 'w', encoding='utf-8') as f:
        json.dump(out_list, f)
    print(f"Wrote {f_export.name}")

if __name__ == '__main__':
    update_events()