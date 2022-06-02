import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#import scipy as sp
#import os

st.set_page_config(layout="wide")

def player_compensation_history(number_of_years = 0):
    '''This function creates a plot about compensation history of players that have served
    x-number of years in MLS.
    By default, players who have played longest in MLS will be shown.
    To view plots other than those for players who have served longest in MLS, users can provide an (int)
    argument that will be deducted from the maximum serving time.
    '''
    years_under_evaluation = longest_serving_player_ranked["uniquename"].max() - number_of_years
    #print(f'Showing plot for players playing in the MLS for {years_under_evaluation} years')
    longest_serving_players_name_s = longest_serving_player_ranked[longest_serving_player_ranked["uniquename"] == longest_serving_player_ranked["uniquename"].max() - number_of_years]
    longest_serving_player_df = mls_data_clubnames[mls_data_clubnames['uniquename'].isin(longest_serving_players_name_s["index"].tolist())]
    longest_serving_player_df = longest_serving_player_df.sort_values(["Last Name", "Year"])
    # plot salary development for players serving longest in MLS
    fig_pch, ax_pch = plt.subplots(figsize=(10,4))
    for key, grp in longest_serving_player_df.groupby(['uniquename']):
        ax_pch.plot(grp['Year'], grp['Compensation'], label=key)
    ax_pch.legend()
    ax_pch.legend(bbox_to_anchor=(1.0, 1.0))
    ax_pch.set_xlabel("Year")
    ax_pch.set_ylabel("Compensation in million $")
    return fig_pch, years_under_evaluation

def read_data(data_):
    datais = pd.read_csv(data_)
    return datais

mls_data_clubnames = read_data("mls_clean.csv")

col1, col2 = st.columns([2,1])
with col2:
    st.write("")

with col1:
    st.header(
    '''
    Major League Soccer (2007-2022)
    '''
    )
    st.subheader(
    '''
    Analyses of players and compensations
    '''
    )
    st.markdown(
    '''
    ### Overview
    **Section 1** - *interactive (sidebar)*
    * Highest paid players across all years
    * Top ten paid players for each year
    **Section 2** - *interactive (sidebar)*
    * Top-paid players (top 10, 25, 50 across all years) and distribution of their playing position
    * *Optional* - Compensation allocated to playing position for each year
    **Section 3** - *interactive (sidebar)*
    * Longest serving players (10+ years) and compensation across their career
    **Section 4** - *non-interactive*
    * Compensation across all years - maximum, median, mean
    * Development of mean pay across all years
    * Development of median pay across all years
    * Development of maximum pay across all years
    * Development of minimum pay across all years
    **Section 5** - *interactive (sidebar)*
    * Extract player information
    * Teams playing in the MLS (by year)
    * Extract team information
    '''
    )

st.markdown('#')
st.markdown('#')

st.sidebar.title(
    '''
    MLS 2007-2022
    '''
)

st.sidebar.subheader(
    '''
    Insights into players and compensation
    '''
)
st.sidebar.write(
    '''
    Raw data obtained from https://mlsplayers.org/resources/salary-guide.
    Code base/info available at https://github.com/afborn/MLS_soccer
    Data updated on an annual basis
    '''
)

st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

st.subheader(
    '''
    Section 1 - Highest paid players
    '''
)

col1, col2 = st.columns(2)
with col1:
    idx = mls_data_clubnames.groupby(['Year'])['Compensation'].transform(max) == mls_data_clubnames['Compensation']
    highest_paid_player_each_year = mls_data_clubnames[idx].sort_values(by=['Year'])
    #plt.figure(figsize=(6, 6))
    #x=sns.barplot(x = highest_paid_player_each_year["Year"].astype(int), y = highest_paid_player_each_year["Compensation"], hue = highest_paid_player_each_year['Last Name'], dodge=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax = sns.barplot(x = highest_paid_player_each_year["Year"].astype(int), y = highest_paid_player_each_year["Compensation"], hue = highest_paid_player_each_year['Last Name'], dodge=False)
    ax.set_ylabel("Compensation in million $")
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    ax.set_title("Highest paid players per year")
    ax.get_xticks()
    ax.tick_params(axis='x', labelrotation = 60)
    #ax.set_xticklabels(ax.get_xticks(), rotation = 60)
    #ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=60)
    #ax.set_xticks(rotation=45)    
    st.pyplot(fig)
    
