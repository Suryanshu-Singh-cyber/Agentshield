# backend/dataset_loader.py
# Load and use evaluation datasets

import json
from typing import List, Dict

class DatasetLoader:
    """Load and manage evaluation datasets."""
    
    def __init__(self):
        self.datasets = {}
    
    def load_dataset(self, name: str, data: List[Dict]):
        """Load a dataset."""
        self.datasets[name] = data
    
    def get_tests_from_dataset(self, name: str, limit: int = 10) -> List[Dict]:
        """Extract tests from a dataset."""
        if name not in self.datasets:
            return []
        
        data = self.datasets[name][:limit]
        tests = []
        for item in data:
            tests.append({
                "id": f"dataset_{len(tests)+1:03d}",
                "input": item.get("input", ""),
                "attack_type": item.get("attack_type", "dataset"),
                "expected_behavior": item.get("expected", "block"),
                "source": f"dataset_{name}"
            })
        return tests
