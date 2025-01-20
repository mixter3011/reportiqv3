import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_table_and_pie(Holding, equity_allocation_percentage):
    Holding = Holding.dropna()
    Holding = Holding.dropna(axis=1)
    Holding = Holding.dropna(how='all')
    
    df_equity = Holding[Holding['Unnamed: 0'] == 'Equity']
    df_debt = Holding[Holding['Unnamed: 0'] == 'Debt']

    df_equity.loc[:, 'Unnamed: 4'] = pd.to_numeric(df_equity['Unnamed: 4'], errors='coerce')
    df_debt.loc[:, 'Unnamed: 4'] = pd.to_numeric(df_debt['Unnamed: 4'], errors='coerce')
    df_equity.loc[:, 'Unnamed: 6'] = pd.to_numeric(df_equity['Unnamed: 6'], errors='coerce')
    df_debt.loc[:, 'Unnamed: 6'] = pd.to_numeric(df_debt['Unnamed: 6'], errors='coerce')
    df_equity.loc[:, 'Unnamed: 11'] = pd.to_numeric(df_equity['Unnamed: 11'], errors='coerce')
    df_debt.loc[:, 'Unnamed: 11'] = pd.to_numeric(df_debt['Unnamed: 11'], errors='coerce')
    df_equity.loc[:, 'Unnamed: 13'] = pd.to_numeric(df_equity['Unnamed: 13'], errors='coerce')
    df_debt.loc[:, 'Unnamed: 13'] = pd.to_numeric(df_debt['Unnamed: 13'], errors='coerce')

    equity_sum = df_equity['Unnamed: 4'].sum()
    debt_sum = df_debt['Unnamed: 4'].sum()
    equity_mkt_val = df_equity['Unnamed: 6'].sum()
    debt_mkt_val = df_debt['Unnamed: 6'].sum()
    equity_dividend = df_equity['Unnamed: 11'].sum()
    debt_dividend = df_debt['Unnamed: 11'].sum()
    equity_gl = df_equity['Unnamed: 13'].sum()
    debt_gl = df_debt['Unnamed: 13'].sum()

    equity_sum_in_lacs = equity_sum / 100000
    debt_sum_in_lacs = debt_sum / 100000
    equity_mkt_val_in_lacs = equity_mkt_val / 100000
    debt_mkt_val_in_lacs = debt_mkt_val / 100000
    equity_dividend_in_lacs = equity_dividend / 100000
    debt_dividend_in_lacs = debt_dividend / 100000

    total_investment = equity_sum_in_lacs + debt_sum_in_lacs
    total_market_value = equity_mkt_val_in_lacs + debt_mkt_val_in_lacs
    total_dividend = equity_dividend_in_lacs + debt_dividend_in_lacs
    total_gl = equity_gl + debt_gl

    fig = plt.figure(figsize=(15.8, 10))
    ax = fig.add_subplot(111)
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    gradient = np.linspace(1, 0.9, 500).reshape(1, -1)
    ax.imshow(gradient, extent=(0, 1, 0, 1), cmap='Blues', aspect='auto', alpha=0.3)

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
            fontsize=28, color='#CD0000', weight='light')
    ax.text(0.56, 0.92, f"For Period (As On {current_date})",
            fontsize=12, color='#000000', weight='normal')

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
        ],
        "Dividend Since Inception": [
            round(equity_dividend_in_lacs, 2), "-", round(debt_dividend_in_lacs, 2),
            "-", "-", "-", round(total_dividend, 2)
        ],
        "Unrealised G/L %": [
            round(equity_gl, 2), "-", round(debt_gl, 2),
            "-", "-", "-", round(total_gl, 2)
        ]
    }

    asset_df = pd.DataFrame(asset_data)

    ax.text(0.05, 0.85, "Investment Summary", 
            fontsize=16, fontweight='bold', color='#000000')
    ax.text(0.52, 0.85, "(Amount in Lacs)", 
            fontsize=12, color='#666666')
    ax.add_patch(plt.Rectangle((0.035, 0.85), 0.004, 0.015,
                              facecolor='#CD0000'))

    table_ax1 = fig.add_axes([0.05, 0.48, 0.55, 0.35])
    table_ax1.axis('off')
    
    table1 = table_ax1.table(
        cellText=asset_df[asset_df.columns[:4]].values,
        colLabels=asset_df.columns[:4],
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

    pie_ax = fig.add_axes([0.65, 0.48, 0.3, 0.35])
    
    portfolio_data = list(zip(asset_data['Asset Class'], asset_data['% of Portfolio']))
    portfolio_data = [(asset, float(pct)) for asset, pct in portfolio_data 
                     if pct != '-' and asset != 'PORTFOLIO TOTAL']
    
    labels = [item[0] for item in portfolio_data]
    sizes = [item[1] for item in portfolio_data]
    colors = {'EQUITY': 'orange', 'DEBT': 'darkgreen', 'CASH': 'cyan'}
    pie_colors = [colors[label] for label in labels]
    
    wedges, texts, autotexts = pie_ax.pie(sizes, 
                                         colors=pie_colors,
                                         autopct='%1.1f%%',
                                         startangle=90)
    
    pie_ax.axis('equal')
    plt.setp(autotexts, size=9, weight="bold")
    
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                 markerfacecolor=colors[label], label=label, markersize=10)
                      for label in labels]
    
    pie_ax.legend(handles=legend_elements,
                 loc='center left',
                 bbox_to_anchor=(0.9, 0.5),
                 title='Asset Classes',
                 title_fontsize=10,
                 fontsize=9)
    
    pie_ax.set_title("Portfolio Allocation", pad=20, fontsize=12, fontweight='bold')

    ax.text(0.05, 0.44, "Portfolio Snapshot", 
            fontsize=16, fontweight='bold', color='#000000')
    ax.text(0.52, 0.44, "(Amount in Lacs)", 
            fontsize=12, color='#666666')
    ax.add_patch(plt.Rectangle((0.035, 0.44), 0.004, 0.015,
                              facecolor='#CD0000'))

    table_ax2 = fig.add_axes([0.05, 0.06, 0.9, 0.35])
    table_ax2.axis('off')
    
    table2 = table_ax2.table(
        cellText=asset_df.values,
        colLabels=asset_df.columns,
        cellLoc='right',
        loc='center',
        bbox=[0, 0, 1, 1],
        colWidths=[0.2, 0.15, 0.15, 0.15, 0.15, 0.2]
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


def create_holdings_summary(equity_file, debt_file, holding_df):
    fig = plt.figure(figsize=(15.8, 10))
    ax = fig.add_subplot(111)
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    gradient = np.linspace(1, 0.9, 500).reshape(1, -1)
    ax.imshow(gradient, extent=(0, 1, 0, 1), cmap='Blues', aspect='auto', alpha=0.3)
    
    current_date = pd.Timestamp.now().strftime('%d-%b-%Y')
    current_time = pd.Timestamp.now().strftime('%I:%M %p')
    
    ax.text(0.11, 0.915, 'Holding Summary and Performance', 
            color='#CD0000', fontsize=28, fontweight='light')
    ax.text(0.56, 0.92, f"For Period (As On {current_date})",
            fontsize=12, color='#000000', weight='normal')
    
    ax.text(0.05, 0.77, "Productwise Performance", 
            fontsize=16, fontweight='bold', color='#000000')
    ax.text(0.83, 0.77, "(Amount in Lacs)", 
            fontsize=12, color='#666666')
    ax.add_patch(plt.Rectangle((0.035, 0.77), 0.004, 0.015,
                                facecolor='#CD0000'))
    
    try:
        logo = plt.imread('logo.png')
        header = plt.imread('header.png')
        
        logo_ax = fig.add_axes([0.79, 0.9, 0.2, 0.08])
        logo_ax.imshow(logo)
        logo_ax.axis('off')
        
        header_ax = fig.add_axes([0.02, 0.77, 0.9, 0.3])
        header_ax.imshow(header)
        header_ax.axis('off')
    except:
        print("Warning: Image files not found")
    
    summary_tables = []
    for df, category_label in [(equity_file, 'Equity'), (debt_file, 'Debt')]:
        temp_summary = pd.DataFrame()
        for category in df['Category'].unique():
            category_data = df[df['Category'] == category]
            numeric_cols = category_data.select_dtypes(include=['number']).columns
            summary_row = category_data[numeric_cols].sum().to_frame().T
            summary_row.insert(0, 'Category', category)
            temp_summary = pd.concat([temp_summary, summary_row], ignore_index=True)
        summary_tables.append(temp_summary)
    
    combined_summary = pd.concat(summary_tables, ignore_index=True)
    combined_summary = combined_summary.drop(columns=['PandL', 'CMP', 'Quantity', 'Type'], errors='ignore')
    numeric_cols = combined_summary.select_dtypes(include=['number']).columns
    combined_summary[numeric_cols] = combined_summary[numeric_cols].apply(lambda x: (x / 1000).round(2))
    combined_summary = combined_summary.rename(columns={
        'Category': 'Asset Class',
        'Buy Price': 'Investment at Cost'
    })
    
    combined_summary['Dividend Since Inception'] = '-'  
    combined_summary['Unrealised G/L %'] = '-'

    combined_summary['Asset Class'] = combined_summary['Asset Class'].str.upper()
    
    if 'Market Value' in numeric_cols:
        combined_summary['Market Value'] = combined_summary['Market Value'].apply(lambda x: round(x, 3))
    combined_summary['Unrealised G/L %'] = combined_summary['Unrealised G/L %'].round(2)
    
    total_row = pd.DataFrame(combined_summary.select_dtypes(include=['number']).sum()).T
    total_row.insert(0, 'Asset Class', 'TOTAL')
    total_row['Dividend Since Inception'] = '-'
    if 'Market Value' in numeric_cols:
        total_row['Market Value'] = round(total_row['Market Value'].iloc[0], 2)  
    total_row['Unrealised G/L %'] = '-'  
    combined_summary = pd.concat([combined_summary, total_row], ignore_index=True)
    
    table_ax = fig.add_axes([0.03, 0.25, 0.9, 0.5])
    table_ax.axis('off')
    
    table = table_ax.table(
        cellText=combined_summary.values,
        colLabels=combined_summary.columns,
        cellLoc='center',
        loc='center',
        bbox=[0, 0, 1, 1]
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(combined_summary.columns))))
    
    for (row, col), cell in table._cells.items():
        cell.set_edgecolor('black')
        if row == 0:  
            cell.set_facecolor('#E6E6E6')
            cell.set_text_props(weight='bold')
        elif row == len(combined_summary):  
            cell.set_facecolor('#ADD8E6')  
            cell.set_text_props(weight='bold')
        elif 'Market Value' in combined_summary.columns and col == combined_summary.columns.get_loc('Market Value'):
            if row != len(combined_summary) - 1:  
                cell.get_text().set_text(f"{float(cell.get_text().get_text()):.3f}")
    
    current_time = pd.Timestamp.now()
    footer_text = (
        "This document is not valid without disclosure, Please refer to the last page for the disclaimer. | "
        "Strictly Private & Confidential.\n"
        f"Incase of any query / feedback on the report, please write to query@motilaloswal.com. | "
        f"Generated Date & Time : {current_time.strftime('%d-%b-%Y')} & {current_time.strftime('%I:%M %p')}"
    )
    
    ax.text(0.5, 0.02, footer_text,
            horizontalalignment='center',
            fontsize=10,
            color='#2F4F4F',
            wrap=True)
    
    return fig

