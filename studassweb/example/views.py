from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.template.context import RequestContext

team_members = ['Lundis', 'Magnus', 'Johnny', 'Oscar', 'J', 'Asis']
# Create your views here.
def choose(request):
	return render(request, 'example/choose.html', {'members' : team_members})

def result(request, winner):
	vars = {'winner' : _('No one')}
	try:
		result = int(winner)
		# make sure that it's a valid option
		if 0 <= result and result < len(team_members):
			vars = {'winner' : team_members[result]}
	except:
		pass
	return render(request, 'example/result.html', vars)
