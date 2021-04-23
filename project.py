#reference below is mentions as reference for myself
import pandas as pd
by=pd.read_csv('/Users/bhaskaryuvaraj/Desktop/Downloads/Credit_Card_Complaints.csv')
#The length of rows and columns
len(by)
len(by.columns)
#the length of rows and columns are: rows=87718, columns=18
by.columns
##the column names are: ['Date received', 'Product', 'Sub-product', 'Issue', 'Sub-issue',
#       'Consumer complaint narrative', 'Company public response', 'Company',
#       'State', 'ZIP code', 'Tags', 'Consumer consent provided?',
#       'Submitted via', 'Date sent to company', 'Company response to consumer',
#       'Timely response?', 'Consumer disputed?', 'Complaint ID'] 

#extracting the 1st 5 data
by.head()
#extracting the last 5 data
by.tail()
#finding the missing values
by.isnull().sum()
#the missing values are found to be: 
#Date received                       0
#Product                             0
#Sub-product                     87718
#Issue                               0
#Sub-issue                       87718
#Consumer complaint narrative    70285
#Company public response         67762
#Company                             0
#State                             738
#ZIP code                          738
#Tags                            74460
#Consumer consent provided?      58155
#Submitted via                       1
#Date sent to company                0
#Company response to consumer        0
#Timely response?                    0
#Consumer disputed?               3810
#Complaint ID                       0
# from the above observation, it is found that there is no missing values in issue column, but,
# since there are 738 missing values in state, it can be filtered out
by=by[by['State'].notnull()]
by=by[by['ZIP code'].notnull()]
by.describe()
#sstatstical summary cannot be done, since there is no any numerical data in the data as shown:
#       Sub-product  Sub-issue  Complaint ID
#count          0.0        0.0  8.771800e+04
#mean           NaN        NaN  1.151420e+06
#std            NaN        NaN  7.736195e+05
#min            NaN        NaN  1.000000e+00
#25%            NaN        NaN  4.078432e+05
#50%            NaN        NaN  1.182588e+06
#75%            NaN        NaN  1.860373e+06
#max            NaN        NaN  2.428845e+06

by['Issue'].unique() #reference

#Now creating a new column "issue type" based on issue variable
by['issue type']=by['Issue'].replace(['Delinquent account','Closing/Cancelling account',
  'Forbearance / Workout plans','Payoff process','Credit determination','Balance transfer',
  'Rewards','Billing statement','Billing disputes','Balance transfer fee','Late fee',
  'Overlimit fee','Cash advance fee','Credit line increase/decrease','Transaction issue',
  'Credit card protection / Debt protection','Unsolicited issuance of credit card','Privacy',
  'Bankruptcy','Arbitration','Sale of account','Credit reporting','Collection practices',
  'Collection debt dispute','Identity theft / Fraud / Embezzlement','APR or interest rate',
  'Advertising and marketing','Application processing delay','Other','Customer service / Customer relations',
  'Cash advance','Convenience checks','Other fee'],['Account related',
    'Account related','Account related','Benefits','Benefits','Benefits','Benefits',
    'Billing and Fee','Billing and Fee','Billing and Fee','Billing and Fee','Billing and Fee',
    'Billing and Fee','Credit line','Dispute','Dispute','Dispute','Dispute','Dispute','Dispute',
    'Dispute','Dispute','Dispute','Dispute','Fraud','Interest Rate','Other','Other','Other',
    'Other','Other','Other','Other'])

by['Company response to consumer'].unique() #reference

#now creating a new subset with just closed in beginning
ab=by[(by['Company response to consumer']=='Closed') | (by['Company response to consumer']==
      'Closed with explanation') | (by['Company response to consumer']== 'Closed with monetary relief') 
| (by['Company response to consumer']=='Closed with non-monetary relief') | 
(by['Company response to consumer']=='Closed without relief') | (by['Company response to consumer']==
'Closed with relief')]
#alternate method
ab=by[by['Company response to consumer'].str[0:6]=='Closed']

