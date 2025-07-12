Deal with '?' in

family_spec = family_spec_excplicit?
family_spec_explicit = IP close_scope_ip | IP6 close_scope_ip6 | INET | ARP close_scope_arp | BRIDGE | NETDEV

table_spec = family_spec identifier
chain_spec = table_spec identifier
