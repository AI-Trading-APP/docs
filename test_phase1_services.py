"""
Test script for Phase 1 services
Tests Portfolio Service and Paper Trading Service
"""

from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
for import_path in (CURRENT_DIR, CURRENT_DIR.parent, CURRENT_DIR.parent.parent):
    import_path_str = str(import_path)
    if import_path_str not in sys.path:
        sys.path.insert(0, import_path_str)

from ai_trading_common.logging_config import setup_logging, get_logger

setup_logging("docs")
logger = get_logger()


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
    logger.info("script_output", message="\n" + "="*60)
    logger.info("script_output", message="TESTING PORTFOLIO SERVICE (Port 8004)")
    logger.info("script_output", message="="*60)
    
    # Test 1: Get portfolio
    logger.info("script_output", message="\n1. Getting portfolio...")
    response = requests.get(f"{BASE_URL_PORTFOLIO}/api/portfolio", headers=headers)
    logger.info("script_output", message=f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        logger.info("script_output", message=f"Cash: ${data.get('cash', 0):,.2f}")
        logger.info("script_output", message=f"Total Value: ${data.get('totalValue', 0):,.2f}")
        logger.info("script_output", message=f"Positions: {len(data.get('positions', []))}")
    else:
        logger.error("script_output", message=f"Error: {response.text}")
    
    # Test 2: Buy stock
    logger.info("script_output", message="\n2. Buying 10 shares of AAPL...")
    buy_data = {
        "ticker": "AAPL",
        "quantity": 10,
        "price": 150.00
    }
    response = requests.post(f"{BASE_URL_PORTFOLIO}/api/portfolio/buy", headers=headers, json=buy_data)
    logger.info("script_output", message=f"Status: {response.status_code}")
    if response.status_code == 200:
        logger.info("script_output", message=f"Response: {response.json()}")
    else:
        logger.error("script_output", message=f"Error: {response.text}")
    
    # Test 3: Get updated portfolio
    logger.info("script_output", message="\n3. Getting updated portfolio...")
    response = requests.get(f"{BASE_URL_PORTFOLIO}/api/portfolio", headers=headers)
    if response.status_code == 200:
        data = response.json()
        logger.info("script_output", message=f"Cash: ${data.get('cash', 0):,.2f}")
        logger.info("script_output", message=f"Total Value: ${data.get('totalValue', 0):,.2f}")
        logger.info("script_output", message=f"Positions: {len(data.get('positions', []))}")
        for pos in data.get('positions', []):
            logger.info("script_output", message=f"  - {pos['ticker']}: {pos['quantity']} shares @ ${pos['avgCostBasis']:.2f}")
    
    # Test 4: Get transactions
    logger.info("script_output", message="\n4. Getting transaction history...")
    response = requests.get(f"{BASE_URL_PORTFOLIO}/api/portfolio/transactions", headers=headers)
    if response.status_code == 200:
        data = response.json()
        logger.info("script_output", message=f"Total transactions: {len(data.get('transactions', []))}")
        for txn in data.get('transactions', [])[:3]:
            logger.info("script_output", message=f"  - {txn['type']} {txn['quantity']} {txn['ticker']} @ ${txn['price']:.2f}")

def test_paper_trading_service():
    """Test Paper Trading Service"""
    logger.info("script_output", message="\n" + "="*60)
    logger.info("script_output", message="TESTING PAPER TRADING SERVICE (Port 8005)")
    logger.info("script_output", message="="*60)
    
    # Test 1: Get account
    logger.info("script_output", message="\n1. Getting paper trading account...")
    response = requests.get(f"{BASE_URL_PAPER}/api/paper/account", headers=headers)
    logger.info("script_output", message=f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        logger.info("script_output", message=f"Cash: ${data.get('cash', 0):,.2f}")
        logger.info("script_output", message=f"Total Value: ${data.get('totalValue', 0):,.2f}")
        logger.info("script_output", message=f"Positions: {len(data.get('positions', []))}")
    else:
        logger.error("script_output", message=f"Error: {response.text}")
    
    # Test 2: Place market buy order
    logger.info("script_output", message="\n2. Placing market buy order for 5 shares of MSFT...")
    import time
    time.sleep(2)  # Small delay to avoid rate limiting
    order_data = {
        "ticker": "MSFT",
        "type": "market",
        "side": "buy",
        "quantity": 5
    }
    response = requests.post(f"{BASE_URL_PAPER}/api/paper/order", headers=headers, json=order_data)
    logger.info("script_output", message=f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        logger.info("script_output", message=f"Order ID: {data.get('orderId')}")
        logger.info("script_output", message=f"Status: {data.get('status')}")
        if data.get('filledPrice'):
            logger.info("script_output", message=f"Filled Price: ${data.get('filledPrice'):.2f}")
        logger.info("script_output", message=f"Message: {data.get('message')}")
    else:
        logger.error("script_output", message=f"Error: {response.text}")
    
    # Test 3: Get updated account
    logger.info("script_output", message="\n3. Getting updated account...")
    response = requests.get(f"{BASE_URL_PAPER}/api/paper/account", headers=headers)
    if response.status_code == 200:
        data = response.json()
        logger.info("script_output", message=f"Cash: ${data.get('cash', 0):,.2f}")
        logger.info("script_output", message=f"Total Value: ${data.get('totalValue', 0):,.2f}")
        logger.info("script_output", message=f"Total P&L: ${data.get('totalPL', 0):,.2f} ({data.get('totalPLPercent', 0):.2f}%)")
        for pos in data.get('positions', []):
            logger.info("script_output", message=f"  - {pos['ticker']}: {pos['quantity']} shares @ ${pos['avgCostBasis']:.2f}")
    
    # Test 4: Get order history
    logger.info("script_output", message="\n4. Getting order history...")
    response = requests.get(f"{BASE_URL_PAPER}/api/paper/orders", headers=headers)
    if response.status_code == 200:
        data = response.json()
        logger.info("script_output", message=f"Total orders: {len(data.get('orders', []))}")
        for order in data.get('orders', [])[:3]:
            logger.info("script_output", message=f"  - {order['side'].upper()} {order['quantity']} {order['ticker']} @ ${order['filledPrice']:.2f}")

def main():
    """Run all tests"""
    logger.info("script_output", message="\n" + "="*60)
    logger.info("script_output", message="PHASE 1 SERVICES TEST SUITE")
    logger.info("script_output", message="="*60)
    
    try:
        test_portfolio_service()
    except Exception as e:
        logger.error("script_output", message=f"\n❌ Portfolio Service Error: {e}")
    
    try:
        test_paper_trading_service()
    except Exception as e:
        logger.error("script_output", message=f"\n❌ Paper Trading Service Error: {e}")
    
    logger.info("script_output", message="\n" + "="*60)
    logger.info("script_output", message="TEST SUITE COMPLETE")
    logger.info("script_output", message="="*60)

if __name__ == "__main__":
    main()

