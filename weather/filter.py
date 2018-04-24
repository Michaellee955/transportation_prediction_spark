def count_zero(line):
    return 2

def filter(lines):
    lines_new = [line for line in lines if count_zero(line)>2]
    return lines_new