ab['Company response to consumer'].isnull().sum() #reference
#changing the date format
ab=ab[ab['Date received'].replace('%m-%d-%y','%m/%d/%y')]
ab=ab[ab['Date sent to company'].replace('%m-%d-%y','%m/%d/%y')]

#now creating anew column('case handled')
ab['Case handled']=ab['Timely response?'].replace(['Yes','No'],['Handed properly','Not Handed properly'])

#exporting as excel file
ab.to_excel('/Users/bhaskaryuvaraj/Desktop/Downloads/Data Report.xlsx')

import matplotlib.pyplot as plt
#finding the count of top 5 states
ab.groupby('State')['Consumer complaint narrative'].count().sort_values(ascending=False).head()
#filtering the data only on top 5 states
ab=ab[(ab['State']=='CA') | (ab['State']=='NY') | (ab['State']=='FL') | (ab['State']=='TX') | (ab['State']=='NJ')]
ab['issue type'].unique()#reference
ab['Case handled'].unique()#reference

ab.groupby('issue type')['Case handled'].count() #reference(code for both handled and not handled)
#creating seperate dataframe for case handled and case not handled properly seperately
case_handled1=ab[ab['Case handled']=='Handed properly']
case_not_handled_properly=ab[ab['Case handled']=='Not Handed properly']
#now finding the count of case handled properly and not handled properly seperately with graph
case_handled1.groupby('issue type')['Case handled'].count().plot(kind='barh')
#from graph it is found that billing and fees case has been handled properly the most
case_not_handled_properly.groupby('issue type')['Case handled'].count().plot(kind='bar')
#from the graph it is found that 'billing and fees', 'dispute', 'others' section has the most not handled case
#these three catagories has to be paid attention on

#to find the percentage of complaints submitted on each of the issue type
#y=ab.groupby('issue type')['Consumer complaint narrative'].count()
#ab.groupby('issue type')['Consumer complaint narrative'].count().apply(lambda x: x/y*100)
#alternate for the above code
ab.groupby('issue type')['Complaint ID'].count()/len(ab['Complaint ID'])*100
#issue type
#Account related    12.793664
#Benefits           12.055309
#Billing and Fee    24.687878
#Credit line         2.053967
#Dispute            11.384078
#Fraud               9.142167
#Interest Rate       4.416700
#Other              23.466237

#the percentage of the customer complaint narrative based on issue type is shown above, and 'billing and fee'
# and 'other' sections have most number of complaints

#the ratio of timely response with yes or no is given by:
ab.groupby('Timely response?')['Timely response?'].count()
#Timely response?
#No       340
#Yes    36628

ab['Submitted via'].unique()#reference
#now finding the key sources with which the complaints are submitted
ab.groupby('Submitted via')['Submitted via'].count()
#it is found that most of the customer submitted their issues through the web(25090 customers)

#filtering the complaints that are not resolved on time
complaints_not_resolved_ontime=ab[ab['Timely response?']=='No']
complaints_not_resolved_ontime['Case handled'].unique()#reference

#now exporting the above data in excel
complaints_not_resolved_ontime.to_excel('/users/bhaskaryuvaraj/Desktop/Downloads/Unresolved_complaints_ontime.xlsx')
#count of unresolved cases state wise
complaints_not_resolved_ontime.groupby('State')['State'].count()
# if you c at the complaints not resolved data, it is found that CA has the most number of unsolved data with 131.
#count of unresolved cases state wise and issue type
complaints_not_resolved_ontime.groupby(['State','issue type'])['issue type'].count().plot(kind='bar')
#again further in CA the most number of unresolved case is found in 'Dispute' section
#and it is clear from the graph also that CA has the most number of unresolved cases in "dispute" section.
#the least number of unresolved cases are in FL and NJ in "account related" and "credit line" sections respectively.