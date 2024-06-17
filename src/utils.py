from datetime import datetime

import humanize

from models import User, IssueWithUsersAndTeams, GithubInfo


def issue_to_tabulate(issue: IssueWithUsersAndTeams, github_info: GithubInfo) -> list[str]:
    title = f"[DRAFT] {issue.title}" if issue.draft else issue.title
    creator = make_bold(str(issue.creator)) if issue.creator in github_info.team else str(issue.creator)
    return [
        format_url(title, issue.html_url),
        issue.repo.name,
        humanize_date(issue.updated_at),
        creator,
        sort_assigned_team_user(issue.assigned_team_user, github_info.user),
        humanize_date(issue.created_at),
    ]


def make_bold(text: str) -> str:
    return f"[bold]{text}[/bold]"


def sort_assigned_team_user(assigned_team_user: set[User], user: User) -> str:
    str_assigned_team_user = [str(u) for u in assigned_team_user]
    if user in assigned_team_user:
        str_assigned_team_user.remove(str(user))
        str_assigned_team_user = [make_bold(str(user))] + str_assigned_team_user
    return ", ".join(str_assigned_team_user)


def humanize_date(date: datetime) -> str:
    now = datetime.now()
    diff = now - date
    return humanize.naturaltime(now - diff)


def format_url(title: str, url: str) -> str:
    return f"[link={url}]{title}[/link]"

