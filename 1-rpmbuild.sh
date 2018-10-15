#!/bin/bash

cd $(dirname $0)

package=$(basename $PWD)
echo ${package}

rpmdev-setuptree >&2

version=${version:-1.0}.${build:-0}

git_commit_count=$(git rev-list HEAD | wc -l | awk '{print $1}')
short_commit=$(git log --no-color --max-count=1 --oneline | awk '{print $1}')
release="${git_commit_count}_${short_commit}"

echo "$version-$release" >&2
rpmbuild --define="%debug_package %{nil}" --define="%_builddir $PWD" --define="%version ${version}" --define="%release ${release}" -bb ${package}.spec >&2 || exit 1
ls -1 $HOME/rpmbuild/RPMS/x86_64/${package}-$version-$release.x86_64.rpm >&2 &&
echo ${package}-$version-$release.x86_64.rpm
