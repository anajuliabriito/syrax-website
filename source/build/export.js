// Exports the Design canvas pages (project/*.dc.html) to a plain static website
// with clean URLs, real <head> SEO tags, JSON-LD structured data, sitemap.xml,
// robots.txt and llms.txt. Usage: node export.js <outDir>
const fs = require('fs');
const path = require('path');

const SRC = '/home/claude/syrax/project';
const OUT = process.argv[2] || '/home/claude/syrax-website/docs';
const cfg = JSON.parse(fs.readFileSync('/home/claude/syrax/site.config.json', 'utf8'));
const SITE = cfg.siteUrl.replace(/\/$/, '');

const PAGES = {
  'Main.dc.html': '',
  'CattleCounting.dc.html': 'cattle-counting/',
  'WaterFeed.dc.html': 'water-and-feed-monitoring/',
  'FenceWelfare.dc.html': 'fence-and-welfare-checks/',
  'HowItWorks.dc.html': 'how-it-works/',
  'WhoItsFor.dc.html': 'who-its-for/',
  'About.dc.html': 'about/',
  'FAQ.dc.html': 'faq/',
  'Contact.dc.html': 'contact/',
  'Resources.dc.html': 'resources/',
  'ArticleMidMorning.dc.html': 'resources/mid-morning-cattle-counts/',
  'ArticleCountCost.dc.html': 'resources/drone-count-vs-mustering/',
  'ArticleDroneInABox.dc.html': 'resources/drone-in-a-box-cattle/',
  'SiteMap.dc.html': 'site-plan/',
};
const SERVICES = {
  'CattleCounting.dc.html': 'Drone cattle counting',
  'WaterFeed.dc.html': 'Drone water trough and feed bunk monitoring',
  'FenceWelfare.dc.html': 'Drone fence line and livestock welfare checks',
};
const ARTICLES = ['ArticleMidMorning.dc.html', 'ArticleCountCost.dc.html', 'ArticleDroneInABox.dc.html'];
const ASSETS = {
  '929aeba2faf7c9b2e31c98dcf9054ace': ['assets/syrax-logo-gold.png', '/home/claude/logo_gold@2x.png'],
  'e5b59bfd169bfeddc5064b3634f8f848': ['assets/syrax-workflow.mp4', '/home/claude/vid/syrax-workflow.mp4'],
  'd6ed1865dfdead58dafbed3bf7429c2e': ['assets/workflow-poster.jpg', '/home/claude/vid/poster.jpg'],
  'ff1b44b7cc7ff10c30dd25a26026ab94': ['assets/drone-dock-paddock.jpg', '/home/claude/vid/img_dock.jpg'],
  'd0bf85568f3e8bf6a923d6d9d3a5913d': ['assets/drone-launch-fence.jpg', '/home/claude/vid/img_launch.jpg'],
  '12b4d05099d015bf5d7e1dc8bd1517dd': ['assets/grazier-phone-alert.jpg', '/home/claude/vid/img_farmer.jpg'],
  'c0a15f989bab8aaf166c4b74388dd7e5': ['assets/cattle-detection-aerial.jpg', '/home/claude/vid/img_detect.jpg'],
  'b28f07d833468d60ed20c4549447ecef': ['assets/drone-flyover-cattle.jpg', '/home/claude/vid/img_flyover.jpg'],
  'b9c4bce3c610a699f6c180fdf9a07197': ['assets/syrax-icon.png', '/home/claude/vid/appicon.png'],
};

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const unesc = (s) => s.replace(/&#x27;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const strip = (s) => unesc(s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim());

function renderVals(code, propsJson) {
  class DCLogic { constructor() { this.props = {}; this.state = {}; } setState() {} forceUpdate() {} }
  const Component = new Function('DCLogic', code + '\nreturn Component;')(DCLogic);
  const c = new Component();
  const decl = JSON.parse(propsJson || '{}');
  for (const k of Object.keys(decl)) if (decl[k] && 'default' in decl[k]) c.props[k] = decl[k].default;
  return c.renderVals();
}
function resolve(p, scope) {
  return p.trim().split('.').reduce((o, k) => (o == null ? undefined : o[k]), scope);
}
function expand(html, scope) {
  let out = '';
  let i = 0;
  while (true) {
    const start = html.indexOf('<sc-for', i);
    if (start < 0) { out += html.slice(i); break; }
    out += html.slice(i, start);
    const tagEnd = html.indexOf('>', start);
    const tag = html.slice(start, tagEnd + 1);
    let depth = 1, j = tagEnd + 1;
    while (depth) {
      const o = html.indexOf('<sc-for', j), c = html.indexOf('</sc-for>', j);
      if (o >= 0 && o < c) { depth++; j = o + 7; } else { depth--; j = c + 9; }
    }
    const inner = html.slice(tagEnd + 1, j - 9);
    const list = resolve(tag.match(/list="\{\{([^}]+)\}\}"/)[1], scope) || [];
    const as = tag.match(/as="([^"]+)"/)[1];
    list.forEach((item, idx) => { out += expand(inner, { ...scope, [as]: item, $index: idx }); });
    i = j;
  }
  return out.replace(/\{\{\s*([^}]+?)\s*\}\}/g, (m, p) => { const v = resolve(p, scope); return v == null ? '' : esc(v); });
}
function rel(fromSlug, toSlug) {
  const depth = fromSlug.split('/').filter(Boolean).length;
  return ('../'.repeat(depth) + toSlug) || './';
}

