from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count

from .models import (
    Candidate,
    Voter,
    Vote,
    ElectionStatus,
    ElectionApplication
)

# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == "POST":
        role = request.POST.get("role")

        if role == "staff":
            return redirect("staff_dashboard")
        elif role == "candidate":
            return redirect("candidate_dashboard")
        elif role == "voter":
            return redirect("voter_dashboard")

    return render(request, "login.html")


# ---------------- DASHBOARD ----------------
def staff_dashboard(request):
    return render(request, "staff_dashboard.html")


def candidate_dashboard(request):
    return render(request, "candidate_dashboard.html")


def voter_dashboard(request):
    candidates = Candidate.objects.all()
    status = ElectionStatus.objects.get_or_create(id=1)[0]

    voter = Voter.objects.last()  # TEMP FIX (login not implemented)

    if request.method == "POST":

        if not status.is_active:
            return render(request, "voter_dashboard.html", {
                "candidates": candidates,
                "message": "Election is closed!"
            })

        if voter.voted:
            return render(request, "voter_dashboard.html", {
                "candidates": candidates,
                "message": "You already voted!"
            })

        candidate_id = request.POST.get("candidate_id")
        candidate = get_object_or_404(Candidate, id=candidate_id)

        Vote.objects.create(voter=voter, candidate=candidate)

        voter.voted = True
        voter.save()

        return render(request, "voter_dashboard.html", {
            "candidates": candidates,
            "message": "Vote submitted successfully!"
        })

    return render(request, "voter_dashboard.html", {
        "candidates": candidates
    })


# ---------------- CANDIDATE ----------------
def add_candidate(request):
    if request.method == "POST":
        Candidate.objects.create(
            name=request.POST.get("name"),
            department=request.POST.get("department")
        )
        return render(request, "add_candidate.html", {
            "message": "Candidate Added Successfully!"
        })

    return render(request, "add_candidate.html")


def view_candidates(request):
    candidates = Candidate.objects.all()
    return render(request, "view_candidates.html", {
        "candidates": candidates
    })


def edit_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)

    if request.method == "POST":
        candidate.name = request.POST.get("name")
        candidate.department = request.POST.get("department")
        candidate.save()
        return redirect("view_candidates")

    return render(request, "edit_candidate.html", {
        "candidate": candidate
    })


def delete_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    candidate.delete()
    return redirect("view_candidates")


# ---------------- VOTER ----------------
def add_voter(request):
    if request.method == "POST":
        Voter.objects.create(
            name=request.POST.get("name"),
            enrollment_no=request.POST.get("enrollment_no"),
            password=request.POST.get("password")
        )
        return render(request, "add_voter.html", {
            "message": "Voter Added Successfully!"
        })

    return render(request, "add_voter.html")


def view_voters(request):
    voters = Voter.objects.all()
    return render(request, "view_voters.html", {
        "voters": voters
    })


def edit_voter(request, voter_id):
    voter = get_object_or_404(Voter, id=voter_id)

    if request.method == "POST":
        voter.name = request.POST.get("name")
        voter.enrollment_no = request.POST.get("enrollment_no")
        voter.save()
        return redirect("view_voters")

    return render(request, "edit_voter.html", {
        "voter": voter
    })


def delete_voter(request, voter_id):
    voter = get_object_or_404(Voter, id=voter_id)
    voter.delete()
    return redirect("view_voters")


# ---------------- ELECTION CONTROL ----------------
def start_election(request):
    status = ElectionStatus.objects.get_or_create(id=1)[0]
    status.is_active = True
    status.save()
    return redirect("staff_dashboard")


def stop_election(request):
    status = ElectionStatus.objects.get_or_create(id=1)[0]
    status.is_active = False
    status.save()
    return redirect("staff_dashboard")


# ---------------- RESULTS ----------------
def results(request):
    candidates = Candidate.objects.annotate(
        total_votes=Count('vote')
    )
    return render(request, "results.html", {
        "candidates": candidates
    })


def declare_winner(request):
    winner = Candidate.objects.annotate(
        total_votes=Count('vote')
    ).order_by('-total_votes').first()

    return render(request, "declare_winner.html", {
        "winner": winner
    })


# ---------------- APPLICATION SYSTEM ----------------
def apply_election(request):
    if request.method == "POST":
        ElectionApplication.objects.create(
            name=request.POST.get("name"),
            department=request.POST.get("department"),
            status="Pending"
        )

        return render(request, "apply_election.html", {
            "message": "Application Submitted Successfully!"
        })

    return render(request, "apply_election.html")


def view_applications(request):
    applications = ElectionApplication.objects.all()
    return render(request, "view_applications.html", {
        "applications": applications
    })


def approve_application(request, application_id):
    app = get_object_or_404(ElectionApplication, id=application_id)
    app.status = "Approved"
    app.save()
    return redirect("view_applications")


def reject_application(request, application_id):
    app = get_object_or_404(ElectionApplication, id=application_id)
    app.status = "Rejected"
    app.save()
    return redirect("view_applications")


# ---------------- LOGOUT ----------------
def logout_view(request):
    request.session.flush()
    return redirect("login")

def change_candidate_password(request):
    return render(
        request,
        "change_candidate_password.html"
    )
# ---------------- DECLARE WINNER ----------------
from django.db.models import Count

def declare_winner(request):

    candidates = Candidate.objects.annotate(
        total_votes=Count('vote')
    ).order_by('-total_votes')

    winner = candidates.first()

    return render(request, "declare_winner.html", {
        "winner": winner,
        "candidates": candidates
    })