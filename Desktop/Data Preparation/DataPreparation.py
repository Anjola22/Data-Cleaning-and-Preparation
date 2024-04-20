#!/usr/bin/env python
# coding: utf-8

# # This notebook is for course two : Data understanding and Preparation  
# Please try to go through the code steps mentioned in the course and try to create the code on your own. Use this document as a reference incase you face problems in writing the code

# # Importing Data files

# In[2]:


#Import Product DataSet here


# In[3]:


#Import Transaction DataSet Here


# In[4]:


#Import Customer Dataset Here


# # Quick Data Exploration

# In[5]:


product_data.shape


# In[5]:


transactions_data.shape


# In[6]:


customer_data.shape


# ###### We can conclude from the above that Retailer X sells 30 products and served 500 customers in a total of 10,000 recorded transactions. 

# In[7]:


type(customer_data)


# In[8]:


type(customer_data.AGE)


# In[9]:


customer_data.dtypes


# In[1]:


customer_data['INCOME']=customer_data['INCOME'].map(lambda x : x.replace('$',''))


# In[11]:


customer_data.head(2)


# In[12]:


customer_data['INCOME']=customer_data['INCOME'].map(lambda x : int(x.replace(',','')))


# In[13]:


customer_data.head(2)


# In[14]:


customer_data.dtypes


# Now running the “dtypes” method reveals that data type conversion of INCOME was successful 

# In[15]:


customer_data["MARITAL STATUS"].describe()


# In[16]:


customer_data["INCOME"].describe()


# In[22]:


customer_data["MARITAL STATUS"].unique()


# In[20]:


from datetime import datetime
customer_data['ENROLLMENT DATE']=customer_data['ENROLLMENT DATE'][customer_data['ENROLLMENT DATE'].notnull()].map(lambda x :datetime.strptime(x, '%d-%m-%Y') )


# In[21]:


customer_data.dtypes


# ## Data Quality
# Data used in this tutorial is mostly free from data quality issues, however in real life, data scientists deal with data sets that needs to be cleaned and corrected for their quality issues

# In[23]:


print('null values for transactoins ?',transactions_data.isnull().values.any())
print('null values for products ?',product_data.isnull().values.any())
print('null values for customers ?',customer_data.isnull().values.any())


# In[1]:


customer_data.columns[customer_data.isna().any()]tolist()


# It turned out that ENROLMENT DATE is the only column which has null values. 
# The reasons behind is that not all customers are enrolled to loyalty and hence there is no enrolment date

# # Analysis of the distribution of variables using graphs 

# In[25]:


import matplotlib.pyplot as plt


# ### Univariate Analysis (Single variable analysis)

# In[ ]:


customer_data['MARITAL STATUS'].value_counts().plot(kind='bar')
plt.xlabel("Marital Status")
plt.ylabel("Frequency Distribution")
plt.show()


# In[27]:


customer_data['AGE'].hist(bins=10)  
plt.show()


# In[28]:


plt.figure(figsize=(8,8))
plt.boxplot(customer_data.AGE,0,'rs',1)
plt.grid(linestyle='-',linewidth=1)
plt.show()


# In[29]:


customer_data['AGE'].describe()


# ### Constructing new features and generating Insights

# Remember our business understanding objectives
# 1-Understanding the factors associated with loyalty program participation
# 2-Understanding the factors associated with increased spending
# 

# In[30]:


trans_products=transactions_data.merge(product_data,how='inner', left_on='PRODUCT NUM', right_on='PRODUCT CODE')


# In[31]:


trans_products.head()


# In[32]:


trans_products['UNIT LIST PRICE']=trans_products['UNIT LIST PRICE'].map(lambda x : float(x.replace('$','')))


# In[33]:


trans_products.dtypes


# In[34]:


trans_products['Total_Price']=trans_products['QUANTITY PURCHASED'] * trans_products['UNIT LIST PRICE'] * (1- trans_products['DISCOUNT TAKEN'])


# In[35]:


trans_products.head()


# In[36]:


Income_by_product = trans_products.groupby('PRODUCT CATEGORY').agg({'Total_Price':'sum'}).sort_values('Total_Price',ascending=False)


# In[37]:


Income_by_product


# In[38]:


Revenue_by_product=Income_by_product.rename(columns={'Total_Price':'Revenue Per Product'})


# In[39]:


Revenue_by_product['Revenue Per Product'].plot(kind='pie',autopct='%1.1f%%',legend = True)


# ##### For each customer , we will calculate total spend ,total spend per category ,recent transaction date

# In[40]:


customer_prod_categ=trans_products.groupby(['CUSTOMER NUM','PRODUCT CATEGORY']).agg({'Total_Price':'sum'})


# In[41]:


customer_prod_categ.head()


# In[42]:


customer_prod_categ.columns


# In[45]:


