#!/usr/bin/env python
import os
import sys

sys.path.append(os.path.abspath('wagtail_i18n_poc'))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
