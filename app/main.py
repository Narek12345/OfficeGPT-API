from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from llama_index import (
	Document,
	LLMPredictor,
	PromptHelper,
	StorageContext,
	GPTVectorStoreIndex,
	load_index_from_storage,
)

from langchain.llms import OpenAI

import os

app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
	return templates.TemplateResponse('index.html', {'request': request})


@app.post('/upload_file_for_training')
async def upload_file_for_training(file: UploadFile, OPENAI_API_KEY: str):
	os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

	try:
		contents = file.file.read()
		with open(file.filename, 'wb') as f:
			f.write(contents)
	except Exception:
		return {"message": "There was an error uploading the file"}
	finally:
		file.file.close()
		os.remove(file.filename)

	text = contents.decode()

	llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name='text-davinci-003', max_tokens=300))
	prompt_helper = PromptHelper(4096, 300, 0.2, chunk_size_limit=600)

	documents = [Document(text=text)]

	index = GPTVectorStoreIndex.from_documents(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

	index.storage_context.persist()


@app.get('/make_request_in_chatgpt')
async def make_request_in_chatgpt(text: str):
	storage_context = StorageContext.from_defaults(persist_dir='./storage')
	index = load_index_from_storage(storage_context)

	query_engine = index.as_query_engine()
	response = query_engine.query(text)

	return response
