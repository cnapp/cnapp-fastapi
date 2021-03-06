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
import time

import fastapi
from starlette import staticfiles
import starlette_prometheus

from cnapps.api import health
from cnapps.api import version
from cnapps.api.v1 import core
from cnapps.middleware.logging import log
from cnapps import settings
from cnapps import version as app_version
from cnapps import web


LOGGER = logging.getLogger(__name__)


def creates_app():
    """Create the application

    Returns:
        [fastapi.FastAPI]: the main application
    """

    LOGGER.info("Create application %s", app_version.RELEASE)
    app = fastapi.FastAPI(
        version=app_version.RELEASE,
        title=settings.PROJECT_NAME,
        openapi_url="/api/%s/openapi.json" % core.PATH,
        template_directory='templates'
        )
    app.mount('/static', staticfiles.StaticFiles(directory='cnapps/static'), name='static')
    app.include_router(health.router)
    app.include_router(version.router)
    app.include_router(web.router)
    app.include_router(core.api_router, prefix="/api/%s" % core.PATH)
    app.add_middleware(starlette_prometheus.PrometheusMiddleware)
    app.add_route("/metrics/", starlette_prometheus.metrics)
    return app


