def compare_three(pos1, pos2, pos3):
    val1 = query(pos1)
    val2 = query(pos2)
    val3 = query(pos3)
    
    if val1 == val2 and val1 == val3:
        return pos1
    if val1 > val2 and val1 > val3:
        return pos1
    elif val2 > val1 and val2 > val3:
        return pos2
    else:
        return pos3

def query(x):
    return -1 * (x - 7)**2 + 49  

def locate_peak(limit):
    position = 0
    previous = position - 1
    forward = position + 1

    # prints it in a table format for better understanding, dry run is done seperately on a page in the other file
    optimal = compare_three(position, forward, previous)
    print(f"{'Step':<6} {'Prev':<6} {'Curr':<6} {'Next':<6}")
    step = 1
    while optimal > position and position <= limit:
        print(f"{step:<6} {previous:<6} {position:<6} {forward:<6}")
        position = optimal
        forward = position + 1
        previous = position - 1
        optimal = compare_three(position, forward, previous)
        step += 1


    peak_height = query(position)
    print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(f"    HIGHEST POINT INDEX IS: {position}")
    print(f"    ELEVATION OF IT IS: {peak_height}")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    
locate_peak(100)
