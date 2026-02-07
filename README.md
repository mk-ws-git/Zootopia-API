Zootopia is a Python project that generates a static HTML website displaying information about animals.
The animal data is fetched dynamically from the API Ninjas Animals API instead of being read from a local JSON file.

Features:
- Fetches animal data from an external API
- Generates a styled HTML website (`animals.html`)
- Handles cases where an animal does not exist
- Keeps API keys secure using environment variables

Installation:
1. Clone the repository:
   ```
   bash
   git clone https://github.com/mk-ws-git/Zootopia-API.git
   cd Zootopia-Codio-API
   
2. Install the required dependencies:
   ```
   pip install -r requirements.txt

3. Set up your API key:
   - Sign up for an API key at [API Ninjas](https://api-ninjas.com/api/animals)
   - Create a `.env` file in the project root and add your API key:
     ```
     API_KEY=your_api_key_here

Usage:
To use the program, run the application:
```
python3 animals_web_generator.py

This will generate an `animals.html` file in the project directory, which you can open in a web browser to view the animal information.
The program will prompt you to enter the name of an animal. If the animal exists in the API, its information will be displayed on the website. If it does not exist, a message will be shown indicating that the animal was not found.

Contributing:
Contributions are welcome! Please fork the repository and create a pull request with your changes.
