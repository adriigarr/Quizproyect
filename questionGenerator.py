from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

# Load the model and tokenizer
model_name = 'gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(model_name, padding_side='left')
model = GPT2LMHeadModel.from_pretrained(model_name)

# Set padding token if undefined
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

def generate_question_and_answers(topic):
    # More directive prompt
    prompt = f"Generate a clear multiple-choice question on {topic} with one correct answer and three incorrect answers. Clearly state which one is correct."
    # Encode the prompt
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
        max_length=encoded_input['input_ids'].shape[-1] + 100,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        pad_token_id=tokenizer.eos_token_id,
        temperature=0.7  # Lower temperature to reduce randomness
    )

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text[len(prompt):]


def main():
    while True:
        topic = input("Enter a topic (type 'exit' to quit): ")
        if topic.lower() == 'exit':
            break
        question_and_answers = generate_question_and_answers(topic)
        print("Generated Question and Answers:", question_and_answers)


if __name__ == '__main__':
    main()
