import requests, json

URL = 'http://127.0.0.1:8000'


def upload_file_for_training():
	url = URL + '/upload_file_for_training'
	params = {'OPENAI_API_KEY': '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'}
	file = {'file': open(r'C:\Users\Нарек\Desktop\document.txt')}
	resp = requests.post(url=url, params=params, files=file)


def make_request_in_chatgpt():
	text = 'Как меня зовут. Какая у меня нация ?'
	url = URL + '/make_request_in_chatgpt'
	params = {'text': text}
	resp = requests.get(url=url, params=params)

	data = resp.json()
	print(data)


upload_file_for_training()
make_request_in_chatgpt()