const faqAll = [];
const sitemap = [];
const meta = {};
fs.mkdirSync(path.join(OUT, 'assets'), { recursive: true });
for (const [id, [dest, src]] of Object.entries(ASSETS)) fs.copyFileSync(src, path.join(OUT, dest));

for (const [file, slug] of Object.entries(PAGES)) {
  const src = fs.readFileSync(path.join(SRC, file), 'utf8');
  const title = unesc(src.match(/<title>([\s\S]*?)<\/title>/)[1]);
  const descM = src.match(/<meta name="description" content="([^"]*)"/);
  const desc = descM ? unesc(descM[1]) : '';
  const helmet = src.match(/<helmet>([\s\S]*?)<\/helmet>/)[1];
  let body = src.match(/<x-dc>([\s\S]*?)<\/x-dc>/)[1].replace(/<helmet>[\s\S]*?<\/helmet>/, '');
  const sm = src.match(/<script type="text\/x-dc" data-dc-script data-props='([^']*)'>([\s\S]*?)<\/script>/);
  const vals = renderVals(sm[2], sm[1]);
  body = expand(body, vals);
  body = body.replace(/\/_blob\/([0-9a-f]{32})/g, (m, id) => rel(slug, ASSETS[id][0]));
  body = body.replace(/href="([A-Za-z]+\.dc\.html)"/g, (m, f) => `href="${rel(slug, PAGES[f])}"`);
  // Wrap the home page content in <main> for structure (subpages already have it)
  const url = SITE + '/' + slug;
  const h1 = strip((body.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || ['', ''])[1]);
  meta[file] = { title, desc, url, slug, h1 };

  // ---------- structured data ----------
  const org = { '@type': 'Organization', '@id': SITE + '/#org', name: 'Syrax Solutions', url: SITE + '/',
    logo: SITE + '/assets/syrax-icon.png', description: 'Automated drone herd monitoring for Australian grazing properties: daily cattle counts, water, feed, fence and welfare checks.',
    areaServed: { '@type': 'Country', name: 'Australia' }, address: { '@type': 'PostalAddress', addressLocality: 'Sydney', addressRegion: 'NSW', addressCountry: 'AU' } };
  const graph = [org];
  if (file === 'Main.dc.html') graph.push({ '@type': 'WebSite', '@id': SITE + '/#website', url: SITE + '/', name: 'Syrax Solutions', publisher: { '@id': SITE + '/#org' } });
  if (SERVICES[file]) graph.push({ '@type': 'Service', name: SERVICES[file], serviceType: SERVICES[file], description: desc, provider: { '@id': SITE + '/#org' }, areaServed: { '@type': 'Country', name: 'Australia' }, url });
  if (ARTICLES.includes(file)) graph.push({ '@type': 'Article', headline: h1, description: desc, image: SITE + '/' + (body.match(/assets\/[a-z-]+\.jpg/) || ['assets/workflow-poster.jpg'])[0], datePublished: cfg.published, author: { '@id': SITE + '/#org' }, publisher: { '@id': SITE + '/#org' }, mainEntityOfPage: url });
  if (slug) {
    const crumbs = [{ '@type': 'ListItem', position: 1, name: 'Home', item: SITE + '/' }];
    if (slug.startsWith('resources/') && slug !== 'resources/') crumbs.push({ '@type': 'ListItem', position: 2, name: 'Resources', item: SITE + '/resources/' });
    crumbs.push({ '@type': 'ListItem', position: crumbs.length + 1, name: h1.replace(/\.$/, ''), item: url });
    graph.push({ '@type': 'BreadcrumbList', itemListElement: crumbs });
  }
  const qa = [...body.matchAll(/<summary[^>]*>\s*<span>([\s\S]*?)<\/span>[\s\S]*?<\/summary>\s*<p[^>]*>([\s\S]*?)<\/p>/g)].map((m) => ({ q: strip(m[1]), a: strip(m[2]) }));
  if (qa.length) {
    graph.push({ '@type': 'FAQPage', mainEntity: qa.map(({ q, a }) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) });
    if (file === 'FAQ.dc.html') faqAll.push(...qa);
  }
  const jsonld = JSON.stringify({ '@context': 'https://schema.org', '@graph': graph }, null, 1).replace(/</g, '\\u003c');

  const noindex = cfg.noindex || slug === 'site-plan/';
  const ogImage = SITE + '/assets/workflow-poster.jpg';
  const fontLinks = helmet.match(/<link[^>]+>/g).join('\n');
  const style = helmet.match(/<style>([\s\S]*?)<\/style>/)[1];
  const doc = `<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
${desc ? `<meta name="description" content="${esc(desc)}">` : ''}
<link rel="canonical" href="${url}">
${noindex ? '<meta name="robots" content="noindex, nofollow">' : '<meta name="robots" content="index, follow, max-image-preview:large">'}
<meta property="og:type" content="${ARTICLES.includes(file) ? 'article' : 'website'}">
<meta property="og:site_name" content="Syrax Solutions">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:url" content="${url}">
<meta property="og:image" content="${ogImage}">
<meta property="og:locale" content="en_AU">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="${rel(slug, 'assets/syrax-icon.png')}">
${fontLinks}
<style>${style}
img,video{max-width:100%}
</style>
<script type="application/ld+json">${jsonld}</script>
</head>
<body>
${body.trim()}
</body>
</html>
`;
  const dir = path.join(OUT, slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), doc);
  if (slug !== 'site-plan/') sitemap.push(url);
}