def create_portfolio_table(df):
    target_stocks = [
        "Bajaj Finserv Ltd",
        "Central Depository Services (India) Ltd",
        "HDFC Bank Ltd",
        "IDFC First Bank Ltd",
        "Kotak Mahindra Bank Ltd",
        "Shriram Finance Ltd",
    ]
    
    equity_data = []
    equity_section = False
    for idx, row in df.iterrows():
        if isinstance(row['Unnamed: 0'], str) and 'Equity' in row['Unnamed: 0']:
            equity_section = True
            continue
        if equity_section and isinstance(row['Unnamed: 0'], str) and any(stock in row['Unnamed: 0'] for stock in target_stocks):
            equity_data.append(row.tolist())
        if equity_section and isinstance(row['Unnamed: 0'], str) and 'Total' in row['Unnamed: 0']:
            equity_section = False
    
    cols = [
        "Instrument Name", "Quantity", "Purchase Price", "Purchase Value",
        "Market Price", "Market Value", "ST Qty", "ST G/L", "LT Qty", "LT G/L",
        "Unrealised Gain/Loss", "Unrealised Gain/Loss %", "ISIN", "Unused_1", "Unused_2"
    ]
    equity = pd.DataFrame(equity_data, columns=df.columns)
    equity.columns = cols
    
    if target_stocks:
        equity = equity[equity["Instrument Name"].isin(target_stocks)]
    
    display_cols = [
        "Instrument Name", "Quantity", "Purchase Price", "Purchase Value",
        "Market Price", "Market Value", "Unrealised Gain/Loss",
        "Unrealised Gain/Loss %", "ISIN"
    ]
    
    fig = plt.figure(figsize=(15.8, 10))
    ax = fig.add_subplot(111)
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    gradient = np.linspace(1, 0.9, 500).reshape(1, -1)
    ax.imshow(gradient, extent=(0, 1, 0, 1), cmap='Blues', aspect='auto', alpha=0.3)
    
    current_date = pd.Timestamp.now().strftime('%d-%b-%Y')
    current_time = pd.Timestamp.now().strftime('%I:%M %p')
    
    ax.text(0.11, 0.915, 'Detailed Holdings and Performance', 
            color='#CD0000', fontsize=28, fontweight='light')
    ax.text(0.56, 0.92, f"For Period (As On {current_date})",
            fontsize=12, color='#000000', weight='normal')
    
    ax.text(0.05, 0.77, "Equity - ", 
            fontsize=16, fontweight='bold', color='#CD0000')
    ax.text(0.12, 0.77, "Direct Equity", 
            fontsize=16, fontweight='light', color='#666666')
    ax.text(0.83, 0.77, "(Amount in Lacs)", 
            fontsize=12, color='#666666')
    ax.add_patch(plt.Rectangle((0.035, 0.77), 0.004, 0.015,
                              facecolor='#CD0000'))
    
    try:
        logo = plt.imread('logo.png')
        logo_ax = fig.add_axes([0.79, 0.9, 0.2, 0.08])
        logo_ax.imshow(logo)
        logo_ax.axis('off')
            
        header = plt.imread('header.png')
        header_ax = fig.add_axes([0.02, 0.77, 0.9, 0.3])
        header_ax.imshow(header)
        header_ax.axis('off')
    except Exception as e:
        print(f"Warning: Image loading error: {e}")
    
    table_data = equity[display_cols].values.tolist()
    
    table_ax = fig.add_axes([0.03, 0.25, 0.94, 0.5])
    table_ax.axis('off')
    
    table = table_ax.table(
        cellText=table_data,
        colLabels=display_cols,
        cellLoc='center',
        loc='center',
        bbox=[0, 0, 1, 1]
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    
    col_widths = [0.25] + [0.09375] * (len(display_cols) - 1)
    for i, width in enumerate(col_widths):
        table.auto_set_column_width([i])
    
    for (row, col), cell in table._cells.items():
        cell.set_edgecolor('black')
        
        if row == 0:
            cell.set_facecolor('#E6E6E6')
            cell.set_text_props(weight='bold')
        
        if col == 0 and row != 0:
            cell._loc = 'left'
            
        if row > 0 and col in [6, 7]:  
            text = cell.get_text().get_text()
            if text.startswith('(') or (text.replace('.','').replace('-','').isdigit() and float(text) < 0):
                cell.get_text().set_color('red')
    
    footer_text = (
        "This document is not valid without disclosure, Please refer to the last page for the disclaimer. | "
        "Strictly Private & Confidential.\n"
        f"Incase of any query / feedback on the report, please write to query@motilaloswal.com. | "
        f"Generated Date & Time : {current_date} & {current_time}"
    )
    
    ax.text(0.5, 0.02, footer_text,
            horizontalalignment='center',
            fontsize=10,
            color='#2F4F4F',
            wrap=True)
    
    return fig

def analyze_fno_holdings(df):
    fno_start = df[df.iloc[:, 0] == 'FnO:-'].index[0]
    fno_end = df[df.iloc[:, 0] == 'Currency:-'].index[0]
    
    fno_data = df.iloc[fno_start+1:fno_end-4].copy()
    fno_data.columns = fno_data.iloc[0]
    fno_data = fno_data.iloc[1:]
    fno_data = fno_data.reset_index(drop=True)
    fno_data = fno_data.dropna(subset=['Instrument Name'])
    
    fig = plt.figure(figsize=(15.8, 10))
    ax = fig.add_subplot(111)
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    gradient = np.linspace(1, 0.9, 500).reshape(1, -1)
    ax.imshow(gradient, extent=(0, 1, 0, 1), cmap='Blues', aspect='auto', alpha=0.3)
    
    current_date = pd.Timestamp.now().strftime('%d-%b-%Y')
    current_time = pd.Timestamp.now().strftime('%I:%M %p')
    
    ax.text(0.11, 0.915, 'Detailed Holdings and Performance', 
            color='#CD0000', fontsize=28, fontweight='light')
    ax.text(0.56, 0.92, f"For Period (As On {current_date})",
            fontsize=12, color='#000000', weight='normal')
    
    ax.text(0.05, 0.77, "Derivatives", 
            fontsize=16, fontweight='bold', color='#000000')
    ax.text(0.83, 0.77, "(Amount in Lacs)", 
            fontsize=12, color='#666666')
    ax.add_patch(plt.Rectangle((0.035, 0.77), 0.004, 0.015,
                              facecolor='#CD0000'))
    
    try:
        logo = plt.imread('logo.png')
        logo_ax = fig.add_axes([0.79, 0.9, 0.2, 0.08])
        logo_ax.imshow(logo)
        logo_ax.axis('off')
            
        header = plt.imread('header.png')
        header_ax = fig.add_axes([0.02, 0.77, 0.9, 0.3])
        header_ax.imshow(header)
        header_ax.axis('off')
    except Exception as e:
        print(f"Warning: Image loading error: {e}")
    
    columns = [
        'Instrument Name', 'B/S', 'Quantity', 'Rate', 'Value',
        'Market Price', 'Market Value', 'UnrealisedGain/Loss',
        'Unrealised Gain/Loss%'
    ]
    
    table_ax = fig.add_axes([0.03, 0.25, 0.94, 0.5])
    table_ax.axis('off')
    
    table = table_ax.table(
        cellText=fno_data[columns].values,
        colLabels=columns,
        cellLoc='center',
        loc='center',
        bbox=[0, 0, 1, 1]
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    
    col_widths = [0.25] + [0.09375] * (len(columns) - 1)
    for i, width in enumerate(col_widths):
        table.auto_set_column_width([i])
    
    for (row, col), cell in table._cells.items():
        cell.set_edgecolor('black')
        
        if row == 0:
            cell.set_facecolor('#E6E6E6')
            cell.set_text_props(weight='bold')
        
        if col == 0 and row != 0:
            cell._loc = 'left'
            
        if row > 0 and col in [7, 8]:  
            text = cell.get_text().get_text()
            if text.startswith('(') or (text.replace('.','').replace('-','').isdigit() and float(text) < 0):
                cell.get_text().set_color('red')
    
    footer_text = (
        "This document is not valid without disclosure, Please refer to the last page for the disclaimer. | "
        "Strictly Private & Confidential.\n"
        f"Incase of any query / feedback on the report, please write to query@motilaloswal.com. | "
        f"Generated Date & Time : {current_date} & {current_time}"
    )
    
    ax.text(0.5, 0.02, footer_text,
            horizontalalignment='center',
            fontsize=10,
            color='#2F4F4F',
            wrap=True)
    
    return fig

def eqmf(df):
    eq_strt = df[df.iloc[:, 0] == 'Mutual Fund:-'].index[0]
    eq_end = df[df.iloc[:, 0] == 'FnO:-'].index[0]
    
    eq_data = df.iloc[eq_strt+1:eq_end-4].copy()
    eq_data.columns = eq_data.iloc[0]
    eq_data = eq_data.iloc[1:]
    eq_data = eq_data.reset_index(drop=True)
    eq_data = eq_data[~eq_data['Asset Type'].isin(['Debt']) & ~eq_data['Asset Type'].isna()]
    
    fig = plt.figure(figsize=(15.8, 10))
    ax = fig.add_subplot(111)
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    gradient = np.linspace(1, 0.9, 500).reshape(1, -1)
    ax.imshow(gradient, extent=(0, 1, 0, 1), cmap='Blues', aspect='auto', alpha=0.3)
    
    current_date = pd.Timestamp.now().strftime('%d-%b-%Y')
    current_time = pd.Timestamp.now().strftime('%I:%M %p')

    ax.text(0.11, 0.915, 'Detailed Holdings and Performance', 
            color='#CD0000', fontsize=28, fontweight='light')
    ax.text(0.56, 0.92, f"For Period (As On {current_date})",
            fontsize=12, color='#000000', weight='normal')
    
    ax.text(0.05, 0.77, "Equity - ", 
            fontsize=16, fontweight='bold', color='#CD0000')
    ax.text(0.12, 0.77, "Mutual Fund", 
            fontsize=16, fontweight='light', color='#666666')
    ax.text(0.83, 0.77, "(Amount in Lacs)", 
            fontsize=12, color='#666666')
    ax.add_patch(plt.Rectangle((0.035, 0.77), 0.004, 0.015,
                              facecolor='#CD0000'))
    
    try:
        logo = plt.imread('logo.png')
        logo_ax = fig.add_axes([0.79, 0.9, 0.2, 0.08])
        logo_ax.imshow(logo)
        logo_ax.axis('off')
            
        header = plt.imread('header.png')
        header_ax = fig.add_axes([0.02, 0.77, 0.9, 0.3])
        header_ax.imshow(header)
        header_ax.axis('off')
    except Exception as e:
        print(f"Warning: Image loading error: {e}")
        
    
    columns = [
        'Scheme Name', 'Units', 'Purchase NAV', 'Purchase Value', 'Current NAV',
        'Market Value', 'ST Qty', 'ST G/L', 'LT Qty', 'LT G/L', 'Dividend','Unrealised GainLoss',
        'Unrealised GainLoss Per'
    ]        

    table_ax = fig.add_axes([0.03, 0.25, 0.94, 0.5])
    table_ax.axis('off')
    
    table = table_ax.table(
        cellText=eq_data[columns].values,
        colLabels=columns,
        cellLoc='center',
        loc='center',
        bbox=[0, 0, 1, 1]
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    
    col_widths = [0.25] + [0.09375] * (len(columns) - 1)
    for i, width in enumerate(col_widths):
        table.auto_set_column_width([i])
    
    for (row, col), cell in table._cells.items():
        cell.set_edgecolor('black')
        
        if row == 0:
            cell.set_facecolor('#E6E6E6')
            cell.set_text_props(weight='bold')
        
        if col == 0 and row != 0:
            cell._loc = 'left'
            
        if row > 0 and col in [7, 8]:  
            text = cell.get_text().get_text()
            if text.startswith('(') or (text.replace('.','').replace('-','').isdigit() and float(text) < 0):
                cell.get_text().set_color('red')
    
    footer_text = (
        "This document is not valid without disclosure, Please refer to the last page for the disclaimer. | "
        "Strictly Private & Confidential.\n"
        f"Incase of any query / feedback on the report, please write to query@motilaloswal.com. | "
        f"Generated Date & Time : {current_date} & {current_time}"
    )
    
    ax.text(0.5, 0.02, footer_text,
            horizontalalignment='center',
            fontsize=10,
            color='#2F4F4F',
            wrap=True)
    
    return fig

def dmf(df):
    d_strt = df[df.iloc[:, 0] == 'Mutual Fund:-'].index[0]
    d_end = df[df.iloc[:, 0] == 'FnO:-'].index[0]
    
    d_data = df.iloc[d_strt+1:d_end-4].copy()
    d_data.columns = d_data.iloc[0]
    d_data = d_data.iloc[1:]
    d_data = d_data.reset_index(drop=True)
    d_data = d_data[~d_data['Asset Type'].isin(['Equity']) & ~d_data['Asset Type'].isna()]
    
    fig = plt.figure(figsize=(15.8, 10))
    ax = fig.add_subplot(111)
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    gradient = np.linspace(1, 0.9, 500).reshape(1, -1)
    ax.imshow(gradient, extent=(0, 1, 0, 1), cmap='Blues', aspect='auto', alpha=0.3)
    
    current_date = pd.Timestamp.now().strftime('%d-%b-%Y')
    current_time = pd.Timestamp.now().strftime('%I:%M %p')

    ax.text(0.11, 0.915, 'Detailed Holdings and Performance', 
            color='#CD0000', fontsize=28, fontweight='light')
    ax.text(0.56, 0.92, f"For Period (As On {current_date})",
            fontsize=12, color='#000000', weight='normal')
    
    ax.text(0.05, 0.77, "Debt - ", 
            fontsize=16, fontweight='bold', color='#CD0000')
    ax.text(0.12, 0.77, "Mutual Fund", 
            fontsize=16, fontweight='light', color='#666666')
    ax.text(0.83, 0.77, "(Amount in Lacs)", 
            fontsize=12, color='#666666')
    ax.add_patch(plt.Rectangle((0.035, 0.77), 0.004, 0.015,
                              facecolor='#CD0000'))
    
    try:
        logo = plt.imread('logo.png')
        logo_ax = fig.add_axes([0.79, 0.9, 0.2, 0.08])
        logo_ax.imshow(logo)
        logo_ax.axis('off')
            
        header = plt.imread('header.png')
        header_ax = fig.add_axes([0.02, 0.77, 0.9, 0.3])
        header_ax.imshow(header)
        header_ax.axis('off')
    except Exception as e:
        print(f"Warning: Image loading error: {e}")
        
    
    columns = [
        'Scheme Name', 'Units', 'Purchase NAV', 'Purchase Value', 'Current NAV',
        'Market Value', 'ST Qty', 'ST G/L', 'LT Qty', 'LT G/L', 'Dividend','Unrealised GainLoss',
        'Unrealised GainLoss Per'
    ]        

    table_ax = fig.add_axes([0.03, 0.25, 0.94, 0.5])
    table_ax.axis('off')
    
    table = table_ax.table(
        cellText=d_data[columns].values,
        colLabels=columns,
        cellLoc='center',
        loc='center',
        bbox=[0, 0, 1, 1]
    )
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    
    col_widths = [0.25] + [0.09375] * (len(columns) - 1)
    for i, width in enumerate(col_widths):
        table.auto_set_column_width([i])
    
    for (row, col), cell in table._cells.items():
        cell.set_edgecolor('black')
        
        if row == 0:
            cell.set_facecolor('#E6E6E6')
            cell.set_text_props(weight='bold')
        
        if col == 0 and row != 0:
            cell._loc = 'left'
            
        if row > 0 and col in [7, 8]:  
            text = cell.get_text().get_text()
            if text.startswith('(') or (text.replace('.','').replace('-','').isdigit() and float(text) < 0):
                cell.get_text().set_color('red')
    
    footer_text = (
        "This document is not valid without disclosure, Please refer to the last page for the disclaimer. | "
        "Strictly Private & Confidential.\n"
        f"Incase of any query / feedback on the report, please write to query@motilaloswal.com. | "
        f"Generated Date & Time : {current_date} & {current_time}"
    )
    
    ax.text(0.5, 0.02, footer_text,
            horizontalalignment='center',
            fontsize=10,
            color='#2F4F4F',
            wrap=True)
    
    return fig
    