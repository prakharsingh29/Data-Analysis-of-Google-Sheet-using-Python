import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

# File uploader for CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

st.title("Linear Analysis")

# Check if a file is uploaded
if uploaded_file is not None:
    # Load data from the uploaded file
    df = pd.read_csv(uploaded_file)

    

    # Display data preview
    st.write("### Data Preview")
    st.dataframe(df.head())

    # Descriptive statistics
    st.write("### Descriptive Statistics")
    st.write(df.describe())

    # Convert 'Created Date' to datetime and set it as the index
    df['Created Date'] = pd.to_datetime(df['Created Date'])
    df.set_index('Created Date', inplace=True)

    # Chart 1: Tasks by Client (Bar Chart)
    st.write("### Tasks by Client")
    tasks_by_client = df['Client'].value_counts()
    st.bar_chart(tasks_by_client)

    # Chart 2: Tasks by Type (Bar Chart)
    st.write("### Tasks by Type")
    tasks_by_type = df['Format'].value_counts()
    st.bar_chart(tasks_by_type)

    # Chart 3: Tasks by Status (Pie Chart)
    st.write("### Tasks by Status")
    tasks_by_status = df['Status'].value_counts()
    fig = px.pie(tasks_by_status, values=tasks_by_status, names=tasks_by_status.index, title='Tasks by Status')
    st.plotly_chart(fig)

    # Chart 4: Task volume over time
    st.write("### Task Volume Over Time")
    volume_over_time = df.resample('M').size()
    st.line_chart(volume_over_time)

    # Chart 5: Top Clients Over Time (Line Chart)
    st.write("### Top Clients Over Time")
    # Get the top 5 clients
    top_clients = tasks_by_client.head(5).index

# Filter the DataFrame for the top clients
    top_clients_over_time = df[df['Client'].isin(top_clients)]

# Group by 'Client' and frequency ('M' for monthly) and get the count of tasks
    top_clients_over_time = top_clients_over_time.groupby(['Client', pd.Grouper(freq='M')]).size().unstack().fillna(0)

# Plot the line chart
    st.line_chart(top_clients_over_time)

    # Chart 6: Client Workload Over Time (Line Chart)
    st.write("### Client Workload Over Time")

# Group by 'Client' and frequency ('M' for monthly) and get the count of tasks
    client_workload_over_time = df.groupby(['Client', pd.Grouper(freq='M')]).size().unstack().fillna(0)

# Plot the line chart
    st.line_chart(client_workload_over_time)

# Chart 7: Format Overview Over Time (Bar Chart)
    st.write("### Format Overview Over Time")

# Group by format and frequency ('M' for monthly) and get the count of tasks
    format_overview_over_time = df.groupby(['Format', pd.Grouper(freq='M')]).size().unstack().fillna(0)

# Plot the bar chart
    st.bar_chart(format_overview_over_time)



# Chart 8: Client vs Format - Grouped Bar Chart
    st.write("### Client vs Format - Grouped Bar Chart")
    chart_client_vs_format = alt.Chart(df).mark_bar().encode(
        alt.X('Client:N', title='Client'),
        alt.Y('count()', title='Number of Tasks'),
        alt.Color('Format:N', title='Task Type'),
        tooltip=['Client', 'Format', 'count()']
    ).interactive()
    st.altair_chart(chart_client_vs_format, use_container_width=True)

# Chart 9: Client Workload - Bar Chart
    st.write("### Client Workload - Bar Chart")
    chart_client_workload = alt.Chart(df).mark_bar().encode(
        alt.X('Client:N', title='Client'),
        alt.Y('count():Q', title='Number of Tasks'),
        tooltip=['Client', 'count()']
    ).interactive()
    st.altair_chart(chart_client_workload, use_container_width=True)

# Chart 10: Cross-reference with Client - Stacked Bar Chart
    st.write("### Cross-referenced: Number of Tasks by Format and Client")
    chart_formats_client = alt.Chart(df).mark_bar().encode(
        alt.X('Client:N', title='Client'),
        alt.Y('count():Q', title='Number of Tasks'),
        alt.Color('Format:N', title='Output Format'),
        tooltip=['Client', 'Format', 'count()']
    ).interactive()
    st.altair_chart(chart_formats_client, use_container_width=True)

else:
    st.write("Please upload a CSV file.")