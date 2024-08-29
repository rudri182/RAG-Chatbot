import os
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling


def prepare_data_for_finetuning(data_dir, output_file):
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
    
        for root, dirs, files in os.walk(data_dir):
            for file in files:
    
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
    
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        text = infile.read()
                        outfile.write(text + '\n\n')

def load_dataset(file_path, tokenizer, block_size=128):

    return TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=block_size
    )

def fine_tune_model(train_dataset, model_name='gpt2', output_dir='./fine_tuned_model', epochs=3):
    
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=epochs,
        per_device_train_batch_size=2,
        save_steps=1000,
        save_total_limit=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator,
    )

    trainer.train()

    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    print(f"Model fine-tuned and saved to {output_dir}")

# Prepare the data for fine-tuning
input_directory = 'cleaned_data'  
output_file = 'prepared_data.txt' 

prepare_data_for_finetuning(input_directory, output_file)

# Load the tokenizer and dataset
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
train_dataset = load_dataset(output_file, tokenizer)

# Fine-tune the model
fine_tune_model(
    train_dataset, 
    model_name = 'gpt2', 
    output_dir = './fine_tuned_model', 
    epochs = 3)
