import matplotlib.pyplot as plt

def create_pie_chart(df):
    """Creates and returns a Matplotlib pie chart figure of spending by category."""
    category_spending = df.groupby('Category')['Amount'].sum()
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(category_spending, labels=category_spending.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    return fig

def create_monthly_bar_chart(df):
    """Creates and returns a Matplotlib bar chart figure of monthly spending."""
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_spending = df.groupby('Month')['Amount'].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    monthly_spending.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Amount (₹)")
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    return fig

def create_daily_bar_chart(df):
    """Creates and returns a Matplotlib bar chart figure of daily spending."""
    daily_spending = df.groupby(df['Date'].dt.date)['Amount'].sum()
    fig, ax = plt.subplots(figsize=(10, 6))
    daily_spending.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Amount (₹)")
    ax.tick_params(axis='x', rotation=90)
    plt.tight_layout()
    return fig