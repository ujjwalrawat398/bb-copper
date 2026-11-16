# BB Copper — QA, security, SEO & AEO report

Audit date: 16 November 2026. Scope: workspace static build, local Chromium and source/deployment configuration. This is not a penetration-test certification or a guarantee of ranking/security.

## Verified results

| Check | Result |
|---|---|
| Generated content pages | 207, plus custom 404 |
| Inventory | 191 distinct consecutive codes, 11 categories |
| Titles / descriptions | 207 unique titles and 207 unique descriptions |
| Local links/assets and image alt/dimensions | Pass across all 207 content pages |
| JSON-LD parsing and per-page CSP script hash | Pass across all 207 content pages |
| Sitemap | 206 canonical content URLs; empty reviews page intentionally excluded and noindexed |
| Browser responsive matrix | 63 checks: 9 routes × 320, 360, 390, 430, 768, 1024 and 1440px widths; no document horizontal overflow, missing H1 or broken loaded images |
| Browser runtime | No page errors or console errors in tested matrix |
| Interactions | Code search, empty results, photo filter, menu toggle/Escape, whitespace-name rejection and exact encoded WhatsApp payload passed |
| Automated accessibility | axe WCAG 2 A/AA + WCAG 2.1 AA scan: zero detected violations on Home, catalogue, product with photo, product without photo, Contact at 390px |
| Mobile Lighthouse: Home | Performance 100 / Accessibility 100 / Best Practices 100 / SEO 100 |
| Mobile Lighthouse: BB-1185 | Performance 100 / Accessibility 100 / Best Practices 100 / SEO 100 |
| npm dependencies | npm audit reported 0 known vulnerabilities for retained test dependencies; no production JavaScript dependencies |

Lighthouse scores are single-run local lab measurements, not field Core Web Vitals or production scores. Testing uses desktop Chromium viewport emulation, not physical iPhones/Android devices. Automated accessibility does not establish full WCAG conformance. WhatsApp payload was intercepted and inspected, not actually sent to the business.

## Bugs and UX issues corrected

- Avoid eager configuration fetch/unhandled rejected promises on pages that never submit an enquiry. Configuration now loads when needed, validates recipient and HTTPS origin, and retries after a fetch failure.
- Reject whitespace-only names; preserve special characters using URL encoding, not HTML insertion.
- Clear popup opener immediately, retain popup-blocker fallback and safe error recovery.
- Increase text contrast and supporting font sizes. Fix skipped heading levels and conflicting accessible names.
- Improve keyboard focus, skip link, mobile menu state and Escape behaviour.
- Harden narrow-screen grid sizing, wrapping, email links, enquiry controls, 16px mobile form text, target sizes and safe-area position.
- Prioritise main product photos rather than lazy-loading the above-fold image.
- Remove duplicated original JPEG assets from deploy output. Source originals remain editable in the source archive.

## Security improvements

- Strict per-page Content Security Policy via HTML meta: local assets only, no eval, no inline executable JavaScript or inline CSS, no objects, no base URL override, no form network submission. JSON-LD has an exact SHA-256 hash allowance.
- Schema JSON escapes markup-significant characters. Template display values use HTML escaping. Search uses textContent/visibility and enquiry data is URL-encoded; no user-controlled innerHTML.
- Cloudflare Pages/Netlify `_headers` config includes nosniff, referrer policy, restricted browser permissions, anti-framing and HTTPS upgrade policy. HTML meta policy and HTTP policy complement each other.
- No backend, database, API tokens, payment processing, analytics or enquiry persistence. Added concise enquiry privacy notice.
- Cache configuration for CSS/JS and images. Free-host CDN compression is expected but must be verified after deployment.

**Important:** `_headers` is deployment configuration. Python's local preview does not serve these HTTP headers. Verify actual response headers on Cloudflare Pages/Netlify after launch. GitHub Pages does not natively apply `_headers`; use appropriate host configuration instead. Anti-framing intentionally prevents production iframe embedding. HSTS is not enabled blindly; configure it at the chosen host after confirming HTTPS and domain/subdomain readiness. No public production domain was scanned.

## SEO / answer-engine readiness

- Unique product-specific descriptions, canonical URLs, Open Graph/Twitter tags and a default social image (typographic, not an official logo).
- Linked WebSite, WebPage and LocalBusiness entities; Product schema on product pages without invented offers, stock, ratings or prices.
- BreadcrumbList on inner pages and ItemList on catalogue/category pages.
- Six visible, factual FAQs with matching FAQPage markup on Home, covering product range, location, enquiry steps, unavailable specifications, image links and enquiry privacy.
- Readable product facts, crawlable static content and clear business identity/contact details support question answering without JavaScript rendering.
- No fabricated testimonials, unverified medical claims, AI-targeted hidden text or keyword stuffing.

