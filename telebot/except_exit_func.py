import os
import sys

def except_exit_func():
    """
    Forcefully terminates the application process.
    
    This function first attempts a standard termination via sys.exit(0).
    If a SystemExit exception is caught (or to ensure immediate termination
    of all threads), it falls back to low-level termination via os._exit(0).
    """
    print("\n\nForce Stop.\nExit.\n\n")
    try:
        sys.exit(0)
    except SystemExit:
        # Absolute low-level process termination fallback
        os._exit(0)