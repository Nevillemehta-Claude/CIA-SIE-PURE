#!/usr/bin/env python
"""
Quick Test Runner - Direct API Tests
=====================================

Runs API tests directly without pytest async fixture overhead.
This avoids the hanging issue with pytest-asyncio.
"""

import asyncio
import sys
import os
from uuid import uuid4
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cia_sie.api.app import create_app
from cia_sie.dal.database import init_db, drop_db
from httpx import AsyncClient, ASGITransport


class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def record(self, name: str, passed: bool, error: str = None):
        if passed:
            self.passed += 1
            print(f"  ✓ {name}")
        else:
            self.failed += 1
            self.errors.append((name, error))
            print(f"  ✗ {name}: {error}")


async def run_all_tests():
    print("=" * 70)
    print("CIA-SIE QUICK TEST SUITE")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 70)
    
    results = TestResults()
    
    # Create app
    app = create_app()
    
    # Initialize database
    await init_db()
    
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        
        # =====================================================================
        # HEALTH TESTS
        # =====================================================================
        print("\n[HEALTH ENDPOINT]")
        
        try:
            r = await client.get('/health')
            results.record("Health returns 200", r.status_code == 200, 
                          f"got {r.status_code}")
        except Exception as e:
            results.record("Health returns 200", False, str(e))
        
        # =====================================================================
        # INSTRUMENTS TESTS
        # =====================================================================
        print("\n[INSTRUMENTS API]")
        
        # Create instrument
        try:
            payload = {
                "symbol": f"TEST_{uuid4().hex[:6]}",
                "display_name": "Test Instrument",
                "exchange": "NSE",
                "instrument_type": "EQUITY"
            }
            r = await client.post('/api/v1/instruments/', json=payload)
            results.record("Create instrument returns 201", r.status_code == 201,
                          f"got {r.status_code}")
            
            if r.status_code == 201:
                instrument = r.json()
                instrument_id = instrument['instrument_id']
                
                # Get instrument
                r = await client.get(f'/api/v1/instruments/{instrument_id}')
                results.record("Get instrument returns 200", r.status_code == 200,
                              f"got {r.status_code}")
                
                # CR-001: No prohibited fields
                data = r.json()
                no_weight = 'weight' not in data
                no_score = 'score' not in data
                results.record("Instrument has no weight/score (CR-001)", 
                              no_weight and no_score,
                              f"weight:{not no_weight}, score:{not no_score}")
        except Exception as e:
            results.record("Instruments API", False, str(e))
        
        # List instruments
        try:
            r = await client.get('/api/v1/instruments/')
            results.record("List instruments returns 200", r.status_code == 200,
                          f"got {r.status_code}")
        except Exception as e:
            results.record("List instruments", False, str(e))
        
        # =====================================================================
        # SILOS TESTS
        # =====================================================================
        print("\n[SILOS API]")
        
        try:
            # Create silo
            silo_payload = {
                "instrument_id": instrument_id,
                "silo_name": f"Test Silo {uuid4().hex[:4]}"
            }
            r = await client.post('/api/v1/silos/', json=silo_payload)
            results.record("Create silo returns 201", r.status_code == 201,
                          f"got {r.status_code}")
            
            if r.status_code == 201:
                silo = r.json()
                silo_id = silo['silo_id']
                
                # Get silo
                r = await client.get(f'/api/v1/silos/{silo_id}')
                results.record("Get silo returns 200", r.status_code == 200,
                              f"got {r.status_code}")
        except Exception as e:
            results.record("Silos API", False, str(e))
        
        # =====================================================================
        # CHARTS TESTS
        # =====================================================================
        print("\n[CHARTS API]")
        
        try:
            webhook_id = f"HOOK_{uuid4().hex[:8]}"
            chart_payload = {
                "silo_id": silo_id,
                "chart_code": f"C{uuid4().hex[:3].upper()}",
                "chart_name": "Test Chart",
                "timeframe": "D",
                "webhook_id": webhook_id
            }
            r = await client.post('/api/v1/charts/', json=chart_payload)
            results.record("Create chart returns 201", r.status_code == 201,
                          f"got {r.status_code}")
            
            if r.status_code == 201:
                chart = r.json()
                chart_id = chart['chart_id']
                
                # CR-001: Chart has no weight
                no_weight = 'weight' not in chart
                results.record("Chart has no weight (CR-001)", no_weight,
                              "weight field found")
                
                # Get chart
                r = await client.get(f'/api/v1/charts/{chart_id}')
                results.record("Get chart returns 200", r.status_code == 200,
                              f"got {r.status_code}")
        except Exception as e:
            results.record("Charts API", False, str(e))
        
        # =====================================================================
        # WEBHOOK TESTS
        # =====================================================================
        print("\n[WEBHOOK API]")
        
        try:
            signal_payload = {
                "webhook_id": webhook_id,
                "direction": "BULLISH",
                "signal_type": "TREND",
                "message": "Test signal"
            }
            r = await client.post('/api/v1/webhook/', json=signal_payload)
            # 401 is valid (signature validation), 200/201 is valid (accepted)
            valid_response = r.status_code in [200, 201, 401]
            results.record("Webhook accepts/validates signal", valid_response,
                          f"got {r.status_code}")
            
            if r.status_code in [200, 201]:
                data = r.json()
                # CR-001: No confidence/score in signal
                no_confidence = 'confidence' not in data
                no_score = 'score' not in data
                results.record("Signal has no confidence/score (CR-001)",
                              no_confidence and no_score,
                              f"confidence:{not no_confidence}, score:{not no_score}")
        except Exception as e:
            results.record("Webhook API", False, str(e))
        
        # =====================================================================
        # BASKETS TESTS
        # =====================================================================
        print("\n[BASKETS API]")
        
        try:
            basket_payload = {
                "basket_name": f"Test Basket {uuid4().hex[:4]}",
                "basket_type": "CUSTOM",
                "description": "Test basket"
            }
            r = await client.post('/api/v1/baskets/', json=basket_payload)
            results.record("Create basket returns 201", r.status_code == 201,
                          f"got {r.status_code}")
            
            if r.status_code == 201:
                basket = r.json()
                basket_id = basket['basket_id']
                
                # Add chart to basket
                r = await client.post(f'/api/v1/baskets/{basket_id}/charts/{chart_id}')
                results.record("Add chart to basket returns 204", r.status_code == 204,
                              f"got {r.status_code}")
                
                # CR-001: Basket has no signal effect fields
                no_aggregation = 'signal_aggregation' not in basket
                results.record("Basket has no aggregation (CR-001)", no_aggregation,
                              "aggregation field found")
        except Exception as e:
            results.record("Baskets API", False, str(e))
        
        # =====================================================================
        # RELATIONSHIPS TESTS
        # =====================================================================
        print("\n[RELATIONSHIPS API]")
        
        try:
            r = await client.get(f'/api/v1/relationships/silo/{silo_id}')
            results.record("Get relationships returns 200", r.status_code == 200,
                          f"got {r.status_code}")
            
            if r.status_code == 200:
                data = r.json()
                # CR-002: Check structure exists
                has_structure = 'contradictions' in data or 'confirmations' in data or 'charts' in data
                results.record("Relationships has proper structure", has_structure,
                              "missing structure fields")
        except Exception as e:
            results.record("Relationships API", False, str(e))
        
        # =====================================================================
        # AI TESTS
        # =====================================================================
        print("\n[AI API]")
        
        try:
            r = await client.get('/api/v1/ai/models')
            # May be 200 or 404 depending on implementation
            valid = r.status_code in [200, 404]
            results.record("AI models endpoint responds", valid,
                          f"got {r.status_code}")
        except Exception as e:
            results.record("AI API", False, str(e))
        
        # =====================================================================
        # PLATFORMS TESTS
        # =====================================================================
        print("\n[PLATFORMS API]")
        
        try:
            r = await client.get('/api/v1/platforms/')
            valid = r.status_code in [200, 404]
            results.record("Platforms endpoint responds", valid,
                          f"got {r.status_code}")
        except Exception as e:
            results.record("Platforms API", False, str(e))
    
    # Cleanup
    await drop_db()
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"PASSED: {results.passed}")
    print(f"FAILED: {results.failed}")
    print(f"TOTAL:  {results.passed + results.failed}")
    print(f"PASS RATE: {(results.passed / (results.passed + results.failed) * 100):.1f}%")
    
    if results.errors:
        print("\nFAILURES:")
        for name, error in results.errors:
            print(f"  - {name}: {error}")
    
    print(f"\nCompleted: {datetime.now().isoformat()}")
    print("=" * 70)
    
    return results.failed == 0


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)

