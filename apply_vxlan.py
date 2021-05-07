#!/usr/bin/env python

import json
import subprocess
import sys

try:
    peer_file_path = sys.argv[1]
except IndexError:
    print('peer file must be passed as firs argument', file=sys.stderr)
    sys.exit(1)

try:
    with open(peer_file_path, 'r') as peer_file:
        contents = peer_file.read()
except FileNotFoundError as e:
    print(e, file=sys.stderr)
    sys.exit(2)

try:
    peers = json.loads(contents)
    assert isinstance(peers, list)
except Exception as e:
    print(f'Error while parsing JSON file: {e}', file=sys.stderr)
    sys.exit(3)


remote_peers = {}

for peer in peers:
    remote_peers[f'vxlan-vxlan{peer["vni"]}'] = peer


class Nmcli:
    @classmethod
    def _exec_command(cls, command):
        process = subprocess.Popen(
            command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        if stderr:
            raise ValueError(stderr)
        return stdout.decode('utf8').strip()

    @classmethod
    def list_connections(cls, type=None):
        output = cls._exec_command('nmcli connection show')
        lines = output.split('\n')
        connections = []
        for line in lines[1:]:
            parts = line.split()
            connection = {
                'name': parts[0].strip(),
                'uuid': parts[1].strip(),
                'type': parts[2].strip(),
                'device': parts[3].strip(),
            }
            if not type or type and type == connection['type']:
                connections.append(connection)
        return connections

    @classmethod
    def get_connection(cls, connection):
        output = cls._exec_command(f'nmcli connection show {connection}')
        data = {}
        lines = output.split('\n')
        for line in lines:
            parts = line.split()
            data[parts[0][:-1]] = parts[1]
        return data

    @classmethod
    def get_local_vxlan_peers(cls):
        peers = {}
        vxlan_connections = cls.list_connections(type='vxlan')
        for vxlan in vxlan_connections:
            data = cls.get_connection(vxlan['uuid'])
            peers[data['connection.id']] = {
                'remote': data['vxlan.remote'],
                'vni': int(data['vxlan.id']),
            }
        return peers

    @classmethod
    def add_connection(cls, ifname, vni, remote):
        return cls._exec_command(
            f'nmcli connection add type vxlan ifname {ifname} '
            f'id {vni} remote {remote} destination-port 4789 '
            'ipv4.method link-local ipv6.method link-local'
        )

    @classmethod
    def edit_connection(cls, connection, vni, remote):
        return cls._exec_command(
            f'nmcli connection modify {connection} vxlan.id {vni} vxlan.remote {remote}'
        )

    @classmethod
    def delete_connection(cls, connection):
        return cls._exec_command(f'nmcli connection delete {connection}')


local_peers = Nmcli.get_local_vxlan_peers()


for connection_name, peer_data in local_peers.items():
    if connection_name not in remote_peers:
        Nmcli.delete_connection(connection_name)
        print(f'Removed {connection_name}')


for connection_name, peer_data in remote_peers.items():
    vni = peer_data['vni']
    remote = peer_data['remote']
    if connection_name not in local_peers:
        Nmcli.add_connection(f'vxlan{vni}', vni, remote)
        print(f'Added {connection_name}')
        continue
    elif peer_data == local_peers[connection_name]:
        print(f'Skipping {connection_name}, already up to date')
        continue
    else:
        Nmcli.edit_connection(connection_name, vni, remote)
        print(f'Updated {connection_name}')
