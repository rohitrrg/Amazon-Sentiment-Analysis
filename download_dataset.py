import kagglehub
import shutil

# Download latest version
path = kagglehub.dataset_download("bittlingmayer/amazonreviews")
print('Dataset Downloaded !!')
# C:\Users\rohit\.cache\kagglehub\datasets\bittlingmayer\amazonreviews\versions\7

print('Moving Dataset to the working directory !!')
shutil.move(path, './dataset')

print(f"Data Done !!")