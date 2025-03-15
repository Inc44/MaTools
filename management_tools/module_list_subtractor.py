def subtract_lists(original_list, subtracted_list):
	subtracted_set = set(subtracted_list)
	return [line for line in original_list if line not in subtracted_set]
