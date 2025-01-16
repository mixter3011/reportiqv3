import datetime
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from typing import List, Dict
import pandas as pd
import numpy as np


def plot_table_and_pie(df, Holding, xirr, cash_equivalent_value, cash_equivalent_percentage, equity_allocation_percentage):
    Holding = Holding.dropna()
    Holding = Holding.dropna(axis=1)
    Holding = Holding.dropna(how='all')
    
    df_equity = Holding[Holding['Unnamed: 0'] == 'Equity']
    df_debt = Holding[Holding['Unnamed: 0'] == 'Debt']

    df_equity.loc[:, 'Unnamed: 4'] = pd.to_numeric(df_equity['Unnamed: 4'], errors='coerce')
    df_debt.loc[:, 'Unnamed: 4'] = pd.to_numeric(df_debt['Unnamed: 4'], errors='coerce')

    equity_sum = df_equity['Unnamed: 4'].sum()
    debt_sum = df_debt['Unnamed: 4'].sum()

    equity_sum_in_lacs = equity_sum / 100000
    debt_sum_in_lacs = debt_sum / 100000

    df_equity.loc[:, 'Unnamed: 6'] = pd.to_numeric(df_equity['Unnamed: 6'], errors='coerce')
    df_debt.loc[:, 'Unnamed: 6'] = pd.to_numeric(df_debt['Unnamed: 6'], errors='coerce')

    equity_mkt_val = df_equity['Unnamed: 6'].sum()
    debt_mkt_val = df_debt['Unnamed: 6'].sum()

    equity_mkt_val_in_lacs = equity_mkt_val / 100000
    debt_mkt_val_in_lacs = debt_mkt_val / 100000

    total_investment = equity_sum_in_lacs + debt_sum_in_lacs
    total_market_value = equity_mkt_val_in_lacs + debt_mkt_val_in_lacs

    fig = plt.figure(figsize=(15.8, 10))
    ax = fig.add_subplot(111)
    
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    gradient = np.linspace(1, 0.9, 500).reshape(1, -1)
    ax.imshow(
        gradient,
        extent=(0, 1, 0, 1),
        cmap='Blues',
        aspect='auto',
        alpha=0.3
    )

    try:
        logo = plt.imread('logo.png')
        header_img = plt.imread('header.png')
        
        logo_ax = fig.add_axes([0.79, 0.9, 0.2, 0.08])
        logo_ax.imshow(logo)
        logo_ax.axis('off')
        
        header_ax = fig.add_axes([0.02, 0.77, 0.9, 0.3])
        header_ax.imshow(header_img)
        header_ax.axis('off')
    except:
        print("Warning: One or more image files not found")

    current_date = pd.Timestamp.now().strftime('%d-%b-%Y')
    current_time = pd.Timestamp.now().strftime('%I:%M %p')
    
    ax.text(0.11, 0.915, "Holding Summary and Performance", 
            fontsize=28, color='#CD0000',
            weight='light')
    
    ax.text(0.56, 0.92, f"For Period (As On {current_date})",
            fontsize=12, color='#000000',
            weight='normal')
    
    client_info_raw = (
        Holding['Unnamed: 1'].iloc[1]
        if not Holding.empty and 'Unnamed: 1' in Holding.columns and len(Holding) > 1
        else "N/A"
    )
    if '/' in client_info_raw:
        parts = client_info_raw.split('/')
        name = parts[-1]
        id_num = parts[0]
    else:
        name = client_info_raw
        id_num = ""

    asset_data = {
        "Asset Class": [
            "EQUITY", "MULTI ASSET", "DEBT", "ALTERNATE QUOTED", 
            "CASH", "ALTERNATE UNQUOTED", "PORTFOLIO TOTAL"
        ],
        "% of Portfolio": [
            round(equity_allocation_percentage, 2), "-", 
            round(100 - equity_allocation_percentage, 2), "-", "-", "-", 100.00
        ],
        "Investment at Cost": [
            round(equity_sum_in_lacs, 2), "-", round(debt_sum_in_lacs, 2), 
            "-", "-", "-", round(total_investment, 2)
        ],
        "Market Value": [
            round(equity_mkt_val_in_lacs, 2), "-", round(debt_mkt_val_in_lacs, 2), 
            "-", "-", "-", round(total_market_value, 2)
        ]
    }

    asset_df = pd.DataFrame(asset_data)
    
    ax.text(0.05, 0.85, "Investment Summary", 
            fontsize=16, fontweight='bold', color='#000000')
    ax.text(0.52, 0.85, "(Amount in Lacs)", 
            fontsize=12, color='#666666')
    
    ax.add_patch(plt.Rectangle((0.035, 0.85), 0.004, 0.015,
                              facecolor='#CD0000'))
    
    table_ax1 = fig.add_axes([0.05, 0.55, 0.55, 0.25])
    table_ax1.axis('off')
    
    table1 = table_ax1.table(
        cellText=asset_df.values,
        colLabels=asset_df.columns,
        cellLoc='right',
        loc='center',
        bbox=[0, 0, 1, 1],
        colWidths=[0.3, 0.2, 0.25, 0.25]
    )

    table1.auto_set_font_size(False)
    table1.set_fontsize(10)

    for (row, col), cell in table1._cells.items():
        cell.set_edgecolor('black')
        
        if col == 0:  
            cell._loc = 'left' 
        else:
            cell._loc = 'right'  
            
        if row == 0:
            cell.set_facecolor('#E6E6E6')
            cell.set_text_props(weight='bold')
        
        if row == len(asset_df) and col > 0:
            cell.set_facecolor('#E6F3FF')
            
        if row == len(asset_df):
            cell.get_text().set_weight('bold')
    
    ax.text(0.05, 0.5, "Portfolio Snapshot", 
            fontsize=16, fontweight='bold', color='#000000')
    ax.text(0.52, 0.5, "(Amount in Lacs)", 
            fontsize=12, color='#666666')
    
    ax.add_patch(plt.Rectangle((0.035, 0.5), 0.004, 0.015,
                              facecolor='#CD0000'))
    
    table_ax2 = fig.add_axes([0.05, 0.20, 0.55, 0.25])
    table_ax2.axis('off')
    
    table2 = table_ax2.table(
        cellText=asset_df.values,
        colLabels=asset_df.columns,
        cellLoc='right',
        loc='center',
        bbox=[0, 0, 1, 1],
        colWidths=[0.3, 0.2, 0.25, 0.25]
    )

    table2.auto_set_font_size(False)
    table2.set_fontsize(10)

    for (row, col), cell in table2._cells.items():
        cell.set_edgecolor('black')
        
        if col == 0:  
            cell._loc = 'left'  
        else:
            cell._loc = 'right'  
            
        if row == 0:
            cell.set_facecolor('#E6E6E6')
            cell.set_text_props(weight='bold')
        
        if row == len(asset_df) and col > 0:
            cell.set_facecolor('#E6F3FF')
            
        if row == len(asset_df):
            cell.get_text().set_weight('bold')

    footer_text = (
        "This document is not valid without disclosure, Please refer to the last page for the disclaimer. | "
        "Strictly Private & Confidential.\n"
        f"Incase of any query / feedback on the report, please write to query@motilaloswal.com. | "
        f"Generated Date & Time : {current_date} & {current_time}"
    )
    ax.text(
        0.5, 0.02, footer_text,
        horizontalalignment='center',
        fontsize=10,
        color='#2F4F4F',
        wrap=True
    )

    return fig


