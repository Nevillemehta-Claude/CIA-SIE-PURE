#!/usr/bin/env python3
"""
Gold Correlation Analysis: XAU/USD vs GOLDBEES
Institutional-grade visualization with dual-axis overlay
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Headless mode - no display
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path

# Set style for institutional-grade aesthetics
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'SF Pro Display'
plt.rcParams['axes.facecolor'] = '#0d1117'
plt.rcParams['figure.facecolor'] = '#0d1117'
plt.rcParams['axes.edgecolor'] = '#30363d'
plt.rcParams['axes.labelcolor'] = '#c9d1d9'
plt.rcParams['text.color'] = '#c9d1d9'
plt.rcParams['xtick.color'] = '#8b949e'
plt.rcParams['ytick.color'] = '#8b949e'
plt.rcParams['grid.color'] = '#21262d'
plt.rcParams['grid.alpha'] = 0.5

# Load data
print("Loading XAU/USD data...")
xau_df = pd.read_csv('/Users/nevillemehta/Desktop/OANDA_XAUUSD, 60.csv')
xau_df['time'] = pd.to_datetime(xau_df['time'], utc=True)
xau_df['time'] = xau_df['time'].dt.tz_localize(None)  # Remove timezone for comparison
xau_df = xau_df.set_index('time')

print("Loading GOLDBEES data...")
goldbees_df = pd.read_csv('/Users/nevillemehta/Desktop/NSE_GOLDBEES, 1D (1).csv')
goldbees_df['time'] = pd.to_datetime(goldbees_df['time'])
goldbees_df = goldbees_df.set_index('time')

# Resample XAU/USD to daily for comparison
xau_daily = xau_df.resample('D').agg({
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last'
}).dropna()

# Align date ranges
common_start = max(xau_daily.index.min(), goldbees_df.index.min())
common_end = min(xau_daily.index.max(), goldbees_df.index.max())

xau_aligned = xau_daily[common_start:common_end]
goldbees_aligned = goldbees_df[common_start:common_end]

# Merge on common dates
merged = pd.merge(
    xau_aligned[['close']].rename(columns={'close': 'XAU_USD'}),
    goldbees_aligned[['close']].rename(columns={'close': 'GOLDBEES'}),
    left_index=True,
    right_index=True,
    how='inner'
)

print(f"Merged data: {len(merged)} common trading days")
print(f"Date range: {merged.index.min()} to {merged.index.max()}")

# Calculate correlation
correlation = merged['XAU_USD'].corr(merged['GOLDBEES'])
print(f"\nCorrelation coefficient: {correlation:.4f}")

# Normalize for overlay comparison (percentage change from start)
merged['XAU_USD_norm'] = (merged['XAU_USD'] / merged['XAU_USD'].iloc[0] - 1) * 100
merged['GOLDBEES_norm'] = (merged['GOLDBEES'] / merged['GOLDBEES'].iloc[0] - 1) * 100

# Calculate rolling correlation (5-day window)
merged['rolling_corr'] = merged['XAU_USD'].rolling(window=5).corr(merged['GOLDBEES'])

# ============================================================================
# FIGURE 1: Main Correlation Chart with Dual Axis
# ============================================================================
fig, axes = plt.subplots(3, 1, figsize=(16, 14), height_ratios=[3, 1.5, 1])
fig.suptitle('GOLD CORRELATION ANALYSIS\nXAU/USD vs NSE:GOLDBEES', 
             fontsize=20, fontweight='bold', color='#f0f6fc', y=0.98)

# --- Top Panel: Dual Axis Price Overlay ---
ax1 = axes[0]
ax2 = ax1.twinx()

# XAU/USD on left axis
color_xau = '#ffd700'  # Gold color
line1 = ax1.plot(merged.index, merged['XAU_USD'], color=color_xau, linewidth=2.5, 
                  label='XAU/USD (Spot Gold)', zorder=3)
ax1.fill_between(merged.index, merged['XAU_USD'].min() * 0.99, merged['XAU_USD'], 
                  alpha=0.1, color=color_xau)
ax1.set_ylabel('XAU/USD ($)', color=color_xau, fontsize=12, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=color_xau)
ax1.set_ylim(merged['XAU_USD'].min() * 0.98, merged['XAU_USD'].max() * 1.02)

# GOLDBEES on right axis
color_bees = '#00d4aa'  # Teal/cyan
line2 = ax2.plot(merged.index, merged['GOLDBEES'], color=color_bees, linewidth=2.5, 
                  label='GOLDBEES (₹)', linestyle='--', zorder=2)
ax2.fill_between(merged.index, merged['GOLDBEES'].min() * 0.99, merged['GOLDBEES'], 
                  alpha=0.1, color=color_bees)
ax2.set_ylabel('GOLDBEES (₹)', color=color_bees, fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor=color_bees)
ax2.set_ylim(merged['GOLDBEES'].min() * 0.98, merged['GOLDBEES'].max() * 1.02)

# Add data points
ax1.scatter(merged.index, merged['XAU_USD'], color=color_xau, s=50, zorder=4, alpha=0.8)
ax2.scatter(merged.index, merged['GOLDBEES'], color=color_bees, s=50, zorder=4, alpha=0.8)

# Correlation annotation
corr_color = '#58a6ff' if correlation > 0.7 else '#f85149'
ax1.annotate(f'Correlation: {correlation:.2%}', 
             xy=(0.02, 0.95), xycoords='axes fraction',
             fontsize=16, fontweight='bold', color=corr_color,
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#161b22', edgecolor=corr_color, alpha=0.9))

# Legend
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper right', facecolor='#161b22', edgecolor='#30363d', fontsize=11)

ax1.set_title('Price Overlay (Dual Axis)', fontsize=14, color='#8b949e', pad=10)
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=2))

# --- Middle Panel: Normalized Performance Comparison ---
ax3 = axes[1]
ax3.plot(merged.index, merged['XAU_USD_norm'], color=color_xau, linewidth=2, label='XAU/USD % Change')
ax3.plot(merged.index, merged['GOLDBEES_norm'], color=color_bees, linewidth=2, label='GOLDBEES % Change', linestyle='--')
ax3.axhline(y=0, color='#8b949e', linestyle='-', linewidth=0.5, alpha=0.5)
ax3.fill_between(merged.index, 0, merged['XAU_USD_norm'], alpha=0.2, color=color_xau)
ax3.fill_between(merged.index, 0, merged['GOLDBEES_norm'], alpha=0.2, color=color_bees)

ax3.set_ylabel('% Change from Start', fontsize=11)
ax3.set_title('Normalized Performance Comparison', fontsize=14, color='#8b949e', pad=10)
ax3.legend(loc='upper left', facecolor='#161b22', edgecolor='#30363d')
ax3.grid(True, alpha=0.3)
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

# Add final values
final_xau = merged['XAU_USD_norm'].iloc[-1]
final_bees = merged['GOLDBEES_norm'].iloc[-1]
ax3.annotate(f'+{final_xau:.1f}%', xy=(merged.index[-1], final_xau), 
             xytext=(10, 0), textcoords='offset points', color=color_xau, fontweight='bold')
ax3.annotate(f'+{final_bees:.1f}%', xy=(merged.index[-1], final_bees), 
             xytext=(10, 0), textcoords='offset points', color=color_bees, fontweight='bold')

# --- Bottom Panel: Rolling Correlation ---
ax4 = axes[2]
ax4.plot(merged.index, merged['rolling_corr'], color='#a371f7', linewidth=2)
ax4.fill_between(merged.index, 0, merged['rolling_corr'], alpha=0.3, color='#a371f7')
ax4.axhline(y=0.8, color='#3fb950', linestyle='--', linewidth=1, alpha=0.7, label='Strong (0.8)')
ax4.axhline(y=0.5, color='#d29922', linestyle='--', linewidth=1, alpha=0.7, label='Moderate (0.5)')
ax4.axhline(y=0, color='#8b949e', linestyle='-', linewidth=0.5, alpha=0.5)

ax4.set_ylabel('Rolling Correlation', fontsize=11)
ax4.set_xlabel('Date', fontsize=11)
ax4.set_title('5-Day Rolling Correlation', fontsize=14, color='#8b949e', pad=10)
ax4.set_ylim(-0.2, 1.1)
ax4.legend(loc='lower right', facecolor='#161b22', edgecolor='#30363d', fontsize=9)
ax4.grid(True, alpha=0.3)
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

plt.tight_layout()
plt.subplots_adjust(top=0.93)

# Save the figure
output_path = '/Users/nevillemehta/Downloads/CIA-SIE-PURE/docs/gold_correlation_analysis.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
print(f"\nChart saved to: {output_path}")

# ============================================================================
# FIGURE 2: Scatter Plot with Regression
# ============================================================================
fig2, ax5 = plt.subplots(figsize=(10, 10))
fig2.suptitle('XAU/USD vs GOLDBEES\nScatter Correlation Analysis', 
              fontsize=18, fontweight='bold', color='#f0f6fc', y=0.96)

# Scatter plot
scatter = ax5.scatter(merged['XAU_USD'], merged['GOLDBEES'], 
                       c=range(len(merged)), cmap='plasma', s=100, alpha=0.8, zorder=3)

# Regression line
z = np.polyfit(merged['XAU_USD'], merged['GOLDBEES'], 1)
p = np.poly1d(z)
x_line = np.linspace(merged['XAU_USD'].min(), merged['XAU_USD'].max(), 100)
ax5.plot(x_line, p(x_line), color='#f85149', linewidth=2, linestyle='--', 
         label=f'Regression: y = {z[0]:.4f}x + {z[1]:.2f}', zorder=2)

# Colorbar for time progression
cbar = plt.colorbar(scatter, ax=ax5, pad=0.02)
cbar.set_label('Trading Days (Earlier → Later)', color='#c9d1d9')
cbar.ax.yaxis.set_tick_params(color='#8b949e')

# Labels and formatting
ax5.set_xlabel('XAU/USD ($)', fontsize=12, fontweight='bold')
ax5.set_ylabel('GOLDBEES (₹)', fontsize=12, fontweight='bold')
ax5.grid(True, alpha=0.3)
ax5.legend(loc='upper left', facecolor='#161b22', edgecolor='#30363d', fontsize=11)

# Correlation annotation
ax5.annotate(f'R = {correlation:.4f}\nR² = {correlation**2:.4f}', 
             xy=(0.95, 0.05), xycoords='axes fraction',
             fontsize=14, fontweight='bold', color='#58a6ff',
             ha='right', va='bottom',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#161b22', edgecolor='#58a6ff', alpha=0.9))

# Add date labels for first and last points
ax5.annotate(f'{merged.index[0].strftime("%b %d")}', 
             xy=(merged['XAU_USD'].iloc[0], merged['GOLDBEES'].iloc[0]),
             xytext=(-30, -20), textcoords='offset points',
             fontsize=9, color='#8b949e',
             arrowprops=dict(arrowstyle='->', color='#8b949e', alpha=0.5))
ax5.annotate(f'{merged.index[-1].strftime("%b %d")}', 
             xy=(merged['XAU_USD'].iloc[-1], merged['GOLDBEES'].iloc[-1]),
             xytext=(10, 10), textcoords='offset points',
             fontsize=9, color='#8b949e',
             arrowprops=dict(arrowstyle='->', color='#8b949e', alpha=0.5))

plt.tight_layout()
plt.subplots_adjust(top=0.92)

output_path2 = '/Users/nevillemehta/Downloads/CIA-SIE-PURE/docs/gold_scatter_correlation.png'
plt.savefig(output_path2, dpi=150, bbox_inches='tight', facecolor='#0d1117')
print(f"Scatter chart saved to: {output_path2}")

# ============================================================================
# Print Summary Statistics
# ============================================================================
print("\n" + "="*60)
print("CORRELATION ANALYSIS SUMMARY")
print("="*60)
print(f"\n📊 Data Overview:")
print(f"   • Common trading days: {len(merged)}")
print(f"   • Date range: {merged.index.min().strftime('%Y-%m-%d')} to {merged.index.max().strftime('%Y-%m-%d')}")

print(f"\n📈 Price Statistics:")
print(f"   XAU/USD:")
print(f"   • Start: ${merged['XAU_USD'].iloc[0]:,.2f}")
print(f"   • End:   ${merged['XAU_USD'].iloc[-1]:,.2f}")
print(f"   • Change: {final_xau:+.2f}%")

print(f"\n   GOLDBEES:")
print(f"   • Start: ₹{merged['GOLDBEES'].iloc[0]:.2f}")
print(f"   • End:   ₹{merged['GOLDBEES'].iloc[-1]:.2f}")
print(f"   • Change: {final_bees:+.2f}%")

print(f"\n🔗 Correlation Metrics:")
print(f"   • Pearson Correlation (R): {correlation:.4f}")
print(f"   • R-squared (R²): {correlation**2:.4f}")
print(f"   • Interpretation: {'VERY STRONG' if correlation > 0.9 else 'STRONG' if correlation > 0.7 else 'MODERATE'}")

print(f"\n📐 Regression Equation:")
print(f"   GOLDBEES = {z[0]:.6f} × XAU/USD + {z[1]:.4f}")
print(f"   (For every $1 move in XAU/USD, GOLDBEES moves ₹{z[0]:.4f})")

# Implied GOLDBEES levels
print(f"\n🎯 Implied GOLDBEES Targets (based on regression):")
xau_targets = [4650, 4700, 4750, 4800]
for target in xau_targets:
    implied_bees = p(target)
    print(f"   If XAU/USD = ${target:,} → GOLDBEES ≈ ₹{implied_bees:.2f}")

print("\n" + "="*60)
print("Charts saved successfully!")
print("="*60)

# Done - charts saved (no display in headless mode)
print("\n✅ All charts generated successfully!")
