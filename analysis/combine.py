"""Combine the three factors into one score per club.

Score = quality - 0.1 * walk_min + k * youth, all in standard-deviation units.
quality and walk_min come from analysis.py (set HOME there to your address);
youth comes from popular_times.py. k sets how much a young crowd counts.
"""
import runpy, io, contextlib, os
import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    a = runpy.run_path(os.path.join(here, "analysis.py"))
    p = runpy.run_path(os.path.join(here, "popular_times.py"))
for f in ("results.json", "popular_times.json"):
    if os.path.exists(f): os.remove(f)

names = list(a["names"]); z = a["z"]; walk = a["walk_min"]
youth = np.array([p["out"][n]["youth_score"] for n in names])
for k in (0, 0.5, 1):
    s = z - 0.1 * walk + k * youth
    print(f"\nyouth weight k = {k}")
    for i in np.argsort(-s):
        print(f"  {names[i]:17s} quality {z[i]:+.2f}  walk {-0.1*walk[i]:+.2f}  youth {k*youth[i]:+.2f}  total {s[i]:+.2f}")
