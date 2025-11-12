"""
Test script for Phase 1 services
Tests Portfolio Service and Paper Trading Service
"""

import requests
import json

BASE_URL_PORTFOLIO = "http://localhost:8004"
BASE_URL_PAPER = "http://localhost:8005"

# Mock token for testing (in production, get from user service)
MOCK_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidGVzdF91c2VyIiwiZW1haWwiOiJ0ZXN0QGV4YW1wbGUuY29tIn0.test"

headers = {
    "Authorization": f"Bearer {MOCK_TOKEN}",
    "Content-Type": "application/json"
}

def test_portfolio_service():
    """Test Portfolio Management Service"""
    print("\n" + "="*60)
    print("TESTING PORTFOLIO SERVICE (Port 8004)")
    print("="*60)
    
    # Test 1: Get portfolio
    print("\n1. Getting portfolio...")
    response = requests.get(f"{BASE_URL_PORTFOLIO}/api/portfolio", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Cash: ${data.get('cash', 0):,.2f}")
        print(f"Total Value: ${data.get('totalValue', 0):,.2f}")
        print(f"Positions: {len(data.get('positions', []))}")
    else:
        print(f"Error: {response.text}")
    
    # Test 2: Buy stock
    print("\n2. Buying 10 shares of AAPL...")
    buy_data = {
        "ticker": "AAPL",
        "quantity": 10,
        "price": 150.00
    }
    response = requests.post(f"{BASE_URL_PORTFOLIO}/api/portfolio/buy", headers=headers, json=buy_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")
    
    # Test 3: Get updated portfolio
    print("\n3. Getting updated portfolio...")
    response = requests.get(f"{BASE_URL_PORTFOLIO}/api/portfolio", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"Cash: ${data.get('cash', 0):,.2f}")
        print(f"Total Value: ${data.get('totalValue', 0):,.2f}")
        print(f"Positions: {len(data.get('positions', []))}")
        for pos in data.get('positions', []):
            print(f"  - {pos['ticker']}: {pos['quantity']} shares @ ${pos['avgCostBasis']:.2f}")
    
    # Test 4: Get transactions
    print("\n4. Getting transaction history...")
    response = requests.get(f"{BASE_URL_PORTFOLIO}/api/portfolio/transactions", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"Total transactions: {len(data.get('transactions', []))}")
        for txn in data.get('transactions', [])[:3]:
            print(f"  - {txn['type']} {txn['quantity']} {txn['ticker']} @ ${txn['price']:.2f}")

def test_paper_trading_service():
    """Test Paper Trading Service"""
    print("\n" + "="*60)
    print("TESTING PAPER TRADING SERVICE (Port 8005)")
    print("="*60)
    
    # Test 1: Get account
    print("\n1. Getting paper trading account...")
    response = requests.get(f"{BASE_URL_PAPER}/api/paper/account", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Cash: ${data.get('cash', 0):,.2f}")
        print(f"Total Value: ${data.get('totalValue', 0):,.2f}")
        print(f"Positions: {len(data.get('positions', []))}")
    else:
        print(f"Error: {response.text}")
    
    # Test 2: Place market buy order
    print("\n2. Placing market buy order for 5 shares of MSFT...")
    import time
    time.sleep(2)  # Small delay to avoid rate limiting
    order_data = {
        "ticker": "MSFT",
        "type": "market",
        "side": "buy",
        "quantity": 5
    }
    response = requests.post(f"{BASE_URL_PAPER}/api/paper/order", headers=headers, json=order_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Order ID: {data.get('orderId')}")
        print(f"Status: {data.get('status')}")
        if data.get('filledPrice'):
            print(f"Filled Price: ${data.get('filledPrice'):.2f}")
        print(f"Message: {data.get('message')}")
    else:
        print(f"Error: {response.text}")
    
    # Test 3: Get updated account
    print("\n3. Getting updated account...")
    response = requests.get(f"{BASE_URL_PAPER}/api/paper/account", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"Cash: ${data.get('cash', 0):,.2f}")
        print(f"Total Value: ${data.get('totalValue', 0):,.2f}")
        print(f"Total P&L: ${data.get('totalPL', 0):,.2f} ({data.get('totalPLPercent', 0):.2f}%)")
        for pos in data.get('positions', []):
            print(f"  - {pos['ticker']}: {pos['quantity']} shares @ ${pos['avgCostBasis']:.2f}")
    
    # Test 4: Get order history
    print("\n4. Getting order history...")
    response = requests.get(f"{BASE_URL_PAPER}/api/paper/orders", headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"Total orders: {len(data.get('orders', []))}")
        for order in data.get('orders', [])[:3]:
            print(f"  - {order['side'].upper()} {order['quantity']} {order['ticker']} @ ${order['filledPrice']:.2f}")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("PHASE 1 SERVICES TEST SUITE")
    print("="*60)
    
    try:
        test_portfolio_service()
    except Exception as e:
        print(f"\n❌ Portfolio Service Error: {e}")
    
    try:
        test_paper_trading_service()
    except Exception as e:
        print(f"\n❌ Paper Trading Service Error: {e}")
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()

