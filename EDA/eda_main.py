# Imports
import jsonlines

# Global Constants or Configuration
DEBUG_MODE = False


def count_lines(file_path: str) -> int:
    with open(file_path, 'r') as f:
        num_lines = sum(1 for line in f)
    return num_lines


def read_jsonl(file_path: str, num_lines: int = 0):
    
    max_lines = count_lines(file_path)

    num_lines = 0 if num_lines <= 0 else max_lines if num_lines > max_lines else num_lines

    with jsonlines.open(file_path, 'r') as reader:
        for line_num, obj in enumerate(reader):
            print(f"\n\n Line number: {line_num}\n\n {obj.keys()}")
            if line_num == num_lines:
                break
    return

# Main Function or Entry Point
def main():
    print("Starting the program...")

    if DEBUG_MODE:
        print("Debug mode is enabled.")

    
    read_jsonl(file_path=".\discrim-eval\explicit.jsonl", num_lines=3)



# Conditional Execution
if __name__ == "__main__":
    
    main()