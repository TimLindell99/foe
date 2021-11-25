#!/usr/bin/env python
# Program name: snurk.py
# Version: 1.1
# Purpose: Processes FOE guild statistics and creates CSV output
#          that that be used to generate reports.

import sys
import argparse
from collections import defaultdict


def parse_args():
    """
       Parse the arguments passed to the program
    """
    parser = argparse.ArgumentParser(description='Snurk Statistics Tool')

    parser.add_argument('--guildmember', help="Print goods contributions for a single guild member",
                        nargs=1, default="")
    parser.add_argument('--allguildmembers', help="Print goods contributions for all guild members",
                        action="store_true", default=True)
    parser.add_argument('--file', help="The file containing the raw data",
                         nargs=1, required=True)
    args = parser.parse_args()

    return  args.guildmember, args.allguildmembers, args.file[0]


def process_player_data(file):
    """
       Parse player data and normalize it into a collection for future use.
    """
    players = defaultdict(lambda: defaultdict(int))

    try:
        with open(file, 'r') as treasury_data:
            for entry in treasury_data:
                list = entry.split(",")
                player_name = list[1].lower()
                good_type = list[3]

                if "GE" in entry:
                    pass
                elif "GvG" in entry:
                    pass
                elif "GBG" in entry:
                    pass
                elif "Bldg" in entry or "Donate" in entry:
                    players[player_name][good_type] += int(list[4])
                elif "Good" in entry:
                    pass
                else:
                    print("Found unknown player data in input file.")
                    print("Line that couldn't be parsed: " + entry)
    except IOError:
         print("Could not open file " + file + " for processing")
         sys.exit(1)

    return(players)


def print_goods_by_player(player_collection, guild_member):
    """
       Print goods data for one player
    """
    header = guild_member
    goods  = guild_member

    for good in player_collection[guild_member]:
        header += "," + good
        goods  += "," + str(player_collection[guild_member][good])

    print(header)
    print(goods)


def print_goods_for_all_players(player_collection):
    """
       Print goods donations for all players in the guild
    """
    goods_set = set()

    # Dynamically generate the list of goods in the heading. This
    # will allow the program to continue working when new ages
    # are added in the future.
    for player in player_collection:
        for good in player_collection[player]:
            goods_set.add(good)

    print("Player Name," + ",".join(goods_set))

    for player in player_collection: 
        csv_entry = player
        for good in goods_set:
            if good in player_collection[player]:
                csv_entry += "," + str(player_collection[player][good])
            else:
                csv_entry += ",0"
        print(csv_entry)


def main():
    """
       Main program logic
    """
    gm, agm, file = parse_args()
    player_data = process_player_data(file)

    if gm:
        print_goods_by_player(player_data, gm[0])
    elif agm:
        print_goods_for_all_players(player_data)


if __name__ == "__main__":
    main()
