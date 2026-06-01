import requests
import json
import os

def fetch_products(category_id, keywords):
    print(f"Buscando produtos para a categoria: {category_id}...")
    # Simulação de busca na API do Mercado Livre
    # Em um cenário real, usaríamos a API oficial com token
    query = "+".join(keywords)
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}&limit=50"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            products = []
            for item in data.get('results', []):
                product = {
                    'id': item.get('id'),
                    'title': item.get('title'),
                    'price': item.get('price'),
                    'permalink': item.get('permalink'),
                    'thumbnail': item.get('thumbnail'),
                    'condition': item.get('condition')
                }
                products.append(product)
            return products
        else:
            print(f"Erro ao buscar produtos: {response.status_code}. Usando dados de exemplo.")
            # Dados de exemplo para garantir que o robô funcione mesmo sem API key no momento
            return [
                {
                    'id': f'MLB{category_id}1',
                    'title': f'Produto de Exemplo {category_id.capitalize()} 1',
                    'price': 199.90,
                    'permalink': 'https://www.mercadolivre.com.br',
                    'thumbnail': 'https://http2.mlstatic.com/D_NQ_NP_614131-MLB44622340767_012021-O.webp',
                    'condition': 'new'
                },
                {
                    'id': f'MLB{category_id}2',
                    'title': f'Produto de Exemplo {category_id.capitalize()} 2',
                    'price': 450.00,
                    'permalink': 'https://www.mercadolivre.com.br',
                    'thumbnail': 'https://http2.mlstatic.com/D_NQ_NP_614131-MLB44622340767_012021-O.webp',
                    'condition': 'new'
                }
            ]
    except Exception as e:
        print(f"Erro: {e}")
        return []

def main():
    config_path = os.path.join(os.path.dirname(__file__), '../data/ROBO3_CONFIG.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    for cat in config['categorias']:
        products = fetch_products(cat['id'], cat['keywords'])
        output_path = f"../data/products_{cat['id']}.json"
        with open(os.path.join(os.path.dirname(__file__), output_path), 'w') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        print(f"Salvo {len(products)} produtos para {cat['nome']}")

if __name__ == "__main__":
    main()
