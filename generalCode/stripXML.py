def stripXML(filename):
	import subprocess
	regexList = [
	"s#.*<data timestep=.*\n.*<lanes/>\n.*</data>\n##g",
	's#queueing_length_experimental=".*"##g',
	"s#queueing_#q#g",
	"s#length#len#g",
	"s#timestep#tstep#g",
	"s#\n<!--([^\n]*\n+)+-->\n##g"]

	cmd = ['perl', '-0777', '-i', '-pe', 'regex', filename]
	if('queue' in filename):
		for regexStr in regexList:
			cmd[4] = regexStr
			subprocess.call(cmd)
	else:
		cmd[4] = regexList[-1]
		subprocess.call(cmd)
