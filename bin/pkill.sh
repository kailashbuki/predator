#!/usr/bin/sh

# force kills processes
function hard_kill(){ 
    for X in `ps acx | grep -i $1 | awk '{print $1}'`;
        do
            sudo kill -9 $X;
        done
}

# sends a TERM signal to the processes
function soft_kill(){ 
    for X in `ps acx | grep -i $1 | awk '{print $1}'`;
        do
            sudo kill -15 $X;
        done
}