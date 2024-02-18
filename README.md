# News sentiment crawler

This project is a small Python crawler for news sentiment

# Components

## API

This is a minimal REST API for data access. The plan is to eventually expose
this data publicly through this API.

## Crawler

This process crawls for the latest news articles reachable from the home pages of
German publications. These are currently [Zeit](https://zeit.de) and
[Spiegel](https://spiegel.de) but this is easily extensible to more news
sources.

# How to run it

Currently you can run this locally by cloning the repository and running `docker compose up`

# Future work

This is by no means complete, coming soon:

- [ ] Set up a github action to deploy this to `api.christof-schramm.net`
- [ ] Add a TS frontend on [christof-schramm.net](https://christof-schramm.net)
- [ ] Add some more news platforms
