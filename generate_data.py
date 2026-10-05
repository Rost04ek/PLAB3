import csv
import random
from pathlib import Path

def generate_tasks_csv(path: Path, count: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    
    priorities = ["Low", "Medium", "High", "Critical"]
    statuses = ["Open", "In Progress", "Review", "Done"]
    
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        # Хедер згідно з варіантом 14
        writer.writerow(["task_id", "title", "description", "priority", "status"])
        
        for i in range(1, count + 1):
            # Штучно створюємо 1% битих/некоректних записів для перевірки валідатора
            if random.random() < 0.01:
                writer.writerow([i, "", "Missing title error", "Unknown", "Open"])
                continue
                
            priority = random.choice(priorities)
            status = random.choice(statuses)
            
            writer.writerow([
                i,
                f"Task {i}",
                f"Detailed description for task number {i}",
                priority,
                status
            ])
            
    print(f"File created: {path} ({count} records)")

if __name__ == "__main__":
    # Генеруємо три набори даних для майбутнього бенчмаркінгу
    generate_tasks_csv(Path("data/tasks_10k.csv"), 10_000)
    generate_tasks_csv(Path("data/tasks_100k.csv"), 100_000)
    generate_tasks_csv(Path("data/tasks_500k.csv"), 500_000)