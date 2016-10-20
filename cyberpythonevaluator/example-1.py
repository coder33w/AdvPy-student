from cyberpythonevaluator import CyberPythonEvaluator

cpe = CyberPythonEvaluator()

challenge = cpe.get_challenge(1)

print "Description", challenge.description
print "Example Input", challenge.example_input
print "Example Output", challenge.example_output

def solution (lhs, rhs) :
    return lhs + rhs

#print challenge.validate(solution, debug=True)
print challenge.validate(solution, debug=True)