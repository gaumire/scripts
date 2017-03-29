"""
Get EC2 instance details.

Displays details of stopped or running ec2 instances.
along with key_name, region and total EBS storage occupied
"""
import boto
import sys
import prettytable


def get_instance_details(state='stopped'):
    """
    Return instance details under a particular state.

    Details include key_name, volume, instance_type, state and region
    """
    valid_states = ['stopped', 'running']
    if state not in valid_states:
        raise Exception('{0} is not a valid state'.format(state))

    regions = boto.connect_ec2().get_all_regions()
    data = prettytable.PrettyTable(
        ["key_name", "instance", "volume", "instance_type", "state", "region"])
    total_ebs_storage = 0

    for region in regions:
        ec2 = boto.ec2.connect_to_region(region.name)
        reservations = ec2.get_all_instances()
        if len(reservations) > 0:
            for reservation in reservations:
                for inst in reservation.instances:
                    if inst.state == state:
                        bdm = inst.block_device_mapping.current_value
                        volumes = ec2.get_all_volumes(bdm.volume_id)
                        volume = [(vol.size, vol.type) for vol in volumes]
                        total_ebs_storage += int(vol.size)
                        data.add_row(
                            [inst.key_name,
                                inst.id,
                                volume,
                                inst.instance_type,
                                inst.state,
                                inst.region.name])
    return (data.get_string(sortby="key_name"), total_ebs_storage)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage {0} (stopped|running)".format(sys.argv[0])
        sys.exit(1)
    state = sys.argv[1]
    result = get_instance_details(state)
    print "Instance Details...."
    print result[0]
    print "\n"
    print "Total EBS Storage occupied = {0} GB".format(result[1])
