def custom_max(lst):
    max_value = lst[0]
    
    for item in lst[1:]:
        if item > max_value:
            max_value = item
            
    return max_value

# Example usage:
my_list = [10, 15, 0, 10000, 20 , 50 , 20]
maximum = custom_max(my_list)
print(f"The maximum value is: {maximum}")
