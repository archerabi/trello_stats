from trello import TrelloClient
from time import sleep
import os
import argparse
from parse import print_stats

if 'TRELLO_API_KEY' not in os.environ or 'TRELLO_API_SECRET' not in os.environ:
    raise Exception('TRELLO_API_KEY and TRELLO_API_SECRET are required')

parser = argparse.ArgumentParser(description='Get stats for your trello boards')
parser.add_argument('-boards', required=True,help='list of comma separated boards to get stats for')
parser.add_argument('-label' , help='label to filter cards by')
parser.add_argument('-days' , help='number of days to lookback')


args = parser.parse_args()

boards = args.boards.split(',')

client = TrelloClient(
    api_key=os.environ['TRELLO_API_KEY'],
    api_secret=os.environ['TRELLO_API_SECRET']
)

trello_boards = client.list_boards()
trello_board_names = [b.name for b in trello_boards]
for b in boards:
    if b not in trello_board_names:
        raise Exception('{} not a valid board'.format(b))

trello_boards = [b for b in trello_boards if b.name in boards]

card_filter = "created:120" if not args.days else args.days
if args.label:
    card_filter = "{} label:{}".format(card_filter, args.label)

def fetch_cards_in_board(board):
    cards = client.search(query=card_filter, board_ids=[board.id],cards_limit=1000)

    filename = "{}.csv".format(board.name)

    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'a') as the_file:
        the_file.write('labels;id;created_at\n')
        for card in cards:
            labels = [label.name for label in card.labels]
            actions=card.fetch_actions()
            the_file.write("{};{};{}\n".format(labels, card.id, actions[0].get('date')))
            sleep(0.05)
    print_stats(filename, board.name)

for board in trello_boards:
    fetch_cards_in_board(board)