// ---------- sitemap.xml, robots.txt, llms.txt, 404, .nojekyll ----------
fs.writeFileSync(path.join(OUT, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${sitemap.map((u) => `  <url><loc>${u}</loc><lastmod>${cfg.published}</lastmod></url>`).join('\n')}
</urlset>
`);
const bots = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'PerplexityBot', 'Google-Extended', 'Applebot-Extended', 'CCBot'];
fs.writeFileSync(path.join(OUT, 'robots.txt'), (cfg.noindex
  ? `# Preview build: search engines are asked not to index this site yet.\nUser-agent: *\nDisallow: /\n`
  : `User-agent: *\nAllow: /\nDisallow: /site-plan/\n\n# AI assistants and AI search are welcome to read and cite this site\n${bots.map((b) => `User-agent: ${b}\nAllow: /`).join('\n\n')}\n`) + `\nSitemap: ${SITE}/sitemap.xml\n`);
const L = (f) => `[${meta[f].h1.replace(/\.$/, '')}](${meta[f].url}): ${meta[f].desc}`;
fs.writeFileSync(path.join(OUT, 'llms.txt'), `# Syrax Solutions

> Syrax Solutions is a Sydney-based Australian company that provides automated drone herd monitoring for grazing properties. A drone-in-a-box (DJI Dock 3) lives on the property, flies a mapped route each day, and Syrax software turns the flight into a cattle head count by paddock, plus water trough, feed bunk, fence line and welfare checks. Results are sent by SMS, daily summary, weekly email and a phone and web app.

Key facts:
- Service area: Australia-wide. Based in Sydney, NSW.
- What it counts: cattle, by paddock, compared with the previous flight. Each report includes the aerial photo with every animal marked.
- Flight timing: counting flights run mid-morning, when shadows are short, so cattle under trees are easier to see.
- Hardware: a weatherproof dock and an enterprise drone with visual and thermal cameras. Syrax assesses the property, installs the dock and maps routes.
- Property needs: power at the dock site and a mobile or satellite internet connection.
- Welfare flags are prompts to check an animal, not a veterinary diagnosis.
- Individual animal identification is not currently offered.
- Pricing: a fixed quote after a property assessment.

## Product
- ${L('CattleCounting.dc.html')}
- ${L('WaterFeed.dc.html')}
- ${L('FenceWelfare.dc.html')}
- ${L('HowItWorks.dc.html')}

## Company
- ${L('WhoItsFor.dc.html')}
- ${L('About.dc.html')}
- ${L('FAQ.dc.html')}
- ${L('Contact.dc.html')}

## Guides
- ${L('ArticleMidMorning.dc.html')}
- ${L('ArticleCountCost.dc.html')}
- ${L('ArticleDroneInABox.dc.html')}

## FAQ
${faqAll.map(({ q, a }) => `- ${q} ${a}`).join('\n')}
`);
fs.writeFileSync(path.join(OUT, '.nojekyll'), '');
fs.copyFileSync(path.join(OUT, 'index.html'), path.join(OUT, '404.html'));
console.log('exported', Object.keys(PAGES).length, 'pages to', OUT);
