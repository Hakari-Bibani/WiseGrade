import re

def preprocess_student_code(code_str):
    """
    1. Remove (or un-indent) the if __name__ == "__main__": block, so that code always runs.
    2. Insert lines that create map_object or df_object if we detect a line
       like `earthquake_map = create_map(...)` or `df = process_data(...)`.
    """
    lines = code_str.split('\n')
    new_lines = []
    skip_block = False
    indent_level_of_main = None

    # --- PART A: Remove or "de-guard" the if __name__ == "__main__": block ---
    for i, line in enumerate(lines):
        # Detect if line has: if __name__ == '__main__':
        if re.search(r'if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:', line):
            skip_block = True
            indent_level_of_main = len(line) - len(line.lstrip())
            # We skip adding this line to new_lines
            continue

        if skip_block:
            # We are inside the if __main__ block
            current_indent = len(line) - len(line.lstrip())
            if current_indent > indent_level_of_main:
                # "Un-indent" or remove the extra indentation
                unindented_line = line.lstrip()
                new_lines.append(unindented_line)
                continue
            else:
                # Found a line that is no longer indented => block ended
                skip_block = False

        if not skip_block:
            new_lines.append(line)

    code_without_main = "\n".join(new_lines)

    # --- PART B: Insert top-level references to help detection of map & df ---
    final_lines = []
    for line in code_without_main.split('\n'):
        final_lines.append(line)

        # If we see something like `earthquake_map = create_map(...)` or `my_map = folium.Map(...)`
        map_assign_match = re.match(
            r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*folium\.Map.*|.*create_map.*)',
            line
        )
        if map_assign_match:
            var_name = map_assign_match.group(1).strip()
            final_lines.append(f"map_object = {var_name}")

        # If we see something like `df = process_data(...)` or `df = pd.DataFrame(...)`
        df_assign_match = re.match(
            r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*pd\.DataFrame.*|.*process_data.*|.*read_csv.*)',
            line
        )
        if df_assign_match:
            var_name = df_assign_match.group(1).strip()
            final_lines.append(f"df_object = {var_name}")

    return "\n".join(final_lines)
