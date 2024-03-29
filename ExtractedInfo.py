from __future__ import unicode_literals
# Object to hold model information for information extracted from an article

class ExtractedInfo:
    def __init__(self, id, incident, weapons, perp_indivs, perp_orgs, targets, victims):
        self.id = id
        self.incident = incident
        self.weapons = weapons
        self.perp_indivs = perp_indivs
        self.perp_orgs = perp_orgs
        self.targets = targets
        self.victims = victims

        self.data = [weapons, perp_indivs, perp_orgs, targets, victims]


    def write_list(self, header, arr, file_output):
        if arr:
        	printed_once = False
        	for item in arr:
        		if (not printed_once):
        			printed_once = True
        			file_output.write(header + item + '\n')
        		else:
        		    file_output.write('               ' + item + '\n')
        else:
        	file_output.write(header + '-\n')

    # Writes a string in the format specified in the project file
    def write_template(self, file_output):
        file_output.write('ID:            ' + self.id + '\n')
        file_output.write('INCIDENT:      ' + self.incident + '\n')

        headers = ['WEAPON:        ', 'PERP INDIV:    ', 'PERP ORG:      ',
        'TARGET:        ', 'VICTIM:        ']


        for (header, arr) in zip(headers, self.data):
            self.write_list(header, arr, file_output)

        file_output.write('\n')
