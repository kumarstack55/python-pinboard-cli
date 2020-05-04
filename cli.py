#!/usr/bin/env python
# coding: utf-8

import argparse
import datetime
import json
import os
import pinboard
import sys
import tqdm

API_TOKEN_NAME = 'PINBOARD_API_TOKEN'


def get_api_token():
    """Get pinboard api token"""
    api_token = os.environ.get(API_TOKEN_NAME)
    if api_token is None:
        print("ERROR: %s is not set" % (API_TOKEN_NAME), file=sys.stderr)
        sys.exit(1)
    return api_token


def get_post_dict(post):
    d = dict()
    d.setdefault('description', post.description)
    d.setdefault('extended', post.extended)
    d.setdefault('hash', post.hash)
    d.setdefault('meta', post.meta)
    d.setdefault('shared', post.shared)
    d.setdefault('tags', post.tags)
    d.setdefault('time', post.time)
    d.setdefault('toread', post.toread)
    d.setdefault('url', post.url)
    return d


def get_post_json(post):
    d = get_post_dict(post)
    d.update(time=post.time.strftime("%F %H:%M:%S"))
    return json.dumps(d, indent=2, ensure_ascii=False)


def list_all_posts():
    """List all posts"""
    api_token = get_api_token()
    pb = pinboard.Pinboard(api_token)
    for post in pb.posts.all():
        print(get_post_json(post))


def unshare_all_posts(dry_run=True):
    """Make all posts unshared"""
    api_token = get_api_token()
    pb = pinboard.Pinboard(api_token)
    shared_posts = list(filter(lambda p: p.shared, pb.posts.all()))
    for post in tqdm.tqdm(shared_posts):
        if post.share:
            post.shared = False
            if not dry_run:
                post.save()


def handler_posts_list(args):
    list_all_posts()


def handler_posts_unshare_all(args):
    unshare_all_posts(dry_run=args.dry_run)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--dry-run', action='store_true', default=True)
    group.add_argument('--force', dest='dry_run', action='store_false')
    parser.add_argument('--verbose', '-v', action='count', default=0)

    subparsers = parser.add_subparsers()

    parser_posts_list = subparsers.add_parser('posts_list')
    parser_posts_list.set_defaults(handler=handler_posts_list)

    parser_posts_unshare_all = subparsers.add_parser('posts_unshare_all')
    parser_posts_unshare_all .set_defaults(handler=handler_posts_unshare_all)

    args = parser.parse_args()

    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
