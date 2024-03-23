import requests
from bs4 import BeautifulSoup
import os

# URL of the web page containing the images
url = "https://wallpaperaccess.com/3d-4k#google_vignette"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find all image tags
image_tags = soup.find_all('img')

# Directory to save the images
output_dir = "downloaded_images"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Download each image
for img_tag in image_tags:
    # Get the URL of the image
    img_url = img_tag['src']

    # Get the filename of the image
    img_filename = img_url.split('/')[-1]

    # Combine the output directory and filename
    img_path = os.path.join(output_dir, img_filename)

    # Send a GET request to the image URL
    img_response = requests.get(img_url)

    # Save the image to a file
    with open(img_path, 'wb') as img_file:
        img_file.write(img_response.content)
        print(f"Downloaded: {img_path}")

print("All images downloaded successfully.")
