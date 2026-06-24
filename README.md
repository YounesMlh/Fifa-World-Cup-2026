# 🏆 2026 World Cup Group Stage Simulator & Standings Analyzer

## 📝 Project Overview
This project is an automated data analysis tool and standings simulator for the 2026 World Cup group stage matches using **Python** and **Pandas**. 

The script dynamically processes raw match text data, filters completed fixtures (those with recorded scores), and automatically calculates tournament metrics for each team:
- **Points ($PTS$):** 3 for a win, 1 for a draw, and 0 for a loss.
- **Goals For ($GF$) & Goals Against ($GA$)**
- **Goal Difference ($GD$):** Dynamically calculated as $GF - GA$.

Finally, it groups all nations into their respective 12 tournament groups and ranks them in strict accordance with official FIFA tie-breaking rules ($PTS \rightarrow GD \rightarrow GF \rightarrow GA$).

---

## 🛠️ Tech Stack
- **Python 3.x**
- **Pandas:** For data manipulation, metric calculation, and group aggregation.
- **Jupyter Notebook (.ipynb):** As the interactive development and execution environment.

---

## 🚀 How to Use & Extract Analytics
Once you run the main Notebook file, the complete tournament standings database is retained in memory under the `standings` DataFrame variable. You can open a new code cell at the bottom to perform custom queries, such as:

### Extract specific team statistics (e.g., Algeria 🇩🇿):
```python
algeria_stats = standings[standings['Team'] == 'Algeria']
print(algeria_stats)

Filter and compare specific regional teams (e.g., Arab Nations):

Python
arab_teams = ['Algeria', 'Morocco', 'Saudi Arabia', 'Egypt', 'Tunisia', 'Qatar', 'Jordan', 'Iraq']
arab_standings = standings[standings['Team'].isin(arab_teams)].sort_values(by='PTS', ascending=False)
print(arab_standings)

Find the top scoring attack in the tournament:
Python
top_attack = standings.nlargest(1, 'GF')
print(top_attack[['Team', 'GF']])

📊 Sample Output Structure
When running the script, the 12 groups are generated dynamically and displayed as follow:

Plaintext
===== Group A =====
            Team  PTS  GD  GF  GA
0         Mexico    6   2   3   1
1 Korea Republic    3   0   3   3
2        Czechia    1  -1   2   3
3   South Africa    1  -1   1   2
