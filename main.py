from parser.load_all import load_all

risks, mitigations, relationships = load_all()

print("Loaded Number of Risks:", len(risks))
print("Loaded Number of Mitigations:", len(mitigations))
print("Loaded Number of Relationships:", len(relationships))