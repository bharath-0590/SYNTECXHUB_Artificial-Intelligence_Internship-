class RuleBasedExpertSystem:
    def __init__(self):
        self.facts = set()  # Facts base (e.g., symptoms)
        self.rules = []     # List of rules: each is a dict with 'conditions', 'conclusion', 'confidence'
        self.inference_log = []  # Log of steps for reasoning path

    def add_fact(self, fact):
        """Add a fact to the facts base."""
        self.facts.add(fact.lower().strip())

    def add_rule(self, conditions, conclusion, confidence=1.0):
        """Add a rule: conditions (list of facts, supports AND/OR), conclusion (fact), confidence (0-1)."""
        self.rules.append({
            'conditions': conditions,  # e.g., [{'fact': 'fever', 'op': 'AND'}, {'fact': 'cough', 'op': 'OR'}]
            'conclusion': conclusion.lower().strip(),
            'confidence': confidence
        })

    def evaluate_rule(self, rule):
        """Check if a rule's conditions are satisfied."""
        satisfied = True
        for cond in rule['conditions']:
            fact = cond['fact'].lower().strip()
            op = cond.get('op', 'AND')  # Default to AND
            if op == 'AND':
                if fact not in self.facts:
                    satisfied = False
                    break
            elif op == 'OR':
                if fact in self.facts:
                    satisfied = True
                    break
                else:
                    satisfied = False
        return satisfied

    def forward_chain(self, max_steps=100):
        """Perform forward chaining: apply rules repeatedly until no new facts."""
        self.inference_log = []  # Reset log
        step = 0
        new_facts_added = True
        
        while new_facts_added and step < max_steps:
            new_facts_added = False
            step += 1
            self.inference_log.append(f"Step {step}: Current facts: {sorted(self.facts)}")
            
            for rule in self.rules:
                if rule['conclusion'] not in self.facts and self.evaluate_rule(rule):
                    self.facts.add(rule['conclusion'])
                    self.inference_log.append(f"  Rule fired: {rule['conditions']} -> {rule['conclusion']} (confidence: {rule['confidence']})")
                    self.inference_log.append(f"  New fact added: {rule['conclusion']}")
                    new_facts_added = True
                    break  # Fire one rule per step for controlled chaining
        
        if step >= max_steps:
            self.inference_log.append("Inference stopped: Max steps reached (possible loop).")
        else:
            self.inference_log.append("Inference complete: No more rules can fire.")

    def backward_chain(self, goal):
        """Optional: Backward chaining to check if a goal can be proven."""
        # Simplified: Check if goal is in facts or can be derived via rules
        if goal in self.facts:
            return True, [f"Goal '{goal}' directly in facts."]
        
        for rule in self.rules:
            if rule['conclusion'] == goal and self.evaluate_rule(rule):
                return True, [f"Goal '{goal}' derived via rule: {rule['conditions']} -> {rule['conclusion']}"]
        return False, [f"Goal '{goal}' cannot be proven."]

    def print_log(self):
        """Print the inference log."""
        print("\nInference Reasoning Path:")
        for entry in self.inference_log:
            print(entry)

    def export_log(self, filename="inference_log.txt"):
        """Export log to a file."""
        with open(filename, 'w') as f:
            f.write("\n".join(self.inference_log))
        print(f"Log exported to {filename}")

# Sample Setup: Medical Diagnosis System
def setup_medical_system():
    system = RuleBasedExpertSystem()
    
    # Sample Rules (multi-step chaining example)
    system.add_rule([{'fact': 'fever', 'op': 'AND'}, {'fact': 'cough', 'op': 'AND'}], 'flu', 0.9)
    system.add_rule([{'fact': 'flu', 'op': 'AND'}, {'fact': 'headache', 'op': 'AND'}], 'severe_flu', 0.8)
    system.add_rule([{'fact': 'rash', 'op': 'AND'}, {'fact': 'fever', 'op': 'OR'}], 'allergy', 0.7)
    system.add_rule([{'fact': 'sore_throat', 'op': 'AND'}, {'fact': 'cough', 'op': 'AND'}], 'cold', 0.85)
    
    return system

# Interactive Usage
if __name__ == "__main__":
    system = setup_medical_system()
    
    # User Input: Add initial facts (symptoms)
    print("Enter symptoms (one per line, type 'done' to finish):")
    while True:
        symptom = input("> ").strip()
        if symptom.lower() == 'done':
            break
        system.add_fact(symptom)
    
    print(f"Initial facts: {sorted(system.facts)}")
    
    # Perform Forward Chaining
    system.forward_chain()
    system.print_log()
    
    # Optional: Check a specific goal with backward chaining
    goal = input("Enter a goal to check (e.g., 'flu'), or press Enter to skip: ").strip().lower()
    if goal:
        proven, path = system.backward_chain(goal)
        print(f"Backward Chaining for '{goal}': {'Proven' if proven else 'Not Proven'}")
        for step in path:
            print(f"  {step}")
    
    # Export log
    system.export_log()
