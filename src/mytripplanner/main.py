#!/usr/bin/env python
import sys
import warnings

from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from crew import Mytripplanner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run the LangGraph Workflow"""
    inputs={
        "location":"Nagar Khas",
        "days":"7"
    }
    results=Mytripplanner().crew().kickoff(inputs=inputs)
    print(results.raw)


if __name__ =="__main__":
    run()
