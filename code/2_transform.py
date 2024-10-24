import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here
states_data = pd.read_csv('cache/states.csv')
survey_data = pd.read_csv('cache/survey.csv')

# create a unique list of years from the survey data
years = survey_data['year'].unique()

#For each year in the survey data, load the cost of living data from the cache into a dataframe,
#then combine all the dataframes into a single cost of living (COL) dataframe col_data

col1 = pd.read_csv('cache/col_2021.csv')
col2 = pd.read_csv('cache/col_2022.csv')
col3 = pd.read_csv('cache/col_2023.csv')
col4 = pd.read_csv('cache/col_2024.csv')

col_data = pd.concat([col1, col2, col3, col4])

# First, clean the entry under "Which country do you work in?" so that all US countries say "United States" 
# use the clean_country_usa function in pandaslib.py function here and generate a new column _country

survey_data['_country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)

#Next under the "If you're in the U.S., what state do you work in?" column we need to convert the states into state codes 
# Example: "New York => NY" to do this, join the states dataframe to the survey dataframe. User and inner join to drop non-matches. 
# Call the new dataframe survey_states_combined

survey_states_combined = pd.merge(survey_data, states_data, left_on='If you\'re in the U.S., what state do you work in?', right_on='State', how='inner')

#Engineer a new column consisting of the city, a comma, the 2-character state abbreviation,
#  another comma and _country For example: "Syracuse, NY, United States". name this column _full_city

survey_states_combined['_full_city'] = survey_states_combined['What city do you work in?'] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['_country']

#create the dataframe combined by matching the survey_states_combined to cost of living data matching on the year and _full_city columns

combined = pd.merge(survey_states_combined, col_data, left_on=['year', '_full_city'], right_on=['year', 'City'], how='inner')

#Finally we want to normalize each annual salary based on cost of living. How do you do this?
#  A COL 90 means the cost of living is 90% of the average, so $100,000 in a COL city of 90 is the equivalent buying power of(100/90) * $100,000 == $111,111.11
#Clean the salary column so that its a float. Use clean_currency function in pandaslib.py. generate a new column __annual_salary_cleaned

combined['__annual_salary_cleaned'] = combined['What is your annual salary? (You\'ll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)'].apply(pl.clean_currency)

#generate a column _annual_salary_adjusted based on this formula.

combined['_annual_salary_adjusted'] = (combined['__annual_salary_cleaned'] / combined['Cost of Living Index']) * 100

#4. Dataset is engineered, time to produce the reports:
#At this point you have engineerd the dataset required to produce the necessary reports.
#Save the engineered dataset to the cache survey_dataset.csv
#create the first report to show a pivot table of the the average _annual_salary_adjusted with _full_city
# in the row and Age band (How old are you?) in the column. Save this back to the cache as annual_salary_adjusted_by_location_and_age.csv

combined.to_csv('cache/survey_dataset.csv', index=False)

pivot = combined.pivot_table(index='_full_city', columns='How old are you?', values='_annual_salary_adjusted', aggfunc='mean')

pivot.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')
#create a similar report but show highest level of education in the column. 

pivot2 = combined.pivot_table(index='_full_city', columns='What is your highest level of education completed?', values='_annual_salary_adjusted', aggfunc='mean')
#Save this back to the cache as annual_salary_adjusted_by_location_and_education.csv

pivot2.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')