with col2:
    top_ten_paid_each_year = mls_data_clubnames.sort_values(['Year','Compensation'],ascending = False).groupby('Year').head(10) 
    options = top_ten_paid_each_year["Year"].unique().astype(int)
    st.sidebar.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    st.sidebar.subheader(
        '''
        Section 1
        Highest paid players (top ten)
        '''
    )
    tt_year = st.sidebar.selectbox("Choose year", options, index=0)
    st.sidebar.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
    top_ten_paid_each_year_year = top_ten_paid_each_year[top_ten_paid_each_year["Year"] == tt_year]
    #plt.figure(figsize=(6, 6))
    figs, axs = plt.subplots(figsize=(6, 3))
    axs = sns.barplot(x = top_ten_paid_each_year_year["Last Name"], y = top_ten_paid_each_year_year["Compensation"], hue= top_ten_paid_each_year_year["Club"], dodge=False)
    axs.set_ylabel("Compensation in million $")
    axs.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    axs.set_title(f'Highest paid players (top ten): year {tt_year}')
    axs.get_xticks()
    axs.tick_params(axis='x', labelrotation = 60)
    #axs.set_xticklabels(ax.get_xticks(), rotation = 60)
    #axs.set_xticks(axs.get_xticks(), axs.get_xticklabels())
    #axs.xticks(rotation=60)
    st.pyplot(figs)
    
st.container()
st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

st.subheader(
    '''
    Section 2 - Top-paid players and their playing position
    '''
)
st.text("")
col1, col2, col3, col4 = st.columns([1,2,2,1])
with col1:
    st.write("")
with col2:
    pie_1, ax_1 = plt.subplots()
    mls_ration_pos = read_data("player_ratio_pos_mls.csv")
    labels = mls_ration_pos["Pos"]
    ax_1.pie(x=mls_ration_pos["Pos ratio MLS"], autopct="%.1f%%", explode=[0.03]*len(mls_ration_pos["Pos ratio MLS"]), labels=labels, textprops={'fontsize': 10}, colors=["#CDAD00", "#5CACEE", "#9FB6CD", "#F8F8FF", "#FF7D40", "#F08080"], \
    pctdistance=0.75, labeldistance=1.2)
    ax_1.set_title("Distribution of playing position of all players \n in MLS 2007-2022", fontsize=10);
    st.pyplot(pie_1)
with col3:
    options=[10, 25, 50]
    st.sidebar.subheader(
        '''
        Section 2
        Distribution of playing positions of highest paid players across MLS for 2007-2022
        '''
    )
    no_highest_player = st.sidebar.selectbox("Choose number of highest paid players per year", options, index=0)
    if no_highest_player == 10:
        top_ten_paid_obs_exp = read_data("top_ten_paid_obs_exp.csv")
    elif no_highest_player == 25:
        top_ten_paid_obs_exp = read_data("top_twenty_five_paid_obs_exp.csv")
    elif no_highest_player == 50:
        top_ten_paid_obs_exp = read_data("top_fifty_paid_obs_exp.csv")
    pie_2, ax_2 = plt.subplots()
    labels = top_ten_paid_obs_exp["Pos"]
    ax_2.pie(x=top_ten_paid_obs_exp["Observed_value"], autopct="%.1f%%", explode=[0.03]*len(top_ten_paid_obs_exp["Observed_value"]), labels=labels, textprops={'fontsize': 10}, colors=["#CDAD00", "#5CACEE", "#9FB6CD", "#F8F8FF", "#FF7D40", "#F08080"], \
    pctdistance=0.75, labeldistance=1.2)
    ax_2.set_title(f'Distribution of playing positions of top {no_highest_player} \n highest paid players 2007-2022', fontsize=10);
    st.pyplot(pie_2)
with col4:
    st.write("")
    #pvalue = sp.stats.chisquare(f_obs=top_ten_paid_obs_exp.Observed_value, f_exp=top_ten_paid_obs_exp.Expected_value)[1]
    #st.write('p-value ' + '{:.3g}'.format(pvalue))
    #st.text(pvalue)
grid_yes = st.sidebar.checkbox('Display compensation & playing position for each year')
if grid_yes:
    st.markdown("***")
    st.markdown(
        '''
        **Compensation & playing position for each year**
        '''
    )
    st.text("")
    col1, col2, col3 = st.columns([1,6,1])
    grid = sns.FacetGrid(mls_data_clubnames, col = "Year", hue = "Pos", col_wrap=3)
    grid.map(sns.scatterplot, "Pos", "Compensation")
    grid.set_ylabels("Compensation in million $")
    grid.add_legend(loc='upper right')
    with col1:
        st.write("")
    with col2:
        st.pyplot(grid)
    with col3:
        st.write("")

st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
st.subheader(
    "Section 3 - Compensation of long-term players (10+ years)"
    )

