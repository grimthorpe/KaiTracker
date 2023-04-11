# KaiTracker boot.py
#
# SPDXVersion: SPDX-2.3
# SPDX-FileCopyrightText: Copyright 2023 Lisa St.John
# SPDX-License-Identifier: GPL-3.0+

import storage

# If we're connected to a computer then we want the USB drive to be read-only
# from our point of view.
storage.remount("/", True)

