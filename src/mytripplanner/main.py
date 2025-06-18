#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from mytripplanner.crew import Mytripplanner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run the Crew"""
    inputs={
        "location":"London",
        "days":"4"
    }
    results=Mytripplanner().crew().kickoff(inputs=inputs)
    print(results.raw)


if __name__ =="__main__":
    run()
