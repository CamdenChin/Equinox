"""Equinox Lower Manhattan analysis — data collected Nov 8, 2026.
Ratings/review counts/coords: Google Places. Amenities & hours: equinox.com club pages.
Opening years: press coverage (see sources in writeup). Set HOME to your own coordinates.
"""
import json, math
import numpy as np
from scipy import stats

HOME = (40.7308, -73.9973)  # Washington Square Park; replace with your own lat/lng

# name, lat, lng, rating, reviews, year_opened, year_note, amenity_count, recovery_count, weekly_hours
clubs = [
    ("SoHo",             40.7240841, -73.9970289, 3.5, 185, 2006, "lease signed Aug 2005", 10, 1, 102.5),
    ("Bond Street",      40.7271457, -73.9947863, 4.0, 139, 2016, "", 13, 2, 102.5),
    ("Orchard Street",   40.7223554, -73.9879141, 3.6, 174, 2018, "", 14, 1, 110.5),
    ("Hudson Square",    40.7234536, -74.0064248, 4.4,  68, 2025, "opened 2025 (est.)", 10, 3, 103.5),
    ("Tribeca",          40.7141211, -74.0098516, 3.4, 114, 2003, "", 17, 3, 102.5),
    ("Printing House",   40.7298600, -74.0072895, 3.6, 229, 2011, "Equinox took over 2010-11", 14, 2, 102.5),
    ("Wall Street",      40.7075383, -74.0109028, 3.6, 144, 2000, "", 15, 4, 103.5),
    ("Brookfield Place", 40.7127358, -74.0149258, 3.8, 135, 2015, "", 17, 1, 105.5),
    ("Greenwich Avenue", 40.7375937, -74.0019133, 3.3, 223, 2004, "est. (built after theater closed 2000)", 15, 2, 112.5),
]
names = [c[0] for c in clubs]
lat = np.array([c[1] for c in clubs]); lng = np.array([c[2] for c in clubs])
rating = np.array([c[3] for c in clubs]); n_rev = np.array([c[4] for c in clubs])
year = np.array([c[5] for c in clubs]); amen = np.array([c[7] for c in clubs])
recov = np.array([c[8] for c in clubs]); hours = np.array([c[9] for c in clubs])

def haversine_mi(a, b):
    R = 3958.8
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = p2 - p1; dl = math.radians(b[1] - a[1])
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(h))

crow = np.array([haversine_mi(HOME, (la, lo)) for la, lo in zip(lat, lng)])
walk_mi = crow * 1.25              # Manhattan detour factor (grid + avenues)
walk_min = walk_mi / 3.0 * 60      # 3 mph walking pace

# Bayesian (shrunk) rating: pulls low-review clubs toward the group mean
m = np.average(rating, weights=n_rev); C = 100
bayes = (C*m + rating*n_rev) / (C + n_rev)

def ols(y, Xcols, labels):
    X = np.column_stack([np.ones(len(y))] + Xcols)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    n, k = X.shape; dof = n - k
    s2 = resid @ resid / dof
    cov = s2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov)); t = beta / se
    p = 2 * stats.t.sf(np.abs(t), dof)
    ss_tot = ((y - y.mean())**2).sum(); r2 = 1 - (resid @ resid)/ss_tot
    adj = 1 - (1-r2)*(n-1)/dof
    return {"labels": ["intercept"] + labels, "beta": beta.tolist(), "se": se.tolist(),
            "p": p.tolist(), "r2": r2, "adj_r2": adj, "n": n, "resid": resid.tolist(),
            "fitted": (X @ beta).tolist()}

out = {}
out["m1_year"] = ols(rating, [year], ["year_opened"])
out["m2_distance"] = ols(rating, [walk_min], ["walk_min"])
out["m3_year_recovery"] = ols(rating, [year, recov], ["year_opened", "recovery_amenities"])
out["m4_amenities"] = ols(rating, [amen], ["amenity_count"])
out["m5_reviews"] = ols(rating, [n_rev], ["review_count"])
# robustness: drop Hudson Square (newest, fewest reviews) and Greenwich (estimated year)
mask = np.array([nm not in ("Hudson Square",) for nm in names])
out["m1_no_hudson"] = ols(rating[mask], [year[mask]], ["year_opened"])
mask2 = np.array([nm != "Greenwich Avenue" for nm in names])
out["m1_no_greenwich"] = ols(rating[mask2], [year[mask2]], ["year_opened"])
r_s, p_s = stats.spearmanr(year, rating); out["spearman_year"] = (r_s, p_s)

# Personal score: quality minus commute penalty.
# Quality = z-score of shrunk rating; each extra 10 min of walking each way costs 0.5 SD.
z = (bayes - bayes.mean()) / bayes.std(ddof=0)
score = z - 0.05 * walk_min
order = np.argsort(-score)

rows = []
for i in order:
    rows.append({"club": names[i], "rating": rating[i], "reviews": int(n_rev[i]),
                 "bayes": round(float(bayes[i]), 2), "year": int(year[i]),
                 "walk_mi": round(float(walk_mi[i]), 2), "walk_min": round(float(walk_min[i])),
                 "amenities": int(amen[i]), "recovery": int(recov[i]), "hours": hours[i],
                 "resid_year_model": round(out["m1_year"]["resid"][i], 2),
                 "score": round(float(score[i]), 2)})
out["table"] = rows
out["group_mean_weighted"] = m

def fmt(mod, key):
    md = out[key]
    s = f"\n== {key} (n={md['n']}, R2={md['r2']:.3f}, adjR2={md['adj_r2']:.3f})\n"
    for l, b, se, p in zip(md["labels"], md["beta"], md["se"], md["p"]):
        s += f"  {l:22s} b={b:+.4f}  se={se:.4f}  p={p:.4f}\n"
    return s

for k in ["m1_year","m2_distance","m3_year_recovery","m4_amenities","m5_reviews","m1_no_hudson","m1_no_greenwich"]:
    print(fmt(None, k))
print("spearman year~rating", out["spearman_year"])
print("weighted mean rating", round(m,3))
print("\nRANKING")
for r in rows: print(r)

json.dump(out, open("results.json","w"), indent=1, default=float)
