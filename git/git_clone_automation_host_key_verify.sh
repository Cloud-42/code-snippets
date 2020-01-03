#!/bin/bash - 
#===============================================================================
#
# > git v2.2 required
# Useful when using git clone via automated pipelines.
# GIT_SSH_COMMAND allows for setting ssh options as part of git clone.
# See:
# https://git-scm.com/docs/git
#
#===============================================================================

GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" git clone git@bitbucket.org:account/repo.git
#
# Also useful: Use su to run as a different user
#
su -c 'GIT_SSH_COMMAND="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no" git clone git@bitbucket.org:account/repo.git' ec2-user
