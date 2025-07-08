
# Memory Management Simulator

## Overview

This is a GUI-based **Memory Management Simulator** developed in **Python (Tkinter)**. The tool simulates two main memory management techniques commonly taught in operating systems courses:

- **Contiguous Memory Allocation**  
  Algorithms implemented: First Fit, Best Fit, and Worst Fit.

- **Paging and Page Replacement Algorithms**  
  Algorithms implemented: FIFO, LRU, and Optimal.

The project provides a visual and textual representation of how processes are allocated in memory and how page replacement is handled using different algorithms.

---

## Features

### 🧠 Contiguous Memory Allocation
- User-defined memory partitions and process configurations
- Supports **First-Fit**, **Best-Fit**, and **Worst-Fit** allocation
- Shows:
  - Memory blocks before and after allocation
  - External and internal fragmentation
  - Average waiting time
  - Allocated and waiting processes

### 📄 Paging & Page Replacement
- Simulates page replacement using:
  - FIFO (First-In-First-Out)
  - LRU (Least Recently Used)
  - Optimal
- Shows page fault history and total page faults

---

## How to Run

1. Make sure you have **Python 3.x** installed.
2. Install Tkinter (usually included by default in standard Python distributions).
3. Run the script:

```bash
python main_memory_allocator.py
```

---


## Developer

- **Erfan Nada**
  Under the supervision of **Dr. Mohamed Ghoneimy**  
  Project developed at **MSA University**

---

## License

This project is for educational purposes and does not carry any specific license.
