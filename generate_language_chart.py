import requests
import matplotlib.pyplot as plt
from collections import defaultdict
import time
import os

SECRET_TOKEN = os.getenv('SECRET_TOKEN')

if not SECRET_TOKEN:
    raise ValueError("No GitHub token provided. Please set the SECRET_TOKEN environment variable.")


def fetch_all_repos(owner):
    repos = []
    page = 1
    while True:
        url = f'https://api.github.com/users/{owner}/repos'
        params = {'page': page, 'per_page': 100} 
        headers = {'Authorization': f'token {SECRET_TOKEN}'}
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    print(f"len(repos): {len(repos)}")
    return repos

def fetch_language_data(owner, repo_name):
    url = f'https://api.github.com/repos/{owner}/{repo_name}/languages'
    headers = {'Authorization': f'token {SECRET_TOKEN}'}
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 403:
            print("Rate limit exceeded. Waiting to retry...")
            time.sleep(60)  
            continue
        response.raise_for_status()
        return response.json()

def aggregate_language_data(owner):
    repos = fetch_all_repos(owner)
    aggregate_data = defaultdict(int)

    for repo in repos:
        repo_name = repo['name']
        print(f"Fetching data for {repo_name}")
        languages = fetch_language_data(owner, repo_name)
        for language, bytes_of_code in languages.items():
            aggregate_data[language] += bytes_of_code

    return aggregate_data

def calculate_percentages(data):
    total_bytes = sum(data.values())
    if total_bytes == 0:
        return {lang: 0 for lang in data}  
    percentages = {lang: (bytes_of_code / total_bytes) * 100 for lang, bytes_of_code in data.items()}
    return percentages

def create_stacked_bar_chart(data, owner):
    languages = list(data.keys())
    percentages = list(data.values())
    colors = plt.cm.tab20(range(len(languages))) 

    fig, ax = plt.subplots(figsize=(10, 4)) 

    left = 0
    for i, (lang, pct) in enumerate(zip(languages, percentages)):
        ax.barh(0, pct, left=left, color=colors[i], edgecolor='white', label=f'{lang} ({pct:.2f}%)')
        left += pct

    ax.set_xlabel('Percentage of Code')
    ax.set_title(f'Languages used in {owner}\'s GitHub Repositories')
    ax.set_yticks([]) 

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3)

    plt.tight_layout()
    plt.savefig('language_chart.png', bbox_inches='tight')

if __name__ == '__main__':
    owner = 'KushRohra' 
    aggregate_data = aggregate_language_data(owner)
    percentage_data = calculate_percentages(aggregate_data)
    create_stacked_bar_chart(percentage_data, owner)
