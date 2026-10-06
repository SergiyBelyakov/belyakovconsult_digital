BELYAKOV CONSULT | SEO-OPTIMIZED UA / EN / PT

Стартова сторінка: index.html
Англійська: en/index.html
Португальська: pt/index.html
Збірка, npm і встановлення залежностей не потрібні.

Що оптимізовано:
- canonical для www-версії та взаємні hreflang uk / en / pt-PT / x-default;
- прибрано дублікати hreflang з попередньої версії;
- SEO Title і meta description для кожної мовної версії;
- robots/googlebot directives для повних сніпетів і великих image previews;
- Open Graph і Twitter Card;
- social preview assets/og-belyakov-consult.jpg 1200×630;
- JSON-LD: WebSite, Organization, Person, WebPage та каталог послуг;
- sitemap.xml з hreflang і lastmod;
- robots.txt;
- site.webmanifest та іконки 192/512;
- виправлено intrinsic width/height hero-зображення для зменшення CLS;
- service-*.png конвертовано у WebP та HTML переведено на WebP;
- hero preload та fetchpriority=high;
- додано 404.html з noindex;
- LinkedIn профіль позначено rel=me;
- прибрано стрілочки після «Результат / Results» у картках напрямів.

Після завантаження на сервер:
1. Залишити Cloudflare 301: https://belyakovconsult.com/* → https://www.belyakovconsult.com/${1}.
2. Перевірити /robots.txt та /sitemap.xml.
3. У Search Console повторно подати sitemap.xml та URL /, /en/, /pt/ на індексацію.
4. Перевірити social preview через LinkedIn Post Inspector / Facebook Sharing Debugger.
5. Надіслати тестову форму Formspree і перевірити доставку.

SEO EXPANSION — 06.10.2026
New indexable Ukrainian pages:
/data-strategy/
/data-governance/
/data-quality/
/data-architecture/
/business-intelligence/
/geospatial-analysis/
/cases/
/insights/
/sergiy-belyakov/

After deployment:
1. Verify every new URL returns HTTP 200.
2. Open https://www.belyakovconsult.com/sitemap.xml and confirm the new URLs are present.
3. Re-submit the same sitemap in Google Search Console.
4. Use URL Inspection for the main service pages and request indexing.
5. Do not create redirects from these new URLs unless their paths change later.
