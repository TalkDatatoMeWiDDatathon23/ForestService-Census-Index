import pandas as pd
import geopandas as gpd
import pyarrow
import sys
import requests
import os
import zipfile


def download_census():

	print('Downloading Census zip file from data.gov')
	zip_url = "https://www2.census.gov/geo/tiger/TIGER2019/COUNTY/tl_2019_us_county.zip"
	local_zip_file = "tl_2019_us_county.zip"

	if not os.path.exists(local_zip_file):
		print(f"Downloading {zip_url}...")
		response = requests.get(zip_url)
	
		if response.status_code == 200:
			with open(local_zip_file, 'wb') as zip_file:
				zip_file.write(response.content)
			print(f"Downloaded {local_zip_file} successfully.")
		else:
			print(f"Failed to download {zip_url}. Status code: {response.status_code}")
	else:
		print(f"{local_zip_file} already exists. Skipping download.")


	# Path to the downloaded ZIP file
	zip_file_path = "tl_2019_us_county.zip"

	# Directory where you want to extract the contents
	extracted_dir = "tl_2019_us_county"

	# Check if the extracted directory already exists; if not, unzip the file
	if not os.path.exists(extracted_dir):
		print(f"Extracting {zip_file_path} to {extracted_dir}...")
		with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
			zip_ref.extractall(extracted_dir)
		print(f"Extracted {zip_file_path} successfully to {extracted_dir}.")
	else:
		print(f"{extracted_dir} already exists. Skipping extraction.")



def open_shapefile_state():
	download_census()
	
	print('Opening census shapefile dataset')

	gdf = gpd.read_file('tl_2019_us_county/tl_2019_us_county.shp') #file is too large to commit; download from https://catalog.data.gov/dataset/tiger-line-shapefile-2019-nation-u-s-current-county-and-equivalent-national-shapefile
	print('Shapefile ready')

	#reading FIPS info from https://gist.github.com/dantonnoriega/bf1acd2290e15b91e6710b6fd3be0a53#file-us-state-ansi-fips-csv
	print('Opening state information dataset')
	stateFP = pd.read_csv('data/us-state-ansi-fips.csv')
	stateFP['ST'] = stateFP['ST'].str.replace(' ', '')


	print('State information ready!')

	#keep FP and ST only
	
	stateFP = stateFP.drop(['STATE_NAME'], axis=1)
	
	#reformat FP numbers
	
	stateFP.FP = [str(num).zfill(2) for num in stateFP.FP]
	
	
	
	return gdf,stateFP
	

def filter_state(state):
	'''
	Input = state as a string, 
	abbreviation of a US state input to run the function
	'''
	gdf,stateFP = open_shapefile_state()
	fp_state = stateFP[stateFP['ST'] == state]
	
	gdf_state = gdf[gdf['STATEFP'] == str(fp_state.iloc[0,0])]
	
	return gdf_state
	

def main():
	if len(sys.argv) == 2:
		state_abbreviation = sys.argv[1].upper()  # Convert to uppercase for consistency

		# List of valid state abbreviations
		valid_state_abbreviations = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
									 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
									 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
									 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
									 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

		if state_abbreviation in valid_state_abbreviations:
			
			print(f'Processing census shapefile for {state_abbreviation} state.')

			print('Preparing files to process')


			print('Filtering about to beginning')

			state = state_abbreviation

			gdf_sub = filter_state(state)

			print(f'The census data for {state_abbreviation} is ready to be saved.')

			filename_shapefile = f'census_{state_abbreviation}.shp'
			gdf_sub.to_file(f'data/{filename_shapefile}', index=False)
			
			print(f'Census data Shapefile for {state_abbreviation} saved!')
			print('You can now check the data/ folder and proceed to the next steps of the analysis. Enjoy!')
			
			

		else:
			print(f'{state_abbreviation} is not a valid state abbreviation.')

	else:
		print('Please provide a single state abbreviation as the argument. Example: python state_filtering.py NY')



if __name__ == "__main__":
	main()

