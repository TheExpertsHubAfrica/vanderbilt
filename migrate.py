import os

def migrate():
    source_file = 'index.html'
    about_file = 'about.html'
    contact_file = 'contact.html'
    news_file = 'news.html'

    # Read index.html
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Define the range to replace (homepage specific content)
    # Based on observation:
    # Line 2305: <section id="content" class="page-home">
    # Line 4044: </section> (closes content)
    
    start_line_idx = 2304 # 0-indexed (Line 2305)
    end_line_idx = 4043   # 0-indexed (Line 4044)
    
    # Verify markers
    print(f"Checking start line {start_line_idx+1}: {lines[start_line_idx].strip()}")
    print(f"Checking end line {end_line_idx+1}: {lines[end_line_idx].strip()}")
    
    if '<section id="content" class="page-home">' not in lines[start_line_idx]:
        print("WARNING: Start marker not found exactly at 2305. Searching...")
        for i, line in enumerate(lines):
            if '<section id="content" class="page-home">' in line:
                start_line_idx = i
                print(f"Found start at {i+1}")
                break
    
    # Finding the end is trickier if specific line is wrong
    # But let's assume valid scope based on indent or just manual confirmation
    # We want to keep the closing </section> of the main wrapper?
    # No, we want to replace the `page-home` section with a `page-cms` section.
    # So we replace from start_line_idx to end_line_idx (inclusive).
    
    # Let's find end_line_idx by looking for the closing section before </section> (main)
    # We saw </section> at 4044 (content), 4048 (main), 4053 (content-wrapper), 4062 (footer)
    # We can search backwards from footer line.
    

    footer_line = -1
    for i in range(len(lines)-1, -1, -1):
        if '<footer id="footer">' in lines[i]:
            footer_line = i
            break
            
    if footer_line != -1:
        # The content usually ends a few lines before footer or at footer.
        # Check backward from footer for the closing </section> of the main content wrapper.
        # In index.html, we have:
        # </section> (content)
        # <footer id="footer">
        # So likely footer_line - 1 or -2.
        # Let's search for the last </section> before footer.
        for i in range(footer_line, start_line_idx, -1):
            if '</section>' in lines[i]:
                end_line_idx = i
                print(f"Found end marker at {i+1}")
                break

    # About Content
    about_content = """                        <section id="content" class="page-content page-cms">
                            <div class="container" style="padding: 40px 15px;">
                                <div class="row">
                                    <div class="col-xs-12">
                                        <h1 class="text-uppercase mb-4">About Vanderbilt Limited</h1>
                                        <div class="cms-content">
                                            <p style="font-size: 1.1em; margin-bottom: 20px;">Vanderbilt is a medical equipment distribution company based in Accra, Ghana. We specialize in the distribution of high-quality medical equipment, accessories, and consumables to hospitals, clinics, and other healthcare facilities across Ghana and beyond.</p>
                                            
                                            <h3>Our Mission</h3>
                                            <p>Our mission is to provide healthcare professionals with the best tools and resources to deliver exceptional patient care. We are committed to sourcing products from reputable manufacturers worldwide, ensuring that our clients have access to the latest advancements in medical technology.</p>
                                            
                                            <h3>Client Relationships</h3>
                                            <p>At Vanderbilt, we believe in building strong, lasting relationships with our clients. We strive to understand their unique needs and provide personalized solutions that meet their specific requirements. Our team of experienced professionals is dedicated to offering unparalleled customer service, technical support, and training to ensure optimal product performance and client satisfaction.</p>
                                            
                                            <h3>Our Products</h3>
                                            <p>We offer a comprehensive range of products, including but not limited to:</p>
                                            <ul style="list-style-type: disc; padding-left: 20px; column-count: 2;">
                                                <li>X-ray films and accessories</li>
                                                <li>Imaging plates and cassettes</li>
                                                <li>CR Systems</li>
                                                <li>X-ray protection equipment</li>
                                                <li>Individual protection equipment (IPE)</li>
                                                <li>Collective protection equipment (CPE)</li>
                                                <li>Printers</li>
                                                <li>Radiology equipment</li>
                                                <li>MRI equipment and accessories</li>
                                                <li>Nuclear medicine solutions</li>
                                                <li>Ultrasound consumables and accessories</li>
                                                <li>Biopsy instruments</li>
                                                <li>Draping solutions</li>
                                                <li>Furniture and lighting for medical facilities</li>
                                                <li>Hygiene and disinfection products</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>\n"""

    # Contact Content
    contact_content = """                        <section id="content" class="page-content page-cms">
                            <div class="container" style="padding: 40px 15px;">
                                <div class="row">
                                    <div class="col-xs-12 text-center mb-5">
                                        <h1 class="text-uppercase" style="margin-bottom: 30px;">Contact Us</h1>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 col-sm-12">
                                         <div class="contact-info-box" style="padding: 20px; background: #f9f9f9; border-radius: 5px;">
                                            <h3>Get A Quote</h3>
                                            <p class="text-muted">Contact us for pricing, availability, and expert advice.</p>
                                            
                                            <hr>
                                            
                                            <div class="media mt-4">
                                                <div class="media-body">
                                                    <h5 class="mt-0"><i class="material-icons" style="vertical-align: middle; margin-right: 10px; color: #ff5e15;">phone</i> Phone</h5>
                                                    <p><a href="tel:+233542664687" style="font-size: 1.2em; font-weight: bold;">+233 54 266 4687</a></p>
                                                </div>
                                            </div>
                                            
                                            <div class="media mt-4">
                                                <div class="media-body">
                                                    <h5 class="mt-0"><i class="material-icons" style="vertical-align: middle; margin-right: 10px; color: #ff5e15;">email</i> Email</h5>
                                                    <p><a href="mailto:sales@vanderbiltco.com" style="font-size: 1.2em; font-weight: bold;">sales@vanderbiltco.com</a></p>
                                                </div>
                                            </div>

                                            <div class="media mt-4">
                                                <div class="media-body">
                                                    <h5 class="mt-0"><i class="material-icons" style="vertical-align: middle; margin-right: 10px; color: #ff5e15;">location_on</i> Location</h5>
                                                    <p>Greater Accra, Ghana</p>
                                                </div>
                                            </div>
                                         </div>
                                    </div>
                                    <div class="col-md-6 col-sm-12">
                                        <!-- Placeholder for Form or Map -->
                                        <div style="background: #eef; height: 300px; display: flex; align-items: center; justify-content: center; border-radius: 5px; color: #777;">
                                            [Map or Contact Form Placeholder]
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>\n"""
    
    # News Content Extraction
    news_source = 'vanderbiltContent/vanderbilt News/index.html'
    news_html = ""
    
    if os.path.exists(news_source):
        with open(news_source, 'r', encoding='utf-8') as f:
            news_raw = f.read()
        
        # Simple regex extraction for articles
        import re
        # Find all article blocks
        articles = re.findall(r'<article class="blog-post hentry halaman-indeks">(.*?)</article>', news_raw, re.DOTALL)
        
        news_html += '<div class="row">'
        for art in articles:
            # Extract Title
            title_match = re.search(r'<h2 class="post-title">\s*<a.*?>(.*?)</a>', art, re.DOTALL)
            title = title_match.group(1).strip() if title_match else "No Title"
            
            # Extract Image
            img_match = re.search(r'<img.*?src="(.*?)".*?>', art)
            img_src = img_match.group(1) if img_match else ""
            
            # Extract Link (Optional, assuming we might migrate these later or just link needed)
            # For now, we will link to # or the original external link if it's there
            link_match = re.search(r'<h2 class="post-title">\s*<a href="(.*?)".*?>', art, re.DOTALL)
            link = link_match.group(1) if link_match else "#"
            
            # Format as Bootstrap Column
            news_html += f"""
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <img src="{img_src}" class="card-img-top" alt="{title}" style="height: 200px; object-fit: cover;">
                    <div class="card-body">
                        <h5 class="card-title">{title}</h5>
                        <a href="{link}" class="btn btn-primary" style="background-color: #ff5e15; border-color: #ff5e15;">Read More</a>
                    </div>
                </div>
            </div>
            """
        news_html += '</div>'
    else:
        news_html = "<p>No news content found.</p>"

    news_content = f"""                        <section id="content" class="page-content page-cms">
                            <div class="container" style="padding: 40px 15px;">
                                <h1 class="text-uppercase mb-4">Latest News</h1>
                                {news_html}
                            </div>
                        </section>\\n"""

    # FAQ Content (Generic Placeholder based on site info)
    faq_content = """                        <section id="content" class="page-content page-cms">
                            <div class="container" style="padding: 40px 15px;">
                                <h1 class="text-uppercase mb-4">Frequently Asked Questions</h1>
                                <div class="accordion" id="faqAccordion">
                                    <div class="card">
                                        <div class="card-header" id="headingOne">
                                            <h5 class="mb-0">
                                                <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne" style="color: #ff5e15; font-weight: bold; text-decoration: none;">
                                                    How do I place an order?
                                                </button>
                                            </h5>
                                        </div>

                                        <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#faqAccordion">
                                            <div class="card-body">
                                                You can place an order by contacting our sales team via email at sales@vanderbiltco.com or by calling us at +233 54 266 4687. We will provide you with a quote and guide you through the process.
                                            </div>
                                        </div>
                                    </div>
                                    <div class="card">
                                        <div class="card-header" id="headingTwo">
                                            <h5 class="mb-0">
                                                <button class="btn btn-link collapsed" type="button" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo" style="color: #ff5e15; font-weight: bold; text-decoration: none;">
                                                    Do you ship internationally?
                                                </button>
                                            </h5>
                                        </div>
                                        <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#faqAccordion">
                                            <div class="card-body">
                                                Yes, we deliver to over 50 countries worldwide. Please contact us for shipping rates and delivery times to your location.
                                            </div>
                                        </div>
                                    </div>
                                    <div class="card">
                                        <div class="card-header" id="headingThree">
                                            <h5 class="mb-0">
                                                <button class="btn btn-link collapsed" type="button" data-toggle="collapse" data-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree" style="color: #ff5e15; font-weight: bold; text-decoration: none;">
                                                    Where are you located?
                                                </button>
                                            </h5>
                                        </div>
                                        <div id="collapseThree" class="collapse" aria-labelledby="headingThree" data-parent="#faqAccordion">
                                            <div class="card-body">
                                                We are based in Accra, Ghana.
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>\\n"""

    faq_file = 'faq.html'

    # Generate About Page
    with open(about_file, 'w', encoding='utf-8') as f:
        f.writelines(lines[:start_line_idx])
        f.write(about_content)
        f.writelines(lines[end_line_idx+1:])
    print(f"Created {about_file}")

    # Generate Contact Page
    with open(contact_file, 'w', encoding='utf-8') as f:
        f.writelines(lines[:start_line_idx])
        f.write(contact_content)
        f.writelines(lines[end_line_idx+1:])
    print(f"Created {contact_file}")

    # Generate News Page
    with open(news_file, 'w', encoding='utf-8') as f:
        f.writelines(lines[:start_line_idx])
        f.write(news_content)
        f.writelines(lines[end_line_idx+1:])
    print(f"Created {news_file}")

    # Generate FAQ Page
    with open(faq_file, 'w', encoding='utf-8') as f:
        f.writelines(lines[:start_line_idx])
        f.write(faq_content)
        f.writelines(lines[end_line_idx+1:])
    print(f"Created {faq_file}")

if __name__ == "__main__":
    migrate()
