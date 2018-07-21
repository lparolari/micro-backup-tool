.. These are the Travis-CI and Coveralls badges for your repository. Replace
   your *github_repository* and uncomment these lines by removing the leading
   two dots.

.. image:: https://travis-ci.org/lparolari/micro-backup-tool.svg?branch=master
    :target: https://travis-ci.org/lparolari/micro-backup-tool

.. image:: https://coveralls.io/repos/github/lparolari/micro-backup-tool/badge.svg?branch=master
    :target: https://coveralls.io/github/lparolari/micro-backup-tool?branch=master


*Note:* this specs are a draft, might change.


=================
Micro Backup Tool
=================
Micro Backup Tool (shorted from here with *mbt*) is a **light-weighted**,
**cross-platform** and very **simple** program for backing-up files.

It is made with python to allows portability on different operative system,
and it's main goal is to make is work done without hand-waving.

The project is at very being, so for now the main implementation will be
rude and straight to the objective.



***************
Features
***************
- multiple dirctory trees backup
- common compressions
- logs keeping
- easy configuration and schedule
- files ignore with regular expression
- easy customization
- ready to go



***************
How it works
***************
*mbt* backup files and directories compressing it in a **.tar.gz** or
**.zip** file, setting the starting point equals to the launcher path.
If the directory option is specified *mbt* backups all the directories
listed in the option, excluding (if not explicitly specified) the
launcher path.


Fails
=================
Avoiding any type of failures is nearly impossible.

However, a good policy of error handling and process flow can help to
reduce the problems.

If something goes wrong the backup process **continues**, but the error
is written on logs (see logs section) and an "unbacked-up" files list is
stored (see unbacked-up list subsection).


Logs
===============
*mbt* writes many kinds of logs in order to:

- allow the user to handle and understand the whole situation, even if it is critical;
- allow the recovery module to try to makes some decisions automatically.

History logs
---------------
During the backup process logs are keeped and if something fails it
will be written on logs.

Error logs
---------------
If something goes wrong while backing up, the process continues but the
error log file will be written with error details.

Unbacked-up list
------------------
At the end of every backup a list containing "unbacked" up files is written,
and with the right option *mbt* automatically tries to backup again those
files (see options section). [TODO: define better this point]


Ignore
===============
*mbt* allows to specify in the ``.mbtignore`` files which directories must be
excluded from the backup.

Rules are similar to Git's .gitignore, but may differ slightly due to the different implementation.

- lines that start with # are comments
- leading and trailing spaces ignored unless escaped with \
- non-empty lines without ! in front are treated as "exclude" patterns
- non-empty lines with ! in front are treated as "include" patterns and have a priority over all "exclude" ones
- patterns are matched against the filenames relative to the grive root
- a/**/b matches any number of subpaths between a and b, including 0
- **/a matches a inside any directory
- b/** matches everything inside b, but not b itself
- * matches any number of any characters except /
- ? matches any character except /
- .griveignore itself isn't ignored by default, but you can include it in itself to ignore



***************
Guide
***************

Installation
===============
Install with `pip`

``pip install mbt``

Usage
===============
Define your own .mbtignore if needed to include or exclude certain files or
directories based on their names.

Coming soon...

Options
===============
*mbt* has options for every need.

Base:

-h, --help  prints help
--verbose   prints verbose output on console
--silent    does not print anything on console (useful with machine integration)

Backup:

-b, --backup_paths  allows to specify what are the paths to backup
-c, --archive_type  allows to specify the archive type between: *.tar.gz*, *.zip*

Logs:

-l, --logs_disabled    disables logs
-e, --errorlogs_disabled    disables error logs
-u, --unbacked_list_disabled    disable unbacked-up list



***************
Contributor(s)
***************

Luca Parolari   <luca.parolari23@gmail.com>
