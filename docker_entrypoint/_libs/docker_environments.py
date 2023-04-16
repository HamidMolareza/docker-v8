import os

from on_rails import Result, def_result


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
