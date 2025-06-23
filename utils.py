from pathlib import Path
import os
media_folder = "UserFiles"

def parse_file(filename: str, out_filename=None):
    if not out_filename:
        path = Path(filename)
        out_filename = str(path.parent / (path.stem + "_parsed.wl"))
    with open(filename, "r") as file:
        file_lines = file.readlines()

    with open(out_filename, "w") as file:
        skip_mode = False 
        prev_line_empty = False  
        
        for line in file_lines:
            if line.startswith("(* ::Text:: *)"):
                skip_mode = True
                continue

            if skip_mode and line == "\n":
                if prev_line_empty:
                    skip_mode = False 
                    prev_line_empty = False
                    continue
                prev_line_empty = True
                continue

            if not skip_mode and line not in ("(* ::Input:: *)\n", "(* ::Package:: *)\n"):
                if line.startswith("(*") and line.endswith("*)\n"):
                    file.write(line[2:-3] + "\n")
                else:
                    file.write(line)

            prev_line_empty = (line == "\n")

    return out_filename


def hash_user_id(user_id: int | str):
    return str(user_id)