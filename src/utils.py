from datetime import datetime

import humanize

from models import User, IssueWithUsersAndTeams

HEADERS = [
    "Title",
    "Updated",
    "Creator",
    "Creator in team",
    "Team user",
    "Created",
    "State",
]


def issue_to_tabulate(issue: IssueWithUsersAndTeams, user: User) -> list[str]:
    title = f"[DRAFT] {issue.title}" if issue.draft else issue.title
    return [
        format_url(title, issue.html_url),
        humanize_date(issue.updated_at),
        str(issue.creator),
        bool_to_emoji(issue.creator_in_team),
        sort_assigned_team_user(issue.assigned_team_user, user),
        humanize_date(issue.created_at),
        issue.state,
    ]


def bool_to_emoji(variable: bool) -> str:
    return "✅" if variable else "❌"


def make_bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"


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
    return f"\x1b]8;;{url}\x1b\\{title}\x1b]8;;\x1b\\"
