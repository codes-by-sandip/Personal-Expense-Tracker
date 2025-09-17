import streamlit as st
import pandas as pd
from datetime import datetime

# Import functions from the new modules
from data_manager import get_expenses, add_expense_to_csv, generate_report_data, get_dataframe, delete_expense
from charts import create_pie_chart, create_monthly_bar_chart, create_daily_bar_chart

# --- Streamlit UI ---

st.set_page_config(page_title="Personal Expense Tracker", layout="wide")
st.title("💸 Personal Expense Tracker")

# Using tabs to organize the UI, including the new 'Delete Record' tab
tab1, tab2, tab3, tab4 = st.tabs(["Add Expense", "View & Reports", "Dashboard", "Delete Record"])

# Tab 1: Add Expense
with tab1:
    st.header("Add a New Expense")
    with st.form("expense_form", clear_on_submit=True):
        date = st.date_input("Date", datetime.now().date())
        amount = st.number_input("Amount (₹)", min_value=1.0, format="%.2f")
        category = st.text_input("Category")
        payment_method = st.selectbox("Payment Method", ("Cash", "UPI", "Card", "Bank Transfer"))

        submitted = st.form_submit_button("Add Expense")
        if submitted:
            if add_expense_to_csv(date, amount, category, payment_method):
                st.success("Expense added successfully!")
            else:
                st.error("There was an error saving the expense.")

# Tab 2: View & Reports
with tab2:
    st.header("Reports & History")
    
    # Sub-tabs within Tab 2
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["Expense Table", "Spending Report", "Daily Expenses"])
    
    # Sub-tab 1: Expense Table
    with sub_tab1:
        st.subheader("All Expenses")
        expenses_data = get_expenses()
        if expenses_data:
            df_display = pd.DataFrame(expenses_data, columns=['Date', 'Amount', 'Category', 'Payment Method'])
            st.dataframe(df_display)
        else:
            st.info("No expenses found. Please add one in the 'Add Expense' tab.")
            
    # Sub-tab 2: Spending Report
    with sub_tab2:
        st.subheader("Spending Report by Category")
        report_data = generate_report_data()
        if report_data:
            report_df = pd.DataFrame(report_data, columns=['Category', 'Total Amount'])
            st.dataframe(report_df)
        else:
            st.info("No expenses to generate a report.")
    
    # Sub-tab 3: Daily Expenses
    with sub_tab3:
        st.subheader("Daily Expenses")
        st.write("View expenses for a specific date.")
        
        selected_date = st.date_input("Select a Date", datetime.now().date())
        
        # Get DataFrame and filter by date
        df = get_dataframe()
        if not df.empty:
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            daily_expenses = df[df['Date'] == selected_date]
            
            if not daily_expenses.empty:
                st.dataframe(daily_expenses)
                st.write(f"Total spending on {selected_date}: {daily_expenses['Amount'].sum():.2f} Rupee")
            else:
                st.info(f"No expenses found for {selected_date}.")
        else:
            st.info("No data available to filter. Please add expenses first.")

# Tab 3: Dashboard (The new, professional dashboard)
with tab3:
    st.header("Your Spending Insights")
    df = get_dataframe()

    if not df.empty:
        # --- Filters ---
        st.subheader("Filter Your Data")
        
        # Using columns to arrange filters horizontally
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            df['Date'] = pd.to_datetime(df['Date'])
            min_date = df['Date'].min().date()
            max_date = df['Date'].max().date()
            start_date, end_date = st.date_input(
                "Select a Date Range",
                [min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
        
        with filter_col2:
            all_categories = sorted(df['Category'].unique())
            selected_categories = st.multiselect(
                "Select Category(s)",
                all_categories,
                default=all_categories
            )

        with filter_col3:
            all_methods = sorted(df['Payment Method'].unique())
            selected_methods = st.multiselect(
                "Select Payment Method(s)",
                all_methods,
                default=all_methods
            )

        # Apply filters to the DataFrame
        filtered_df = df[
            (df['Date'].dt.date >= start_date) & 
            (df['Date'].dt.date <= end_date) & 
            (df['Category'].isin(selected_categories)) & 
            (df['Payment Method'].isin(selected_methods))
        ]

        # --- Main Dashboard Content ---
        if filtered_df.empty:
            st.warning("No data matches the selected filters. Please adjust your selections.")
        else:
            # --- Key Metrics (KPIs) ---
            st.subheader("Quick Summary")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                total_expenses = filtered_df['Amount'].sum()
                st.metric("Total Expenses", f"₹{total_expenses:,.2f}")

            with col2:
                num_days = (end_date - start_date).days + 1
                avg_daily_spending = total_expenses / num_days
                st.metric("Avg. Daily Spending", f"₹{avg_daily_spending:,.2f}")
                
            with col3:
                most_common_category = filtered_df['Category'].mode()[0]
                st.metric("Most Common Category", most_common_category)
                
            with col4:
                total_transactions = filtered_df.shape[0]
                st.metric("Total Transactions", total_transactions)

            # --- Visualizations ---

            st.subheader("Detailed Spending Visualizations")
            
            vis_col1, vis_col2 = st.columns([1, 1])

            with vis_col1:
                st.subheader("Daily Spending Trend")
                st.markdown("*(View how your spending changes day-to-day)*")
                fig_bar = create_daily_bar_chart(filtered_df)
                st.pyplot(fig_bar) 
            
            with vis_col2:
                st.subheader("Monthly Spending Trend")
                st.markdown("*(Analyze your total spending for each month)*")
                fig_monthly = create_monthly_bar_chart(filtered_df)
                st.pyplot(fig_monthly)

            st.divider()

            st.subheader("Spending by Category")
            st.markdown("*(Percentage breakdown of your spending across different categories)*")
            fig_pie = create_pie_chart(filtered_df)
            st.pyplot(fig_pie)

    else:
        st.info("No data available to create visualizations. Please add some expenses first.")

# Tab 4: Delete Record
with tab4:
    st.header("Delete an Expense Record")
    st.write("Select a date to view and delete specific records.")

    df_to_delete = get_dataframe()

    if not df_to_delete.empty:
        # Use a date input to select a specific day
        selected_date = st.date_input("Select a Date to delete from:", datetime.now().date())

        # Filter the DataFrame for the selected date
        df_to_delete['Date'] = pd.to_datetime(df_to_delete['Date']).dt.date
        daily_expenses = df_to_delete[df_to_delete['Date'] == selected_date]

        if not daily_expenses.empty:
            st.subheader(f"Expenses on {selected_date}")
            # Display the filtered daily expenses
            st.dataframe(daily_expenses.reset_index(drop=True), use_container_width=True)

            # Get the actual index from the original dataframe to delete the record
            original_indices = daily_expenses.index.tolist()
            
            # Use a number input for the index of the row to delete
            index_to_delete = st.number_input(
                "Enter the row number to delete (starts from 0):",
                min_value=0,
                max_value=len(daily_expenses) - 1,
                step=1,
                key="daily_delete_index_input"
            )

            if st.button("Delete Selected Record", key="daily_delete_button"):
                # Use the actual original index for deletion
                if delete_expense(df_to_delete, original_indices[index_to_delete]):
                    st.success("Record deleted successfully!")
                    st.rerun()
                else:
                    st.error("Error: Could not delete the record. Please check the row number.")
        else:
            st.info(f"No expenses found for {selected_date}.")
    else:
        st.info("No expenses available to delete.")