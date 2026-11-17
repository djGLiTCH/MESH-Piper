#!/usr/bin/env bash
# Prints the tag a release of this branch takes, from the Piper commit in .github/PIPER_COMMIT. Where Piper tagged
# that commit as a release of its own, the tag is Piper's. Where it is newer than Piper's last release, the tag is one
# patch step past the version Piper's setup.py gives, with -rc and the next number this repository has not used, as
# v1.8.1-rc1 follows 1.8.0. Run from the top of the branch, with this repository's tags fetched.
set -euo pipefail
piper="$(tr -d '[:space:]' < .github/PIPER_COMMIT)"
released="$(git ls-remote --tags https://github.com/OHF-Voice/piper1-gpl.git \
  | awk -v c="$piper" '$1 == c { print $2 }' \
  | sed -n 's#^refs/tags/\(v[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\)\(\^{}\)\{0,1\}$#\1#p' | head -1)"
if [ -n "$released" ]; then
  echo "$released"
  exit 0
fi
version="$(sed -n 's/.*version="\([0-9][0-9]*\)\.\([0-9][0-9]*\)\.\([0-9][0-9]*\).*/\1 \2 \3/p' setup.py | head -1)"
if [ -z "$version" ]; then echo "setup.py gives no version" >&2; exit 1; fi
read -r major minor patch <<< "$version"
next="v$major.$minor.$((patch + 1))"
used="$(git tag --list "$next-rc*" | sed -n "s/^$next-rc\([0-9][0-9]*\)$/\1/p" | sort -n | tail -1)"
echo "$next-rc$(( ${used:-0} + 1 ))"
