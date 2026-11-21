
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from items.models import Item
from .forms import ClaimForm, VerificationQuestionForm, ClaimVerificationForm
from .models import Claim


@login_required
def submit_claim(request, item_id):

    if request.user.role != 'STUDENT':
        return redirect('login')

    item = get_object_or_404(
        Item,
        id=item_id,
        item_type='FOUND'
    )

    if item.reported_by == request.user:
        messages.error(request, "You cannot claim your own reported item.")
        return redirect('browse_items')

    if Claim.objects.filter(
        item=item,
        claimant=request.user
    ).exists():
        messages.error(request, "You have already claimed this item.")
        return redirect('browse_items')

    if request.method == 'POST':
        form = ClaimForm(request.POST)

        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimant = request.user
            claim.save()

            messages.success(request, "Claim submitted successfully!")
            return redirect('verify_claim', claim_id=claim.id)

    return redirect('browse_items')


@login_required
def add_verification_question(request, item_id):

    if request.user.role != 'STAFF':
        return redirect('login')

    item = get_object_or_404(
        Item,
        id=item_id,
        item_type='FOUND'
    )

    if not item.private_details:
        messages.error(
            request,
            "This item has no private identifying details. Please ask the reporter to provide them first."
        )
        return redirect('browse_items')

    if request.method == 'POST':
        form = VerificationQuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.item = item
            question.save()

            messages.success(
                request,
                "Verification question added successfully!"
            )

            return redirect('browse_items')

    else:
        form = VerificationQuestionForm()

    return render(request, 'claims/add_question.html', {
        'form': form,
        'item': item,
    })


@login_required
def verify_claim(request, claim_id):

    if request.user.role != 'STUDENT':
        return redirect('login')

    claim = get_object_or_404(
        Claim,
        id=claim_id,
        claimant=request.user
    )

    if claim.verification_passed:
        messages.info(request, "Your claim is already verified.")
        return redirect('browse_items')

    if claim.verification_attempts >= 3:
        messages.error(request, "Maximum verification attempts reached.")
        return redirect('browse_items')

    questions = claim.item.verification_questions.all()

    if not questions.exists():
        messages.error(request, "No verification questions are available.")
        return redirect('browse_items')

    if request.method == 'POST':
        form = ClaimVerificationForm(
            request.POST,
            questions=questions
        )

        if form.is_valid():

            if form.answers_correct():
                claim.verification_passed = True
                claim.save()

                messages.success(
                    request,
                    "Verification successful! Your claim is awaiting staff approval."
                )

            else:
                claim.verification_attempts += 1
                claim.save()

                messages.error(
                    request,
                    f"Incorrect answers. Attempts used: {claim.verification_attempts}/3"
                )

            return redirect('browse_items')

    else:
        form = ClaimVerificationForm(questions=questions)

    return render(request, 'claims/verify_claim.html', {
        'form': form,
        'claim': claim,
    })


@login_required
def my_claims(request):

    if request.user.role != 'STUDENT':
        return redirect('login')

    claims = Claim.objects.filter(
        claimant=request.user
    ).select_related('item').order_by('-created_at')

    return render(request, 'claims/my_claims.html', {
        'claims': claims,
    })


@login_required
def staff_claims(request):

    if request.user.role != 'STAFF':
        return redirect('login')

    claims = Claim.objects.filter(
        status__in=['PENDING', 'APPROVED']
    ).select_related(
        'item', 'claimant', 'returned_by'
    ).order_by('-created_at')

    return render(request, 'claims/staff_claims.html', {
        'claims': claims,
    })


@login_required
@require_POST
def update_claim_status(request, claim_id, action):

    if request.user.role != 'STAFF':
        return redirect('login')

    claim = get_object_or_404(
        Claim,
        id=claim_id,
        status='PENDING'
    )

    if action == 'approve':

        if not claim.verification_passed:
            messages.error(
                request,
                "Cannot approve a claim before verification."
            )
            return redirect('staff_claims')

        claim.status = 'APPROVED'

    elif action == 'reject':
        claim.status = 'REJECTED'

    else:
        return redirect('staff_claims')

    claim.save()

    messages.success(
        request,
        f"Claim successfully {action}d."
    )

    return redirect('staff_claims')


@login_required
@require_POST
def mark_as_returned(request, claim_id):

    if request.user.role != 'STAFF':
        return redirect('login')

    claim = get_object_or_404(
        Claim,
        id=claim_id,
        status='APPROVED',
        returned=False
    )

    claim.returned = True
    claim.returned_by = request.user
    claim.returned_at = timezone.now()
    claim.save()

    messages.success(
        request,
        "Item successfully marked as returned!"
    )

    return redirect('staff_claims')