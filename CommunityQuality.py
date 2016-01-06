#!/usr/bin/python

import CommunityQuality
import argparse

import sys
import logging

import os

import shutil

def main():

    args = setUpArgs()
    logger = setUpLogging()

    if not args.communityDirectory:
        print 'missing required argument: community directory'
        sys.exit(-1)
    if args.chris:
        makeCommunity(args, logger)
    logger.info('makeCommunity complete. Beginning work on directory')
    results_directory = os.path.join(args.communityDirectory+'_results')
    if os.path.isdir(results_directory):
        shutil.rmtree(results_directory)
    os.makedirs(results_directory)
    CommunityQuality.runQualityExtractOnDirectory(args.communityDirectory, os.path.join(results_directory,'results.txt'))

    

def makeCommunity(args, logger):
    if os.path.isdir(args.communityDirectory):
        shutil.rmtree(args.communityDirectory)

    os.makedirs(args.communityDirectory)
    
    

    CommunityQuality.makeCommunity(args.chris, args.communityDirectory)

    

    
    

def setUpArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--chris', help='Chris style input file')
    parser.add_argument('-d','--communityDirectory', help='Community file directory')
    return parser.parse_args()


def setUpLogging():
    logger = logging.getLogger('simple_example')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('spam.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


    
if __name__ == '__main__':
    main()
