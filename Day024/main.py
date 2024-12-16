import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Create output directory if it doesn't exist
output_dir =  os.path.join(CURRENT_DIR, "Output")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read the letter template
template_path = os.path.join(CURRENT_DIR, "letters", "starting_letter.txt")
with open(template_path, "r") as template_file:
    letter_template = template_file.read()

# Read the names
names_path = os.path.join(CURRENT_DIR, "names", "invited_names.txt")
with open(names_path, "r") as names_file:
    names = names_file.readlines()

# Create personalized letters
for name in names:
    name = name.strip()  # Remove any whitespace/newlines
    personalized_letter = letter_template.replace("[Recipient Name]", name)
    
    # Save the personalized letter
    output_path = os.path.join(output_dir, f"letter_for_{name}.txt")
    with open(output_path, "w") as output_file:
        output_file.write(personalized_letter)
