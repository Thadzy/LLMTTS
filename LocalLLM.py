from transformers import AutoModelForCausalLM, AutoTokenizer

# Path to the directory containing the model files
model_directory = "D:\LLM\llama-3-typhoon-v1.5-8b-instruct.Q4_K_M.gguf"

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_directory)
model = AutoModelForCausalLM.from_pretrained(model_directory)

# Tokenize input
inputs = tokenizer("Hello, how are you?", return_tensors="pt")

# Generate output
outputs = model.generate(**inputs)

# Decode and print output
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
