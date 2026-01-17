#!/usr/bin/env python3
"""
CIA-SIE Sample Data Seeding Script
===================================
Creates comprehensive sample data for Visual QA testing.

This script populates the database with:
- 5 Instruments (NIFTY, BANKNIFTY, GOLD, CRUDE, FINNIFTY)
- 5 Silos (one per instrument)
- 15 Charts (3 per silo with different timeframes)
- 5 Analytical Baskets
- 50+ Signals (with contradictions for testing)
"""

import sqlite3
import uuid
from datetime import datetime, timedelta
import json
import random

DB_PATH = "data/cia_sie.db"

def generate_uuid():
    return str(uuid.uuid4())

def now():
    return datetime.utcnow().isoformat()

def past_time(minutes_ago):
    return (datetime.utcnow() - timedelta(minutes=minutes_ago)).isoformat()

def main():
    print("═══════════════════════════════════════════════════════════════")
    print("         CIA-SIE SAMPLE DATA SEEDING")
    print("═══════════════════════════════════════════════════════════════")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Clear existing data
    print("\n[1/6] Clearing existing data...")
    tables_to_clear = ['signals', 'basket_charts', 'charts', 'analytical_baskets', 'silos', 'instruments']
    for table in tables_to_clear:
        cursor.execute(f"DELETE FROM {table}")
    conn.commit()
    print("      ✅ All tables cleared")
    
    # Create Instruments
    print("\n[2/6] Creating Instruments...")
    instruments = [
        (generate_uuid(), "NIFTY50", "NIFTY 50 Index", now(), now(), True, json.dumps({"exchange": "NSE", "type": "INDEX"})),
        (generate_uuid(), "BANKNIFTY", "Bank NIFTY Index", now(), now(), True, json.dumps({"exchange": "NSE", "type": "INDEX"})),
        (generate_uuid(), "GOLD", "Gold Futures", now(), now(), True, json.dumps({"exchange": "MCX", "type": "COMMODITY"})),
        (generate_uuid(), "CRUDE", "Crude Oil Futures", now(), now(), True, json.dumps({"exchange": "MCX", "type": "COMMODITY"})),
        (generate_uuid(), "FINNIFTY", "Financial Services Index", now(), now(), True, json.dumps({"exchange": "NSE", "type": "INDEX"})),
    ]
    cursor.executemany(
        "INSERT INTO instruments (instrument_id, symbol, display_name, created_at, updated_at, is_active, metadata_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
        instruments
    )
    conn.commit()
    print(f"      ✅ Created {len(instruments)} instruments")
    
    instrument_map = {inst[1]: inst[0] for inst in instruments}  # symbol -> id
    
    # Create Silos
    print("\n[3/6] Creating Silos...")
    silos = []
    for symbol, inst_id in instrument_map.items():
        silo_id = generate_uuid()
        silos.append((
            silo_id,
            inst_id,
            f"{symbol} Primary Silo",
            True,  # heartbeat_enabled
            15,    # heartbeat_frequency_min
            5,     # current_threshold_min
            30,    # recent_threshold_min
            60,    # stale_threshold_min
            now(),
            now(),
            True
        ))
    
    cursor.executemany(
        """INSERT INTO silos (silo_id, instrument_id, silo_name, heartbeat_enabled, 
           heartbeat_frequency_min, current_threshold_min, recent_threshold_min, 
           stale_threshold_min, created_at, updated_at, is_active) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        silos
    )
    conn.commit()
    print(f"      ✅ Created {len(silos)} silos")
    
    silo_map = {s[2].replace(" Primary Silo", ""): s[0] for s in silos}  # symbol -> silo_id
    
    # Create Charts (3 per silo - 15m, 1h, D)
    # NOTE: Timeframe pattern is case-sensitive: ^(1m|5m|15m|30m|1h|4h|D|W|M)$
    print("\n[4/6] Creating Charts...")
    charts = []
    timeframes = ["15m", "1h", "D"]  # Valid: lowercase h, uppercase D/W/M
    chart_names = ["Momentum", "Trend", "Volume Profile"]
    
    for symbol, silo_id in silo_map.items():
        for i, (tf, name) in enumerate(zip(timeframes, chart_names)):
            chart_id = generate_uuid()
            charts.append((
                chart_id,
                silo_id,
                f"{symbol}_{tf}_{name[:3].upper()}",
                f"{symbol} {name} ({tf})",
                tf,
                f"wh_{symbol.lower()}_{tf.lower()}_{i+1}",
                now(),
                now(),
                True
            ))
    
    cursor.executemany(
        """INSERT INTO charts (chart_id, silo_id, chart_code, chart_name, timeframe, 
           webhook_id, created_at, updated_at, is_active) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        charts
    )
    conn.commit()
    print(f"      ✅ Created {len(charts)} charts")
    
    chart_ids = [c[0] for c in charts]
    
    # Create Analytical Baskets
    # Valid BasketType values: LOGICAL, HIERARCHICAL, CONTEXTUAL, CUSTOM
    print("\n[5/6] Creating Analytical Baskets...")
    baskets = [
        (generate_uuid(), "Index Momentum", "LOGICAL", "Tracks momentum across NIFTY indices", instrument_map["NIFTY50"], now(), now(), True),
        (generate_uuid(), "Commodity Watch", "CONTEXTUAL", "Monitors GOLD and CRUDE signals", instrument_map["GOLD"], now(), now(), True),
        (generate_uuid(), "Intraday Scalping", "HIERARCHICAL", "15-minute scalping signals", instrument_map["BANKNIFTY"], now(), now(), True),
        (generate_uuid(), "Swing Trading", "LOGICAL", "Daily timeframe swing setups", instrument_map["NIFTY50"], now(), now(), True),
        (generate_uuid(), "Volatility Monitor", "CUSTOM", "Cross-asset volatility signals", instrument_map["FINNIFTY"], now(), now(), True),
    ]
    
    cursor.executemany(
        """INSERT INTO analytical_baskets (basket_id, basket_name, basket_type, description, 
           instrument_id, created_at, updated_at, is_active) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        baskets
    )
    conn.commit()
    print(f"      ✅ Created {len(baskets)} analytical baskets")
    
    # Link some charts to baskets
    basket_charts = []
    for basket in baskets[:3]:  # Link first 3 baskets
        selected_charts = random.sample(chart_ids, 3)
        for chart_id in selected_charts:
            basket_charts.append((basket[0], chart_id, now()))
    
    cursor.executemany(
        "INSERT INTO basket_charts (basket_id, chart_id, added_at) VALUES (?, ?, ?)",
        basket_charts
    )
    conn.commit()
    print(f"      ✅ Linked {len(basket_charts)} chart-basket associations")
    
    # Create Signals (with intentional contradictions)
    print("\n[6/6] Creating Signals with Contradictions...")
    signals = []
    signal_types = ["MOMENTUM", "TREND", "REVERSAL", "BREAKOUT"]
    directions = ["LONG", "SHORT", "NEUTRAL"]
    
    # Generate signals for each chart
    for chart in charts:
        chart_id = chart[0]
        num_signals = random.randint(3, 6)
        
        for _ in range(num_signals):
            signal_id = generate_uuid()
            minutes_ago = random.randint(1, 120)
            signals.append((
                signal_id,
                chart_id,
                past_time(minutes_ago),
                past_time(minutes_ago + random.randint(0, 5)),
                random.choice(signal_types),
                random.choice(directions),
                json.dumps({
                    "rsi": round(random.uniform(20, 80), 2),
                    "macd": round(random.uniform(-10, 10), 2),
                    "volume_ratio": round(random.uniform(0.5, 2.5), 2),
                    "atr": round(random.uniform(0.5, 3.0), 2)
                }),
                json.dumps({
                    "source": "TradingView",
                    "confidence": round(random.uniform(0.6, 0.95), 2)
                })
            ))
    
    # Add specific contradictions for NIFTY charts (LONG vs SHORT at same time)
    nifty_charts = [c for c in charts if "NIFTY50" in c[3]]
    if len(nifty_charts) >= 2:
        contradiction_time = past_time(10)  # 10 minutes ago
        
        # LONG signal on Chart 1
        signals.append((
            generate_uuid(),
            nifty_charts[0][0],
            contradiction_time,
            contradiction_time,
            "TREND",
            "LONG",
            json.dumps({"rsi": 65, "macd": 5.2, "note": "Bullish breakout"}),
            json.dumps({"source": "TradingView", "confidence": 0.85})
        ))
        
        # SHORT signal on Chart 2 (CONTRADICTION)
        signals.append((
            generate_uuid(),
            nifty_charts[1][0],
            contradiction_time,
            contradiction_time,
            "TREND",
            "SHORT",
            json.dumps({"rsi": 35, "macd": -4.8, "note": "Bearish reversal"}),
            json.dumps({"source": "TradingView", "confidence": 0.82})
        ))
        
        print("      ⚡ Added intentional LONG/SHORT contradiction for NIFTY50")
    
    cursor.executemany(
        """INSERT INTO signals (signal_id, chart_id, received_at, signal_timestamp, 
           signal_type, direction, indicators, raw_payload) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        signals
    )
    conn.commit()
    print(f"      ✅ Created {len(signals)} signals")
    
    # Final Summary
    print("\n═══════════════════════════════════════════════════════════════")
    print("                    SEEDING COMPLETE")
    print("═══════════════════════════════════════════════════════════════")
    
    # Verify counts
    for table in ['instruments', 'silos', 'charts', 'analytical_baskets', 'signals', 'basket_charts']:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table:20} : {count:4} records ✅")
    
    conn.close()
    print("\n═══════════════════════════════════════════════════════════════")
    print("  Database is now populated and ready for Visual QA")
    print("═══════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    main()

