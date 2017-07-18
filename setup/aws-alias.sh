alias aws-get-p2='export instanceId=`aws ec2 describe-instances --filters "Name=instance-state-name,Values=stopped,Name=instance-type,Values=p2.xlarge" --query "Reservations[0].Instances[0].InstanceId"` && echo $instanceId'
alias aws-get-t2='export instanceId=`aws ec2 describe-instances --filters "Name=instance-state-name,Values=stopped,Name=instance-type,Values=t2.xlarge" --query "Reservations[0].Instances[0].InstanceId"` && echo $instanceId'
alias aws-start='aws ec2 start-instances --instance-ids $instanceId && aws ec2 wait instance-running --instance-ids $instanceId && export instanceIp=`aws ec2 describe-instances --filters "Name=instance-id,Values=$instanceId" --query "Reservations[0].Instances[0].PublicIpAddress"` && echo $instanceIp'
alias aws-ip='export instanceIp=`aws ec2 describe-instances --filters "Name=instance-id,Values=$instanceId" --query "Reservations[0].Instances[0].PublicIpAddress"` && echo $instanceIp'
alias aws-ssh='ssh -i ~/.ssh/aws-key-fast-ai.pem ubuntu@$instanceIp'
alias aws-stop='aws ec2 stop-instances --instance-ids $instanceId'
alias aws-state='aws ec2 describe-instances --instance-ids $instanceId --query "Reservations[0].Instances[0].State.Name"'

# Get the id, public ip, state and name of all instances
aws_get_all() {
  aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,PublicIpAddress,State.Name,Tags[?Key==`Name`].Value]'
}

# A more generic alias for retrieving the id, public ip, state and name of an instance by type (t2.micro, p2.xlarge, etc.)
aws_get_by_type() {
  aws ec2 describe-instances --filters "Name=instance-type,Values=$1" --query 'Reservations[*].Instances[*].[InstanceId,PublicIpAddress,State.Name,Tags[?Key==`Name`].Value]'
}

# A more generic alias for retrieving the id, public ip and state of an instance by tag with key=Name
aws_get_by_name() {
  aws ec2 describe-instances --filters "Name=tag:Name,Values=$1" --query 'Reservations[*].Instances[*].[InstanceId,PublicIpAddress,State.Name]'
}

# A more generic ssh alias that accepts an instance ip, an ssh username (.ie ec2-user, ubuntu) and an optional path
# to a certificate file (otherwise uses a default path)
aws_ssh() {
  ssh -i ${3:-~/.ssh/keys/aws/aws-key-fast-ai.pem} "$2"@"$1"
}

# A more generic start instance alias
aws_start() {
  aws ec2 start-instances --instance-ids "$1" && aws ec2 wait instance-running --instance-ids "$1" && echo "we're in business baby!"
}

# A more generic stop instance alias
aws_stop() {
  aws ec2 stop-instances --instance-ids "$1" && aws ec2 wait instance-stopped --instance-ids "$1" && echo "business is closed!"
}

if [[ `uname` == *"CYGWIN"* ]]
then
    # This is cygwin.  Use cygstart to open the notebook
    alias aws-nb='cygstart http://$instanceIp:8888'
fi

if [[ `uname` == *"Linux"* ]]
then
    # This is linux.  Use xdg-open to open the notebook
    alias aws-nb='xdg-open http://$instanceIp:8888'
fi

if [[ `uname` == *"Darwin"* ]]
then
    # This is Mac.  Use open to open the notebook
    alias aws-nb='open http://$instanceIp:8888'
fi
