#!/bin/bash
set -eu

# create provider-networks
for net in 839:172.22.136 840:172.22.140; do
    neutron net-create provider-${net%%':'*} \
        --shared \
        --router:external True \
        --provider:physical_network vlan \
        --provider:network_type vlan \
        --provider:segmentation_id ${net%%':'*}
done

# Subnet create for our networks
for net in 839:172.22.136 840:172.22.140; do
    neutron subnet-create provider-${net%%':'*} ${net#*':'}.0/22 \
        --name subnet-provider-${net%%':'*} \
        --gateway ${net#*':'}.1 \
        --allocation-pool start=${net#*':'}.101,end=${net#*':'}.255 \
        --dns-nameservers list=true 8.8.4.4 8.8.8.8
done

# create environment network
for net in db_net:192.168.1 rabbit_net:192.168.2 backend_net:192.168.3; do
    neutron net-create ${net%%':'*}
done

# subnets for our environment networks
for net in db_net:192.168.1 rabbit_net:192.168.2 backend_net:192.168.3; do
    neutron subnet-create ${net%%':'*} ${net#*':'}.0/24 \
        --name subnet-${net%%':'*} \
        --allocation-pool start=${net#*':'}.101,end=${net#*':'}.254 \
        --dns-nameservers list=true 8.8.4.4 8.8.8.8
done

# create one security group for now and allow everything
openstack security group create folsom
# Allow ICMP
neutron security-group-rule-create --protocol icmp \
                                   --direction ingress \
                                   folsom

# Allow all TCP
neutron security-group-rule-create --protocol tcp \
                                   --port-range-min 1 \
                                   --port-range-max 65535 \
                                   --direction ingress \
                                   folsom
# Allow all UDP
neutron security-group-rule-create --protocol udp \
                                   --port-range-min 1 \
                                   --port-range-max 65535 \
                                   --direction ingress \
                                   folsom

# add a Ubuntu14.04 image
wget http://uec-images.ubuntu.com/releases/14.04/release/ubuntu-14.04-server-cloudimg-amd64-disk1.img
glance image-create --name 'Ubuntu 14.04 LTS' \
                    --container-format bare \
                    --disk-format qcow2 \
                    --visibility public \
                    --progress \
                    --file ubuntu-14.04-server-cloudimg-amd64-disk1.img
rm ubuntu-14.04-server-cloudimg-amd64-disk1.img

# create a nova flavor
nova flavor-create folsom.large 45  2048 80 4

# create a key pair
if [ ! -f "/opt/id_rsa" ];then
  ssh-keygen -t rsa -N '' -f /opt/id_rsa
fi
nova keypair-add --pub-key /opt/id_rsa.pub  env_pair

# create environment vms and containers and attach them to the right container
# create frontend vm
nova boot --flavor folsom.large --image 'Ubuntu 14.04 LTS' --security-groups folsom --nic net-name=provider-839 --nic net-name=db_net --nic net-name=rabbit_net --key-name env_pair front_end

# create Mysql VM
nova boot --flavor folsom.large --image 'Ubuntu 14.04 LTS' --security-groups folsom --nic net-name=db_net --nic net-name=backend_net --key-name env_pair sql_vm

# create Rabbit VM
nova boot --flavor folsom.large --image 'Ubuntu 14.04 LTS' --security-groups folsom --nic net-name=rabbit_net --nic net-name=backend_net --key-name env_pair rabbit_vm

# create Backend VM
nova boot --flavor folsom.large --image 'Ubuntu 14.04 LTS' --security-groups folsom --nic net-name=backend_net --key-name env_pair backend_vm
