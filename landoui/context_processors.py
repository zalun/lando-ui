# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from landoui.forms import UserSettingsForm


def user_settings_processor():
    form = UserSettingsForm()
    return dict(settings_form=form)
