"""GitHub repository GraphQL node."""

import graphene

from apps.common.graphql.nodes import BaseNode
from apps.github.graphql.nodes.issue import IssueNode
from apps.github.graphql.nodes.release import ReleaseNode
from apps.github.graphql.nodes.repository_contributor import RepositoryContributorNode
from apps.github.models.repository import Repository

RECENT_ISSUES_LIMIT = 5
RECENT_RELEASES_LIMIT = 5


class RepositoryNode(BaseNode):
    """Repository node."""

    issues = graphene.List(IssueNode)
    languages = graphene.List(graphene.String)
    latest_release = graphene.String()
    owner_key = graphene.String()
    releases = graphene.List(ReleaseNode)
    top_contributors = graphene.List(RepositoryContributorNode)
    topics = graphene.List(graphene.String)
    url = graphene.String()

    class Meta:
        model = Repository
        fields = (
            "commits_count",
            "contributors_count",
            "created_at",
            "description",
            "forks_count",
            "key",
            "license",
            "name",
            "open_issues_count",
            "organization",
            "size",
            "stars_count",
            "subscribers_count",
            "updated_at",
        )

    def resolve_issues(self, info):
        """Resolve recent issues."""
        return self.issues.select_related(
            "author",
        ).order_by(
            "-created_at",
        )[:RECENT_ISSUES_LIMIT]

    def resolve_languages(self, info):
        """Resolve languages."""
        return self.languages.keys()

    def resolve_latest_release(self, info):
        """Resolve latest release."""
        return self.latest_release

    def resolve_owner_key(self, info):
        """Resolve owner key."""
        return self.owner_key

    def resolve_releases(self, info):
        """Resolve recent releases."""
        return self.published_releases.order_by(
            "-published_at",
        )[:RECENT_RELEASES_LIMIT]

    def resolve_top_contributors(self, info):
        """Resolve top contributors."""
        return self.idx_top_contributors

    def resolve_topics(self, info):
        """Resolve topics."""
        return self.topics

    def resolve_url(self, info):
        """Resolve URL."""
        return self.url
