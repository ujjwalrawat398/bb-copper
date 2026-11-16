# BB Copper Products — static catalogue

A warm, responsive catalogue with **191 product pages, 11 category pages**, searchable catalogue, About, Reviews and Contact. No backend, database, payment system, paid integration or runtime server is required.

## Run locally

Requirements: Python 3 and Pillow. Node is optional (only used for the convenient npm scripts).

```sh
python3 -m pip install -r requirements.txt
python3 build.py
python3 -m http.server 3000 --bind 0.0.0.0 --directory dist
```

Open http://localhost:3000. Alternatively use `npm run build` and `npm run dev` after installing Pillow.

## Deploy for free

**Simplest:** unzip `bb-copper-deploy.zip`, and upload its contents to a Cloudflare Pages direct-upload project or Netlify. `index.html` must be at the upload root.

**Git deployment:** push this source directory to a repository. Set build command to `pip install -r requirements.txt && python3 build.py`, output directory `dist`. A Python-capable build environment is needed. No Python or Node runs on the deployed website.

Set `domain` in `src/data/site.json` to the confirmed production origin **before building**. The current value `https://www.bbcopper.com` comes from the supplied brief and is not confirmed as purchased or controlled. It supplies canonical, sitemap, structured-data and WhatsApp image/page URLs. DNS and domain registration are not configured by this project.

## Content editing

- `src/data/products.json`: sole editable product inventory, one entry per code. Names transcribed from the brief, **not verified against the original PDF**.
- `src/data/categories.json`: category names and counts.
- `src/data/site.json`: business contact details and domain. Change the phone, email and address here only; rebuild afterward.
- `src/data/reviews.json`: empty intentionally. Review rendering is intentionally not enabled until verified review text and exact listing URL are supplied.
- `assets/images/`: 20 original supplied JPEGs. Source product paths point here. Build converts them into code-named WebP images and thumbnails.
- `build.py`: dependency-light static page generator and editable page templates.
- `assets/style.css`, `assets/app.js`: responsive styles and small vanilla-JavaScript interactions.

Every rebuild regenerates 207 static HTML pages. All products have indexable URLs such as `/products/bb-1185/`. Product pages include unique metadata, canonical URLs and Product JSON-LD without prices/offers/ratings. Products with photos include product Open Graph images. There are no external fonts, scripts, stylesheets or tracking services.

## WhatsApp behaviour

The customer enters a required name, plus optional quantity/message, on a product page. The button opens WhatsApp with product name, item code, category, absolute image URL (when present), absolute product URL and customer fields. WhatsApp only prefills text: it cannot attach the image, preview generation is not guaranteed, and the user must press Send. Preview-domain image links will not work publicly until the configured domain is deployed. Static hosting supports deep product URLs via generated directory index files.

## Required before launch

1. Supply the original `BB_COPPER_final_catlogure.pdf`. Only 20 uploaded photos were available. **171 products use an honest 'Product photo coming soon' panel**; no unrelated photo is substituted. Check all names, codes, compositions and variants against the PDF.
2. Supply/extract the official logo. The visible BB header/footer treatment and SVG favicon are **provisional typography, not the extracted official logo**. The unused `assets/brand/logo.svg` is likewise a temporary mark. Replace these with approved official artwork. Final dark logo, PNG favicon sizes, apple-touch icon and default social image are not yet provided.
3. Confirm pincode (281001 versus 281004), printed email spelling, legal footer name, domain ownership, weekly hours, social URLs and optional GST details. Pincode and unconfirmed hours are omitted.
4. Verify exact Google Business listing and copy genuine reviews. No reviews, summary snippets or unverified rating are published. Contact uses a clearly labelled Maps **search link**, not a verified place embed. Replace with verified Maps Share iframe if desired.
5. Confirm material composition, capacities, weights, sizes, finishes, MOQ and availability. None are invented. No prices, medical claims, certifications or unconfirmed custom-design promises are shown.
6. Test WhatsApp sending on actual iOS/Android devices, verify DNS/SSL and image previews, and run Lighthouse on the deployed domain. No Lighthouse score or real-device test is claimed.
7. Add approved logo/default social image and OG imagery for products without supplied photos before launch.

