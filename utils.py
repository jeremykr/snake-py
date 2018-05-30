import os.path

def subtract_tuples(t1, t2):
    x = t1[0] - t2[0]
    y = t1[1] - t2[1]
    return (x, y)
	
def add_tuples(t1, t2):
    x = t1[0] + t2[0]
    y = t1[1] + t2[1]
    return (x, y)
	
# Compare current score to high score. If current score is greater, save it.
# Return high score.
def process_score(current_score):
    high_score = 0
    filename = "./snake_scores.txt"

    if not os.path.exists(filename):
        with open("./snake_scores.txt", "w+") as f:
            f.write("0")

    with open("./snake_scores.txt", "r+") as f:
        try:
            high_score = int([line for line in f][0])
        except:
            print("Could not read high score.")
            pass
	
    if current_score > high_score:
        with open("./snake_scores.txt", "w+") as f:
            f.write(str(current_score))
            high_score = current_score

    return high_score