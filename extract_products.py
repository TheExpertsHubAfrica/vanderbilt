import os
import re
import json
from html.parser import HTMLParser

# Base directory
CONTENT_DIR = "vanderbiltContent"
OUTPUT_FILE = "products.json"

class ProductParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_post_title = False
        self.in_post_link = False
        self.in_article = False
        self.current_product = {}
        self.products = []
        self.found_title = False
        self.found_image = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        
        # Identify Product Container (approximate based on inspection)
        # We look for "post-title" which implies a post.
        # But we need a container. Let's assume common Blogger structure: "post hentry" or similar.
        # Or just extract distinct items.
        
        if tag == "a" and "post-title" in attrs.get("class", ""):
            # Note: The class might be on the h3 or div parental to a. 
            pass

        # Check for Title Link
        # grep showed: .mega-content .post-title a
        if tag == "a":
            # Heuristic: Check parent tag in handle_data? No, parser is stream.
            pass
            
    # Simple Regex approach might be more robust for this specific task 
    # as we just need to grab "Title", "Image", "Category".

def extract_products():
    all_products = []
    
    # Updated regex for the specific template structure found
    # Looking for <article ... class="blog-post ..."> ... </article>
    
    for root, dirs, files in os.walk(CONTENT_DIR):
        if "index.html" in files:
            category = os.path.basename(root).replace("vanderbilt Product Listing for ", "").replace("vanderbilt ", "")
            if category in ["HomePage", "AboutPage", "Contact-us", "News", "vanderbiltContent"]:
                continue
                
            filepath = os.path.join(root, "index.html")
            print(f"Scanning {category}...")
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Use regex to find article blocks
            # Note: dependent on formatting, but "article" tag is robust enough here
            articles = re.findall(r'<article[^>]*class=["\']blog-post[^>]*>([\s\S]*?)</article>', content)
            
            for post in articles:
                # Extract Title
                # <h2 class="post-title"> <a ...> TITLE </a> </h2>
                title_match = re.search(r'<h2 class=["\']post-title["\'][^>]*>[\s\S]*?<a[^>]*href=["\']([^"\']*)["\'][^>]*>([\s\S]*?)</a>', post)
                
                # Extract Image
                # <img ... src="..." ...>
                img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', post)
                
                if title_match:
                    link = title_match.group(1)
                    title = title_match.group(2).strip()
                    image_src = img_match.group(1) if img_match else "assets/images/placeholder.png"
                    
                    # Fix Image Path
                    if not image_src.startswith("http") and not image_src.startswith("data:"):
                        # It's local, e.g. "images/image.png"
                        # We need it relative to the root product.html
                        # root is "vanderbiltContent/Folder"
                        # so path is "vanderbiltContent/Folder/images/image.png"
                        # BUT os.walk root gives full path "vanderbiltContent/..."
                        rel_dir = os.path.relpath(root, ".")
                        image_src = f"{rel_dir}/{image_src}"
                    
                    # Clean up title
                    title = re.sub(r'<[^>]+>', '', title)
                    
                    if "Vanderbilt" not in title:
                        all_products.append({
                            "category": category,
                            "title": title,
                            "link": link,
                            "image": image_src
                        })
    
    print(f"Found {len(all_products)} products.")
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(all_products, f, indent=2)

if __name__ == "__main__":
    extract_products()
