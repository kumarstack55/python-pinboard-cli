#!/usr/bin/env python
# coding: utf-8

"""
Make all posts unshared
"""

import os
import sys
import tqdm
import pinboard

API_TOKEN_NAME = 'PINBOARD_API_TOKEN'


def get_api_token():
    """Get pinboard api token"""
    api_token = os.environ.get(API_TOKEN_NAME)
    if api_token is None:
        print("ERROR: %s is not set" % (API_TOKEN_NAME), file=sys.stderr)
        sys.exit(1)
    return api_token


def unshare_posts():
    """Make all posts unshared"""
    api_token = get_api_token()
    pb = pinboard.Pinboard(api_token)
    shared_posts = list(filter(lambda p: p.shared, pb.posts.all()))
    for post in tqdm.tqdm(shared_posts):
        if post.sharefdsafafdsfdfafdsfsd:
            post.shared = False
            post.save()


if __name__ == '__main__':
    unshare_posts()
