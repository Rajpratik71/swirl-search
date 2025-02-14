<h1>&nbsp; Swirl Metasearch 2.5<img alt='Swirl Metasearch Logo' src='https://raw.githubusercontent.com/wiki/swirlai/swirl-search/images/swirl-logo-only-blue.png' width=38 align=left /></h1>

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg?color=blue&logoColor=blue&style=flat)](https://opensource.org/license/apache-2-0/)
[![GitHub Release](https://img.shields.io/github/v/release/swirlai/swirl-search?style=flat&label=Release)](https://github.com/swirlai/swirl-search/releases)
[![Docker Build](https://github.com/swirlai/swirl-search/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/swirlai/swirl-search/actions/workflows/docker-image.yml)
[![Tests](https://github.com/swirlai/swirl-search/actions/workflows/smoke-tests.yml/badge.svg?branch=main)](https://github.com/swirlai/swirl-search/actions/workflows/smoke-tests.yml)
[![Built with spaCy](https://img.shields.io/badge/Built%20with-spaCy-09a3d5.svg?color=blue)](https://spacy.io)
[![Slack](https://img.shields.io/badge/Slack--channel-gray?logo=slack&logoColor=black&style=flat)](https://join.slack.com/t/swirlmetasearch/shared_invite/zt-1qk7q02eo-kpqFAbiZJGOdqgYVvR1sfw)
[![Newsletter](https://img.shields.io/badge/Newsletter-gray?logo=revue&logoColor=black&style=flat)](https://groups.google.com/g/swirl-announce)
[![Twitter](https://img.shields.io/twitter/follow/SWIRL_SEARCH?label=Follow%20%40SWIRL_SEARCH&color=gray&logoColor=black&style=flat)](https://twitter.com/SWIRL_SEARCH)

Swirl Metasearch adapts and distributes user queries to anything with a search API - search engines, databases, noSQL engines, cloud/SaaS services, etc. - and uses AI ([Large Language Models](https://techcrunch.com/2022/04/28/the-emerging-types-of-language-models-and-why-they-matter/)) to re-rank the unified results *without* extracting or indexing *anything*. It includes OAuth2 support for Microsoft 365 alongside integration with enterprise services such as Atlassian Jira and Confluence, JetBrains YouTrack, HubSpot and more.

Using the Galaxy UI, knowledge workers can systematically review the best results from all configured services including Apache [Solr](https://solr.apache.org/), [ChatGPT](https://openai.com/blog/chatgpt/), [Elastic](https://www.elastic.co/cn/downloads/elasticsearch), [OpenSearch](https://opensearch.org/downloads.html), [PostgreSQL](https://www.postgresql.org/), [Google BigQuery](https://cloud.google.com/bigquery), plus generic HTTP/GET/POST with configurations for premium services like [Google's Programmable Search Engine](https://programmablesearchengine.google.com/about/), [Miro](https://miro.com/app/) and [Northern Light Research](https://northernlight.com/).

![Metasearch diagram](https://raw.githubusercontent.com/wiki/swirlai/swirl-search/images/swirl_arch_diagram.jpg)

Built on the Python/Django stack, Swirl is intended for use by anyone who wants to solve multi-silo search problems without moving, re-indexing or re-permissioning sensitive information.

<br/>

# Try Swirl Now In Docker

## Prerequisites

* To run Swirl in Docker, you must have the latest [Docker app](https://docs.docker.com/get-docker/) for MacOS, Linux, or Windows installed and running locally.

* Windows users must also install and configure either the WSL 2 or the Hyper-V backend, as outlined in the  [System Requirements for installing Docker Desktop on Windows](https://docs.docker.com/desktop/install/windows-install/#system-requirements).

## Start Swirl in Docker

:warning: Make sure the Docker app is running before proceeding!

* Download [https://raw.githubusercontent.com/swirlai/swirl-search/main/docker-compose.yaml](https://raw.githubusercontent.com/swirlai/swirl-search/main/docker-compose.yaml)

```
curl https://raw.githubusercontent.com/swirlai/swirl-search/main/docker-compose.yaml -o docker-compose.yaml
```

* In MacOS or Linux, run the following command from the Console:

```
docker-compose pull && docker-compose up
```

* In Windows, run the following command from PowerShell:

```
docker compose up
```

After a few minutes the following or similar should appear:

```
ssdtest-app-1  | Command successful!
ssdtest-app-1  | __S_W_I_R_L__2_._5____________________________________________________________
ssdtest-app-1  |
ssdtest-app-1  | Warning: logs directory does not exist, creating it
ssdtest-app-1  | Start: redis -> redis-server ./redis.conf ... Ok, pid: 28
ssdtest-app-1  | Start: celery-worker -> celery -A swirl_server worker --loglevel INFO ... Ok, pid: 34
ssdtest-app-1  | Start: celery-beats -> celery -A swirl_server beat --scheduler django_celery_beat.schedulers:DatabaseScheduler ... Ok, pid: 45
ssdtest-app-1  | Updating .swirl... Ok
ssdtest-app-1  |
ssdtest-app-1  |   PID TTY          TIME CMD
ssdtest-app-1  |    28 ?        00:00:00 redis-server
ssdtest-app-1  |    34 ?        00:00:02 celery
ssdtest-app-1  |    45 ?        00:00:02 celery
ssdtest-app-1  |
ssdtest-app-1  | Command successful!
ssdtest-app-1  | 2023-08-03 13:16:11,070 INFO     Starting server at tcp:port=8000:interface=0.0.0.0
ssdtest-app-1  | 2023-08-03 13:16:11,074 INFO     HTTP/2 support not enabled (install the http2 and tls Twisted extras)
ssdtest-app-1  | 2023-08-03 13:16:11,075 INFO     Configuring endpoint tcp:port=8000:interface=0.0.0.0
ssdtest-app-1  | 2023-08-03 13:16:11,079 INFO     Listening on TCP address 0.0.0.0:8000
```

* Open this URL with a browser: <http://localhost:8000> (or <http://localhost:8000/galaxy>)

If the search page appears, click `Log Out` at the top, right. The Swirl login page will appear:

![Swirl Login](https://raw.githubusercontent.com/wiki/swirlai/swirl-search/images/swirl_login-galaxy_dark.png)

* Enter the username `admin` and password `password`, then click `Login`.

* Enter a search in the search box and press the `Search` button. Ranked results appear in just a few seconds:

![Swirl Results No M365](https://raw.githubusercontent.com/wiki/swirlai/swirl-search/images/swirl_results_no_m365-galaxy_dark.png)

* To view the raw JSON, open <http://localhost:8000/swirl/search/>

The most recent Search object will be displayed at the top. Click on the `result_url` link to view the full JSON Response.

## Notes

:warning: The Docker version of Swirl does *not* retain any data or configuration when shut down!

:key: Swirl includes three (3) Google Programmable Search Engines (PSEs) to get you up and running right away. The credentials for these are shared with the Swirl Community.

:key: Using Swirl with Microsoft 365 requires installation and approval by an authorized company Administrator. For more information, please review the [M365 Guide](4.-M365-Guide) or [contact us](mailto:hello@swirl.today).


### Want to install Swirl locally? Check out our [Quick Start Guide](https://github.com/swirlai/swirl-search/wiki/1.-Quick-Start) for details!

<br/>

# Try Swirl Cloud

### For information about Swirl as a managed service, please [contact us](mailto:hello@swirl.today)!

<br/>

# Download Swirl

| Version                     | Date                        | Notes |
| --------------------------- | --------------------------- | ----- |
| [Swirl Metasearch 2.5](https://github.com/swirlai/swirl-search/releases/tag/v2.5.0) | 08-03-2023 | [Release 2.5](https://github.com/swirlai/swirl-search/releases) |

<br/>

# Documentation Wiki

### [Home](https://github.com/swirlai/swirl-search/wiki) | [Quick Start](https://github.com/swirlai/swirl-search/wiki/1.-Quick-Start) | [User Guide](https://github.com/swirlai/swirl-search/wiki/2.-User-Guide) | [Admin Guide](https://github.com/swirlai/swirl-search/wiki/3.-Admin-Guide) | [M365 Guide](https://github.com/swirlai/swirl-search/wiki/4.-M365-Guide) | [Developer Guide](https://github.com/swirlai/swirl-search/wiki/5.-Developer-Guide) | [Developer Reference](https://github.com/swirlai/swirl-search/wiki/6.-Developer-Reference)

<br/>

# Key Features

* [Microsoft 365 integration and OAUTH2 support](https://github.com/swirlai/swirl-search/wiki/4.-M365-Guide)

* [SearchProvider configurations](https://github.com/swirlai/swirl-search/tree/main/SearchProviders) for all included Connectors. They can be [organized with the active, default and tags properties](https://github.com/swirlai/swirl-search/wiki/2.-User-Guide#organizing-searchproviders-with-active-default-and-tags).

* [Adaptation of the query for each provider](https://github.com/swirlai/swirl-search/wiki/2.-User-Guide#search-syntax) such as rewriting `NOT term` to `-term`, removing NOTted terms from providers that don't support NOT, and passing down the AND, + and OR operators.

* [Synchronous or asynchronous search federation](https://github.com/swirlai/swirl-search/wiki/5.-Developer-Guide#architecture) via [APIs](http://localhost:8000/swirl/swagger-ui/)

* [Optional subscribe feature](https://github.com/swirlai/swirl-search/wiki/5.-Developer-Guide#subscribe-to-a-search) to continuously monitor any search for new results

* Pipelining of [Processor](https://github.com/swirlai/swirl-search/wiki/5.-Developer-Guide#develop-new-processors) stages for real-time adaptation and transformation of queries, responses and results

* [Results stored](https://github.com/swirlai/swirl-search/wiki/6.-Developer-Reference#result-objects) in SQLite3 or PostgreSQL for post-processing, consumption and/or analytics

* Built-in [Query Transformation](https://github.com/swirlai/swirl-search/wiki/5.-Developer-Guide#using-query-transformations) support, including re-writing and replacement

* [Matching on word stems](https://github.com/swirlai/swirl-search/wiki/6.-Developer-Reference#cosinerelevancypostresultprocessor) and [handling of stopwords](https://github.com/swirlai/swirl-search/wiki/5.-Developer-Guide#configure-stopwords-language) via NLTK

* [Duplicate detection](https://github.com/swirlai/swirl-search/wiki/5.-Developer-Guide#detect-and-remove-duplicate-results) on field or by configurable Cosine Similarity threshold

* Re-ranking of unified results [using Cosine Vector Similarity](https://github.com/swirlai/swirl-search/wiki/6.-Developer-Reference#cosinerelevancypostresultprocessor) based on [spaCy](https://spacy.io/)'s large language model and [NLTK](https://www.nltk.org/)

* [Result mixers](https://github.com/swirlai/swirl-search/wiki/6.-Developer-Reference#mixers-1) order results by relevancy, date or round-robin (stack) format, with optional filtering of just new items in subscribe mode

* Page through all results requested, re-run, re-score and update searches using URLs provided with each result set

* [Sample data sets](https://github.com/swirlai/swirl-search/tree/main/Data) for use with SQLite3 and PostgreSQL

* [Optional spell correction](https://github.com/swirlai/swirl-search/wiki/5.-Developer-Guide#add-spelling-correction) using [TextBlob](https://textblob.readthedocs.io/en/dev/quickstart.html#spelling-correction)

* [Optional search/result expiration service](https://github.com/swirlai/swirl-search/wiki/3.-Admin-Guide#search-expiration-service) to limit storage use

* Easily extensible [Connector](https://github.com/swirlai/swirl-search/tree/main/swirl/connectors) and [Mixer](https://github.com/swirlai/swirl-search/tree/main/swirl/mixers) objects

<br/>

# Support

* [Join the Swirl Metasearch Community on Slack!](https://join.slack.com/t/swirlmetasearch/shared_invite/zt-1qk7q02eo-kpqFAbiZJGOdqgYVvR1sfw)

* Email: [support@swirl.today](mailto:support@swirl.today) with issues, requests, questions, etc. - we'd love to hear from you!

<br/>
