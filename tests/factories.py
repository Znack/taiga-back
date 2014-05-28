import uuid
import threading

from django.db.models.loading import get_model

import factory
from django.conf import settings

# import taiga.projects.models
# import taiga.projects.userstories.models
# import taiga.projects.issues.models
# import taiga.projects.milestones.models
# import taiga.projects.stars.models
# import taiga.users.models
# import taiga.userstorage.models


class Factory(factory.DjangoModelFactory):
    FACTORY_STRATEGY = factory.CREATE_STRATEGY

    _SEQUENCE = 1
    _SEQUENCE_LOCK = threading.Lock()

    @classmethod
    def _setup_next_sequence(cls):
        with cls._SEQUENCE_LOCK:
            cls._SEQUENCE += 1
        return cls._SEQUENCE


class ProjectTemplateFactory(Factory):
    FACTORY_FOR = get_model("projects", "ProjectTemplate")
    FACTORY_DJANGO_GET_OR_CREATE = ("slug", )

    name = "Template name"
    slug = settings.DEFAULT_PROJECT_TEMPLATE

    us_statuses = []
    points = []
    task_statuses = []
    issue_statuses = []
    issue_types = []
    priorities = []
    severities = []
    roles = []


class ProjectFactory(Factory):
    FACTORY_FOR = get_model("projects", "Project")

    name = factory.Sequence(lambda n: "Project {}".format(n))
    slug = factory.Sequence(lambda n: "project-{}-slug".format(n))
    description = "Project description"
    owner = factory.SubFactory("tests.factories.UserFactory")
    creation_template = factory.SubFactory("tests.factories.ProjectTemplateFactory")


class RoleFactory(Factory):
    FACTORY_FOR = get_model("users", "Role")

    name = "Tester"
    project = factory.SubFactory("tests.factories.ProjectFactory")


class PointsFactory(Factory):
    FACTORY_FOR = get_model("projects", "Points")

    name = factory.Sequence(lambda n: "Points {}".format(n))
    value = 2
    project = factory.SubFactory("tests.factories.ProjectFactory")


class RolePointsFactory(Factory):
    FACTORY_FOR = get_model("userstories", "RolePoints")

    user_story = factory.SubFactory("tests.factories.UserStoryFactory")
    role = factory.SubFactory("tests.factories.RoleFactory")
    points = factory.SubFactory("tests.factories.PointsFactory")


class UserFactory(Factory):
    FACTORY_FOR = get_model("users", "User")

    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.LazyAttribute(lambda obj: '%s@email.com' % obj.username)
    password = factory.PostGeneration(lambda obj, *args, **kwargs: obj.set_password(obj.username))


class MembershipFactory(Factory):
    FACTORY_FOR = get_model("projects", "Membership")

    token = factory.LazyAttribute(lambda obj: str(uuid.uuid1()))
    project = factory.SubFactory("tests.factories.ProjectFactory")
    role = factory.SubFactory("tests.factories.RoleFactory")
    user = factory.SubFactory("tests.factories.UserFactory")


class StorageEntryFactory(Factory):
    FACTORY_FOR = get_model("userstorage", "StorageEntry")

    owner = factory.SubFactory("tests.factories.UserFactory")
    key = factory.Sequence(lambda n: "key-{}".format(n))
    value = factory.Sequence(lambda n: "value {}".format(n))


class UserStoryFactory(Factory):
    FACTORY_FOR = get_model("userstories", "UserStory")

    ref = factory.Sequence(lambda n: n)
    project = factory.SubFactory("tests.factories.ProjectFactory")
    owner = factory.SubFactory("tests.factories.UserFactory")
    subject = factory.Sequence(lambda n: "User Story {}".format(n))


class MilestoneFactory(Factory):
    FACTORY_FOR = get_model("milestones", "Milestone")

    name = factory.Sequence(lambda n: "Milestone {}".format(n))
    owner = factory.SubFactory("tests.factories.UserFactory")
    project = factory.SubFactory("tests.factories.ProjectFactory")


class IssueFactory(Factory):
    FACTORY_FOR = get_model("issues", "Issue")

    subject = factory.Sequence(lambda n: "Issue {}".format(n))
    owner = factory.SubFactory("tests.factories.UserFactory")
    project = factory.SubFactory("tests.factories.ProjectFactory")
    status = factory.SubFactory("tests.factories.IssueStatusFactory")
    severity = factory.SubFactory("tests.factories.SeverityFactory")
    priority = factory.SubFactory("tests.factories.PriorityFactory")
    type = factory.SubFactory("tests.factories.IssueTypeFactory")
    milestone = factory.SubFactory("tests.factories.MilestoneFactory")


class IssueStatusFactory(Factory):
    FACTORY_FOR = get_model("projects", "IssueStatus")

    name = factory.Sequence(lambda n: "Issue Status {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class SeverityFactory(Factory):
    FACTORY_FOR = get_model("projects", "Severity")

    name = factory.Sequence(lambda n: "Severity {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class PriorityFactory(Factory):
    FACTORY_FOR = get_model("projects", "Priority")

    name = factory.Sequence(lambda n: "Priority {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class IssueTypeFactory(Factory):
    FACTORY_FOR = get_model("projects", "IssueType")

    name = factory.Sequence(lambda n: "Issue Type {}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class FanFactory(Factory):
    FACTORY_FOR = get_model("stars", "Fan")

    project = factory.SubFactory("tests.factories.ProjectFactory")
    user = factory.SubFactory("tests.factories.UserFactory")


class StarsFactory(Factory):
    FACTORY_FOR = get_model("stars", "Stars")

    project = factory.SubFactory("tests.factories.ProjectFactory")
    count = 0