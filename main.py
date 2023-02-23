import os
from pprint import pprint

from google_api import GoogleAdminSDKDirectoryAPI
from graph import Node
from utils import build_gcp_permission_graph


def main():
    data_path = os.path.join('data', 'gcp_permissions.json')

    graph = build_gcp_permission_graph(data_path)

    # Task 1
    print('task 1')
    print(graph)

    # Task 2
    print('task 2')
    ancestors = graph.get_resource_ancestors(
        Node(id='projects/p1111', type='resource'))
    pprint(ancestors)

    # Task 3
    print('task 3')
    resources_permissions = graph.get_resources_and_permissions_of_identity_node(
        Node(id='user:ron@test.authomize.com', type='identity'))
    pprint(resources_permissions)

    # Task 4
    print('task 4')
    identities_permissions = graph.get_identities_and_permissions_of_resource_node(
        Node(id='projects/p1111', type='resource'))
    pprint(identities_permissions)

    # Task 5 and 6
    print('task 5 and 6')
    api_client = GoogleAdminSDKDirectoryAPI(os.path.join('config', 'account_cred.json'))
    users = api_client.get_all_users()
    groups = api_client.get_all_groups()
    group_members = {}
    if not users:
        print('No users in the domain.')
    else:
        print('Users')
        for user in users:
            print(
                f'{user.get("primaryEmail","")} ({user.get("name",{}).get("fullName", "")})')

    if not groups:
        print('No Groups in the domain')
    else:
        print('\nGroups')
        for group in groups:
            print(f'{group.get("email","")} ({ group.get("name","")})')
            members = api_client.get_members_by_group(group.get('email', ''))
            group_members[group.get('email', '')] = members
            if members:
                for member in members:
                    print(f'{member.get("email", "")} {member.get("role", "")}')
            else:
                print(f'No members in the group {group.get("email", "")}')


if __name__ == '__main__':
    main()
