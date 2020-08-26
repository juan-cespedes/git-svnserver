* Basic usage
** cd /repo/to/export.git
** $git_svnserver/git_side_scripts/init_db
   + This will create "svnserver/db", a SQLite3 database with table "transactions"
** $git_svnserver/git_side_scripts/build_map
   + This will populate table "transactions" in "svnserver/db" with all the commits
** Add '$git_svnserver/git_side_scripts/noddy-post-receive "$@"' to "hooks/post-receive"
   + This will update "svnserver/db" with every update to Git repo
** Execute "./git-svnserver -c config.example"
