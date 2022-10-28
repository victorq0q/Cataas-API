import requests
from random import choice


#check APi and internet connection
try:
    requests.get("https://cataas.com/")
except Exception as e:
    print(">> Cataas API request erro <<")
    raise e

API_URL = "https://cataas.com/cat" 

cat_type_list =  ["small", "sm", "medium", "md", "square","sq", "original","or"]
image_filter_list = ["blur", "mono", "sepia", "negative", "paint", "pixel"]

tag_list = requests.get("https://cataas.com/api/tags").json() #returns a list of all tags 


def _get_data(url_method="", params=None):
	if not params:
	   params = {"json": "true"} #add json parameter for api to return the data as json
	elif type(params) == dict:    
	   params["json"] = "true"   

	data = requests.get(f"{API_URL}{url_method}", params=params)

	error_msg = "Cataas API\n Data not found!, check if the api is working\n or check if the api has a new version = > https://cataas.com/"
	if data.status_code == 404 or data.headers["Content-Type"] != "application/json":
	   print(error_msg)
	
	elif len(data.json()) == 0:
	    print(error_msg)

	else:
	    return data.json()


def cat(tag=False, text=False, cat_type=False, img_filter=False, width=False, heigth=False):
	methods = "" 
	params = {}  
							
	if tag in tag_list:
	    methods = f"{methods}/{tag}"
	if text:
	    methods = f"{methods}/says/{text}"

	if cat_type in cat_type_list:
	    params["type"] = cat_type
	if img_filter in image_filter_list:
	    params["filter"] = img_filter

	if width:
	    params["width"] = width
	if heigth:
	    params["heigth"] = heigth

	resp = _get_data(url_method=methods, params=params) #final url exemple: https://cataas.com/{methods}?{params}
	resp["url"] = "https://cataas.com" + resp["url"]

	return resp


def random(text=False, img_filter=False):
	methods = ""
	params = {}

	methods = f"{methods}/{choice(tag_list)}"
	params["type"] = choice(cat_type_list)

	if text:
	   methods = f"{methods}/says/{text}"

	if img_filter in image_filter_list:
	   params["filter"] = choice(image_filter_list)

	random_resp = _get_data(url_method=methods, params=params)
	random_resp["url"] = "https://cataas.com" + random_resp["url"]

	return random_resp


def download(cat_data):
	if type(cat_data) == dict:
		if "file" in cat_data and "url" in cat_data: #check if filename and url exist

			file_name = cat_data["file"]
			url = cat_data["url"]

			with open(file_name, "wb") as new:
				new.write(requests.get(url).content)

		else:
		    print("Cataas api\n Data not found, unable to save the file")
	else:
	    print("Cataas api\n argument is of type dictionary, unable to save the file")
