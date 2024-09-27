# Customer Chat Assistant For Tymeline

Create the virtual environment using following command:

`python -m venv env_name`

Install the dependencies using the following command:

`pip install -r requirements.txt`

## Data Preparation:

1. `web_crawler.py`
- To get the data about Tymline, a web crawling script is made and the data is collected till depth of 3.

- It will make the folder _data_ in which the scrapped data will be saved level-wise.

2. `clean_text.py`

- This script will clean the scrapped text and remove the special characters, extra whitespace and non-ASCII characters.

- The cleaned data will be stored in _cleaned_data_ directory.

## Model Training:

1. `train_model.py`
- This script will prepare data in the form which is required for transformer model fine-tuning.
- Then it will load the pre-trained model encoder and tokenizer to train the model. Here `gpt2` is used as the application is chatbot.
-  The fine-tuned model is saved in _fine_tuned_model_ directory.

## Chat

1. `chat.py`
- This script calls the trained model and the user can chat.

2. `qa.py`
- This is the script for RAG application to enhance the performance. 
- Here the FAISS vector-store is used for storing the embeddings and GROQ cloud is used to load the LLM `mixtral-8x7b-32768`. 
- Create GROQ API key from this link: https://console.groq.com/ 
- To know more about FAISS, visit this link: https://ai.meta.com/tools/faiss/ 
- To chat with RAG system, run this file.
