from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .models import Module, ModuleProgress


@login_required
def dashboard_view(request):
    patient = request.user.patient_profile
    modules = Module.objects.filter(is_active=True)

    # Make sure a progress row exists for every current module
    existing_module_ids = set(
        ModuleProgress.objects.filter(patient=patient).values_list('module_id', flat=True)
    )
    for module in modules:
        if module.id not in existing_module_ids:
            ModuleProgress.objects.create(patient=patient, module=module)

    progress_qs = ModuleProgress.objects.filter(patient=patient).select_related('module')
    progress_by_module = {p.module_id: p for p in progress_qs}

    module_rows = []
    for module in modules:
        module_rows.append({
            'module': module,
            'progress': progress_by_module.get(module.id),
        })

    completed_count = progress_qs.filter(completed=True).count()
    total_count = modules.count()
    percent_complete = int((completed_count / total_count) * 100) if total_count else 0

    context = {
        'patient': patient,
        'module_rows': module_rows,
        'completed_count': completed_count,
        'total_count': total_count,
        'percent_complete': percent_complete,
    }
    return render(request, 'modules/dashboard.html', context)


@login_required
def module_detail_view(request, pk):
    patient = request.user.patient_profile
    module = get_object_or_404(Module, pk=pk, is_active=True)
    progress, _ = ModuleProgress.objects.get_or_create(patient=patient, module=module)

    if not progress.viewed:
        progress.viewed = True
        progress.first_viewed_at = timezone.now()
        progress.save()

    if request.method == 'POST' and 'mark_complete' in request.POST:
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
        messages.success(request, f"Marked '{module.title}' as complete.")
        return redirect('dashboard')

    return render(request, 'modules/module_detail.html', {'module': module, 'progress': progress})