#mls_data_clubnames["uniquename"] = mls_data_clubnames["Last Name"] + '_' + mls_data_clubnames["First Name"]
longest_serving_player_ranked = mls_data_clubnames["uniquename"].value_counts().reset_index()

st.sidebar.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
st.sidebar.subheader(
        '''
        Section 3
        Development of compensation for players in the MLS for 10+ years
        '''
    )
years_in_mls = st.sidebar.selectbox("Choose number of years played in MLS", options=[10,11,12,13,14,15,16], index=6)
col1, col2, col3 = st.columns([1,4,1])
with col1:
    st.write("")
with col2:   
    if years_in_mls == 10:
        figpch, yue = player_compensation_history(6)
        st.markdown('''
        **Players playing in MLS for {0} years**'''.format(yue))
        st.pyplot(figpch)
    elif years_in_mls == 11:
        figpch, yue = player_compensation_history(5)
        st.markdown('''
        **Players playing in MLS for {0} years**'''.format(yue))
        st.pyplot(figpch)
    elif years_in_mls == 12:
        figpch, yue = player_compensation_history(4)
        st.markdown('''
        **Players playing in MLS for {0} years**'''.format(yue))
        st.pyplot(figpch)
    elif years_in_mls == 13:
        figpch, yue = player_compensation_history(3)
        st.markdown('''
        **Players playing in MLS for {0} years**'''.format(yue))
        st.pyplot(figpch)
    elif years_in_mls == 14:
        figpch, yue = player_compensation_history(2)
        st.markdown('''
        **Players playing in MLS for {0} years**'''.format(yue))
        st.pyplot(figpch)
    elif years_in_mls == 15:
        figpch, yue = player_compensation_history(1)
        st.markdown('''
        **Players playing in MLS for {0} years**'''.format(yue))
        st.pyplot(figpch)
    elif years_in_mls == 16:
        figpch, yue = player_compensation_history(0)
        st.markdown('''
        **Players playing in MLS for {0} years**'''.format(yue))
        st.pyplot(figpch)
with col3:
    st.write("")



st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
st.subheader(
        '''
        Section 4 - Compensation metrics across all years
        '''
    )
#estimate number of bins for histogram
bin_no = int((mls_data_clubnames["Compensation"].max()-mls_data_clubnames["Compensation"].min())/len(mls_data_clubnames))
#gen_metrics = mls_data_clubnames[mls_data_clubnames["Year"] == 2022]
gen_metrics = mls_data_clubnames
fig_gen_metrics, ax_gen_metrics = plt.subplots(figsize = (10,5))
ax_gen_metrics.hist(gen_metrics.Compensation, bins=bin_no, color='skyblue', edgecolor='k', alpha=0.65)
ax_gen_metrics.axvline(mls_data_clubnames.Compensation.mean(), color='k', linestyle='dashed', linewidth=1, label="mean compensation")
ax_gen_metrics.axvline(mls_data_clubnames.Compensation.median(), color='b', linestyle='dashed', linewidth=1, label="median compensation")
ax_gen_metrics.axvline(mls_data_clubnames.Compensation.max(), color='r', linestyle='dashed', linewidth=1, label="max compensation")
ax_gen_metrics.set_xlabel('Compensation in million $')
ax_gen_metrics.set_ylabel('No of players')
ax_gen_metrics.set_title('Compensation distribution for players for 2007-2022')
ax_gen_metrics.legend(loc='upper center')

col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.markdown('''
    *Compensation in $*
    * Mean - {0}
    * Median - {1}
    * Max - {2}
    '''.format(mls_data_clubnames.Compensation.mean().round(2), mls_data_clubnames.Compensation.median().round(2), 
    mls_data_clubnames.Compensation.max().round(2))
    )
with col2:
    st.pyplot(fig_gen_metrics)
with col3:
    st.write("")

st.markdown("***")
col1, col2, col3, col4 = st.columns([1,2,2,1])
with col1:
    st.write("")
with col2:
    st.markdown('''
    **Mean compensation**
    ''')
    compensation_all_years_mean = mls_data_clubnames.groupby("Year")["Compensation"].mean().round(2)
    fig_mean_metrics, ax_mean_metrics = plt.subplots()
    ax_mean_metrics = compensation_all_years_mean.plot(legend=True)
    ax_mean_metrics.set_ylabel('Mean compensation in $')
    st.pyplot(fig_mean_metrics)
with col3:
    st.markdown('''
    **Median compensation**
    ''')
    compensation_all_years_median = mls_data_clubnames.groupby("Year")["Compensation"].median().round(2)
    fig_median_metrics, ax_mean_metrics = plt.subplots()
    ax_median_metrics = compensation_all_years_median.plot(legend=True)
    ax_median_metrics.set_ylabel('Median compensation in $')
    st.pyplot(fig_median_metrics)
