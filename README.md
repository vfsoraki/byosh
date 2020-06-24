# Build Your Own Shecan

`Shecan` is an anti-sanction service offered by a group of researchers in Iran. It allows you to use a different DNS server and have a transparent proxy for the whitelisted domains.

Since Security and Privacy audits have no place in Iran, and `Shecan` obviously hasn't been through proper vetting, I decided to re-engineer something similar to it for personal use.

# Requirements

- Docker
- Docker compose

# Proxied Domains

- Included in `domains` file inside the repository. "borrowed" from [fod](https://github.com/freedomofdevelopers/fod)

# How to Use

- make sure ports 80, 443 and 53 are not used in your system (probably a good idea to disable `systemd-resolvd` service)
- run the command in your server (remember to replace YOUR_PUBLIC_IP with you public facing IP address)

`PUB_IP=<your-public-ip> docker-compose up`

# FAQ

## Why all these ports

Port 53 is used to recieve DNS and act as a DNS server. port 80 and 443 recieve HTTP traffic and handle the proxy side.

## Can I have my own list

Sure! do the following

- clone the repo
- edit the domains file and add/remove your domains
- run `docker-compose build`
- run `docker-compose up`

## Can I have this for ALL domains not just a list

run the following command (not tested):

`DNS_ALLOW_ALL=YES PUB_IP=<your-public-ip> docker-compose up`

NOTE: you still have to provide a list file, albiet an empty one. It'll get ignored once the service is started

## Limitation

This Project is at Alpha stage so expect weird behaviour! I've turned off `ipv6` everywhere so that's a known limitation. Other than that, the `dns.py` script is acting like a DNS server which is not a good practice for enterprise. Feel free to send PRs to make this better :)
