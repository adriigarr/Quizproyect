from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the model and tokenizer
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name, padding_side='left')  # Ensure padding is on the left
model = GPT2LMHeadModel.from_pretrained(model_name)

# Ensure padding token is set, using EOS token if none is set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


def chat_with_gpt2(input_text):
    # Define the specific prompt structure to guide GPT-2
    prompt = f"Create a concise multiple-choice question about {input_text}. Format the question followed by three choices labeled A, B, C, and indicate the correct answer explicitly."

    # Encode the input text with padding enabled
    encoded_input = tokenizer.encode_plus(
        prompt,
        return_tensors='pt',
        padding='max_length',
        max_length=100,
        truncation=True,
        add_special_tokens=True
    )

    # Generate a response from the model
    output = model.generate(
        encoded_input['input_ids'],
        attention_mask=encoded_input['attention_mask'],
        max_length=150,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.7,
        do_sample=True  # Enable sampling to make use of the temperature setting
    )

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text


def main():
    print("GPT-2 Quiz Creator (type 'exit' to quit)")
    while True:
        user_input = input("Enter the topic for a quiz question: ")
        if user_input.lower() == 'exit':
            break
        response = chat_with_gpt2(user_input)
        print("GPT-2 Generated Quiz:", response)


if __name__ == '__main__':
    main()
