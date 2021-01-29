#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)
purchase_data.head(20)


# ## Player Count

# * Display the total number of players
# 

# In[3]:


# display total number of players 
total_players = len(pd.unique(pd.Series(purchase_data["SN"])))
total_df=pd.DataFrame ({"Total Players": [total_players]}, columns=["Total Players"])
total_df


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[4]:


#number of unique items 
unique_items = purchase_data["Item ID"].nunique()

#Overall average price 
avg_price = purchase_data["Price"].mean()

#total number of purchases (count the rows)
total_purchases = purchase_data["Purchase ID"].count()

#calculate total revenue from price column 
total_revenue = purchase_data["Price"].sum()


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[16]:


# create a new data frame and drop duplicate records
gender_info = purchase_data[["SN","Gender"]].drop_duplicates()

#calculate gender totals/count
gender_totals = gender_info["Gender"].value_counts()

#calculate % of each 
gender_percent =[round((gender_totals[0]/total_players)*100,2),round((gender_totals[1]/total_players)*100,2),round((gender_totals[2]/total_players)*100,2)]

#display new df 
gender_df = pd.DataFrame({'Total Count': gender_totals,
                        'Percent of Players': gender_percent})

#fix percent column 
gender_df['Percent of Players'] = gender_df['Percent of Players'].map('{:.1f}%'.format)
gender_df.head()


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[18]:


# calculate purchase count, average purchase price, average purchase total (first dataframe)

purchase_count = purchase_data.groupby(["Gender"]).count()['SN']
purchase_price = purchase_data.groupby(["Gender"]).mean()['Price']
purchase_value = purchase_data.groupby(["Gender"]).sum()['Price']

# Average total per individual
gender_avg_total = purchase_value / gender_df['Total Count']

# building and formatting dataframe to display - round to two instead of one for dollar amounts
gender_data_df = pd.DataFrame({'Purchases Made': purchase_count,
                               'Average Price of Purchases': purchase_price.map('${:,.2f}'.format),
                               'Total Value': purchase_value.map('${:,.2f}'.format),
                               'Avgerage Total Purchase per Person': gender_avg_total.map('${:,.2f}'.format)})
gender_data_df


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[25]:


# new dataframe for age
age_ranges = purchase_data[['Age','SN']].drop_duplicates()

# creating bins by 4 years
age_bins = [0, 9, 14, 19, 24, 29, 34, 39, 80]

# bin names
age_label = ['<10', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40+']

# split players into bins 
age_ranges['Age Ranges'] = pd.cut(age_ranges['Age'], age_bins, labels=age_label)

# total count column values
age_count = age_ranges['Age Ranges'].value_counts()

# percentage of players column values
age_percent = ((age_count / total_players) * 100).round(2)

# building and formating dataframe to display
age_ranges = pd.DataFrame({'Total Amount': age_count,'Percent of Players': age_percent})
age_ranges['Percent of Players'] = age_ranges['Percent of Players'].map('{:.2f}%'.format)
age_ranges.sort_index()


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[29]:


# split into bins
purchase_data['Age Ranges'] = pd.cut(purchase_data['Age'], age_bins, labels=age_label)

# calculating total count of purchases
purch_count = purchase_data.groupby(['Age Ranges']).count()['Purchase ID']

# calculate average purchase price
avg_price = purchase_data.groupby(['Age Ranges']).mean()['Price']

# calculate total purchase value
tot_value = purchase_data.groupby(['Age Ranges']).sum()['Price']

# calculating avg purchase per person total 
avg_per_player = tot_value / age_ranges['Total Amount']

# build dataframe
age_purchases = pd.DataFrame({'Purchases Count': purch_count.map('{:,}'.format),
                          'Average Purchase Price': avg_price.map('${:,.2f}'.format),
                          'Total Purchase Value': tot_value.map('${:,.2f}'.format),
                          'Avg Total per Person': avg_per_player.map('${:,.2f}'.format)})
age_purchases


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[31]:


# calculate purchase count
spend_count = purchase_data.groupby(['SN']).count()['Purchase ID']

# calculate avg purchase price
spend_avg = purchase_data.groupby(['SN']).mean()['Price']

# calculate total purchase value
spend_tot = purchase_data.groupby(['SN']).sum()['Price']

# build dataframe
spending_df = pd.DataFrame({'Purchase Count': spend_count, 'Average Purchase Price': spend_avg, 'Total Value': spend_tot})

# sorting by total purchase value
sorted_spending_df = spending_df.sort_values('Total Value', ascending=False)

# formating average purchase price
sorted_spending_df['Average Purchase Price'] = sorted_spending_df['Average Purchase Price'].map('${:,.2f}'.format)

# formating total purchase value
sorted_spending_df['Total Value'] = sorted_spending_df['Total Value'].map('${:,.2f}'.format)

# display dataframe of top five spenders
sorted_spending_df = sorted_spending_df.loc[:,['Purchase Count', 'Average Purchase Price', 'Total Value']]
sorted_spending_df.head(5)


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, average item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[34]:


# new data frame
items = purchase_data[["Item ID", "Item Name", "Price"]]

# groupe by item id and item name 
item_stats = items.groupby(["Item ID","Item Name"])

# total amount of times an item was purchased
purch_count_item = item_stats["Price"].count()

# calcualte item purchase value 
purch_value = (item_stats["Price"].sum()) 

# price per item
item_price = purch_value/purch_count_item

# building dataframe
most_popular_items = pd.DataFrame({"Purchase Count": purch_count_item, 
                               "Item Price": item_price,
                               "Total Purchase Value":purch_value})

# put purchase count into decesneding order 
most_popular_formatted = most_popular_items.sort_values(["Purchase Count"], ascending=False).head()

# formating dataframe
most_popular_formatted.style.format({"Item Price":"${:,.2f}",
                            "Total Purchase Value":"${:,.2f}"})


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[40]:


# change sorting of the most popular items data frame to find highest purchase value
most_popular_formatted = most_popular_items.sort_values(["Total Purchase Value"],ascending=False)

# formatting dataframe
most_popular_formatted.style.format({"Item Price":"${:,.2f}", "Total Purchase Value":"${:,.2f}"})


# In[ ]:





# In[ ]:




