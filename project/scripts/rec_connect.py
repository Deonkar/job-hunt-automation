# Record one sent LinkedIn connection request (linkedin-connect workflow).
# usage: rec_connect.py company name url title kind country
import datetime
import json
import os
import sys

c, n, u, t, k, co = sys.argv[1:7]
STATE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "state")


def load(name, default):
    path = os.path.join(STATE, name)
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf8") as f:
        return json.load(f)


def save(name, data):
    os.makedirs(STATE, exist_ok=True)
    with open(os.path.join(STATE, name), "w", encoding="utf8") as f:
        json.dump(data, f, indent=1, ensure_ascii=False)


now = datetime.datetime.now().astimezone()
s = load("linkedin-connect.json", {"companies": {}})
e = s["companies"].setdefault(c, {"status": "open", "note": "", "people": []})
e["people"].append({"name": n, "profile_url": u, "title": t, "kind": k, "office_country": co,
                    "sent_at": now.isoformat(timespec="seconds")})
if len(e["people"]) >= 5:
    e["status"] = "full"
save("linkedin-connect.json", s)
o = load("outreach.json", {"people": [], "invites": {}})
d = now.date().isoformat()
o["invites"][d] = o["invites"].get(d, 0) + 1
save("outreach.json", o)
print(c, len(e["people"]), "today", o["invites"][d])
