# Copyright (C) 2019 Nicolas Lamirault <nicolas.lamirault@gmail.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from os import path

import fastapi
import jinja2
from jinja2 import Environment, FileSystemLoader
from starlette import responses

from cnapps import version


LOGGER = logging.getLogger(__name__)

router = fastapi.APIRouter()

THIS_DIR = path.dirname(path.abspath(__file__))
jinja_env = Environment(
    loader=FileSystemLoader("%s/templates" % THIS_DIR), trim_blocks=True)

CHANGELOG_PATH = "%s/../ChangeLog.md" % THIS_DIR
CHANGELOG_DOCKER_PATH = "/srv/ChangeLog.md"


def render_page(page, content, **context):
    """Render a HTML page.

    :param page: the template name
    """

    try:
        LOGGER.info("Render web page: %s", page)
        return jinja_env.get_template(page).render(content)

    except jinja2.TemplateNotFound as err:
        msg = "Can't load template: %s" % str(err)
        LOGGER.warn(msg)
        try:
            return jinja_env.get_template("error.html").render({"error_message": msg}) #, version=version.RELEASE

        except jinja2.TemplateNotFound as err:
            LOGGER.error("Can't find error template")
            return "Not Found. %s" % err.message


def read_file_content(filename):
    LOGGER.debug("Open file: %s", filename)
    with open(filename, "r") as inputfile:
        return inputfile.read()


@router.get("/", content_type=responses.HTMLResponse)
def home_page():
    return render_page("home.html", {"version": version.RELEASE})


@router.get("/changelog", content_type=responses.HTMLResponse)
def changelog_page():
    content = None

    if path.exists(CHANGELOG_PATH):
        content = read_file_content(CHANGELOG_PATH)
    elif path.exists(CHANGELOG_DOCKER_PATH):
        content = read_file_content(CHANGELOG_DOCKER_PATH)
    else:
        LOGGER.info("Changelog file not found")

    return render_page(
        "changelog.html", {"content": content, "version": version.RELEASE})


@router.get("/favicon.ico")
def favicon():
    return responses.FileResponse("%s/static/img/favicon.ico" % THIS_DIR)
