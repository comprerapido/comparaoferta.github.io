import os
import json

def apply_seo_enhancements(file_path, config):
    if not os.path.exists(file_path):
        return
        
    with open(file_path, 'r') as f:
        content = f.read()
        
    # Adicionar Schema Markup
    schema = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "{config['nome_site']}",
      "url": "{config['url_base']}"
    }}
    </script>
    """
    
    if '</head>' in content:
        content = content.replace('</head>', f'{schema}\n</head>')
        
    with open(file_path, 'w') as f:
        f.write(content)

def main():
    config_path = os.path.join(os.path.dirname(__file__), '../data/ROBO3_CONFIG.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
        
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    
    # Aplicar melhorias no index
    apply_seo_enhancements(os.path.join(base_dir, 'index.html'), config)
    
    print("Melhorias de SEO aplicadas!")

if __name__ == "__main__":
    main()
