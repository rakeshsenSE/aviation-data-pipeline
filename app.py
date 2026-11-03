import os
import urllib.parse
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

load_dotenv()

db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "rakeshsen")
db_host = os.getenv("DB_HOST", "localhost")
db_name = os.getenv("DB_NAME", "flight_push")
encoded_pass = urllib.parse.quote_plus(db_password)

DB_URI = f"mysql+pymysql://{db_user}:{encoded_pass}@{db_host}/{db_name}"

st.set_page_config(page_title="Flight Pulse Dashboard", layout="wide")
st.title("✈️ Flight Pulse: Advanced Analytics Dashboard")


@st.cache_data(ttl=600)
def load_data():
  try:
    engine = create_engine(DB_URI)
    df_flights = pd.read_sql("SELECT * FROM flights", con=engine)
    df_weather = pd.read_sql("SELECT * FROM weather", con=engine)
    df_news = pd.read_sql("SELECT * FROM news_alerts", con=engine)
    return df_flights, df_weather, df_news
  except Exception as e:
    st.error(f"Database error: {e}")
    return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()


df_flights, df_weather, df_news = load_data()

if df_flights.empty:
  st.warning("There was no Data!!")
  filtered_df = df_flights.copy()
else:
  st.sidebar.header("🔍 Filter Options")
  countries = df_flights["origin_country"].dropna().unique().tolist()
  selected_country = st.sidebar.selectbox(
      "Select Origin Country", ["All"] + countries
  )

  if selected_country != "All":
    filtered_df = df_flights[
        df_flights["origin_country"] == selected_country
    ]
  else:
    filtered_df = df_flights.copy()

# KPIs Section
st.subheader("📊 Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)

total_flights = len(filtered_df)
avg_velocity = (
    filtered_df["velocity"].mean()
    if not filtered_df.empty and "velocity" in filtered_df.columns
    else 0
)
avg_altitude = (
    filtered_df["geo_altitude"].mean()
    if not filtered_df.empty and "geo_altitude" in filtered_df.columns
    else 0
)

with col1:
  st.metric(label="Total Tracked Flights", value=total_flights)
with col2:
  st.metric(label="Average Velocity (m/s)", value=f"{avg_velocity:.2f}")
with col3:
  st.metric(label="Average Altitude (m)", value=f"{avg_altitude:.2f}")

st.markdown("---")

# Time-based Flight Activity Trend
st.subheader("📈 Time-based Flight Activity Trend")
if "fetched_at" in filtered_df.columns and not filtered_df.empty:
  trend_df = (
      filtered_df.groupby(
          pd.to_datetime(filtered_df["fetched_at"]).dt.floor("min")
      )
      .size()
      .reset_index(name="flight_count")
  )
  fig_line = px.line(
      trend_df,
      x="fetched_at",
      y="flight_count",
      markers=True,
      title="Number of Flights Tracked Over Time",
      labels={"fetched_at": "Time", "flight_count": "Active Flights"},
  )
  st.plotly_chart(fig_line, use_container_width=True)
else:
  st.info("Time series data not available for line chart.")

col_a, col_b = st.columns(2)

with col_a:
  st.subheader("📊 Flights by Origin Country")
  if not filtered_df.empty and "origin_country" in df_flights.columns:
    country_counts = (
        df_flights["origin_country"].value_counts().reset_index()
    )
    country_counts.columns = ["origin_country", "count"]

    fig_bar = px.bar(
        country_counts.head(10),
        x="origin_country",
        y="count",
        color="origin_country",
        title="Top 10 Countries by Active Flights",
        labels={"origin_country": "Country", "count": "Flight Count"},
    )
    st.plotly_chart(fig_bar, use_container_width=True)
  else:
    st.info("No data for bar chart.")

with col_b:
  st.subheader("🌦️ Weather Impact Analysis (Scatter)")
  if not df_weather.empty and "temperature_c" in df_weather.columns:
    fig_scatter = px.scatter(
        df_weather,
        x="temperature_c",
        y="wind_speed_ms",
        color="weather_condition",
        size="visibility_m" if "visibility_m" in df_weather.columns else None,
        hover_data=["weather_description"],
        title="Temperature vs Wind Speed across Weather Conditions",
        labels={
            "temperature_c": "Temperature (°C)",
            "wind_speed_ms": "Wind Speed (m/s)",
        },
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
  else:
    st.info("Weather data fields not available for analysis.")

st.markdown("---")

# Live Flight Positions Map
st.subheader("🌍 Live Flight Positions Map")
if "latitude" in filtered_df.columns and "longitude" in filtered_df.columns:
  fig_map = px.scatter_geo(
      filtered_df,
      lat="latitude",
      lon="longitude",
      hover_name="callsign" if "callsign" in filtered_df.columns else None,
      color="origin_country"
      if "origin_country" in filtered_df.columns
      else None,
      projection="natural earth",
      title="Geographical Distribution of Flights",
  )
  st.plotly_chart(fig_map, use_container_width=True)
else:
  st.info("Latitude/Longitude data not available.")

st.markdown("---")
st.subheader("📰 Latest Aviation News & Alerts")

if not df_news.empty:
  for index, row in df_news.iterrows():
    with st.container():
      st.markdown(f"**🔹 [{row['title']}]({row['url']})**")
      st.caption(
          f"Source: {row['source']} | Published At: {row['published_at']}"
      )
      st.markdown("---")
else:
  st.info("No news alerts found in database.")

# Flight Pulse AI Assistant (Direct Text-to-SQL Pipeline)
gemini_api_key = os.getenv("GEMINI_API_KEY")
st.markdown("---")
st.subheader("🤖 Flight Pulse AI Assistant")
st.markdown("Ask any Question (like: *'Show me the total flights'*):")

user_query = st.text_input("Ask your AI Analyst:")

if user_query:
  with st.spinner("AI is analyzing your database..."):
    try:
      ai_engine = create_engine(DB_URI)

      schema_info = """
            Tables in database:
            - flights (id, callsign, origin_country, time_position, last_contact, longitude, latitude, baro_altitude, velocity, true_track, vertical_rate, geo_altitude, squawk, spi, position_source, fetched_at)
            - weather (id, temperature_c, wind_speed_ms, weather_condition, weather_description, visibility_m, fetched_at)
            - news_alerts (id, title, url, source, published_at)
            """

      llm = ChatGoogleGenerativeAI(
          model="gemini-2.5-flash", google_api_key=gemini_api_key
      )

      prompt = f"""
            You are an expert SQL assistant for a MySQL database.
            Based on the schema below, write ONLY a valid SQL query to answer the user's question. Do not include markdown code blocks like ```sql or any extra text, just write the raw SQL query.

            {schema_info}

            User Question: {user_query}
            """

      sql_response = llm.invoke(prompt)
      sql_query = (
          sql_response.content.replace("```sql", "")
          .replace("```", "")
          .strip()
      )

      with ai_engine.connect() as connection:
        result_df = pd.read_sql(sql_query, con=connection)

      if not result_df.empty:
        summary_prompt = f"""
                The user asked: '{user_query}'
                The SQL query executed was: {sql_query}
                The query result from the database is:
                {result_df.to_string(index=False)}

                Please provide a clear, natural, and concise answer to the user based on this result.
                """
        final_answer = llm.invoke(summary_prompt)
        st.success(final_answer.content)
      else:
        st.info(
            "Query executed successfully, but no matching data found in the"
            " database."
        )

    except Exception as e:
      st.error(f"AI Error: {e}")
