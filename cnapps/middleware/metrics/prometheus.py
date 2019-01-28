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

import sanic
from sanic import response
import prometheus_client
from prometheus_client import core
from prometheus_client import exposition


LOGGER = logging.getLogger(__name__)

REST = sanic.Blueprint("prometheus")

GLOBAL_STATUS = prometheus_client.Gauge(
    "cnapps_sanic_up", "Was the last query of cnapps successful", ["service"]
)

REQUEST_LATENCY = prometheus_client.Histogram(
    "cnapps_sanic_request_latency_seconds",
    "Request Latency",
    ["method", "endpoint"],
)

REQUEST_COUNT = prometheus_client.Gauge(
    "cnapps_sanic_request_count",
    "Request Count",
    ["method", "endpoint", "status_code"],
)

API_USER = prometheus_client.Counter(
    "cnapps_sanic_api_usage",
    "API usage (count)",
    ["endpoint", "status_code", "user"],
)


@REST.route("/metrics")
def show_metrics(request):
    """Display metrics for Prometheus."""
    registry = core.REGISTRY
    output = exposition.generate_latest(registry)
    resp = response.raw(output, 200)
    resp.headers["Content-type"] = exposition.CONTENT_TYPE_LATEST
    return resp
