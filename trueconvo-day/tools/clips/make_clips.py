#!/usr/bin/env python3
"""Make a few atmosphere clips for the True Convo story site through fal.ai.

This is a one-off helper for the website. It is NOT how True Convo itself will
make media; that belongs in the planned portable capability layer, where paid
generation is always optional (own key, local model, or upload).

Safety rails:
  * Dry run by default: prints the shots and the estimated cost, spends nothing.
  * Refuses to run while the price in shots.json is missing.
  * Refuses any run whose estimate, plus what this list already spent, is over cap_usd.
  * Every request, its cost estimate and its result go into log.jsonl.

Usage:
  python3 make_clips.py                 # dry run
  python3 make_clips.py --run test      # make one named shot
  python3 make_clips.py --run all       # make every shot not yet made
The key is read from the FAL_KEY environment variable and never printed.
"""
import json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "shots.json"
LOG = HERE / "log.jsonl"
OUT = HERE.parent.parent / "media" / "raw"
QUEUE = "https://queue.fal.run/"


def load_log():
    if not LOG.exists():
        return []
    return [json.loads(l) for l in LOG.read_text().splitlines() if l.strip()]


def log(entry):
    entry["at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def call(url, key, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    req.add_header("Authorization", f"Key {key}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def make(shot, cfg, key):
    endpoint = cfg["model"]["endpoint"]
    prompt = f'{shot["prompt"]} {cfg["style"]}'
    job = call(QUEUE + endpoint, key, {"prompt": prompt})
    log({"shot": shot["id"], "event": "submitted", "endpoint": endpoint,
         "prompt": prompt, "estimate_usd": cfg["model"]["price_usd_per_clip"],
         "request_id": job.get("request_id")})
    status_url, result_url = job["status_url"], job["response_url"]
    for _ in range(180):  # up to about 15 minutes
        time.sleep(5)
        st = call(status_url, key)
        if st.get("status") == "COMPLETED":
            break
        if st.get("status") not in ("IN_QUEUE", "IN_PROGRESS"):
            log({"shot": shot["id"], "event": "failed", "status": st})
            raise SystemExit(f'{shot["id"]}: fal reported {st.get("status")}')
    else:
        log({"shot": shot["id"], "event": "timeout"})
        raise SystemExit(f'{shot["id"]}: still not done after 15 minutes')
    res = call(result_url, key)
    url = res["video"]["url"]
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / f'{shot["id"]}.mp4'
    urllib.request.urlretrieve(url, dest)
    log({"shot": shot["id"], "event": "done", "file": str(dest.relative_to(HERE.parent.parent)),
         "spent_usd": cfg["model"]["price_usd_per_clip"], "seed": res.get("seed")})
    print(f'{shot["id"]}: saved {dest}')


def main():
    cfg = json.loads(SHOTS.read_text())
    entries = load_log()
    done = {e["shot"] for e in entries if e.get("event") == "done"}
    spent = sum(e.get("spent_usd") or 0 for e in entries if e.get("event") == "done")
    price = cfg["model"]["price_usd_per_clip"]
    cap = cfg["cap_usd"]

    which = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--run" else None
    if which == "all":
        todo = [s for s in cfg["shots"] if s["id"] not in done]
    elif which:
        todo = [s for s in cfg["shots"] if s["id"] == which]
        if not todo:
            raise SystemExit(f"No shot called {which!r}")
    else:
        todo = [s for s in cfg["shots"] if s["id"] not in done]

    est = (price or 0) * len(todo)
    print(f'Model: {cfg["model"]["endpoint"]}')
    print(f'Price per clip: {"NOT SET" if price is None else f"${price:.2f}"}')
    print(f"Already spent on this list: ${spent:.2f} of ${cap:.2f} cap")
    for s in todo:
        print(f'  - {s["id"]}: {s["use"]}')
    print(f"Estimate for these {len(todo)}: ${est:.2f}")

    if not which:
        print("Dry run. Nothing was sent.")
        return
    if price is None:
        raise SystemExit("Refusing: set price_usd_per_clip in shots.json from fal's model page first.")
    if spent + est > cap:
        raise SystemExit(f"Refusing: ${spent:.2f} spent + ${est:.2f} would pass the ${cap:.2f} cap.")
    key = os.environ.get("FAL_KEY")
    if not key:
        raise SystemExit("Refusing: FAL_KEY is not set in this environment.")
    for s in todo:
        make(s, cfg, key)


if __name__ == "__main__":
    main()
