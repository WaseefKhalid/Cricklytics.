import streamlit as st
import pandas as pd
import zipfile
import os
import requests
from io import BytesIO
import numpy as np

# Function to download and unzip IPL data
def download_and_unzip_data(url):
    response = requests.get(url)
    zip_file = BytesIO(response.content)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('ipl_data')
    return os.path.join('ipl_data', 'ipl_data.csv')

# Load data
csv_path = download_and_unzip_data('https://github.com/WaseefKhalid/Cricklytics/raw/main/ipl_data.zip?raw=true')
df = pd.read_csv(csv_path)

st.set_page_config(
    page_title="Cricklytics-Verse",  # This sets the title of the tab in the browser
    page_icon="🏏",  # Optional: You can set an icon for your app
    layout="centered",  # Optional: You can set the layout ('centered' or 'wide')
    initial_sidebar_state="auto",  # Optional: You can set the sidebar state
)

def home_section():
    st.markdown(
        """
        <style>
        .blue-bg-white-text {
            background-color: #007BFF;
            color: white;
            padding: 15px;
            border-radius: 10px;
            font-family: Arial, sans-serif;
        }
        .cricklytics-title {
            color: #FFD700; /* Gold color for Cricklytics */
            font-size: 2.5em;
            font-weight: bold;
        }
        .separator {
            height: 2px;
            background-color: white;
            margin: 20px 0;
            border: none;
        }
        .content {
            margin-top: 10px;
            line-height: 1.6;
            font-size: 1.2em;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="blue-bg-white-text">'
        '<h1 class="cricklytics-title">Welcome to Cricklytics</h1>'
        '<hr class="separator"/>'
        '</div>',
        unsafe_allow_html=True
    )
  
    st.markdown(
        """
        <div class="blue-bg-white-text content">
        <p>
        Hey cricket enthusiast, I am <strong>Waseef Khalid Khan</strong>. I have developed this <span class="cricklytics-title">Cricklytics</span> to help the coaching staff, players, 
        and cricket enthusiasts to know more about the game than the basic stats. You can check your favorite player's stats, 
        their strengths, and weaknesses here.
        </p>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="blue-bg-white-text content">
        <p>
        This dashboard provides in-depth analysis of various aspects of cricket matches. 
        Use the sidebar to navigate between different analyses such as:
        </p>
        <ul>
            <li>Best Shots by Ground</li>
            <li>Batsman Strengths and Weaknesses</li>
            <li>Toss Impact on Match Results</li>
            <li>Toss and Match Outcome Analysis</li>
            <li>Player Batting Profiles</li>
            <li>Player Bowling Profile</li>
        </ul>
        <p>Select any section from the sidebar to get started!</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.write("**Developed by [Waseef Khalid Khan](https://www.linkedin.com/in/waseef-khalid-khan-366951237)**")


def effective_shots_on_different_grounds():
    st.markdown(
        """
        <style>
        .blue-bg-yellow-text {
            background-color: #007BFF; /* Blue background */
            color: #FFD700; /* Yellow text */
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        .blue-bg-yellow-text h1 {
            color: #FFD700 !important; /* Force yellow text */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title with blue background and yellow text
    st.markdown('<div class="blue-bg-yellow-text"><h1>Best Shots by Ground</h1></div>', unsafe_allow_html=True)

    # Selectbox for ground selection
    selected_ground_shot = st.selectbox("Select Ground for Shot Analysis", df['ground'].unique(), key='ground_shot_select_1')

    # Bowling Kind Filter with Activation
    activate_bowling_kind_filter_shot = st.checkbox("Activate Bowling Kind Filter for Shot Analysis", key='activate_bowling_kind_shot_1')
    selected_bowling_kinds_shot = None
    if activate_bowling_kind_filter_shot:
        selected_bowling_kinds_shot = st.multiselect("Select Bowling Kind for Shot Analysis", df['bowl_kind'].unique(), key='bowling_kind_shot_select_1')

    # Bowling Style Filter with Activation
    activate_bowling_style_filter_shot = st.checkbox("Activate Bowling Style Filter for Shot Analysis", key='activate_bowling_style_shot_1')
    selected_bowling_styles_shot = None
    if activate_bowling_style_filter_shot:
        selected_bowling_styles_shot = st.multiselect("Select Bowling Style for Shot Analysis", df['bowl_style'].unique(), key='bowling_style_shot_select_1')

    # Bat Hand Filter with Activation
    activate_bat_hand_filter_shot = st.checkbox("Activate Bat Hand Filter for Shot Analysis", key='activate_bat_hand_shot_1')
    selected_bat_hand_shot = None
    if activate_bat_hand_filter_shot:
        selected_bat_hand_shot = st.multiselect("Select Bat Hand for Shot Analysis", df['bat_hand'].unique(), key='bat_hand_shot_select_1')

    # Build the filter conditions
    filter_conditions = (df['ground'] == selected_ground_shot)

    if activate_bowling_kind_filter_shot and selected_bowling_kinds_shot:
        filter_conditions &= df['bowl_kind'].isin(selected_bowling_kinds_shot)

    if activate_bowling_style_filter_shot and selected_bowling_styles_shot:
        filter_conditions &= df['bowl_style'].isin(selected_bowling_styles_shot)

    if activate_bat_hand_filter_shot and selected_bat_hand_shot:
        filter_conditions &= df['bat_hand'].isin(selected_bat_hand_shot)

    filtered_df_shot = df[filter_conditions]

    if filtered_df_shot.empty:
        st.error("No data available for the selected filters.")
    else:
        avg_runs_per_shot = filtered_df_shot.groupby('shot')['batruns'].mean().reset_index()
        avg_runs_per_shot = avg_runs_per_shot.sort_values(by='batruns', ascending=False)

        dismissal_rate_per_shot = filtered_df_shot.groupby('shot')['out'].mean().reset_index()
        dismissal_rate_per_shot['out'] = dismissal_rate_per_shot['out'] * 100

        shot_analysis = pd.merge(avg_runs_per_shot, dismissal_rate_per_shot, on='shot')
        shot_analysis.columns = ['shot', 'avg_runs', 'dismissal_rate']

        shot_analysis = shot_analysis.sort_values(by='avg_runs', ascending=False)

        st.subheader('Average Runs per Shot Type')
        st.bar_chart(shot_analysis.set_index('shot')['avg_runs'], use_container_width=True)

        st.subheader('Dismissal Rate per Shot Type (Percentage)')
        st.bar_chart(shot_analysis.set_index('shot')['dismissal_rate'], use_container_width=True)

def line_and_length():
    st.markdown(
        """
        <style>
        .blue-bg-yellow-text {
            background-color: #007BFF; /* Blue background */
            color: #FFD700; /* Yellow text */
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        .blue-bg-yellow-text h1 {
            color: #FFD700 !important; /* Force yellow text */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title with blue background and yellow text
    st.markdown('<div class="blue-bg-yellow-text"><h1>Bowling Line and Length Insights</h1></div>', unsafe_allow_html=True)

    # Ground Filter (now a multiselect, similar to Line and Length filters in the image)
    selected_ground = st.multiselect('Select Ground', options=df['ground'].unique(), key='ground_select_line_length_1')

    # Bowling Kind Filter with Activation
    activate_bowling_kind_filter = st.checkbox('Activate Bowling Kind Filter', key='bowling_kind_filter_active_1')
    selected_bowling_kind = None
    if activate_bowling_kind_filter:
        bowling_kind_options = df['bowl_kind'].unique()
        selected_bowling_kind = st.multiselect('Select Bowling Kind', options=bowling_kind_options, key='bowling_kind_select_line_length_1')

    # Bowling Style Filter with Activation
    activate_bowling_style_filter = st.checkbox('Activate Bowling Style Filter', key='bowling_style_filter_active_1')
    selected_bowling_style = None
    if activate_bowling_style_filter:
        bowling_style_options = df['bowl_style'].unique()
        selected_bowling_style = st.multiselect('Select Bowling Style', options=bowling_style_options, key='bowling_style_select_line_length_1')

    # Bat Hand Filter with Activation
    activate_bat_hand_filter = st.checkbox('Activate Bat Hand Filter', key='bat_hand_filter_active_1')
    selected_bat_hand = None
    if activate_bat_hand_filter:
        bat_hand_options = df['bat_hand'].unique()
        selected_bat_hand = st.multiselect('Select Bat Hand', options=bat_hand_options, key='bat_hand_select_line_length_1')

    # Filtering DataFrame based on selected filters
    filter_conditions = pd.Series([True] * len(df))

    if selected_ground:
        filter_conditions &= df['ground'].isin(selected_ground)

    if activate_bowling_kind_filter and selected_bowling_kind:
        filter_conditions &= df['bowl_kind'].isin(selected_bowling_kind)

    if activate_bowling_style_filter and selected_bowling_style:
        filter_conditions &= df['bowl_style'].isin(selected_bowling_style)

    if activate_bat_hand_filter and selected_bat_hand:
        filter_conditions &= df['bat_hand'].isin(selected_bat_hand)

    filtered_df = df[filter_conditions]

    if filtered_df.empty:
        st.error("No data available for the selected filters.")
    else:
        # Group by line and length instead of ground
        bowling_analysis = filtered_df.groupby(['line', 'length']).agg({
            'bowlruns': 'sum',
            'ball': 'count',
            'out': 'sum'
        }).reset_index()

        # Avoid division by zero or NaN
        bowling_analysis['bowling_avg'] = bowling_analysis.apply(
            lambda row: row['bowlruns'] / row['out'] if row['out'] > 0 else None, axis=1
        )

        bowling_analysis['economy_rate'] = bowling_analysis['bowlruns'] / (bowling_analysis['ball'] / 6)

        bowling_analysis['bowling_sr'] = bowling_analysis.apply(
            lambda row: row['ball'] / row['out'] if row['out'] > 0 else None, axis=1
        )

        bowling_analysis['bowling_avg'] = bowling_analysis['bowling_avg'].round(2)
        bowling_analysis['economy_rate'] = bowling_analysis['economy_rate'].round(2)
        bowling_analysis['bowling_sr'] = bowling_analysis['bowling_sr'].round(2)

        # Drop the columns that are no longer necessary for display
        bowling_analysis = bowling_analysis.drop(columns=['bowlruns', 'ball', 'out'])

        st.write('Bowling Analysis:', bowling_analysis)



# Function for the Batsman SWOT analysis
def batsman_swot():
    st.markdown(
        """
        <style>
        .blue-bg-yellow-text {
            background-color: #007BFF; /* Blue background */
            color: #FFD700; /* Yellow text */
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        .blue-bg-yellow-text h1 {
            color: #FFD700 !important; /* Force yellow text */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title with blue background and yellow text
    st.markdown('<div class="blue-bg-yellow-text"><h1>Batsman Strengths and Weaknesses</h1></div>', unsafe_allow_html=True)

    # Create three columns with the middle one being wider
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        batsman_input = st.text_input('Type to Search Batsman', key='batsman_input_key_swat_1')

        if batsman_input:
            filtered_batsmen = df['bat'].unique()
            filtered_batsmen = [b for b in filtered_batsmen if batsman_input.lower() in b.lower()]
        else:
            filtered_batsmen = df['bat'].unique()

        selected_batsman = st.selectbox('Select Batsman', options=filtered_batsmen, key='batsman_selectbox_key_swat_1')

        # Activate/Deactivate Bowling Kind Filter
        activate_bowling_kind_filter = st.checkbox("Activate Bowling Kind Filter", key='activate_bowling_kind_key_swat_1')

        if activate_bowling_kind_filter:
            bowling_kind_options = df['bowl_kind'].unique()
            selected_bowling_kinds = st.multiselect('Select Bowling Kind', options=bowling_kind_options, key='bowling_kind_multiselect_key_swat_1')
        else:
            selected_bowling_kinds = df['bowl_kind'].unique()  # If not activated, consider all kinds

        # Activate/Deactivate Bowling Style Filter
        activate_bowling_style_filter = st.checkbox("Activate Bowling Style Filter", key='activate_bowling_style_key_swat_1')

        if activate_bowling_style_filter:
            bowling_style_options = df['bowl_style'].unique()
            selected_bowling_styles = st.multiselect('Select Bowling Style', options=bowling_style_options, key='bowling_style_multiselect_key_swat_1')
            batsman_filtered_df = df[
                (df['bat'] == selected_batsman) &
                (df['bowl_kind'].isin(selected_bowling_kinds)) &
                (df['bowl_style'].isin(selected_bowling_styles))
            ]
        else:
            batsman_filtered_df = df[
                (df['bat'] == selected_batsman) &
                (df['bowl_kind'].isin(selected_bowling_kinds))
            ]

    # Display stats below the filters
    if batsman_filtered_df.empty:
        st.error("No data available for the selected filters.")
    else:
        if activate_bowling_style_filter:
            batsman_analysis = batsman_filtered_df.groupby(['line', 'length', 'bowl_kind', 'bowl_style']).agg({
                'batruns': 'sum',
                'ball': 'count',
                'out': 'sum'
            }).reset_index()
        else:
            batsman_analysis = batsman_filtered_df.groupby(['line', 'length', 'bowl_kind']).agg({
                'batruns': 'sum',
                'ball': 'count',
                'out': 'sum'
            }).reset_index()

        batsman_analysis['batruns'] = pd.to_numeric(batsman_analysis['batruns'], errors='coerce')
        batsman_analysis['out'] = pd.to_numeric(batsman_analysis['out'], errors='coerce')
        batsman_analysis['ball'] = pd.to_numeric(batsman_analysis['ball'], errors='coerce')

        batsman_analysis['out'].replace(0, 1, inplace=True)

        batsman_analysis['batting_avg'] = batsman_analysis.apply(
            lambda row: row['batruns'] / row['out'], axis=1
        )

        batsman_analysis['strike_rate'] = batsman_analysis.apply(
            lambda row: (row['batruns'] / row['ball']) * 100 if pd.notna(row['ball']) and row['ball'] > 0 else np.nan, axis=1
        )

        batsman_analysis['balls_per_dismissal'] = batsman_analysis.apply(
            lambda row: row['ball'] / row['out'], axis=1
        )

        batsman_analysis['batting_avg'] = batsman_analysis['batting_avg'].round(2)
        batsman_analysis['strike_rate'] = batsman_analysis['strike_rate'].round(2)
        batsman_analysis['balls_per_dismissal'] = batsman_analysis['balls_per_dismissal'].round(2)
        
        st.write('Batsman Analysis:', batsman_analysis)

        st.subheader(f'{selected_batsman.title()} vs Selected Bowling Kind(s)')
        summary_df = batsman_filtered_df.groupby('bowl_kind').agg({
            'batruns': 'sum',
            'ball': 'count',
            'out': 'sum'
        }).reset_index()

        summary_df['batting_avg'] = summary_df['batruns'] / summary_df['out']
        summary_df['strike_rate'] = (summary_df['batruns'] / summary_df['ball']) * 100

        summary_df['batting_avg'] = summary_df['batting_avg'].round(2)
        summary_df['strike_rate'] = summary_df['strike_rate'].round(2)

        st.write('Summary of Performance Against Selected Bowling Kinds:')
        st.dataframe(summary_df[['bowl_kind', 'batting_avg', 'strike_rate', 'out']])

        if activate_bowling_style_filter:
            st.subheader(f'{selected_batsman.title()} vs Selected Bowling Style(s)')
            style_summary_df = batsman_filtered_df.groupby('bowl_style').agg({
                'batruns': 'sum',
                'ball': 'count',
                'out': 'sum'
            }).reset_index()

            style_summary_df['batting_avg'] = style_summary_df['batruns'] / style_summary_df['out']
            style_summary_df['strike_rate'] = (style_summary_df['batruns'] / style_summary_df['ball']) * 100

            style_summary_df['batting_avg'] = style_summary_df['batting_avg'].round(2)
            style_summary_df['strike_rate'] = style_summary_df['strike_rate'].round(2)

            st.write('Summary of Performance Against Selected Bowling Styles:')
            st.dataframe(style_summary_df[['bowl_style', 'batting_avg', 'strike_rate', 'out']])

def toss_and_match_outcome_analysis():
    # CSS for blue background and yellow text
    st.markdown(
        """
        <style>
        .blue-bg-yellow-text {
            background-color: #007BFF; /* Blue background */
            color: #FFD700; /* Yellow text */
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        .blue-bg-yellow-text h1 {
            color: #FFD700 !important; /* Force yellow text */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title with blue background and yellow text
    st.markdown('<div class="blue-bg-yellow-text"><h1>Toss Impact on Match Results</h1></div>', unsafe_allow_html=True)

    selected_ground = st.selectbox("Select Ground", options=df['ground'].unique(), key='ground_select')

    team_filter_active = st.checkbox("Activate Team Filter", key='team_filter_active')

    selected_team = None
    if team_filter_active:
        team_options = df['toss'].unique()
        selected_team = st.selectbox("Select Team", options=team_options, key='team_select')

    filtered_df = df[df['ground'] == selected_ground]

    if team_filter_active and selected_team:
        filtered_df = filtered_df[filtered_df['toss'] == selected_team]

    toss_win_and_match_win = filtered_df[filtered_df['toss'] == filtered_df['winner']].shape[0]
    total_toss_wins = filtered_df.shape[0]
    percentage_toss_win_match_win = (toss_win_and_match_win / total_toss_wins) * 100 if total_toss_wins > 0 else 0

    batting_first_wins = filtered_df[(filtered_df['inns'] == 1) & (filtered_df['team_bat'] == filtered_df['winner'])].shape[0]
    total_matches_batting_first = filtered_df[filtered_df['inns'] == 1].shape[0]
    percentage_batting_first_win = (batting_first_wins / total_matches_batting_first) * 100 if total_matches_batting_first > 0 else 0

    st.write(f"Percentage of times the team won the toss and won the match: {percentage_toss_win_match_win:.2f}%")
    st.write(f"Percentage of times the team batting first won the match: {percentage_batting_first_win:.2f}%")
    st.subheader("Bowling Analysis")

    selected_bowling_kinds = st.multiselect("Select Bowling Kind", df['bowl_kind'].unique(), key='bowling_kind_select')

    activate_bowling_style_filter = st.checkbox("Activate Bowling Style Filter", key='activate_bowling_style')

    if activate_bowling_style_filter:
        selected_bowling_styles = st.multiselect("Select Bowling Style", df['bowl_style'].unique(), key='bowling_style_select')
        filtered_bowling_df = filtered_df[
            (filtered_df['bowl_kind'].isin(selected_bowling_kinds)) &
            (filtered_df['bowl_style'].isin(selected_bowling_styles))
        ]
        bowling_analysis_group = ['bowl_kind', 'bowl_style']
    else:
        filtered_bowling_df = filtered_df[filtered_df['bowl_kind'].isin(selected_bowling_kinds)]
        bowling_analysis_group = ['bowl_kind']

    if filtered_bowling_df.empty:
        st.error("No data available for the selected filters.")
    else:
        bowling_analysis = filtered_bowling_df.groupby(bowling_analysis_group).agg({
            'bowlruns': 'sum',
            'ball': 'count',
            'out': 'sum'
        }).reset_index()

        bowling_analysis['bowling_avg'] = bowling_analysis.apply(
            lambda row: row['bowlruns'] / row['out'], axis=1
        )

        bowling_analysis['economy_rate'] = bowling_analysis['bowlruns'] / (bowling_analysis['ball'] / 6)

        bowling_analysis['bowling_sr'] = bowling_analysis.apply(
            lambda row: row['ball'] / row['out'], axis=1
        )

        bowling_analysis['bowling_avg'] = bowling_analysis['bowling_avg'].round(2)
        bowling_analysis['economy_rate'] = bowling_analysis['economy_rate'].round(2)
        bowling_analysis['bowling_sr'] = bowling_analysis['bowling_sr'].round(2)

        bowling_analysis = bowling_analysis.drop(columns=['bowlruns', 'ball', 'out'])

        st.write('Bowling Analysis:', bowling_analysis)
def batsman_profile_analysis():
    # CSS for blue background and yellow text
    st.markdown(
        """
        <style>
        .blue-bg-yellow-text {
            background-color: #007BFF; /* Blue background */
            color: #FFD700; /* Yellow text */
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        .blue-bg-yellow-text h1 {
            color: #FFD700 !important; /* Force yellow text */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title with blue background and yellow text
    st.markdown('<div class="blue-bg-yellow-text"><h1>Batsman Profile Analysis</h1></div>', unsafe_allow_html=True)

    filtered_df = df.groupby('bat').filter(lambda x: x['ball'].count() >= 300)

    def determine_phase(ball_id):
        if ball_id <= 6:
            return 'Powerplay'
        elif ball_id <= 15:
            return 'Middle'
        else:
            return 'Death'

    filtered_df['Phase'] = filtered_df['ball_id'].apply(determine_phase)

    # Ensure 'Phase' is ordered correctly
    phase_order = ['Powerplay', 'Middle', 'Death']
    filtered_df['Phase'] = pd.Categorical(filtered_df['Phase'], categories=phase_order, ordered=True)

    search_term = st.text_input("Start typing the name of the batsman:")
    filtered_batsmen = filtered_df['bat'].str.lower().unique()
    filtered_suggestions = [bat for bat in filtered_batsmen if search_term.lower() in bat]
    selected_batsman = st.selectbox("Select Batsman", options=filtered_suggestions, format_func=lambda x: x.title())

    if selected_batsman:
        # Apply selected batsman
        batsman_name = selected_batsman.lower()

        # Ground filter activation
        activate_ground_filter = st.checkbox("Activate Ground Filter")
        if activate_ground_filter:
            selected_grounds = st.multiselect("Select Ground(s)", options=filtered_df['ground'].unique())
            if selected_grounds:
                filtered_df = filtered_df[filtered_df['ground'].isin(selected_grounds)]

        # Bowling kind filter activation
        activate_bowling_kind_filter = st.checkbox("Activate Bowling Kind Filter")
        if activate_bowling_kind_filter:
            selected_bowling_kinds = st.multiselect("Select Bowling Kind(s)", options=filtered_df['bowl_kind'].unique())
            if selected_bowling_kinds:
                filtered_df = filtered_df[filtered_df['bowl_kind'].isin(selected_bowling_kinds)]

        # Bowling style filter activation
        activate_bowling_style_filter = st.checkbox("Activate Bowling Style Filter")
        if activate_bowling_style_filter:
            selected_bowling_styles = st.multiselect("Select Bowling Style(s)", options=filtered_df['bowl_style'].unique())
            if selected_bowling_styles:
                filtered_df = filtered_df[filtered_df['bowl_style'].isin(selected_bowling_styles)]

        def player_profile(batsman_name):
            filtered_df['bat'] = filtered_df['bat'].str.lower()
            player_df = filtered_df[filtered_df['bat'] == batsman_name]

            if player_df.empty:
                st.write(f"No data available for {batsman_name.title()} or the player has not faced 300 balls.")
                return

            # Calculate metrics
            sr_phase_wise = player_df.groupby('Phase').apply(lambda x: (x['batruns'].sum() / x['ball'].count()) * 100).reset_index()
            sr_phase_wise.columns = ['Phase', 'SR']
            sr_phase_wise['SR'] = sr_phase_wise['SR'].round(2)

            six_ratio_phase_wise = player_df.groupby('Phase').apply(lambda x: x['isSix'].sum() / x['ball'].count()).reset_index()
            six_ratio_phase_wise.columns = ['Phase', 'Six Ratio']
            six_ratio_phase_wise['Balls per Six'] = six_ratio_phase_wise.apply(lambda x: round(1 / x['Six Ratio'], 2) if x['Six Ratio'] > 0 else 0, axis=1)

            four_ratio_phase_wise = player_df.groupby('Phase').apply(lambda x: x['isFour'].sum() / x['ball'].count()).reset_index()
            four_ratio_phase_wise.columns = ['Phase', 'Four Ratio']
            four_ratio_phase_wise['Balls per Four'] = four_ratio_phase_wise.apply(lambda x: round(1 / x['Four Ratio'], 2) if x['Four Ratio'] > 0 else 0, axis=1)

            dot_ball_phase_wise = player_df.groupby('Phase').apply(lambda x: round((x['isDot'].sum() / x['ball'].count()) * 100, 2)).reset_index()
            dot_ball_phase_wise.columns = ['Phase', 'Dot Ball %']

            activity_runs_phase_wise = player_df.groupby('Phase').apply(lambda x: round((x['ActivityRuns'].sum() / x['batruns'].sum()) * 100, 2)).reset_index()
            activity_runs_phase_wise.columns = ['Phase', 'Activity Runs %']

            control_phase_wise = player_df.groupby('Phase').apply(lambda x: round((x['control'].sum() / x['ball'].count()) * 100, 2)).reset_index()
            control_phase_wise.columns = ['Phase', 'Control %']

            st.write(f"Player Profile: {batsman_name.title()}")

            # Display the metrics side by side
            col1, col2 = st.columns(2)

            with col1:
                st.write("### Strike Rate:")
                st.table(sr_phase_wise)

                st.write("### Balls per Six :")
                st.table(six_ratio_phase_wise[['Phase', 'Balls per Six']])

                st.write("### Balls per Four:")
                st.table(four_ratio_phase_wise[['Phase', 'Balls per Four']])

            with col2:
                st.write("### Dot Ball Percentage:")
                st.table(dot_ball_phase_wise)

                st.write("### Percentage of Activity Runs:")
                st.table(activity_runs_phase_wise)

                st.write("### Control Percentage:")
                st.table(control_phase_wise)

        player_profile(batsman_name)


def bowler_profile_analysis():
    # CSS for blue background and yellow text
    st.markdown(
        """
        <style>
        .blue-bg-yellow-text {
            background-color: #007BFF; /* Blue background */
            color: #FFD700; /* Yellow text */
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        .blue-bg-yellow-text h1 {
            color: #FFD700 !important; /* Force yellow text */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title with blue background and yellow text
    st.markdown('<div class="blue-bg-yellow-text"><h1>Bowler Profile Analysis</h1></div>', unsafe_allow_html=True)

    filtered_df = df.groupby('bowl').filter(lambda x: x['ball'].count() >= 300)

    def determine_phase(ball_id):
        if ball_id <= 6:
            return 'Powerplay'
        elif ball_id <= 15:
            return 'Middle'
        else:
            return 'Death'

    filtered_df['Phase'] = filtered_df['ball_id'].apply(determine_phase)
    filtered_df['bowl'] = filtered_df['bowl'].str.lower()

    # Define the phase order
    phase_order = ['Powerplay', 'Middle', 'Death']
    filtered_df['Phase'] = pd.Categorical(filtered_df['Phase'], categories=phase_order, ordered=True)

    bowler_names = filtered_df['bowl'].str.title().unique()
    bowler_name = st.selectbox("Enter or select the name of the bowler:", options=sorted(bowler_names))

    if bowler_name:
        # Apply the selected bowler name
        bowler_name = bowler_name.lower()

        # Ground filter activation (now placed after bowler selection)
        activate_ground_filter = st.checkbox("Activate Ground Filter")
        if activate_ground_filter:
            selected_ground = st.selectbox("Select Ground", options=filtered_df['ground'].unique())
            filtered_df = filtered_df[(filtered_df['ground'] == selected_ground) & (filtered_df['bowl'] == bowler_name)]

        # Batting hand filter activation (now placed after bowler selection)
        activate_bat_hand_filter = st.checkbox("Activate Batting Hand Filter")
        if activate_bat_hand_filter:
            selected_bat_hand = st.selectbox("Select Batting Hand", options=filtered_df['bat_hand'].unique())
            filtered_df = filtered_df[(filtered_df['bat_hand'] == selected_bat_hand) & (filtered_df['bowl'] == bowler_name)]

        def bowler_profile():
            player_df = filtered_df[filtered_df['bowl'] == bowler_name]
            
            if player_df.empty:
                st.write(f"No data available for {bowler_name.title()} or the player has not bowled 300 balls.")
                return
            
            # Calculate metrics and round to two decimal places
            economy_phase_wise = player_df.groupby('Phase').apply(lambda x: round(x['bowlruns'].sum() / (x['ball'].count() / 6), 2)).reset_index()
            economy_phase_wise.columns = ['Phase', 'Economy Rate']
            
            bowling_avg_phase_wise = player_df.groupby('Phase').apply(lambda x: round(x['bowlruns'].sum() / x['out'].sum(), 2) if x['out'].sum() > 0 else 0).reset_index()
            bowling_avg_phase_wise.columns = ['Phase', 'Bowling Avg']
            
            wickets_per_ball_phase_wise = player_df.groupby('Phase').apply(lambda x: round(x['ball'].count() / x['out'].sum(), 2) if x['out'].sum() > 0 else 0).reset_index()
            wickets_per_ball_phase_wise.columns = ['Phase', 'Wickets per Ball']

            non_control_percentage_phase_wise = player_df.groupby('Phase').apply(lambda x: round(((x['ball'].count() - x['control'].sum()) / x['ball'].count()) * 100, 2)).reset_index()
            non_control_percentage_phase_wise.columns = ['Phase', 'Non-Control %']

            # Display the analysis side by side
            st.write(f"Bowler Profile: {bowler_name.title()}")

            col1, col2 = st.columns(2)

            with col1:
                st.write("### Economy Rate:")
                st.table(economy_phase_wise.sort_values('Phase'))

                st.write("### Wickets per Ball:")
                st.table(wickets_per_ball_phase_wise.sort_values('Phase'))

            with col2:
                st.write("### Bowling Average:")
                st.table(bowling_avg_phase_wise.sort_values('Phase'))

                st.write("### Non-Control Percentage:")
                st.table(non_control_percentage_phase_wise.sort_values('Phase'))

        bowler_profile()



# CSS for sidebar radio buttons
st.markdown(
    """
    <style>
    /* Ensure all radio button containers have the same width */
    .stRadio > div {
        display: flex;
        flex-direction: column;
    }
    .stRadio div[role=radiogroup] > label {
        background-color: #007BFF; /* Blue background color */
        color: white; /* White text */
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 8px;
        width: 100%;
        display: flex;  /* Use flexbox to align items */
        align-items: center; /* Center align items */
        text-align: left;
        font-weight: bold;
        font-size: 16px;
        cursor: pointer;
    }
    .stRadio div[role=radiogroup] > label:hover {
        background-color: #0056b3; /* Darker blue on hover */
    }
    .stRadio div[role=radiogroup] > label > div[aria-checked=true] {
        background-color: #FF5733; /* Active or selected item color */
        color: white;
    }
    /* Ensure that the labels have the same width */
    .stRadio div[role=radiogroup] > label {
        width: 100%; /* Uniform width for all options */
    }
    /* Add the arrow symbol before the text */
    .stRadio div[role=radiogroup] > label:before {
        content: "➔ "; /* Unicode arrow symbol */
        visibility: visible;
        margin-right: 10px;
        font-size: 18px;
    }
    /* Ensure the text is visible */
    .stRadio div[role=radiogroup] > label > div {
        display: flex;
        align-items: center;
        color: white; /* Ensure text is white */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with radio buttons for selecting the analysis type
analysis_type = st.sidebar.radio("Choose the analysis", [
    "Home",
    "Best Shots by Ground",
    "Bowling Line and Length Insights",
    "Batsman Strengths and Weaknesses",
    "Toss Impact on Match Results",
    "Player Batting Profiles",
    "Player Bowling Profiles"
])

# Display the selected analysis section
if analysis_type == "Home":
    home_section()
elif analysis_type == "Best Shots by Ground":
    effective_shots_on_different_grounds()
elif analysis_type == "Bowling Line and Length Insights":
    line_and_length()
elif analysis_type == "Batsman Strengths and Weaknesses":
    batsman_swot()
elif analysis_type == "Toss Impact on Match Results":
    toss_and_match_outcome_analysis()
elif analysis_type == "Player Batting Profiles":
    batsman_profile_analysis()
elif analysis_type == "Player Bowling Profiles":
    bowler_profile_analysis()


