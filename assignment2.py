import re

def preprocess_student_code(code_str):
    """
    1. Remove or comment out lines that contain `if __name__ == "__main__":`.
    2. Un-indent the code within that block so it always runs (naive approach).
    3. Insert 'map_object = <var>' or 'df_object = <var>' lines right after
       we see typical assignments for a folium map or a DataFrame.
    """

    # Split into lines
    lines = code_str.split('\n')
    new_lines = []
    skip_block = False
    indent_level_of_main = None

    for i, line in enumerate(lines):
        # Detect if line has "if __name__"
        if re.search(r'if\s+__name__\s*==\s*["\']__main__["\']:', line):
            # We'll skip this line
            # Mark that we should skip subsequent indented lines
            skip_block = True
            # Try to measure indentation:
            indent_level_of_main = len(line) - len(line.lstrip())
            # We could also comment this line out if we like
            continue

        if skip_block:
            # If the current line is more indented than the block's start, skip or un-indent it.
            current_indent = len(line) - len(line.lstrip())
            if current_indent > indent_level_of_main:
                # We "un-indent" by removing some spaces:
                # naive approach: cut down current_indent to indent_level_of_main
                line_stripped = line.lstrip()
                new_lines.append(line_stripped)
                continue
            else:
                # if we hit a line that is no longer indented, we are out of the block
                skip_block = False
        
        # If not skipping the line, add it
        new_lines.append(line)

    # Now we have code with the __main__ block removed or un-indented so it runs.
    code_without_main = "\n".join(new_lines)

    # Next, we insert lines that create `map_object` or `df_object`.
    final_lines = []
    for line in code_without_main.split('\n'):
        final_lines.append(line)

        # Check for typical Folium map assignment
        # e.g. earthquake_map = create_map(...)
        # or some_map = folium.Map(
        map_assign_match = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*folium\.Map.*|.*create_map.*)', line)
        if map_assign_match:
            var_name = map_assign_match.group(1)
            # Add a new line after: map_object = <var_name>
            final_lines.append(f"map_object = {var_name}")

        # Check for typical DataFrame assignment
        # e.g. df = process_data(...) or df = pd.DataFrame(...)
        df_assign_match = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*pd\.DataFrame.*|.*process_data.*|.*read_csv.*)', line)
        if df_assign_match:
            var_name = df_assign_match.group(1)
            final_lines.append(f"df_object = {var_name}")

        # Alternatively, you can do a simpler check for lines that start with 'df' or 'df_' etc.

    final_code = "\n".join(final_lines)
    return final_code
