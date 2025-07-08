import tkinter as tk
from tkinter import ttk, messagebox

class MemoryManagementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Management Simulator")
        self.root.geometry("1000x850")  

        self.setup_tabs()

    def setup_tabs(self):
        tab_control = ttk.Notebook(self.root)

        self.contig_tab = ttk.Frame(tab_control)
        tab_control.add(self.contig_tab, text="Contiguous Allocation")
        self.setup_contiguous_tab()

        self.paging_tab = ttk.Frame(tab_control)
        tab_control.add(self.paging_tab, text="Paging")
        self.setup_paging_tab()

        tab_control.pack(expand=1, fill="both")

    def setup_contiguous_tab(self):
        input_frame = ttk.LabelFrame(self.contig_tab, text="Memory Setup", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(input_frame, text="Partition Sizes (KB, comma-separated):").grid(row=0, column=0, sticky='w')
        self.part_entry = ttk.Entry(input_frame)
        self.part_entry.grid(row=0, column=1, sticky='ew')
        self.part_entry.insert(0, "100,500,200,300,600")

        process_frame = ttk.Frame(input_frame)
        process_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)

        ttk.Label(process_frame, text="Process Sizes (KB):").grid(row=0, column=0, sticky='w')
        self.proc_size_entry = ttk.Entry(process_frame)
        self.proc_size_entry.grid(row=0, column=1, sticky='ew', padx=5)
        self.proc_size_entry.insert(0, "212,417,112,426")

        ttk.Label(process_frame, text="Arrival Times:").grid(row=0, column=2, sticky='w', padx=5)
        self.arrival_entry = ttk.Entry(process_frame)
        self.arrival_entry.grid(row=0, column=3, sticky='ew', padx=5)
        self.arrival_entry.insert(0, "0,1,2,3")

        ttk.Label(process_frame, text="Burst Times:").grid(row=0, column=4, sticky='w', padx=5)
        self.burst_entry = ttk.Entry(process_frame)
        self.burst_entry.grid(row=0, column=5, sticky='ew', padx=5)
        self.burst_entry.insert(0, "5,3,6,4")

        ttk.Label(input_frame, text="Allocation Algorithm:").grid(row=2, column=0, sticky='w')
        self.alloc_method = ttk.Combobox(input_frame, values=["First-Fit", "Best-Fit", "Worst-Fit"])
        self.alloc_method.grid(row=2, column=1, sticky='w')
        self.alloc_method.current(0)

        ttk.Button(input_frame, text="Run Allocation", command=self.run_contiguous).grid(row=3, columnspan=2, pady=5)

        self.contig_canvas = tk.Canvas(self.contig_tab, bg="white", height=300)
        self.contig_canvas.pack(fill='both', expand=True, padx=10, pady=5)

        self.contig_results = tk.Text(self.contig_tab, height=10, wrap=tk.WORD)
        self.contig_results.pack(fill='x', padx=10, pady=5)

    def run_contiguous(self):
        try:
            partitions = [int(x.strip()) for x in self.part_entry.get().split(',')]
            process_sizes = [int(x.strip()) for x in self.proc_size_entry.get().split(',')]
            arrival_times = [int(x.strip()) for x in self.arrival_entry.get().split(',')]
            burst_times = [int(x.strip()) for x in self.burst_entry.get().split(',')]
            
            if len(process_sizes) != len(arrival_times) or len(process_sizes) != len(burst_times):
                raise ValueError("Process sizes, arrival times, and burst times must have the same number of entries")
                
            if not all(x > 0 for x in partitions + process_sizes + burst_times) or not all(x >= 0 for x in arrival_times):
                raise ValueError("All sizes and times must be positive integers (arrival can be 0)")

            algorithm = self.alloc_method.get()
            result = self.simulate_contiguous(partitions, process_sizes, arrival_times, burst_times, algorithm)
            
            self.display_contiguous_result(partitions, process_sizes, arrival_times, burst_times, algorithm, result)

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def simulate_contiguous(self, partitions, process_sizes, arrival_times, burst_times, algorithm):
        memory = [{'size': size, 'free': True, 'process': None} for size in partitions]
        waiting = []
        allocations = []
        
        processes = []
        for pid, (size, arrival, burst) in enumerate(zip(process_sizes, arrival_times, burst_times), 1):
            processes.append({
                'pid': pid,
                'size': size,
                'arrival': arrival,
                'burst': burst,
                'allocated': False,
                'completed': False,
                'wait_time': 0
            })
        
        processes.sort(key=lambda x: x['arrival'])
        
        for process in processes:
            allocated = False
            size = process['size']
            pid = process['pid']
            
            if algorithm == "Best-Fit":
                candidates = sorted([(i, p) for i, p in enumerate(memory) if p['free'] and p['size'] >= size],
                                  key=lambda x: x[1]['size'])
            elif algorithm == "Worst-Fit":
                candidates = sorted([(i, p) for i, p in enumerate(memory) if p['free'] and p['size'] >= size],
                                  key=lambda x: -x[1]['size'])
            else:  
                candidates = [(i, p) for i, p in enumerate(memory) if p['free'] and p['size'] >= size]
            
            if candidates:
                idx, partition = candidates[0]
                partition['free'] = False
                partition['process'] = f"P{pid}({size}K)"
                allocations.append(f"P{pid} ({size}K) arrived at {process['arrival']}, burst {process['burst']} → {partition['size']}K partition")
                process['allocated'] = True
                
                remaining = partition['size'] - size
                if remaining > 0:
                    memory.insert(idx+1, {'size': remaining, 'free': True, 'process': None})
                    partition['size'] = size
            else:
                waiting.append(f"P{pid} ({size}K) arrived at {process['arrival']}, burst {process['burst']}")
                process['wait_time'] += 1
        
        external = sum(p['size'] for p in memory if p['free'])
        internal = sum(p['size'] - int(p['process'].split('(')[1][:-2]) 
                   for p in memory if not p['free'] and p['process'])
        
        total_wait = sum(p['wait_time'] for p in processes)
        avg_wait = total_wait / len(processes) if processes else 0
        
        return {
            'memory': memory,
            'allocations': allocations,
            'waiting': waiting,
            'external_frag': external,
            'internal_frag': internal,
            'avg_wait_time': avg_wait,
            'processes': processes
        }

    def display_contiguous_result(self, partitions, process_sizes, arrival_times, burst_times, algorithm, result):
        self.contig_canvas.delete("all")
        self.contig_results.delete(1.0, tk.END)
        
        y = 20
        total_size = sum(partitions)
        scale = 700 / total_size
        
        for i, part in enumerate(result['memory']):
            width = part['size'] * scale
            color = "#CCFFCC" if not part['free'] else "#DDDDDD"
            
            self.contig_canvas.create_rectangle(20, y, 20 + width, y + 30, fill=color, outline="black")
            label = part['process'] if part['process'] else f"Free\n{part['size']}K"
            self.contig_canvas.create_text(25, y + 15, anchor='w', text=label)
            y += 40
        
        self.contig_results.insert(tk.END, f"=== {algorithm} Algorithm ===\n\n")
        self.contig_results.insert(tk.END, "Process Details:\n")
        
        self.contig_results.insert(tk.END, "PID | Size | Arrival | Burst | Allocated\n")
        self.contig_results.insert(tk.END, "----+------+---------+-------+----------\n")
        for p in result['processes']:
            alloc_status = "Yes" if p['allocated'] else "No"
            self.contig_results.insert(tk.END, f"{p['pid']:3} | {p['size']:4} | {p['arrival']:7} | {p['burst']:5} | {alloc_status:8}\n")
        
        self.contig_results.insert(tk.END, "\nAllocations:\n" + "\n".join(result['allocations']) + "\n\n")
        
        if result['waiting']:
            self.contig_results.insert(tk.END, "Waiting Processes:\n" + "\n".join(result['waiting']) + "\n\n")
        
        self.contig_results.insert(tk.END, f"External Fragmentation: {result['external_frag']}K\n")
        self.contig_results.insert(tk.END, f"Internal Fragmentation: {result['internal_frag']}K\n")
        self.contig_results.insert(tk.END, f"Average Waiting Time: {result['avg_wait_time']:.2f} units\n")

    def setup_paging_tab(self):
        input_frame = ttk.LabelFrame(self.paging_tab, text="Page Replacement", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(input_frame, text="Reference String:").grid(row=0, column=0, sticky='w')
        self.ref_entry = ttk.Entry(input_frame)
        self.ref_entry.grid(row=0, column=1, sticky='ew')
        self.ref_entry.insert(0, "7 0 1 2 0 3 0 4 2 3 0 3 0 3 2 1 2 0 1 7 0 1")

        ttk.Label(input_frame, text="Number of Frames:").grid(row=1, column=0, sticky='w')
        self.frames_entry = ttk.Entry(input_frame)
        self.frames_entry.grid(row=1, column=1, sticky='w')
        self.frames_entry.insert(0, "3")

        ttk.Label(input_frame, text="Algorithm:").grid(row=2, column=0, sticky='w')
        self.page_method = ttk.Combobox(input_frame, values=["FIFO", "LRU", "Optimal"])
        self.page_method.grid(row=2, column=1, sticky='w')
        self.page_method.current(0)

        ttk.Button(input_frame, text="Simulate", command=self.run_paging).grid(row=3, columnspan=2, pady=5)


        self.page_output = tk.Text(self.paging_tab, height=20, wrap=tk.WORD)
        self.page_output.pack(fill='both', expand=True, padx=10, pady=5)

    def run_paging(self):
        try:
            ref_str = list(map(int, self.ref_entry.get().split()))
            num_frames = int(self.frames_entry.get())
            
            if num_frames <= 0:
                raise ValueError("Number of frames must be positive")
                
            method = self.page_method.get()
            result = self.simulate_paging(ref_str, num_frames, method)
            
            self.display_paging_result(ref_str, num_frames, method, result)

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def simulate_paging(self, ref_str, num_frames, method):
        frames = []
        history = []
        faults = 0
        
        for i, page in enumerate(ref_str):
            fault = False
            
            if page in frames:
                if method == "LRU":
                    frames.remove(page)
                    frames.append(page)
            else:
                fault = True
                faults += 1
                
                if len(frames) < num_frames:
                    frames.append(page)
                else:
                    if method == "FIFO":
                        frames.pop(0)
                    elif method == "LRU":
                        frames.pop(0)
                    elif method == "Optimal":
                        future = ref_str[i+1:]
                        indexes = [future.index(f) if f in future else float('inf') for f in frames]
                        frames.pop(indexes.index(max(indexes)))
                    frames.append(page)
            
            history.append((page, list(frames), fault))
        
        return {
            'history': history,
            'total_faults': faults
        }

    def display_paging_result(self, ref_str, num_frames, method, result):
        self.page_output.delete(1.0, tk.END)
        
        self.page_output.insert(tk.END, f"=== {method} Page Replacement ===\n")
        self.page_output.insert(tk.END, f"Reference String: {' '.join(map(str, ref_str))}\n")
        self.page_output.insert(tk.END, f"Frames: {num_frames}\n\n")
        
        for step, (page, frames, fault) in enumerate(result['history'], 1):
            self.page_output.insert(tk.END, 
                f"Step {step:2d}: Page {page} → Frames: {frames} | {'FAULT' if fault else 'HIT'}\n")
        
        self.page_output.insert(tk.END, f"\nTotal Page Faults: {result['total_faults']}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryManagementSimulator(root)
    root.mainloop()