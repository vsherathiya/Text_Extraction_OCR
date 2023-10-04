# from transformers import TrOCRProcessor, VisionEncoderDecoderModel
# from PIL import Image
# import requests

# # # load image from the IAM database (actually this model is meant to be used on printed text)
# # image_path = r"D:\DataForTraining\output_folder\16.jpg"
# # image = Image.open(image_path).convert("RGB")

# # processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-printed')
# # model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-printed')
# # pixel_values = processor(images=image, return_tensors="pt").pixel_values

# # generated_ids = model.generate(pixel_values)
# # generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
# # print(generated_text)


# # import transformers

# # # Load the TrOCR model
# # model = transformers.AutoModelForSeq2SeqLM.from_pretrained("microsoft/trocr-base")

# # # Preprocess the input image
# # image = transformers.Image.from_array(image)

# # # Generate the text
# # generated_text = model.generate(image=image)

# # # Print the generated text
# # print(generated_text)


# # import transformers

# # # Load the TrOCR model
# # model = transformers.AutoModelForSeq2SeqLM.from_pretrained("microsoft/trocr-small")
# # image_path = r"D:\DataForTraining\output_folder\16.jpg"
# # image = Image.open(image_path).convert("RGB")
# # # Preprocess the input image
# # image = transformers.Image.from_array(image)

# # # Generate the text
# # generated_text = model.generate(image=image)

# # # Print the generated text
# # print(generated_text)


# from transformers import list_models

# # List available models
# models = list_models()
# for model_name in models:
#     print(model_name)



import torch
from transformers import AutoTokenizer, AutoModel
from PIL import Image

# Load the TrOCR tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("microsoft/trocr-base-handwritten")
model = AutoModel.from_pretrained("microsoft/trocr-base-handwritten")

# Load the image from the IAM dataset
image_path = r"D:\DataForTraining\output_folder\16.jpg"
image = Image.open(image_path).convert("RGB")

# Preprocess the image using the tokenizer
inputs = tokenizer(image, return_tensors="pt", padding="max_length", truncation=True, max_length=1024)
pixel_values = inputs["pixel_values"]  # Extract pixel values from the processed inputs

# Perform OCR to extract text
with torch.no_grad():
    outputs = model(pixel_values)  # Pass the pixel values to the model

# Get the generated text
generated_text = tokenizer.batch_decode(outputs.logits.argmax(2), skip_special_tokens=True)[0]

# Display the extracted text
print(generated_text)
