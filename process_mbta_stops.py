# Copyright 2021 Pujit Mehrotra
#
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
import json


def select_stop_info(stop):
    attributes = stop["attributes"]
    return {
        "id": stop["id"],
        "lat": attributes["latitude"],
        "long": attributes["longitude"],
        "wheelchair": attributes["wheelchair_boarding"],
        "name": attributes["name"],
    }


data_source_file = "stops_data.json"  # Source file for MBTA /stops response
target_file = "filtered_mbta_stop_data.json"

with open(data_source_file) as response:
    data = json.load(response)["data"]
    filtered = list(map(select_stop_info, data))
    with open(target_file, "w") as stop_data_file:
        json.dump(filtered, stop_data_file)
