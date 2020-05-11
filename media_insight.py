#%%
from defines import getCreds, makeApiCall
import pandas as pd
import csv

#%%
def getMediaInsights(params) :
	""" Get insights for a specific media id
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{ig-media-id}/insights?metric={metric}
	Returns:
		object: data from the endpoint
	"""
	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['metric'] = 'engagement,impressions,reach,saved,video_views'# fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	url = params['endpoint_base'] + params['post_id'] + '/insights' # endpoint url

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call
#%%
usermedia = pd.read_csv("output_usermedia1.csv")
post_id = usermedia['id']
all_value = []


for i in range(len(usermedia['id'])):
	params = getCreds() # get creds
	params['post_id'] = str(post_id[i])
	response = getMediaInsights(params) # get insights for a specific media id
	if not 'error' in response['json_data'].keys(): #비즈니스 계정이 아닌 경우 제외
		for insight in response['json_data']['data'] : # loop over post insights
			#params['latest_media_id'] = 각 id
			if not 'error' in insight.keys():
				all_value.append(insight['values'][0]['value'])

#%%
f = open('media_insight.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow(['engagement','impressions','reach','saved','video_views'])
j = 0
for i in range(int(len(all_value)/5)):
	wr.writerow([all_value[j], all_value[j+1],all_value[j+2], all_value[j+3],all_value[j+4]])
	j+=5
f.close()

#%%
#POST INSIGHTS -----

#	참여 (lifetime): 39
#	노출 (lifetime): 94
#	도달 (lifetime): 83
#	저장됨 (lifetime): 0
#	동영상 조회 (lifetime): 32


