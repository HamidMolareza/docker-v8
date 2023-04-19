import os

from on_rails import Result, def_result
from pylity.decorators.validate_func_params import validate_func_params
from schema import And, Schema


class DockerEnvironments:
    """
    The class `DockerEnvironments` defines a set of attributes and methods for retrieving environment variables
    related to a Docker container.
    """

    maintainer: str
    docker_version: str
    build_date: str
    vcs_url: str
    bug_report: str
    docker_name: str

    @validate_func_params(schema=Schema({
        'maintainer': And(str, len, error='The maintainer is required string and can not be empty.'),
        'docker_version': And(str, len, error='The docker_version is required string and can not be empty.'),
        'build_date': And(str, len, error='The build_date is required string and can not be empty.'),
        'vcs_url': And(str, len, error='The vcs_url is required string and can not be empty.'),
        'bug_report': And(str, len, error='The bug_report is required string and can not be empty.'),
        'docker_name': And(str, len, error='The docker_name is required string and can not be empty.'),
    }), raise_exception=True)
    def __init__(self, maintainer: str, docker_version: str, build_date: str, vcs_url: str, bug_report: str,
                 docker_name: str):
        self.maintainer = maintainer
        self.docker_version = docker_version
        self.build_date = build_date
        self.vcs_url = vcs_url
        self.bug_report = bug_report
        self.docker_name = docker_name

    @staticmethod
    @def_result()
    def get_environments() -> Result:
        """
        Returns a DockerEnvironments object with environment variables as its attributes.
        """

        return Result.ok(value=DockerEnvironments(
            maintainer=os.environ.get('DOCKER_MAINTAINER', 'No Data!'),
            docker_version=os.environ.get('DOCKER_VERSION', 'latest'),
            build_date=os.environ.get('DOCKER_BUILD_DATE', 'No Data!'),
            vcs_url=os.environ.get('VCS_URL', 'No Data!'),
            bug_report=os.environ.get('BUG_REPORT', 'No Data!'),
            docker_name=os.environ.get('DOCKER_NAME', 'No Data!')
        ))
