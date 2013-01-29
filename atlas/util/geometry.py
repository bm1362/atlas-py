# takes tuple 2d vectors and returns if the target vector is in the rectangle created by the other vectors.
def is_in_rectangle(top_left, top_right, bottom_left, bottom_right, target):
	return top_left[0] <= target[0] and top_right[0] >= target[0] and top_left[1] <= target[1] and bottom_left[1] >= target[1]