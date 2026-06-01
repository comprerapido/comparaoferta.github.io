import json
import os

def generate_html(template_name, context, output_path):
    # Template básico para demonstração
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{context.get('title')} - {context.get('site_name')}</title>
        <meta name="description" content="{context.get('description')}">
        <link rel="stylesheet" href="/assets/style.css">
    </head>
    <body>
        <header>
            <h1>{context.get('site_name')}</h1>
            <nav>
                <a href="/">Home</a>
                <a href="/categorias/casa">Casa</a>
                <a href="/categorias/games">Games</a>
                <a href="/categorias/tv-video">TV</a>
                <a href="/categorias/celular">Celular</a>
                <a href="/categorias/moda">Moda</a>
            </nav>
        </header>
        <main>
            <h2>{context.get('title')}</h2>
            <div class="products">
                {context.get('products_html', '<p>Confira as melhores ofertas selecionadas para você!</p>')}
            </div>
        </main>
        <footer>
            <p>&copy; 2026 {context.get('site_name')}. Todos os direitos reservados.</p>
            <nav>
                <a href="/privacidade">Privacidade</a>
                <a href="/termos">Termos</a>
                <a href="/sobre">Sobre</a>
                <a href="/contato">Contato</a>
            </nav>
        </footer>
    </body>
    </html>
    """
    with open(output_path, 'w') as f:
        f.write(html)

def main():
    config_path = os.path.join(os.path.dirname(__file__), '../data/ROBO3_CONFIG.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    
    # Gerar Index
    generate_html('index', {
        'title': 'Página Inicial',
        'site_name': config['nome_site'],
        'description': config['descricao']
    }, os.path.join(base_dir, 'index.html'))
    
    # Gerar Páginas de Categorias
    for cat in config['categorias']:
        cat_dir = os.path.join(base_dir, 'categorias', cat['id'])
        os.makedirs(cat_dir, exist_ok=True)
        
        # Carregar produtos
        products_file = os.path.join(base_dir, 'data', f"products_{cat['id']}.json")
        products_html = ""
        if os.path.exists(products_file):
            with open(products_file, 'r') as f:
                products = json.load(f)
                for p in products:
                    products_html += f"""
                    <div class="product-card">
                        <img src="{p['thumbnail']}" alt="{p['title']}">
                        <h3>{p['title']}</h3>
                        <p class="price">R$ {p['price']}</p>
                        <a href="{p['permalink']}" class="buy-button">Ver no Mercado Livre</a>
                    </div>
                    """
        
        generate_html('category', {
            'title': cat['nome'],
            'site_name': config['nome_site'],
            'description': cat['descricao'],
            'products_html': products_html
        }, os.path.join(cat_dir, 'index.html'))
        
    # Gerar Páginas Legais
    for page in ['privacidade', 'termos', 'sobre', 'contato']:
        page_dir = os.path.join(base_dir, page)
        os.makedirs(page_dir, exist_ok=True)
        generate_html('legal', {
            'title': page.capitalize(),
            'site_name': config['nome_site'],
            'description': f"Página de {page} do site {config['nome_site']}"
        }, os.path.join(page_dir, 'index.html'))

    print("Páginas geradas com sucesso!")

if __name__ == "__main__":
    main()
