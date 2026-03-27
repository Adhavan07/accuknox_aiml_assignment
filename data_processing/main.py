import matplotlib.pyplot as plt

students = [
    {"name": "Alice", "score": 85},
    {"name": "Bob", "score": 72},
    {"name": "Charlie", "score": 90},
    {"name": "David", "score": 60}
]

def calculate_average(data):
    scores = [s["score"] for s in data]
    return sum(scores) / len(scores)

def plot_scores(data, avg):
    names = [s["name"] for s in data]
    scores = [s["score"] for s in data]

    colors = ["blue" if s >= avg else "red" for s in scores]

    plt.bar(names, scores, color=colors)
    plt.axhline(avg, color="gold", linestyle="--", label=f"Avg: {avg:.2f}")
    plt.legend()
    plt.title("Student Scores")
    plt.show()

if __name__ == "__main__":
    avg = calculate_average(students)
    print("Average:", avg)
    plot_scores(students, avg)
