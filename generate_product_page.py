import json
import os
import urllib.parse

def generate_page():
    # Read products
    with open("products.json", "r") as f:
        products = json.load(f)
        
    # Get Categories
    categories = sorted(list(set(p["category"] for p in products)))
    
    # Generate Sidebar HTML
    sidebar_html = """
    <div class="sidebar-wrapper" style="width: 25%; float: left; padding-right: 20px;">
        <div class="widget Label">
            <h3 class="title">Categories</h3>
            <div class="widget-content list-label">
                <ul>
                    <li><a href="#" onclick="filterProducts('all'); return false;">All Products</a></li>
    """
    for cat in categories:
        display_name = cat.title()
        # Clean up category name for display
        display_name = display_name.replace("Vanderbilt Product Listing For ", "").replace("Product Listing For ", "")
        # Safe class name
        cat_class = urllib.parse.quote(cat)
        sidebar_html += f'<li><a href="#" onclick="filterProducts(\'{cat_class}\'); return false;">{display_name}</a></li>'
    sidebar_html += """
                </ul>
            </div>
        </div>
    </div>
    """
    
    # Generate Product Grid HTML
    grid_html = '<div class="main-wrapper" style="width: 75%; float: left;">'
    grid_html += '<div class="row" id="product-grid" style="display: flex; flex-wrap: wrap;">'
    
    for p in products:
        title = p["title"]
        image = p["image"]
        link = p["link"]
        cat = p["category"]
        cat_class = urllib.parse.quote(cat)
        
        # URL Encode image path if local
        if not image.startswith("http") and not image.startswith("data:"):
            # Split and quote parts to handle spaces
            parts = image.split("/")
            image = "/".join([urllib.parse.quote(part) for part in parts])
        
        item_html = f"""
        <div class="product-item {cat_class}" style="width: 30%; margin: 1.5%; box-shadow: 0 2px 5px rgba(0,0,0,0.1); padding: 10px; border-radius: 5px; background: #fff; float: left;">
            <div class="post-image-wrap" style="height: 200px; overflow: hidden; display: flex; align-items: center; justify-content: center;">
                <a href="{link}" target="_blank">
                    <img src="{image}" alt="{title}" style="max-width: 100%; max-height: 100%; width: auto; height: auto;">
                </a>
            </div>
            <h3 class="post-title" style="font-size: 14px; margin-top: 10px; height: 40px; overflow: hidden;">
                <a href="{link}" target="_blank">{title}</a>
            </h3>
            <span class="product-category" style="font-size: 11px; color: #ff5e15;">{cat}</span>
        </div>
        """
        grid_html += item_html
        
    grid_html += '</div></div>'
    
    # Script for filtering
    script_html = """
    <script>
    function filterProducts(category) {
        var items = document.getElementsByClassName('product-item');
        for (var i = 0; i < items.length; i++) {
            if (category == 'all' || items[i].classList.contains(category)) {
                items[i].style.display = 'block';
            } else {
                items[i].style.display = 'none';
            }
        }
    }
    </script>
    """
    
    # Combined Content
    full_content = '<div class="container" style="padding-top: 20px; overflow: hidden;">' + sidebar_html + grid_html + '</div>' + script_html
    
    # Inject into product.html by using index.html as a template
    # We read index.html to get the latest header and footer
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Find Start of Main Content
    # We look for the main content section to replace it
    # Pattern: <section id="content"
    content_start_idx = html.find('<section id="content"')
    
    # Find End of Content (Start of Footer)
    # Pattern: <footer id="footer">
    footer_idx = html.find('<footer id="footer">')
    
    if content_start_idx != -1 and footer_idx != -1:
        header_section = html[:content_start_idx]
        footer_section = html[footer_idx:]
        
        # Wrap our content in the correct structure
        # We usage page-content class for consistency
        new_content = f"""<section id="content" class="page-content page-cms">
            <div class="container" style="padding-top: 20px; padding-bottom: 40px;">
                <div class="row">
                    <div class="col-xs-12">
                         <h1 class="text-uppercase mb-4">Our Products</h1>
                    </div>
                </div>
                {sidebar_html}
                {grid_html}
            </div>
            {script_html}
        </section>
        """
        
        final_html = header_section + new_content + footer_section
        
        with open("product.html", "w", encoding="utf-8") as f:
            f.write(final_html)
        print("Successfully regenerated product.html using index.html branding")
    else:
        print("Error: Could not identify content boundaries in index.html")

if __name__ == "__main__":
    generate_page()
