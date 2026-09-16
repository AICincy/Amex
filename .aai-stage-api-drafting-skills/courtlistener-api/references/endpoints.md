# CourtListener endpoint cache

Fetched 2026-09-13 from https://www.courtlistener.com/help/api/rest/ and https://www.courtlistener.com/help/api/rest/search/.
Re-fetch those pages before changing shapes.

Base URL: `https://www.courtlistener.com/api/rest/v4`

Auth header when a token exists: `Authorization: Token <token>`

Unauthenticated calls are allowed for experimentation. Authenticate before heavy use.

## Search

`GET /search/`

| Param | Meaning |
| --- | --- |
| q | Query string, same operators as the website |
| type | o opinions, r RECAP dockets, rd RECAP documents, d PACER dockets, p judges, oa oral arguments |
| court | Court id filter when the live docs list one |
| filed_after / filed_before | Date bounds when supported |

## Common GET paths

| Path | Use |
| --- | --- |
| /search/ | Full-text search |
| /dockets/ | PACER/RECAP docket objects |
| /docket-entries/ | Entries on a docket |
| /recap-documents/ | Filing documents |
| /clusters/ | Opinion clusters |
| /opinions/ | Opinion text objects |
| /courts/ | Court directory |
| /people/ | Judges |
| /citation-lookup/ | Citation resolver |

## Coverage bound

CourtListener holds opinions plus a large RECAP slice of PACER. It does not replace Enformion Criminal Search V2, a county clerk, or NCIC. Ohio municipal and county criminal often will not hit.

## County fallback

Use `exa-firecrawl` on the official clerk or reporter site for that court. Do not scrape a people-search aggregator as a court source.
