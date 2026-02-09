# import time
# from PIL import Image, ImageDraw
 
# # Import mattplotlib to plot image outputs
# import matplotlib.pyplot as plt
# %matplotlib inline
# plt.rcParams['image.cmap'] = 'gray'
 
# from transformers import AutoModelForCausalLM, AutoTokenizer

# model = AutoModelForCausalLM.from_pretrained(
#     "moondream/moondream-2b-2025-04-14",
#     revision="2025-06-21",
#     trust_remote_code=True,
#     device_map="auto",
# )
 
# dtype = next(model.parameters()).dtype
# print(dtype)
