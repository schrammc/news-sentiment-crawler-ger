# News sentiment crawler

This project is a small Python crawler for news sentiment.

# Components

## API

The API exposes scrapedsentiment data from German news sites. OpenAPI docs of
the API are hosted [here](http://api.christof-schramm.net/docs)

A minimal React frontend for this API is on my homepage [here](https://christof-schramm.net/showcase/news-sentiment).

## Crawler

This process crawls for the latest news articles reachable from the home pages of
German publications. These are currently [Zeit](https://zeit.de) and
[Spiegel](https://spiegel.de) but this is easily extensible to more news
sources.

# How to run it

Currently you can run this locally by cloning the repository and running `docker compose up`


# Future work

This is by no means complete, coming soon:

- [X] Set up a github action to deploy this to `api.christof-schramm.net`
- [X] Configure SSL on `api.christof-schramm.net`
- [X] Add a TS frontend on [christof-schramm.net](https://christof-schramm.net)
- [ ] Add some more news platforms
