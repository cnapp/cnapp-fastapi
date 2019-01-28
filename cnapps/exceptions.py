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

class CnappsError(Exception):
    """Base exception for Cnapps."""

    status_code = 500


class ConfigurationError(CnappsError):

    def __init__(self, message):
        self.message = message
        self.status_code = 500


class APIError(CnappsError):
    """Base error for REST API."""
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code


class DatabaseError(CnappsError):

    def __init__(self, message):
        self.message = message
        self.status_code = 500

class UnauthorizedError(CnappsError):

    def __init__(self, msg=""):
        self.message = "Authentication required. %s" % msg
        self.status_code = 401


class ForbiddenError(CnappsError):

    def __init__(self, msg=""):
        self.message = "Insufficient credentials. %s" % msg
        self.status_code = 403
