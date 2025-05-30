tar -cvzf C:\Users\xxx\Documents\per-diem.tar.gz -C C:\Users\xxx\Documents\per-diem .
scp C:\Users\natsumi.kosaka\Documents\per-diem.tar.gz root@xxx:~/
ssh root@xxx "set -e; mkdir ~/per-diem; tar -xzvf per-diem.tar.gz -C ~/per-diem; /usr/bin/env sh per-diem/utils/install.sh"