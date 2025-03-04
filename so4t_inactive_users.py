'''
This Python script is a working proof of concept example of using Stack Overflow APIs for inactive user report. 
If you run into difficulties, please leave feedback in the Github Issues.
'''

# Standard Python libraries
import argparse
import csv
import time

# Local libraries
from so4t_api_v2 import V2Client


def main():

    # Get command-line arguments
    args = get_args()
    if args.days: # Number of days of inactivity to consider a user inactive
        inactive_days = args.days
    else:
        inactive_days = 180 # Default to 180 days

    # Create a client object
    client = V2Client(args.url, key=args.key, token=args.token)

    # Get user data
    users = get_user_data(client)

    # Create user lists
    current_unix_time = int(time.time())
    inactive_threshold = current_unix_time - (inactive_days * 86400)

    all_inactive_users = []
    inactive_users_without_contributions = []
    inactive_users_with_contributions = []
    for user in users:
        if user['last_access_date'] < inactive_threshold:
            user['inactive_days'] = round((current_unix_time - user['last_access_date']) / 86400)
            all_inactive_users.append(user)
            if not (user['answer_count'] > 0 or user['question_count'] > 0 or user['article_count'] > 0 
                or user['comment_count'] > 0):
                inactive_users_without_contributions.append(user)
            else:
                inactive_users_with_contributions.append(user)

    # Write user data to CSV
    write_user_data(f'all_users_inactive_for_{inactive_days}_days.csv', all_inactive_users)
    write_user_data(f'noncontributing_users_inactive_for_{inactive_days}_days.csv', 
        inactive_users_without_contributions)
    write_user_data(f'contributing_users_inactive_for_{inactive_days}_days.csv',
        inactive_users_with_contributions)


def get_args():

    parser = argparse.ArgumentParser(
        prog='so4t_inactive_users.py',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Uses the Stack Overflow for Teams API to create \
        a user report.',
        epilog = 'Example for Stack Overflow Business: \n'
                'python3 so4t_inactive_users.py --url "https://stackoverflowteams.com/c/TEAM-NAME" '
                '--token "YOUR_TOKEN" \n\n'
                'Example for Stack Overflow Enterprise: \n'
                'python3 so4t_inactive_users.py --url "https://SUBDOMAIN.stackenterprise.co" '
                '--key "YOUR_KEY"\n\n')
    
    parser.add_argument('--url', 
                        type=str,
                        help='Base URL for your Stack Overflow for Teams instance. ')
    parser.add_argument('--token',
                        type=str,
                        help='API token for your Stack Overflow for Teams instance. ')
    parser.add_argument('--key',
                    type=str,
                    help='API key value. Required if using Stack Overflow Enterprise')
    parser.add_argument('--days',
                        type=int,
                        help='Only report on users that have been inactive by at least this many '
                        'days. Default is 180 days.')

    return parser.parse_args()



def get_user_data(client):

    if client.soe: # Stack Overflow Enterprise
        filter_attributes = [
            'user.answer_count',
            'user.down_vote_count',
            'user.is_deactivated',
            'user.question_count',
            'user.up_vote_count',
            'user.verified_email'
        ]
        filter_string = client.create_filter(filter_attributes)
    else: # Stack Overflow Business
        filter_string = '!6WPIommaBqvw3'

    users = client.get_all_users(filter_string)

    # Filter out users with a user_id less than `1`
    users = [user for user in users if user['user_id'] > 0]

    # Add additional user fields
    for user in users:
        user['article_count'] = 0
        user['comment_count'] = 0

    # Get additional user data from comments and articles
    # Question count and answer count are already included in the user data
    articles = client.get_all_articles()
    comments = client.get_all_comments()

    for article in articles:
        try:
            article_owner_id = article['owner']['user_id']
        except KeyError: # Article was made by a deleted user
            continue
        for user in users:
            if user['user_id'] == article_owner_id:
                user['article_count'] += 1
    
    for comment in comments:
        try:
            comment_owner_id = comment['owner']['user_id']
        except KeyError: # Comment was made by a deleted user
            continue
        for user in users:
            if user['user_id'] == comment_owner_id:
                user['comment_count'] += 1

    return users


def write_user_data(file_name, users):

    with open(file_name, 'w', newline='') as csv_file:
        field_names = [
            'user_id',
            'account_id',
            'verified_email',
            'display_name',
            'inactive_days',
            'is_deactivated',
            'reputation',
            'answer_count',
            'question_count',
            'article_count',
            'comment_count',
            'down_vote_count',
            'up_vote_count'
        ]
        writer = csv.DictWriter(csv_file, fieldnames=field_names, extrasaction='ignore')
        writer.writeheader()
        for user in users:
            writer.writerow(user)

        print(f"User data written to {file_name}")


if __name__ == '__main__':

    main()
