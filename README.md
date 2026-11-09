# Equinox Club Finder

Type in your address and age, and the page ranks every Equinox club in your city by how well it fits you. It covers all 123 Equinox locations listed on equinox.com, across the US, Toronto, Vancouver and London.

Live site: [camdenchin.github.io/Equinox](https://camdenchin.github.io/Equinox/)

## How the score works

Each club gets up to three parts. Click **Priorities** to set how much each one matters, from Off to Max.

| Part | What it measures | Source |
| --- | --- | --- |
| Quality | Google rating, pulled toward the average of all clubs when a club has few reviews, in standard deviations | Google Maps, Nov 2026 |
| Walk | Straight-line distance × 1.25 for the street grid, at 3 mph; 10 minutes costs 1 point. Off until you enter an address | Computed from your address |
| Crowd age | Gap between your age and the population-weighted median age of residents within about a quarter mile of the club; 10 years costs 1 point. US clubs only | Census ACS 2024 5-year (via Census Reporter) |

The match score shows each club relative to your best fit, which is always 100.

When you pick an address, the page switches to the city of your nearest club and turns walking on. Address suggestions come from [Photon](https://photon.komoot.io), a free OpenStreetMap search service. Your text is sent only for that lookup and isn't stored. The map uses [Leaflet](https://leafletjs.com) with Esri's dark gray tiles. Neither service needs a key.

## The data

`clubs.tsv` lists every club with its coordinates, Google rating, review count, neighborhood median age and equinox.com page. The same data is embedded in `index.html` as the `RAW` array; update both when ratings change.

Clubs with no Google rating yet (newly opened locations) are scored at the overall average.

## Analysis scripts

`analysis/` has the Python behind the original downtown Manhattan write-up: regressions of rating against opening year, recovery amenities and distance, plus a Google Popular Times summary. Run them with `pip install numpy scipy`, then `python analysis/analysis.py`.

## Limits

Residents aren't members, Google ratings mix gym quality with billing and front-desk complaints, and walking time is a poor guide in cities where people drive. This is an independent project and isn't affiliated with Equinox.
