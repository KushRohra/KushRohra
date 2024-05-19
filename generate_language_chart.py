import requests
import matplotlib.pyplot as plt

def fetch_all_repos(owner):
    repos = []
    page = 1
    while True:
        url = f'https://api.github.com/users/{owner}/repos'
        params = {'page': page, 'per_page': 100} 
        response = requests.get(url, params=params)
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
    response = requests.get(url)
    response.raise_for_status()
    print(f"repo_name: {repo_name}")   
    return response.json()

def aggregate_language_data(owner):
    repos = fetch_all_repos(owner)
    aggregate_data = {}

    for repo in repos:
        repo_name = repo['name']
        # if repo['name'] != 'Covid-19_Tracker':
        #     continue
        languages = fetch_language_data(owner, repo_name)
        for language, bytes_of_code in languages.items():
            aggregate_data[language] = aggregate_data.get(language, 0) + bytes_of_code

    return aggregate_data


def calculate_percentages(data):
    total_bytes = sum(data.values())
    percentages = {lang: (bytes_of_code / total_bytes) * 100 for lang, bytes_of_code in data.items()}
    return percentages

def create_stacked_bar_chart(data, owner):
    languages = list(data.keys())
    percentages = list(data.values())
    colors = plt.cm.tab20(range(len(languages)))  # Use a colormap for distinct colors

    fig, ax = plt.subplots(figsize=(10, 4))  # Adjust height for better visibility

    left = 0
    for i, (lang, pct) in enumerate(zip(languages, percentages)):
        ax.barh(0, pct, left=left, color=colors[i], edgecolor='white', label=f'{lang} ({pct:.2f}%)')
        left += pct

    ax.set_xlabel('Percentage of Code')
    ax.set_title(f'Languages used in {owner}\'s GitHub Repositories')
    ax.set_yticks([])  # Hide y-axis

    # Place legend below the chart
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3)  # Adjust ncol for more columns

    plt.tight_layout()
    plt.savefig('language_chart.png', bbox_inches='tight')

if __name__ == '__main__':
    owner = 'KushRohra'  # Replace with your GitHub username
    data = aggregate_language_data(owner)
    create_stacked_bar_chart(data, owner)
