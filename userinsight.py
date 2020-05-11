#%%
from defines import getCreds, makeApiCall
import time, datetime 
from datetime import timedelta
import csv
#%%
current_time = time.time()
past_time = (datetime.datetime.now() - timedelta(days=30)).timestamp()
print(current_time, past_time)
#%%
def getUserInsights( params ) :
	""" Get insights for a users account
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{ig-user-id}/insights?metric={metric}&period={period}&since={since}&until={until}
	Returns:
		object: data from the endpoint
	"""
	
	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['metric'] = 'follower_count,impressions,profile_views,reach' # fields to get back
	endpointParams['period'] = 'day' # period
	endpointParams['since'] = int(past_time)
	endpointParams['until'] = int(current_time)
	endpointParams['access_token'] = params['access_token'] # access token
	url = params['endpoint_base'] + params['instagram_account_id'] + '/insights' # endpoint url

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call


#https://graph.facebook.com/v7.0/17841432010317578/insights?metric=impressions,reach,profile_views&period=day&since={since}&until={until}

#%%
params = getCreds() 
response = getUserInsights( params ) 

all_values = [] #follower_count-> all_values[0:30],impressions-> all_values[30:60],profile_views-> all_values[60:90],reach-> all_values[90:120]
#모든 값을 append해서  all_values(list)를 완성
for insight in response['json_data']['data'] : 
	for value in insight['values'] :
		v = value['value']
		all_values.append(v)

#%%
#30일전~현재까지의 date를 생성한 end_time(list)를 완성
def createDate():
	end_time = []
	date = datetime.datetime.fromtimestamp(past_time)
	for i in range(30):
		end_time.append(date.date() + datetime.timedelta(+i))
	return end_time
#%%
#'end_time','follower_count','impressions','profile_views','reach'를 변수로 하는 'output.csv' 생성
end_time = createDate()
f = open('output_userinsight1.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow(['end_time','follower_count','impressions','profile_views','reach'])
for i in range(30):
	wr.writerow([end_time[i], all_values[i], all_values[30+i], all_values[60+i], all_values[90+i]])
f.close()

	

