import requests
import json

# Substitua pela sua URL base do Render
BASE_URL = "https://api-render2-2ajc.onrender.com"

def test_endpoints():
    # 1. Teste do endpoint de saúde (health check)
    health = requests.get(f"{BASE_URL}/health")
    print("\n1. Health Check:")
    print(f"Status: {health.status_code}")
    print(f"Response: {health.json()}")

    # 2. Teste do endpoint de transações
    transactions = requests.get(f"{BASE_URL}/transactions")
    print("\n2. Transactions:")
    print(f"Status: {transactions.status_code}")
    if transactions.status_code == 200:
        print(f"Número de registros: {len(transactions.json())}")
        print("Primeira transação:", json.dumps(transactions.json()[0], indent=2))

    # 3. Teste do endpoint de sumário
    summary = requests.get(f"{BASE_URL}/summary")
    print("\n3. Summary:")
    print(f"Status: {summary.status_code}")
    if summary.status_code == 200:
        print(f"Response: {json.dumps(summary.json(), indent=2)}")

    # 4. Teste do endpoint de categorias
    categories = requests.get(f"{BASE_URL}/categories")
    print("\n4. Categories:")
    print(f"Status: {categories.status_code}")
    if categories.status_code == 200:
        print(f"Response: {json.dumps(categories.json()[:2], indent=2)}")  # Primeiras 2 categorias

    # 5. Teste do endpoint de países
    countries = requests.get(f"{BASE_URL}/countries")
    print("\n5. Countries:")
    print(f"Status: {countries.status_code}")
    if countries.status_code == 200:
        print(f"Response: {json.dumps(countries.json()[:2], indent=2)}")  # Primeiros 2 países

if __name__ == "__main__":
    test_endpoints()
