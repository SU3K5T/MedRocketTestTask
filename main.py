from datetime import datetime
import requests
from pathlib import Path

TODOS_URL = 'https://json.medrocket.ru/todos'
USERS_URL = 'https://json.medrocket.ru/users'

# Выводит список задач (выполненных и нет) в формате сиписка с -
def tasks_formatter(tasks):
  return "\n".join(list(map(lambda task: f"- {task["title"]}", tasks)))

# Проверяет, существует ли файл
def is_file_exists(filename):
    return Path(filename).exists()


def create_or_rename_file(username, lines):
  filename = "tasks/" + username + ".txt"

  if not is_file_exists(f"{filename}"):
      with open(f"{filename}", "w") as file:
        file.writelines(lines)
      print("inix")
  else:
    with open(f"{filename}", "r", encoding="utf-8") as file:
      inside_lines = file.readlines()
      if len(inside_lines) >= 2:
          second_line = inside_lines[1].strip()  
          date_str = second_line[-16:]
          parsed_date = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
          formatted_date = parsed_date.strftime("%Y-%m-%dT%H:%M")
          print("inside")
          Path(f"{filename}").rename(f"tasks/old_{username}_{formatted_date}.txt")
    create_or_rename_file(username, lines)


def main():
  todos_response = requests.get(TODOS_URL)
  users_response = requests.get(USERS_URL)

  todos_data = todos_response.json()
  users_data = users_response.json()

  print(todos_data[0]['userId'])

  Path("tasks").mkdir(exist_ok=True)

  for i in range(0, len(users_data)):

    completed_tasks = list(filter(lambda todo: todo.get("userId", '') == users_data[i]["id"] and todo["completed"] == True, todos_data))
    comleted_tasks_count = len(completed_tasks)

    uncompleted_tasks = list(filter(lambda todo: todo.get("userId", '') == users_data[i]["id"] and todo["completed"] == False, todos_data))
    uncomleted_tasks_count = len(uncompleted_tasks)

    tasks_count = comleted_tasks_count + uncomleted_tasks_count

    timesptamp_str = datetime.now().strftime("%d.%m.%Y %H:%M")

    lines = [
      f"Отчет для {users_data[i]["company"]["name"]}\n",
      f"{users_data[i]["name"]} <{users_data[i]["email"]}> {timesptamp_str}\n",
      f"Всего задач {tasks_count}\n",
      f"\n",
      f"## Актуальные задачи: {uncomleted_tasks_count}\n",
      f"{tasks_formatter(uncompleted_tasks)}\n",
      f"## Завершённые задачи: {comleted_tasks_count}\n",
      f"{tasks_formatter(completed_tasks)}\n"
    ]

    username = users_data[i]["username"]
    create_or_rename_file(username, lines)
    

if __name__ == "__main__":
  main()