with col4:
    st.write("")
col1, col2, col3, col4 = st.columns([1,2,2,1])
with col1:
    st.write("")
with col2:
    st.markdown('''
    **Maximum compensation**
    ''')
    compensation_all_years_max = mls_data_clubnames.groupby("Year")["Compensation"].max().round(2)
    fig_max_metrics, ax_max_metrics = plt.subplots()
    ax_max_metrics = compensation_all_years_max.plot(legend=True)
    ax_max_metrics.set_ylabel('Maximum compensation in $')
    st.pyplot(fig_max_metrics)
with col3:
    st.markdown('''
    **Minimum compensation**
    ''')
    compensation_all_years_min = mls_data_clubnames.groupby("Year")["Compensation"].min().round(2)
    fig_min_metrics, ax_min_metrics = plt.subplots()
    ax_min_metrics = compensation_all_years_min.plot(legend=True)
    ax_min_metrics.set_ylabel('Minimum compensation in $')
    st.pyplot(fig_min_metrics)
with col4:
    st.write("")


st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
st.subheader(
        '''
        Section 5
        '''
    )
st.sidebar.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
st.sidebar.subheader(
        '''
        Section 5
        Extract player information
        '''
    )

st.markdown('''
    **Extract player information**
''')
col1, col2, col3 = st.columns([1,3,1])
user_input = st.sidebar.text_input("Please provide player surname, for example", "Vela")
player_search = mls_data_clubnames[mls_data_clubnames["Last Name"] == user_input].sort_values(["First Name", "Year"])
player_search = player_search.drop(["Club", "uniquename"], axis=1).reset_index()
player_search = player_search[["Team", "Last Name", "First Name", "Pos", "Year", "Base Salary", "Compensation"]]
with col1:
    st.write("")
with col2:
    st.write(player_search)
with col3:
    st.write("")
st.sidebar.markdown('''
    ***
''')

st.markdown('''
    ***
''')
st.markdown('''
    **Teams playing in MLS**''')
col1, col2, col3 = st.columns([1.5,2,1])
display_teams = st.sidebar.checkbox("Display teams playing in MLS", value=True)
if display_teams:
    display_team_year = st.sidebar.selectbox("Select year to display", mls_data_clubnames["Year"].sort_values(ascending = False).unique(), index=0)
    display_team_for_year = mls_data_clubnames[mls_data_clubnames["Year"] == display_team_year]
    display_team_for_year = display_team_for_year["Team"].unique().tolist()
with col1:
    st.write("")
with col2:
    if display_teams:
        st.markdown('''
        **Year {0}**'''.format(display_team_year)
        )
        st.write(pd.DataFrame(display_team_for_year, columns=["Team Name"]))
    else:
        st.markdown('''
        **Tick the checkbox 'Display teams playing in MLS' and select a year in the sidebar**
        ''')
with col3:
    st.write("")
st.sidebar.markdown('''
    ***
''')

st.markdown('''
    ***
''')
st.markdown('''
    **Extract team information**
''')

st.sidebar.markdown(
        '''
        Extract team information
        '''
    )
col1, col2, col3 = st.columns([1,3,1])
user_input_team = st.sidebar.text_input("Please provide team name, for example", "Real Salt Lake")
team_search = mls_data_clubnames[mls_data_clubnames["Team"] == user_input_team].sort_values(["Team", "Year"])
team_search = team_search.drop(["Club", "uniquename"], axis=1).reset_index()
team_search = team_search[["Team", "Last Name", "First Name", "Pos", "Year", "Base Salary", "Compensation"]]
with col1:
    st.write("")
with col2:
    st.write(team_search)
with col3:
    st.write("")


#idx = mls_data_clubnames.groupby(['Year'])['Compensation'].transform(max) == mls_data_clubnames['Compensation']
#highest_paid_player_each_year = mls_data_clubnames[idx].sort_values(by=['Year'])
# st.write(highest_paid_player_each_year)

# plt.figure(figsize=(6, 6))
# x= sns.barplot(y = highest_paid_player_each_year["Last Name"], x = highest_paid_player_each_year["Compensation"], hue = highest_paid_player_each_year['Year'], orient='h')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# st.pyplot(x.figure)

# plt.figure(figsize=(60, 60))
# grid = sns.FacetGrid(mls_data_clubnames, col = "Year", hue = "Pos", col_wrap=4)
# grid.map(sns.scatterplot, "Pos", "Compensation")
# grid.add_legend()
# st.pyplot(grid.figure)