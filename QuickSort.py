import numpy as np
import matplotlib.pyplot as plt
import time
import tracemalloc
import sys
from typing import List, Tuple

# Extended recursion depth for handling bigger arrays
sys.setrecursionlimit(10**6)

def quick_sort(x: List[int], start: int, end: int) -> None:
    """
    Apply divide-and-conquer sorting method on array
    
    Args:
        x: Target integer list for sorting
        start: First position of section
        end: Last position of section
    """
    def split_array(start: int, end: int) -> int:
        ref = x[end]
        pos = start - 1
        
        for curr in range(start, end):
            if x[curr] <= ref:
                pos += 1
                x[pos], x[curr] = x[curr], x[pos]
        
        x[pos + 1], x[end] = x[end], x[pos + 1]
        return pos + 1

    if start < end:
        mid = split_array(start, end)
        quick_sort(x, start, mid - 1)
        quick_sort(x, mid + 1, end)

def check_metrics(x: List[int]) -> Tuple[float, float]:
    """
    Calculate speed and RAM usage of sorting process
    """
    tracemalloc.start()
    
    t1 = time.time()
    quick_sort(x, 0, len(x)-1)
    duration = time.time() - t1
    
    now, max_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
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
    p1.set_title('Speed Analysis')
    p1.legend()
    p1.grid(True)
    
    # Memory plot
    for case, data in metrics.items():
        p2.plot(n_list, data['ram'], marker='o', label=case)
    p2.set_xlabel('Array Size')
    p2.set_ylabel('RAM Usage (MB)')
    p2.set_title('Memory Analysis')
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