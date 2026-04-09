# World Bank Projects API (Climate Query)

World Bank Projects API dataset filtered with `qterm=climate`, used to discover and profile climate-related projects and financing records.

## Why we use it
- **Project discovery** - identifies climate-related projects from World Bank metadata
- **Finance context** - captures commitment and disbursement fields where available
- **Geographic coverage** - supports country-level analysis and cross-country comparisons
- **Pipeline candidate** - source for future structured ingestion from API

## Current approved release
**v2**

## Main sources
- [World Bank Projects API](https://search.worldbank.org/api/v2/projects)
- [Climate-filtered query used for review](https://search.worldbank.org/api/v2/projects?format=json&rows=50&os=0&qterm=climate)
