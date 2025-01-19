import numpy as np
import matplotlib.pyplot as plt
import time
import tracemalloc
import sys
from typing import List, Tuple

# Extended recursion depth for handling bigger arrays
sys.setrecursionlimit(10**6)

def merge_sort(x: List[int]) -> List[int]:
    """
    Apply divide-and-conquer mergesort on array
    
    Args:
        x: Target integer list for sorting
    Returns:
        Sorted list of integers
    """
    if len(x) <= 1:
        return x

    mid = len(x) // 2
    left = merge_sort(x[:mid])
    right = merge_sort(x[mid:])
    
    return merge_parts(left, right)

def merge_parts(left: List[int], right: List[int]) -> List[int]:
    """
    Combine two sorted arrays into single sorted array
    """
    merged = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def check_metrics(x: List[int]) -> Tuple[float, float]:
    """
    Calculate speed and RAM usage of sorting process
    """
    tracemalloc.start()
    
    t1 = time.time()
    sorted_arr = merge_sort(x)
    duration = time.time() - t1
    
    now, max_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # Copy sorted result back to original array for consistency
    x[:] = sorted_arr
    
    return duration, max_mem / 10**6  # MB conversion

def create_test_data(n_list: List[int]) -> Tuple[dict, dict, dict]:
    """
    Create test cases with different array arrangements
    """
    asc_data = {n: list(range(n)) for n in n_list}
    desc_data = {n: list(range(n, 0, -1)) for n in n_list}
    mix_data = {n: list(np.random.randint(0, n, n)) for n in n_list}
    
    return mix_data, asc_data, desc_data

def run_analysis() -> None:
    """
    Study and plot sorting behavior across different input types
    """
    n_list = [100, 250, 500, 750, 1000]
    
    # Generate test arrays
    mix_data, asc_data, desc_data = create_test_data(n_list)
    
    # Setup data collection
    metrics = {
        case: {'speed': [], 'ram': []} 
        for case in ['Mixed', 'Ascending', 'Descending']
    }
    
    # Get performance data
    for n in n_list:
        test_sets = {
            'Ascending': asc_data[n].copy(),
            'Descending': desc_data[n].copy(),
            'Mixed': mix_data[n].copy()
        }
        
        for case, test_arr in test_sets.items():
            t, mem = check_metrics(test_arr)
            metrics[case]['speed'].append(t)
            metrics[case]['ram'].append(mem)
    
    # Visual representation
    fig, (p1, p2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Speed plot
    for case, data in metrics.items():
        p1.plot(n_list, data['speed'], marker='o', label=case)
    p1.set_xlabel('Array Size')
    p1.set_ylabel('Processing Time (s)')
    p1.set_title('MergeSort Speed Analysis')
    p1.legend()
    p1.grid(True)
    
    # Memory plot
    for case, data in metrics.items():
        p2.plot(n_list, data['ram'], marker='o', label=case)
    p2.set_xlabel('Array Size')
    p2.set_ylabel('RAM Usage (MB)')
    p2.set_title('MergeSort Memory Analysis')
    p2.legend()
    p2.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    print("\nMetrics Overview:")
    print("-" * 50)
    for case, data in metrics.items():
        print(f"\n{case} array:")
        print(f"Speed average: {np.mean(data['speed']):.6f} s")
        print(f"RAM average: {np.mean(data['ram']):.2f} MB")
        print(f"Peak time: {max(data['speed']):.6f} s")
        print(f"Peak RAM: {max(data['ram']):.2f} MB")

if __name__ == "__main__":
    run_analysis()