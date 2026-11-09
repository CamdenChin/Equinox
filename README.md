# Downtown Equinox Finder

Type in your address and age, and the page ranks the nine Equinox clubs below 14th Street in Manhattan by how well each fits you.

Turn on GitHub Pages for this repo to get a live link (Settings → Pages → deploy from `main`). Opening `index.html` straight from your computer works too, but serve it through Pages for address search to be reliable.

## How the score works

Each club gets three parts, and you can weight each one with the sliders:

| Part | What it measures | Source |
| --- | --- | --- |
| Quality | Google rating, pulled toward the 3.62 group average when a club has few reviews, in standard deviations | Google Places, Nov 8, 2026 |
| Walk | Straight-line distance × 1.25 for the street grid, at 3 mph; 10 minutes costs 1 point | Computed from your address |
| Crowd age | Gap between your age and the median age of residents in the club's census tract; 10 years costs 1 point. Clubs with a big after-8pm crowd read slightly younger | Census ACS 2024 5-year (via Census Reporter), Google Maps Popular Times |

As you type an address, the page suggests matches using [Photon](https://photon.komoot.io), a free OpenStreetMap search service built for search-as-you-type. Your text is sent only for that lookup and isn't stored. The map uses [Leaflet](https://leafletjs.com) with Esri's dark gray street tiles, over an embedded NYC shoreline so it still draws if the tiles can't load. Neither service needs a key.

## The data

All club data lives in the `CLUBS` array near the bottom of `index.html`:

| Club | Rating | Reviews | Opened | Resident median age | After 8pm |
| --- | --- | --- | --- | --- | --- |
| Hudson Square | 4.4 | 68 | 2025 (est.) | 40.1 | 11% |
| Bond Street | 4.0 | 139 | 2016 | 39.5 | 9% |
| Brookfield Place | 3.8 | 135 | 2015 | 39.3 | 6% |
| Orchard Street | 3.6 | 174 | 2018 | 29.4 | 17% |
| Wall Street | 3.6 | 144 | 2000 | 31.4 | 10% |
| Printing House | 3.6 | 229 | 2011 | 36.2 | 6% |
| SoHo | 3.5 | 185 | 2006 | 36.2 | 7% |
| Tribeca | 3.4 | 114 | 2003 | 35.1 | 8% |
| Greenwich Avenue | 3.3 | 223 | 2004 (est.) | 36.4 | 15% |

To refresh it, update the numbers in `CLUBS`. Ratings drift as reviews come in.

## Analysis scripts

`analysis/` has the Python behind the write-up:

- `analysis.py` runs the regressions (rating vs. year opened, recovery amenities, distance) and the ranking. Set `HOME` to your own coordinates.
- `popular_times.py` summarizes the Google Popular Times data by hour.

Run them with `pip install numpy scipy`, then `python analysis/analysis.py`.

## Limits

Residents aren't members, Google ratings mix gym quality with billing and front-desk complaints, and nine clubs is a small sample. Use the ranking to pick two clubs to try, then visit both at the hour you'd actually go.
