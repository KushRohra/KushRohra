import requests
import matplotlib.pyplot as plt

def fetch_language_data(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/languages'
    response = requests.get(url)
    return response.json()

def create_bar_chart(data, owner, repo):
    languages = list(data.keys())
    bytes_of_code = list(data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(languages, bytes_of_code, color='skyblue')
    plt.xlabel('Programming Languages')
    plt.ylabel('Bytes of Code')
    plt.title(f'Languages used in {owner}/{repo} GitHub Repository')
    plt.savefig('language_chart.png')

if __name__ == '__main__':
    owner = 'your-username'  # Replace with your GitHub username
    repo = 'your-repo'       # Replace with your GitHub repository name
    data = fetch_language_data(owner, repo)
    create_bar_chart(data, owner, repo)
