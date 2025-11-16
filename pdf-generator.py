import sys
import urllib.request
import urllib.error
import os

def report(blocknr, blocksize, size):
    """Callback function for urlretrieve to display download progress."""
    current = blocknr * blocksize
    # Check if download is complete
    if current < size:
        sys.stdout.write("\r{0:.2f}%".format(100.0 * current / size))
        sys.stdout.flush() # Forces the output to update immediately

def downloadFile(url):
    """Downloads the file from the given URL with progress reporting."""
    # os.path.basename extracts the filename from the URL
    fname = os.path.basename(urllib.parse.urlparse(url).path)
    
    # Use urllib.request.urlretrieve in Python 3
    print(f"Downloading file to: **{fname}**")
    print("Download starting...")

    try:
        # urlretrieve returns a tuple (filename, headers)
        urllib.request.urlretrieve(url, fname, report)
        print(f"\n✅ Complete PDF for '{query}' has been downloaded to {fname}")
    except urllib.error.HTTPError as e:
        print(f"\n❌ Error: Could not download the file.")
        print(f"HTTP Error Code: {e.code} - {e.reason}")
        print("Please check if the tutorial name is correct and the PDF exists.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")


tld = "http://www.tutorialspoint.com/"
print("Name of Tutorial? (e.g., 'python' or 'java')")
# Use input() instead of raw_input() in Python 3
query = input().strip().lower() 

# Construct the URL
url = tld + query + '/' + query + '_tutorial.pdf'

# Start the download process
downloadFile(url)
