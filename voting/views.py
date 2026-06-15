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
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if role == "voter":
            # Database mein check kar rahe hain ki voter exist karta hai ya nahi
            voter = Voter.objects.filter(name=username, password=password).first()
            if voter:
                request.session['voter_id'] = voter.id
                return redirect("voter_dashboard")
            else:
                return render(request, "login.html", {"message": "Invalid Voter Username or Password!"})

        elif role == "staff":
            # Staff ke liye simple check (Aap isko zarurat ke hisaab se change kar sakte hain)
            if username == "admin" and password == "admin123":
                request.session['staff_logged_in'] = True
                return redirect("staff_dashboard")
            else:
                return render(request, "login.html", {"message": "Invalid Staff Credentials!"})

        elif role == "candidate":
            # Candidate database mein exist karta hai ya nahi (sirf naam se check)
            candidate = Candidate.objects.filter(name=username).first()
            if candidate:
                request.session['candidate_id'] = candidate.id
                return redirect("candidate_dashboard")
            else:
                return render(request, "login.html", {"message": "Candidate not found!"})

    return render(request, "login.html")


# ---------------- DASHBOARD ----------------
def staff_dashboard(request):
    # Security check: Agar staff login nahi hai toh wapas login page par bhejo
    if not request.session.get('staff_logged_in'):
        return redirect("login")
    return render(request, "staff_dashboard.html")


def candidate_dashboard(request):
    if not request.session.get('candidate_id'):
        return redirect("login")
    return render(request, "candidate_dashboard.html")


def voter_dashboard(request):
    # Session se logged-in voter ki ID nikalna
    voter_id = request.session.get('voter_id')
    
    # Agar bina login kiye direct URL open kare, toh wapas login par bhej do
    if not voter_id:
        return redirect("login")

    voter = get_object_or_404(Voter, id=voter_id)
    candidates = Candidate.objects.all()
    status = ElectionStatus.objects.get_or_create(id=1)[0]

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

# ---------------- RESULTS & DECLARE WINNER ----------------
def results(request):
    # 'vote' ki jagah 'votes' use karna hai kyunki related_name='votes' hai
    candidates = Candidate.objects.annotate(
        total_votes=Count('votes') 
    )
    return render(request, "results.html", {
        "candidates": candidates
    })

def declare_winner(request):
    candidates = Candidate.objects.annotate(
        total_votes=Count('votes')
    ).order_by('-total_votes')

    winner = candidates.first()

    return render(request, "declare_winner.html", {
        "winner": winner,
        "candidates": candidates
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
    request.session.flush() # Yeh line session delete kar deti hai (secure logout)
    return redirect("login")

def change_candidate_password(request):
    return render(
        request,
        "change_candidate_password.html"
    )