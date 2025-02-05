import requests
from pathlib import Path

def download_example_data():
    """Download example data files from Zenodo for documentation examples."""
    zenodo_base_url = "https://zenodo.org/record/14812519/files/"
    example_data_dir = Path(__file__).parent.parent.parent / "docs" / "examples" / "example_data"
    example_data_dir.mkdir(parents=True, exist_ok=True)
    
    # List of example data files to download
    files = [
        "sample_glider_data.csv",
        "sample_glider_data.nc",
        "sample_tabs_data.csv"
    ]
    
    for filename in files:
        file_path = example_data_dir / filename
        if not file_path.exists():
            print(f"Downloading {filename}...")
            url = zenodo_base_url + filename
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded {filename}")

if __name__ == "__main__":
    download_example_data()
