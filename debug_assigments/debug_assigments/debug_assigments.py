# The student's name
student_name = "Alex"

# List of scores from 5 assignments
scores = [85, 62, 78, 91, 70]

# --- BUG 1: Indexing Error ---
# Find the highest score
highest_score = max(scores)

# --- BUG 2: Type Error (Incorrect Function Call) ---
# Calculate the total score
total_score = sum(scores) 

# --- BUG 3: Integer Division/Missing Float Conversion ---
# Calculate the average score (should be float)
num_assignments = len(scores)
average_score = total_score / num_assignments

# --- BUG 4: Logic Error (Incorrect List Modification) ---
# The student was granted 5 bonus points on the lowest score.
# Attempt to find the lowest score, add 5, and replace it in the original list.
lowest_score = min(scores)
lowest_index = scores.index(lowest_score)
scores[lowest_index] += 5

# Check if the student passed
PASS_THRESHOLD = 70
if average_score >= PASS_THRESHOLD:
    status = "Passed"
else:
    status = "Failed"

# Print the final results
print(f"Student: {student_name}")
print(f"Final Scores: {scores}")
print(f"Highest Score: {highest_score}")
print(f"Average Score: {average_score}")
print(f"Status: {status}")