"""
# Qiskit-Classroom

Qiskit-classroom is a toolkit that helps implement quantum algorithms by converting and visualizing different
expressions used in the Qiskit ecosystem using Qiskit-classroom-converter.
The following three transformations are supported.

* Quantum Circuit to Dirac notation

* Quantum Circuit to Matrix

* Matrix to Quantum Circuit

## Getting Started

### Prerequisites

* LaTeX distribution(or program) must be installed

  * On GNU/Linux recommend TeX Live

  * On Windows recommend MiKTeX

* git should be installed

* python must be installed (3.9 <= X <= 3.11)

* Qt6(>= 6.0.x) must be installed
    * macOS : https://pyside.readthedocs.io/en/latest/installing/macosx.html

### Install with Flatpak (GNU/Linux)

We're currently packaging flatpak package. please wait for a couple of days

### Install with PyPi (Windows, macOS)

```
pip install qiskit-classroom
```

.. warning:: Apple Silicon
    ARM Processor not supported read this article

you must install latex distribution(program).

## How to debug

```bash
# download package
git https://github.com/KMU-quantum-classrooom/qiksit-classroom.git

# install python packages
cd qiskit-classroom
pip install -r requirements.txt

# run scripts
python -m main.py
```

## Acknowledgement

* 국문 : "본 연구는 2022년 과학기술정보통신부 및 정보통신기획평가원의 SW중심대학사업의 연구결과로 수행되었음"(2022-0-00964)

* English : "This research was supported by the MIST(Ministry of Science, ICT), Korea, under the National Program for Excellence in SW), supervised by the IITP(Institute of Information & communications Technology Planning & Evaluation) in 2022"(2022-0-00964)

## License

Qiskit-Classroom is licensed under the Apache License, Version 2.0
"""

#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from qiskit_class_converter import (
    __FULL_VERSION__ as qiskit_classroom_converter_version,
)

QISKIT_CLASSROOM_CONVERTER_VERSION_STR = " ".join(
    [f"{key}: {value}" for key, value in qiskit_classroom_converter_version.items()]
)
