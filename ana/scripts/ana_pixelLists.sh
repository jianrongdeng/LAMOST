#!/bin/bash
#============================
# ana_pixelLists.sh
#============================
#   date: 20170823 by Jianrong Deng
#   purpose:
#   	bash script to run through pixelLists data to find clusters
#   usage: ./ana_pixelLists.sh $run_flag $year $env_path_out
#             (input data directory = output data directory = $env_path_out)
#
#       ex0: ./ana_pixelLists.sh 201601 1 # will run through pixelLists data of January 2016
#       example1: 
#                ./ana_pixelLists.sh 0 2016  /home/jdeng/LAMOST/ana/outputs/run1_20171205
#           note:
#                test run without running the python analysis code, just checking the script loops
#              test run: 		             
#                       run_flag = 0
#                       year = 2016 (loop through data of year 2016)
#			env_path_out=/home/jdeng/LAMOST/ana/outputs/run1_20171205
#            
#   example2: 
#               nohup ./ana_pixelLists.sh 1 201601 /home/jdeng/LAMOST/ana/outputs/run1_20171205 > ../log/ana_pixelLists/run1_20171205/test_201601.txt
#          note: 
#            short test run: 		             
#                       run_flag = 0
#                       year = 201601 (loop through data of January 2016)
#			env_path_out=/home/jdeng/LAMOST/ana/outputs/run1_20171205
#                     
#============================

run_flag=$1
export env_year=$2
#export env_path_out='/home/jdeng/LAMOST/ana/outputs'
export env_path_out=$3


# if it is a directory 
if [ -d "$env_path_out" ]
  then 
      echo Data Directory = "$env_path_out" 
  else
      echo "ERROR: $env_path_out" directory does not exist
      exit
fi  

total_days_analysized=0

# loop through dates in $year
for i_date in $env_path_out/$env_year*
do
   # if it is a directory 
   if [ -d "$i_date" ]
      then
		# loop through stat files
		n_file=0
		for i_file in  $i_date/bias/*-stat.dat
		do
		    # if file exists
		    if [ -e "$i_file" ]
		       then
			  export env_filename_stat=$i_file
			  echo "env_filename_stat: ${env_filename_stat}"
			  # find clusters
			  # check the run flag, if run_flag=1, run the python analysis process
			  if [ $run_flag == 1 ]
			     then
			        python3 -u ana_pixelLists.py 
			  fi  
		    fi  
		    ((n_file +=1))
		done 
		echo "total number of files: $n_file for $i_date analysed"
                ((total_days_analysized +=1))
		if [ ${run_flag} -eq 1 ]
		   then
		   if [ ${total_days_analysized} -ge 5 ]
		      then
		          break
		   fi  # if [ ${total_days_analysized} -gt 5 ]
		fi	  #if [ ${run_flag} -eq 1 ]
   fi   # if it is a directory 
done # loop through dates in $year
echo "total number of days analyzed = "  ${total_days_analysized} "for year " $env_year 
