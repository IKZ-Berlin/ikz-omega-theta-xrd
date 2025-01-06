#!/bin/sh

if ! command -v rsync >/dev/null 2>&1; then
  echo "rsync required, but not installed!"
  exit 1
else
  rsync -avh ikz_omega_theta_xrd/ .
  rm -rfv ikz_omega_theta_xrd
fi
