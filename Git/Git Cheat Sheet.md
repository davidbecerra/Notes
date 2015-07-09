# Git Cheat Sheet

+ `git init`
    * Creates new repo

---

+ `git status`
    * view repo status; includes current branch and any commits need and untracked files.

---

+ `git add <filename>`
    * Adds new file to be tracked by git repo
    * `git add '*.txt:`: adds all .txt files. Wildcard option
    * `git add -A`: adds all files in current directory except those in `.gitignore`

---

+ `git commit <flags>`
    * Stores changes to repo
    * `git commit -m 'Write commit message here'`: -m flag adds command line message to commit.
    * `git commit -a -m 'Write commit message here'`:
    * `git commit -am 'Write commit message here'`: commits all modifications to existing files. Do this instead of `git add -A` `git commit -m`. However, if new files created, still need to do `git add -A`

---

+ `git log`
    * prints a log of all the changes committed so far.

---

+ `git remote add <remote name> <remote URL>`
    * Adds a remote repository. Allows us to push our local repo. Typical to name main remote origin.

---

+ `git push <flags> <remote repo name> <local branch name>`
    * Pushes local changes to remote repo. Default local branch name is master.

---

+ `git pull <remote repo name> <local branch name>`
    * Pulls changes from remote repo to local repo.

---

+ `git diff`
    * Shows differences between commits
    * `git diff HEAD` : HEAD is a pointer to most recent commit. Quick way to see diffs last commit.
    * `git diff --staged` : see differences of files you just staged files.
    * __Staged Files__ : files we have told git that are ready to be committed.

---

+ `git reset <file name>`
    * Unstages a staged file

---

+ `git checkout -- <target>`
    * Changes file back to how they were last commit
    * `git checkout <branch>` : switches to a particular local branch
    * `git checkout -b <branch>` : create and checkout a branch at the same time. Same as doing `git branch <branch>` then `git checkout <branch>`.

---

+ __branch__ : a copy of the code with separate commits. Good habit to create new branches when working on different project features. Then merge to master branch once feature fully implemented.

---

+ `git branch`
    * Shows all the local branches
    * `git branch <branch name>` : creates a new branch with name _<branch name\>_
    * `git branch -d <branch>` : deletes the given branch assuming branch has been merged.
    * `git branch -d --force` OR `git branch -D` OR `git branch -d --force` : deletes branch even if not merged.

---

+ `git rm '*.txt'` : remove all txts from repo as well as stages the removal of the files
    * `git rm -r <directory>` : recursively removes all folders and riles from a given directory.

---

+ `git merge <branch>` : merge the given branch with current branch.

---

+ `git push` : push changes to remote repo
    * `git push -u <origin_repo> <branch_name>`: use `-u` flag to denote upstream connection (? not entirely certain).

