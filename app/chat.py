from transformers import pipeline, GPT2Tokenizer, GPT2LMHeadModel

def deploy_chat_assistant(model_dir='./fine_tuned_model'):
    
    # Load the fine-tuned model and tokenizer
    model = GPT2LMHeadModel.from_pretrained(model_dir)
    tokenizer = GPT2Tokenizer.from_pretrained(model_dir)

    # Initialize the pipeline for text generation
    chat_assistant = pipeline('text-generation', model = model, tokenizer = tokenizer)

    return chat_assistant

chat_assistant = deploy_chat_assistant()

# Generate a response based on a user prompt
user_input = input("Enter your question here:  ")
response = chat_assistant(user_input, max_length=500, num_return_sequences=1)

print(response[0]['generated_text'])
