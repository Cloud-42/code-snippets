#!/bin/bash
# ----------------
# Install required packages
# ----------------
RequiredPackages=(awscli lsof git wget ruby)
yum install -y "${RequiredPackages[@]}"


# ----------------
# FOR TERRAFORM:
# requires additional escape chracter
# ----------------
RequiredPackages=(awscli lsof git wget ruby)
yum install -y "$${RequiredPackages[@]}"
