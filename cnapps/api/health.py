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

import fastapi
import pydantic

from cnapps import version


LOGGER = logging.getLogger(__name__)

router = fastapi.APIRouter()


class Health(pydantic.BaseModel):
    status: str


@router.get("/health", tags=["health"], response_model=Health)
async def retrieve_status():
    content = {'status': "OK"}
    return Health(**content)
