#!/usr/bin/env python

import os
import subprocess
import shutil
import logging
_logger = logging.getLogger()


def parse_repositories_file(file):
    '''
    Parses the repositories.txt file contents
    and builds an array of tuples:
    [(repo_name, branches)]
    '''
    res = []
    for line in file:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        repo, branches = line.split()
        branches = branches.split(',')
        res.append((repo, branches))
    return res


def clone_repository(repository, branch, dest='~'):
    '''
    Clones a repository and returns the path
    '''
    dest = os.path.join(
        dest, '%s-%s' % (repository, branch))
    subprocess.check_call([
        'git', 'clone', '--depth', '1', '--branch', branch,
        'https://%s:%s@github.com/%s.git' % (
            os.environ.get('BOT_GITHUB_USER'),
            os.environ.get('BOT_GITHUB_TOKEN'),
            repository,
        ),
        dest,
    ])
    return dest


def commit_if_needed(paths, message, add=True):
    if add:
        cmd = ['git', 'add'] + paths
        subprocess.check_call(cmd)
    cmd = ['git', 'diff', '--quiet', '--exit-code', '--cached', '--'] + paths
    r = subprocess.call(cmd)
    if r != 0:
        cmd = ['git', 'commit', '-m', message, '--'] + paths
        subprocess.check_call(cmd)
        return True
    else:
        return False


def sync_repository(repository, branch):
    cwd = os.getcwd()
    local_clone_path = clone_repository(repository, branch)
    # copy common files
    subprocess.check_call([
        'cp', '-ra', 'common/.', local_clone_path])
    # copy branch-specific files
    if os.path.isdir(branch):
        subprocess.check_call([
            'cp', '-ra', '%s/.' % branch, local_clone_path])
    # commit and push
    os.chdir(local_clone_path)
    if commit_if_needed(['.'], '[UPD] Github Workflows'):
        subprocess.check_call(['git', 'push'])
    os.chdir(cwd)
    # cleanup
    shutil.rmtree(local_clone_path)


if __name__ == '__main__':
    if os.path.isfile('repositories.txt'):
        with open('repositories.txt') as file:
            repositories = parse_repositories_file(file)
        for repository, branches in repositories:
            for branch in branches:
                _logger.info('Synchronizing %s:%s' % (repository, branch))
                sync_repository(repository, branch)
