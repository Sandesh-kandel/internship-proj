import base64
import io
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import pymysql
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'Hi.. capital of new delhi is india'
connection = pymysql.connect(host='127.0.0.1',
                            user='root',
                            password='9868346087Sk./',
                            port=3306,
                            database='covid')
def fetch_data_from_db():
    query = "SELECT location, totalConfirmedCases, totalDeaths, totalRecoveredCases,newlyConfirmedCases,newDeaths, newlyRecoveredCases FROM covid_info"
    with connection.cursor() as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['location', 'totalConfirmedCases', 'totalDeaths', 'totalRecoveredCases', 'newlyConfirmedCases', 'newDeaths', 'newlyRecoveredCases'])
    return df

# Function to generate Matplotlib plot
def generate_matplotlib_plots(df):
    # 20 Countries with the Most COVID Cases around the World
    cases_by_country = df.groupby('location').sum()['totalConfirmedCases'].sort_values(ascending=False).head(20)
    plt.figure(figsize=(8, 6))
    cases_by_country.plot(kind='bar')
    plt.title('20 Countries with the Most COVID Cases around the World.')
    plt.xlabel('List of Countries')
    plt.ylabel('Total Confirmed Cases')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    plot_data_1 = base64.b64encode(buf1.getvalue()).decode('utf-8')

    # COVID-19 Cases by Location
    grouped_df = df.groupby('location')[['totalConfirmedCases', 'totalDeaths', 'totalRecoveredCases']].sum().reset_index()
    plt.figure(figsize=(10, 6))
    plt.bar(grouped_df['location'], grouped_df['totalConfirmedCases'], label='Total Confirmed Cases')
    plt.bar(grouped_df['location'], grouped_df['totalDeaths'], label='Total Deaths')
    plt.bar(grouped_df['location'], grouped_df['totalRecoveredCases'], label='Total Recovered Cases')
    plt.xlabel('Location')
    plt.ylabel('Count')
    plt.title('COVID-19 Cases by Location')
    plt.legend()
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    buf2.seek(0)
    plot_data_2 = base64.b64encode(buf2.getvalue()).decode('utf-8')

    # Stacked plot for COVID-19 cases distribution by location where total confirmed cases > 4 million
    filtered_df = df[df['totalConfirmedCases'] > 4000000]
    trace_confirmed = go.Bar(x=filtered_df['location'], y=filtered_df['totalConfirmedCases'], name='Total Confirmed Cases')
    trace_deaths = go.Bar(x=filtered_df['location'], y=filtered_df['totalDeaths'], name='Total Deaths')
    trace_recovered = go.Bar(x=filtered_df['location'], y=filtered_df['totalRecoveredCases'], name='Total Recovered Cases')

    layout = go.Layout(title='COVID-19 Cases Distribution by Location (Total Confirmed Cases > 4 Million)',
                       xaxis=dict(title='Location'),
                       yaxis=dict(title='Count'),
                       barmode='stack')

    fig = go.Figure(data=[trace_confirmed, trace_deaths, trace_recovered], layout=layout)
    buf3 = io.BytesIO()
    fig.write_image(buf3, format='png')
    buf3.seek(0)
    plot_data_3 = base64.b64encode(buf3.getvalue()).decode('utf-8')

    # Top 20 countries with the Highest covid casualties.
    top_20_countries = df.nlargest(20, 'totalDeaths')

    # Create traces for confirmed cases, deaths, and recovered cases
    trace_confirmed = go.Bar(x=top_20_countries['location'], y=top_20_countries['totalConfirmedCases'], name='Total Confirmed Cases')
    trace_deaths = go.Bar(x=top_20_countries['location'], y=top_20_countries['totalDeaths'], name='Total Deaths')
    trace_recovered = go.Bar(x=top_20_countries['location'], y=top_20_countries['totalRecoveredCases'], name='Total Recovered Cases')

    # Set up the layout for the plot
    layout = go.Layout(
        title='Top 20 Countries with the Highest COVID-19 Casualties',
        xaxis=dict(title='Country'),
        yaxis=dict(title='Count'),
        barmode='stack'
    )

    # Create the figure
    fig = go.Figure(data=[trace_confirmed, trace_deaths, trace_recovered], layout=layout)

    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)
    plot_data_4 = base64.b64encode(buf.getvalue()).decode('utf-8')    

    # 20 Countries with the Least COVID Cases
    cases_by_country = df.groupby('location').sum()['totalConfirmedCases'].sort_values(ascending=True).head(20)
    plt.figure(figsize=(5, 4))
    cases_by_country.plot(kind='bar')
    plt.title('20 Countries with the Least COVID Cases.')
    plt.xlabel('List of Countries')
    plt.ylabel('Total Confirmed Cases')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data_5 = base64.b64encode(buf.getvalue()).decode('utf-8')

    # 20 Countries with the Highest COVID-19 Casualties
    cases_by_country = df.groupby('location').sum()['totalDeaths'].sort_values(ascending=False).head(20)
    plt.figure(figsize=(5, 4))
    cases_by_country.plot(kind='bar')
    plt.title('20 Countries with the Highest COVID-19 Casualties around the World.')
    plt.xlabel('List of Countries')
    plt.ylabel('Total Deaths')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data_6 = base64.b64encode(buf.getvalue()).decode('utf-8')

    # 20 Countries with the Least COVID-19 Casualties
    cases_by_country = df.groupby('location').sum()['totalDeaths'].sort_values(ascending=True).iloc[40:60]
    plt.figure(figsize=(5, 4))
    cases_by_country.plot(kind='bar')
    plt.title('20 Countries with the Least COVID-19 Casualties around the World.')
    plt.xlabel('List of Countries')
    plt.ylabel('Total Deaths')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data_7 = base64.b64encode(buf.getvalue()).decode('utf-8')

    # 20 Countries with the Highest COVID-19 Recoveries
    cases_by_country = df.groupby('location').sum()['totalRecoveredCases'].sort_values(ascending=False).head(20)
    plt.figure(figsize=(5, 4))
    cases_by_country.plot(kind='bar')
    plt.title('20 Countries with the Highest COVID-19 Recoveries around the World.')
    plt.xlabel('List of Countries')
    plt.ylabel('Total Recoveries')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data_8 = base64.b64encode(buf.getvalue()).decode('utf-8')


    return plot_data_1, plot_data_2, plot_data_3, plot_data_4, plot_data_5, plot_data_6, plot_data_7, plot_data_8



