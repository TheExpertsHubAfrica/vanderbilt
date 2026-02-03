import json
import os
import re

def create_slug(title):
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

def generate_pages():
    # Load products
    with open('vanderbiltContent/products.json', 'r') as f:
        products = json.load(f)

    # Deduplicate products based on title
    seen_titles = set()
    unique_products = []
    for p in products:
        if p['title'] not in seen_titles:
            unique_products.append(p)
            seen_titles.add(p['title'])
    
    products = unique_products

    # Read index.html for template
    with open('index.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # Extract Header and Footer
    # Assuming <main> or <div id="content-wrapper"> is the divider
    header_match = re.search(r'([\s\S]*?)<section id="content"', template)
    if not header_match:
        # Fallback to similar structure in product.html
        header_match = re.search(r'([\s\S]*?)<section id="main"', template)

    start_content_idx = template.find('<section id="content"') 
    if start_content_idx == -1:
         start_content_idx = template.find('<div id="content-wrapper">')

    # Find Footer
    footer_match = re.search(r'<footer id="footer">([\s\S]*)', template)
    
    if not header_match or not footer_match:
        print("Could not parse template")
        return

    # We can effectively split by content area
    # Simplified approach: Cut out the middle
    header = template[:start_content_idx]
    
    # We need to adjust relative paths in header for the subfolder
    # assets/ -> ../assets/
    # index.html -> ../index.html
    # href=" -> href="../
    
    def fix_paths(html_content):
        # Fix CSS/JS assets
        html_content = html_content.replace('href="assets/', 'href="../assets/')
        html_content = html_content.replace('src="assets/', 'src="../assets/')
        html_content = html_content.replace('href="index.html"', 'href="../index.html"')
        html_content = html_content.replace('href="about.html"', 'href="../about.html"')
        html_content = html_content.replace('href="product.html"', 'href="../product.html"')
        html_content = html_content.replace('href="news.html"', 'href="../news.html"')
        html_content = html_content.replace('href="contact.html"', 'href="../contact.html"')
        html_content = html_content.replace('href="faq.html"', 'href="../faq.html"')
        return html_content

    header = fix_paths(header)
    
    # Footer start
    footer_start_idx = template.find('<footer id="footer">')
    footer = fix_paths(template[footer_start_idx:])

    # Generate pages
    links_mapping = {}

    for p in products:
        slug = create_slug(p['title'])
        filename = f"{slug}.html"
        filepath = os.path.join('products', filename)
        
        # Image handling
        image = p['image']
        if not image.startswith('http'):
            # Relative to root, so in products/ it is ../path
            image = "../" + image
        
        title = p['title']
        category = p['category']
        description = f"The {title} is a premium quality product in our {category} category. Designed for reliability and performance in medical imaging environments."
        
        content = f"""
        <section id="content" class="page-content">
            <div class="container" style="padding: 40px 15px;">
                <div class="row">
                    <div class="col-md-6">
                        <div class="product-detail-image" style="border: 1px solid #eee; padding: 20px; border-radius: 8px;">
                            <img src="{image}" alt="{title}" style="max-width: 100%; height: auto; display: block; margin: 0 auto;">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <h1 class="product-title" style="margin-top: 0; color: #003366; font-size: 2rem;">{title}</h1>
                        <p class="product-category" style="color: #ff5e15; font-weight: bold; text-transform: uppercase; margin-bottom: 20px;">{category}</p>
                        
                        <div class="product-description" style="margin-bottom: 30px; font-size: 1.1rem; line-height: 1.6;">
                            <p>{description}</p>
                            <p>Contact us today for pricing and availability.</p>
                        </div>
                        
                        <div class="product-actions">
                            <a href="../contact.html?product={slug}" class="btn btn-primary" style="background-color: #003366; border-color: #003366; padding: 12px 30px; color: #fff; text-decoration: none; border-radius: 5px; font-weight: bold;">
                                Get a Quote
                            </a>
                            <a href="../product.html" class="btn btn-secondary" style="margin-left: 15px; color: #555; text-decoration: none;">
                                Back to Products
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """
        
        full_html = header + content + footer
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_html)
            
        links_mapping[title] = f"products/{filename}"

    # Update product.html links
    with open('product.html', 'r', encoding='utf-8') as f:
        product_html = f.read()

    # Iterate and replace links
    # Search for title > find parent link or nearest link
    # This is tricky with simple string replace because titles might be partial or formatted differently.
    # But product.html was generated from the same data source effectively.
    
    # We will use BeautifulSoup or just regex to replace links based on titles if possible.
    # Regex approach:
    # Find <a href="..."> ... TITLE ... </a>
    # Replace href
    
    for title, new_link in links_mapping.items():
        # Escape title for regex
        esc_title = re.escape(title)
        
        # Regex to match the anchor tag containing the title
        # We look for the anchor wrapping the title text, or the image anchor if it has alt text matching
        # The structure is:
        # <a href="OLD_LINK" target="_blank"> ... <img ... alt="TITLE"> ... </a>
        # AND
        # <h3 class="post-title" ...> <a href="OLD_LINK" target="_blank">TITLE</a> </h3>
        
        # Replace href in anchor tags containing the title text
        # Be careful not to break HTML.
        
        # Update Link in H3 Title
        product_html = re.sub(
            r'(<a\s+href=")[^"]+("\s+target="_blank">[^<]*' + esc_title + r'</a>)', 
            r'\1' + new_link + r'\2', 
            product_html
        )
        
        # Update Link in Image (by Alt Text)
        # Needs to match the A tag wrapping the IMG with matching ALT
        # Pattern: <a href="OLD" ...> <img ... alt="TITLE" ...> </a>
        # This is harder to do in one regex because attributes order varies.
        # But in product.html generated/formatted by us:
        # <a href="..." target="_blank"> <img src="..." alt="TITLE" ...> </a>
        
        # We can try to replace the href if the following content contains the alt="TITLE"
        # Not perfect.
        
        # Simpler approach: If the old link is found in products.json, we know the mapping!
        pass

    # Better Approach: Map Old Link -> New Link
    # products.json contains the OLD link.
    for p in products:
        old_link = p['link']
        title = p['title']
        if title in links_mapping:
            new_link = links_mapping[title]
            product_html = product_html.replace(old_link, new_link)

    # Also remove target="_blank" since it's now internal
    # We can do this globally or per link replacement.
    # Let's replace 'href="products/..." target="_blank"' with 'href="products/..."'
    # But string replace is simple.
    
    with open('product.html', 'w', encoding='utf-8') as f:
        f.write(product_html)

    # Clean up target="_blank" for local links
    with open('product.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(r'(href="products/[^"]+")\s+target="_blank"', r'\1', content)
    
    with open('product.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Generated {len(links_mapping)} pages and updated product.html")

if __name__ == '__main__':
    generate_pages()
