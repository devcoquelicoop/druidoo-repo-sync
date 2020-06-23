# druidoo-repo-sync
This repository is used to sync maintainer files to project repositories, using GitHub Actions

- All files in `common/` will be copied to all branches, and replace existing files.
- Branch-specific files may be added in its own folder (ie: `12.0/` files will be copied only to `12.0` branches)

It's triggered by Github Actions automatically after each push, so changes on this repository will be synchronized to the repositories and branches specified in `repositories.txt`.

# Known Issues / Roadmap

- Do an actual synchronization, also removing files. Currently this script will only copy the new files, replacing them if they exist. But there's no way to synchronize the removal of a file.