## Checks completed

- Build succeeds and emits 207 HTML pages.
- 191 unique item codes BB-1001 through BB-1191, grouped into 11 categories.
- 20 supplied photos converted to WebP, each matched by its file item code.
- Automated HTML scan: all local `href` and `src` targets exist.
- Responsive 2-column mobile product grid and desktop layouts implemented; visual browser and real-device QA remains outstanding.

This is a working catalogue build with clearly documented content gaps, **not an assertion that the full acceptance checklist is complete**.

## QA/security/SEO update — 16 November 2026

See **AUDIT-REPORT.md** for the latest verified status (supersedes earlier QA/asset notes above). The build now invokes `harden.py`: unique descriptions, visible FAQs with matching schema, breadcrumbs/entity graph, strict CSP, host security/cache headers, default social preview image, accessible navigation and mobile readability fixes. A custom 404 is included.

63 responsive Chromium checks passed; five key page types passed the targeted axe scan. Local mobile Lighthouse scored 100 in all four categories on Home and BB-1185, with raw reports included. Physical-device QA and deployed-domain/header verification are still required. Default OG artwork is typographic and does not replace the missing official logo. `dist` contains only optimised product assets, not the original JPEG copies. Test tooling is optional and is not shipped with the production site.

## Catalogue photography update

11 newly supplied catalogue JPEGs are saved in `assets/source/catalogue/` (source archive only). Run `python prepare-images.py` to regenerate edited WebP lifestyle crops and official logo/icon PNGs; run `python build.py` afterward. Build includes `visual.py` before the security pass. Header/footer now use the extracted official catalogue logo; PNG favicon and apple-touch icon use the extracted BB mark. About copy follows the provided company page without medical claims.

All 11 images contribute cropped photography or logo assets across Home, About and category pages. Group imagery is collection context, not a claim that all photos show a single purchasable product. BB-1143 has its exact, visibly coded catalogue lifestyle photo. 21 products now have mapped images; 170 still need individually matched photographs. The PDF is still needed for complete verification. Original source pages are not published in the deploy ZIP. Medical and unverified claims embedded in source page artwork are excluded from the displayed crops.

Latest Home mobile Lighthouse after photography update: Performance 98, Accessibility 100, Best Practices 100, SEO 100 (local single-run lab result). Responsive matrix and targeted axe checks rerun successfully.

## Image proportion correction

Following visual feedback, square product frames now size independently of their images, with positioned `object-fit: contain` photographs to prevent intrinsic image dimensions from elongating cards. Hero uses a compact responsive frame; editorial, story and collection images have bounded aspect ratios; mobile banners are 165px high. Product images are not stretched or clipped. Lifestyle crops remain within their designed frames.

Latest checks: 63 existing responsive checks plus 30 media-specific route/viewport checks pass. Media checks verify loaded images, square product frames, horizontal overflow and excessive displayed image heights at 320/390/600/768/1440px. Five-page axe scan rerun. This is emulated browser testing, not physical-device verification. Prior Lighthouse scores refer to the previous image sizing edition; Lighthouse was not rerun after this proportion adjustment.

## Back navigation update

Inner pages now have an explicit Back link. With a same-origin referrer and available history it uses native history.back(); direct or external entries use a deterministic in-site fallback (product → category; category → catalogue; other main pages → Home). Native browser Back/Forward is not trapped or padded with fake history entries. A browser Back action at the first site history entry can still leave the site, intentionally. Catalogue search/photo filters are restored per page using sessionStorage (no enquiry/name persistence). Six navigation scenarios passed in Chromium, including direct/external entry, native Back/Forward and filter restoration. 63 responsive checks and five targeted axe scans rerun successfully. See navigation-results.json and test-navigation.cjs.
