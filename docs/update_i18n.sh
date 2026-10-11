#!/bin/sh

cd "$(dirname "$0")" || exit 1

make gettext
echo "Currently support zh_CN only."
sphinx-intl update -p build/gettext -l zh_CN
