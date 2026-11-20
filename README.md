# Syrax Solutions website

Every head counted. Every day. Automated drone herd monitoring for Australian grazing properties.

This repository holds the Syrax marketing website: 13 public pages plus an internal site plan.

## Preview

The site in `docs/` is published with GitHub Pages. It is currently a **preview for partners**:
search engines are asked not to index it (`noindex` and `robots.txt`), and contact details are placeholders.

## Site structure

| Page | URL | Target search |
|---|---|---|
| Home | `/` | drone cattle counting Australia |
| Cattle counting | `/cattle-counting/` | drone cattle counting, automated head count |
| Water and feed | `/water-and-feed-monitoring/` | water trough monitoring, feed bunk monitoring |
| Fences and welfare | `/fence-and-welfare-checks/` | drone fence checks, livestock welfare monitoring |
| How it works | `/how-it-works/` | drone in a box farm |
| Who it's for | `/who-its-for/` | remote livestock monitoring, agistment stock check |
| About | `/about/` | Syrax Solutions |
| FAQ | `/faq/` | drone cattle monitoring questions |
| Contact | `/contact/` | drone cattle monitoring quote |
| Resources | `/resources/` | cattle monitoring guides |
| 3 articles | `/resources/...` | long-tail guides |
| Site plan (internal) | `/site-plan/` | not indexed |

## Built for search engines and AI assistants

- Plain HTML on every page, readable without JavaScript
- One `<h1>` per page, descriptive titles, meta descriptions, canonical URLs, Open Graph tags
- Schema.org structured data: Organization, WebSite, Service, Article, FAQPage, BreadcrumbList
- `sitemap.xml`, `robots.txt` (AI crawlers explicitly allowed once live) and `llms.txt`, a plain-language summary for AI assistants

## Folders

- `docs/`: the published static website
- `source/canvas/`: the design files (Claude Design canvas pages)
- `source/build/`: scripts that generate the pages and export the static site

## Rebuilding the site

```
cd source/build
python3 gen_site.py      # subpages
python3 build.py         # home page
node export.js ../../docs
```

Set the real domain and switch indexing on in `source/build/site.config.json`:

```
{ "siteUrl": "https://www.your-domain.com.au", "noindex": false, "published": "2026-11-20" }
```

## Before going live

- [ ] Replace `[YOUR EMAIL]` and `[YOUR PHONE]`
- [ ] Connect the contact form to an inbox or CRM
- [ ] Confirm product claims (drone licence handling, weather behaviour, power options, roadmap items)
- [ ] Replace AI-generated imagery with real photos from site
- [ ] Add a real customer quote
- [ ] Set the domain and `noindex: false`, then submit `sitemap.xml` in Google Search Console
