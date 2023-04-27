# KaiTracker fsrename.py
#
# SPDXVersion: SPDX-2.3
# SPDX-FileCopyrightText: Copyright 2023 Lisa St.John
# SPDX-License-Identifier: GPL-3.0+

import supervisor
import storage

storage.remount("/", readonly=False)
storage.getmount("/").label="KaiTracker"

storage.remount("/", readonly=True)
