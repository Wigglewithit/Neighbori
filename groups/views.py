from django.shortcuts import render, redirect, get_object_or_404
from .forms import GroupForm
from .models import Group
from django.contrib.auth.decorators import login_required


@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()
            group.members.add(request.user)
            return redirect('groups:list')
    else:
        form = GroupForm()
    return render(request, 'groups/create_group.html', {'form': form})

@login_required
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'groups/group_list.html', {'groups': groups})

def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    return render(request, 'groups/group_detail.html', {'group': group})

def join_group(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.user in group.members.all():
        messages.info(request, "You are already a member of this group.")
    else:
        group.members.add(request.user)
        messages.success(request, "You joined the group.")

    return redirect('groups:detail', pk=pk)
