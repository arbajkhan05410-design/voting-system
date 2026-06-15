from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('candidate-dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('voter-dashboard/', views.voter_dashboard, name='voter_dashboard'),
    path('results/', views.results, name='results'),
    path('add-candidate/', views.add_candidate, name='add_candidate'),
    path(
    'view-candidates/',
    views.view_candidates,
    name='view_candidates'
),
path('add-voter/', views.add_voter, name='add_voter'),
path('view-voters/', views.view_voters, name='view_voters'),path('start-election/', views.start_election, name='start_election'),

path('stop-election/', views.stop_election, name='stop_election'),

path('logout/', views.logout_view, name='logout'),
path(
    'apply-election/',
    views.apply_election,
    name='apply_election'
),

path(
    'change-candidate-password/',
    views.change_candidate_password,
    name='change_candidate_password'
),path(
    'declare-winner/',
    views.declare_winner,
    name='declare_winner'
),
path(
    'delete-candidate/<int:candidate_id>/',
    views.delete_candidate,
    name='delete_candidate'
),

path(
    'delete-voter/<int:voter_id>/',
    views.delete_voter,
    name='delete_voter'
),path(
    'edit-candidate/<int:candidate_id>/',
    views.edit_candidate,
    name='edit_candidate'
),
path(
    'edit-voter/<int:voter_id>/',
    views.edit_voter,
    name='edit_voter'
),
path(
    'view-applications/',
    views.view_applications,
    name='view_applications'
),

path(
    'approve-application/<int:application_id>/',
    views.approve_application,
    name='approve_application'
),

path(
    'reject-application/<int:application_id>/',
    views.reject_application,
    name='reject_application'
),
]