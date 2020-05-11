#%%
from defines import getCreds, makeApiCall

#%%
permalink =[]
id = []
caption = []
media_type = []
comments = []
comment_n = []
post_date = []
post_n = 100
comments = [[] for i in range(post_n)]

#%%
def getUserMedia( params ) :
	""" Get users media
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['fields'] = 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username,comments' # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	url = params['endpoint_base'] + params['instagram_account_id'] + '/media' # endpoint url

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call
#%%
#%%
params = getCreds() # get creds
response = getUserMedia( params ) # get users media from the api
print(response)
#%%
params = getCreds() # get creds
response = getUserMedia( params ) # get users media from the api
i=0
for post in response['json_data']['data']:
	n=0
	permalink.append(post['permalink']) # link to post
	id.append(post['id'])
	caption.append(post['caption'])# post caption
	media_type.append(post['media_type']) # type of media
	if 'comments' in post.keys():
		for comment in post['comments']['data']:
			comments[i].append(comment['text'])
			n+=1
			#comments.append(comment['text'])
	i+=1
	comment_n.append(n)
		
	post_date.append(post['timestamp']) # when it was posted

	if 'VIDEO' == response['json_data']['data'][0]['media_type'] : # media is a video
		params['metric'] = 'engagement,impressions,reach,saved,video_views'
	else : # media is an image
		params['metric'] = 'engagement,impressions,reach,saved'

#%%
import csv
caption_body = []
caption_tag = []
capt = caption
f = open('output_usermedia1.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
wr.writerow(['permalink', 'id', 'caption_body','caption_tag', 'media_type', 'comments', 'comment_n', 'post_date'])
for i in range(len(id)):
	capt_l = capt[i].replace('\n','').split('#')
	capt_body= capt_l[0]
	capt_tag = capt_l[1:len(capt_l)]
	wr.writerow([permalink[i],id[i],capt_body,capt_tag,media_type[i],comments[i],comment_n[i],post_date[i]])
f.close()

#'permalink', 'id', 'caption', 'media_type', 'comments', 'comment_n', 'post_date'