def plot_combined_table(dataframes: List[pd.DataFrame], raw_sums: List[Dict[str, float]], ax):
    combined_df = pd.concat(dataframes, ignore_index=True)

    if raw_sums:
        grand_totals = {}
        for col in ['Quantity', 'Buy Price', 'CMP', 'PandL', 'Market Value']:
            total = sum(sums.get(col, 0) for sums in raw_sums)
            if total != 0:
                grand_totals[col] = total

        formatted_grand_totals = {col: f"{value:,.2f}" for col, value in grand_totals.items()}

        grand_total_data = []
        for col in combined_df.columns:
            if col == 'Category':
                grand_total_data.append("Grand Total")
            elif col == 'Instrument Name':
                grand_total_data.append("")
            elif col in formatted_grand_totals:
                grand_total_data.append(formatted_grand_totals[col])
            else:
                grand_total_data.append("")

        grand_total_row = pd.DataFrame([grand_total_data], columns=combined_df.columns)
        combined_df = pd.concat([combined_df, grand_total_row], ignore_index=True)

    ax.axis('tight')
    ax.axis('off')
    table = ax.table(
        cellText=combined_df.values,
        colLabels=combined_df.columns,
        loc='center',
        cellLoc='center',
        colLoc='center'
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)

    for key, cell in table._cells.items():
        if key[1] == 1:
            cell.set_width(0.30)
        else:
            cell.set_width(0.15)
        cell.set_height(0.12)
        cell.set_text_props(weight='normal')

        if key[0] > 0:
            cell_text = str(combined_df.iloc[key[0]-1, 0])
            if "Total" in cell_text:
                cell.set_facecolor('#f0f0f0')
                cell.set_text_props(weight='bold')

        if key[0] == 0:
            cell.set_text_props(weight='bold')

    return table

def create_fno_table_and_graph(df):
    df_cleaned = df.drop(columns=['Order'], errors='ignore')
    df_sorted = df_cleaned.sort_values(by='FNO Profits Till Date', ascending=True)

    total_profit = df_sorted['FNO Profits Till Date'].iloc[-1]
    avg_profit = df_sorted['FNO Profits'].mean()

    fig, (ax_table, ax_text, ax_graph) = plt.subplots(
        3, 1, figsize=(12, 14), height_ratios=[2, 0.3, 2], gridspec_kw={'hspace': 0.3}
    )

    ax_table.axis('tight')
    ax_table.axis('off')
    table = ax_table.table(
        cellText=df_sorted.values,
        colLabels=df_sorted.columns,
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    ax_table.set_title("FNO Data Table", pad=20)

    ax_text.axis('off')
    ax_text.text(0.1, 0.5, f"Total FNO Profit: {total_profit:,.2f}", fontsize=12, weight='bold')
    ax_text.text(0.1, 0.1, f"Average FNO Profit: {avg_profit:,.2f}", fontsize=12, weight='bold')

    ax_graph.plot(
        df_sorted['Month'],
        df_sorted['FNO Profits Till Date'],
        marker='o',
        linewidth=2,
        markersize=8
    )
    ax_graph.set_xlabel("Month")
    ax_graph.set_ylabel("FNO Profits Till Date")
    ax_graph.grid(True, linestyle='--', alpha=0.7)
    ax_graph.tick_params(axis='x', rotation=45)

    return fig