customer_prod_categ.reset_index().head()


# In[46]:


customer_prod_categ=customer_prod_categ.reset_index()


# In[47]:


customer_pivot=customer_prod_categ.pivot(index='CUSTOMER NUM',columns='PRODUCT CATEGORY',values='Total_Price')


# In[48]:


customer_pivot.head()


# In[49]:


trans_products['TRANSACTION DATE']=trans_products['TRANSACTION DATE'].map(lambda x :datetime.strptime(x, '%m/%d/%Y') )


# In[50]:


recent_trans_total_spend=trans_products.groupby('CUSTOMER NUM').agg({'TRANSACTION DATE':'max','Total_Price':'sum'}). rename(columns={'TRANSACTION DATE':'RECENT TRANSACTION DATE','Total_Price':'TOTAL SPENT'})
recent_trans_total_spend.head()


# In[51]:


customer_KPIs=customer_pivot.merge(recent_trans_total_spend,how='inner',left_index=True, right_index=True )


# In[52]:


customer_KPIs.head()


# In[53]:


customer_KPIs=customer_KPIs.fillna(0)
customer_KPIs.head()


# In[54]:


customer_all_view=customer_data.merge(customer_KPIs,how='inner', left_on='CUSTOMERID', right_index=True)


# In[56]:


customer_all_view.head()


# ## Bivariate Analysis (2-variable analysis) – Loyalty as a target variable 

# #### Gender

# In[57]:


table=pd.crosstab(customer_all_view['GENDER'],customer_all_view['LOYALTY GROUP'])
table


# In[58]:


table.plot(kind='bar', stacked=True,figsize=(6,6))
plt.show()


# #### Experience Score

# In[59]:


table=pd.crosstab(customer_all_view['EXPERIENCE SCORE'],customer_all_view['LOYALTY GROUP'])
table


# In[60]:


table.plot(kind='bar', stacked=True,figsize=(6,6))
plt.show()


# #### Marital Status

# In[61]:


table=pd.crosstab(customer_all_view['MARITAL STATUS'],customer_all_view['LOYALTY GROUP'])
table.plot(kind='bar', stacked=True,figsize=(6,6))
plt.show()


# #### Age

# In[62]:


customer_all_view['AGE_BINNED'] = pd.cut(customer_all_view['AGE'],10) # 10 bins of age


# In[63]:


customer_all_view['AGE_BINNED'].value_counts()


# In[64]:


table=pd.crosstab(customer_all_view['AGE_BINNED'],customer_all_view['LOYALTY GROUP'])
table.plot(kind='bar', stacked=True,figsize=(6,6))
plt.show()


# In[65]:


customer_all_view.groupby("LOYALTY GROUP").agg({'AGE':'mean'})


# In[66]:


fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
plot1=customer_all_view['AGE'][customer_all_view['LOYALTY GROUP'] == "enrolled"]
plot2=customer_all_view['AGE'][customer_all_view['LOYALTY GROUP'] == "notenrolled"]
list1=[plot1,plot2]
ax.boxplot(list1,0,'rs',1)
ax.set_xticklabels(['Enrolled', 'Not Enrolled'])
plt.grid( linestyle='-', linewidth=1)
plt.show()


# #### Total Spend

# In[67]:


customer_all_view['TOTAL SPENT BINNED'] = pd.cut(customer_all_view['TOTAL SPENT'],10) # 10 bins of age


# In[68]:


table=pd.crosstab(customer_all_view['TOTAL SPENT BINNED'],customer_all_view['LOYALTY GROUP'])
table.plot(kind='bar', stacked=True,figsize=(6,6))
plt.show()


# ## Bivariate Analysis (2-variable analysis) – Customer spend as a target variable 

# #### Age

# In[69]:


plt.scatter(customer_all_view['AGE'],customer_all_view['TOTAL SPENT'])
plt.xlabel("AGE")
plt.ylabel("Total Spent")
plt.show()


# In[70]:


from scipy.stats import pearsonr
pearsonr(customer_all_view['AGE'],customer_all_view['TOTAL SPENT'])


# #### Income

# In[71]:


plt.scatter(customer_all_view['INCOME'],customer_all_view['TOTAL SPENT'])
plt.xlabel("Income")
plt.ylabel("Total Spent")
plt.show()


# In[72]:


pearsonr(customer_all_view['INCOME'],customer_all_view['TOTAL SPENT'])


# #### Experience Score

# In[73]:


table = customer_all_view.groupby(['EXPERIENCE SCORE']).agg({'TOTAL SPENT':'mean'}).reset_index()


# In[74]:


table['TOTAL SPENT'].plot(kind='bar')
plt.xlabel("Experience Score")
plt.ylabel("Average Total Spent per Score")
plt.xticks([0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9,10])    
plt.show()


# In[ ]:




