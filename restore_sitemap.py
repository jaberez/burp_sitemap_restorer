#! /usr/bin/python
import sys
import xml.etree.ElementTree as ET
import base64
import subprocess
import re

def decode_base64(data):
   # Decodes a string from base64.
    print(data)
    return base64.b64decode(data).decode('utf-8')

def parse_xml(file_path):
   # Parses an XML file and returns a list of <item> elements.
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root.findall('item')

def extract_json_data(request_data):
    # Extracts JSON data from the request body, if present.
    # Searches for data in the format {...}
    match = re.search(r'\{.*\}', request_data, re.DOTALL)
    if match:
        json_data = match.group(0).replace('\r\n', '').replace(' ', '')
        return match.group(0)  # Returns the found JSON
    return None

def build_curl_command(item, new_token):

    # Builds a curl command based on data from the <item> element.
    print("Decoding the request field")
    try:
        request_data = decode_base64(item.find('request').text)
    except:
        print(f"Request could not be decoded")

  # Extracts the method, path, and host
    first_line = request_data.splitlines()[0]
    method = first_line.split()[0]
    path = first_line.split()[1]
    host = item.find('host').text

    # Forms the URL
    site_url = f"http://{host}{path}"


   # Extracts JSON data from the request body, if present
    json_data = extract_json_data(request_data)

    # Extracts headers, excluding Cookie
    headers = {}
    for line in request_data.splitlines()[1:]:
        print(line)
        if line.startswith('Cookie:'):
            continue
        if line.startswith('Content-Length:'):
            continue
        if  "{" in line:
            break
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()

    # Replaces the token in the Authorization header
    if 'Authorization' in headers:
        headers['Authorization'] = f"Bearer {new_token}"


    # Forms the curl command
    curl_command = ['curl', '--proxy http://127.0.0.1:8080','-X', method]
    for key, value in headers.items():
        curl_command.extend(['-H', f'"{key}:{value}"'])

    # If JSON data is present, adds it to the command
#    print(json_data)
    if json_data:
        json_data = f"'{json_data}'"
        curl_command.extend(['-d', json_data])

    curl_command.extend([site_url])
#    print(curl_command)
    return curl_command

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <xml_file_name> <new_token>")
        sys.exit(1)

    file_path = sys.argv[1]
    new_token = sys.argv[2]  # New token from the command line
    items = parse_xml(file_path)
    for item in items:
        url = item.find('url').text
        print(f"Workin on the next url: {url}")
        try:
             curl_command = build_curl_command(item, new_token)
        except:
             print("Error building the  command") 
             continue 
        print("Executing command:", ' '.join(curl_command))
        # Executes the curl command
        try:
            result = subprocess.run(' '.join(curl_command), capture_output=True, text=True,shell=True)
        except:
            print("An error occured. It could be binary file ")
        # Outputs the result of the command execution
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)

if __name__ == "__main__":
     main()