FAQ schema does not guarantee Google FAQ rich results (availability is restricted). AEO is clear, verifiable, accessible content, not a guarantee that an AI system will cite the site. Product rich results may require additional verified fields not available in this catalogue; none were invented to remove search-tool warnings.

## Still needed before public launch

1. Original PDF and 171 missing photos; official logo/favicon replacements. Existing placeholder imagery is honest, not completed catalogue photography.
2. Verify business address/pincode, email spelling, legal name, final domain, exact Maps listing and hours. Names/codes remain transcribed from brief, not checked against PDF.
3. Deploy final domain; verify SSL, redirects/canonical host, actual response headers, compression, caching and custom 404 status. Submit sitemap to Search Console and associate Google Business Profile.
4. Real Android/iPhone checks: touch, mobile keyboard, menu, WhatsApp app opening/sending and actual image preview behaviour.
5. Repeat Lighthouse on live production. Validate structured data in Google's Rich Results Test/Schema validator. Watch real-user Core Web Vitals after traffic is available.
6. Replace empty reviews page content only with verified genuine reviews; remove noindex when it has substantive approved content.

## Reproduce

```sh
pip install -r requirements.txt
python build.py
python audit.py
npm ci
npx playwright install --with-deps chromium
# Start preview in a separate terminal:
python -m http.server 3000 --bind 0.0.0.0 --directory dist
# Then:
node test-browser.cjs
node test-a11y.cjs
npm audit
```

For Lighthouse, use `npx --package=lighthouse lighthouse http://localhost:3000/ --chrome-flags='--headless --no-sandbox' --output=json --output-path=lighthouse-home.json`; set CHROME_PATH if no system Chrome exists. Lighthouse is not retained as a project dependency. Raw browser, axe, structural and Lighthouse reports are in the source archive. Builds regenerate dist and all enhancements automatically via harden.py.

## Superseding visual update

The user supplied 11 catalogue page images after the original audit. These are now integrated as edited lifestyle imagery, collection banners and logo artwork. Official extracted colour logo replaces provisional header/footer typography. PNG favicon, 180px apple icon and 512px icon generated. A subtle copper-gradient visual system, larger photographic hero, editorial tiles and collection gallery were added while retaining strict CSP and local-only assets. Source originals are excluded from deployed output.

Product BB-1143 now has its matching coded lifestyle image: **21 mapped product images, 170 still missing**. Group photos are not assigned to individual codes without verification. Printed health claims are not included in the displayed crops. Remaining address/email and domain verification requirements are unchanged.

Latest Home mobile Lighthouse: **98 Performance / 100 Accessibility / 100 Best Practices / 100 SEO**. Latest 63 responsive checks pass; latest five-page axe checks report no detected violations. All homepage image requests were additionally loaded and checked successfully. Scores above describe the earlier edition where different. The original PDF and physical-device tests remain outstanding; the extracted logo is raster catalogue artwork, not a vector master.

## Image proportion correction

Following visual feedback, square product frames now size independently of their images, with positioned `object-fit: contain` photographs to prevent intrinsic image dimensions from elongating cards. Hero uses a compact responsive frame; editorial, story and collection images have bounded aspect ratios; mobile banners are 165px high. Product images are not stretched or clipped. Lifestyle crops remain within their designed frames.

Latest checks: 63 existing responsive checks plus 30 media-specific route/viewport checks pass. Media checks verify loaded images, square product frames, horizontal overflow and excessive displayed image heights at 320/390/600/768/1440px. Five-page axe scan rerun. This is emulated browser testing, not physical-device verification. Prior Lighthouse scores refer to the previous image sizing edition; Lighthouse was not rerun after this proportion adjustment.

## Back navigation update

Inner pages now have an explicit Back link. With a same-origin referrer and available history it uses native history.back(); direct or external entries use a deterministic in-site fallback (product → category; category → catalogue; other main pages → Home). Native browser Back/Forward is not trapped or padded with fake history entries. A browser Back action at the first site history entry can still leave the site, intentionally. Catalogue search/photo filters are restored per page using sessionStorage (no enquiry/name persistence). Six navigation scenarios passed in Chromium, including direct/external entry, native Back/Forward and filter restoration. 63 responsive checks and five targeted axe scans rerun successfully. See navigation-results.json and test-navigation.cjs.