df = fetch_data_from_db()
plot_data_1, plot_data_2, plot_data_3, plot_data_4, plot_data_5, plot_data_6, plot_data_7, plot_data_8 = generate_matplotlib_plots(df)
connection.close() # Close the database connection



@app.route('/register', methods=['GET', 'POST'])

def register():
    connection = pymysql.connect(host='127.0.0.1',
                            user='root',
                            password='9868346087Sk./',
                            port=3306,
                            database='covid')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        # Email validation using regular expression
        email_regex = r"^[a-zA-Z0-9.+_-]+@gmail\.com$"
        if not re.match(email_regex, email):
            return render_template('register.html', error="Invalid email address. Only gmail.com addresses are allowed.")
        # Hash the password for secure storage

        hashed_password = generate_password_hash(password)

        with connection.cursor() as cursor:
            sql = "INSERT INTO users (name, email, password) VALUES (%s, %s,%s)"
            cursor.execute(sql, (name, email, hashed_password))
            connection.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

 
@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = pymysql.connect(host='127.0.0.1',
                            user='root',
                            password='9868346087Sk./',
                            port=3306,
                            database='covid')
    if request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):
            session['user'] = user[1]  # Store the user's name in the session
            
            # Fetch the user's role from the database
            cur = connection.cursor()
            cur.execute("SELECT role FROM users WHERE name = %s", (user[1],))
            user_role = cur.fetchone()[0]
            cur.close()
            
            session['user_role'] = user_role  # Store the user's role in the session
            return redirect(url_for('index'))
        else:
            return 'Invalid email or password'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))



@app.route('/')
def index():
    if 'user' in session:
        if 'user_role' in session:
            user_role = session['user_role']
            if user_role == 'admin':
                return render_template('index.html',
                                        plot_data_1=plot_data_1,
                                        plot_data_2=plot_data_2,
                                        plot_data_3=plot_data_3,
                                        plot_data_4=plot_data_4,
                                        plot_data_5=plot_data_5,
                                        plot_data_6=plot_data_6,
                                        plot_data_7=plot_data_7,
                                        plot_data_8=plot_data_8,
                                        user_role=user_role)
            else:
                return render_template('index.html',
                                       plot_data_1=plot_data_1,
                                       plot_data_6=plot_data_6)
        else:
            return redirect(url_for('login'))  
    else:
        return redirect(url_for('login'))
    

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)



