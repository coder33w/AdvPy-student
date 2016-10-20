from cyberpythonevaluator import CyberPythonEvaluator

cpe = CyberPythonEvaluator()

challenge = cpe.get_challenge(0)

print "Description", challenge.description
print "Example Input", challenge.example_input
print "Example Output", challenge.example_output

def solution (input_string) :
    return input_string

#print challenge.validate(solution, debug=True)
print challenge.validate(solution, debug=True)