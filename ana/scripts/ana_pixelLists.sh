#!/bin/bash
#============================
# ana_clusters.sh
#============================
#	date: 20170823 by Jianrong Deng
#	purpose:
#		bash script to run through pixelLists data to find #		clusters
#        usage: ./ana_clusters.sh $year
#           ex: ./ana_clusters.sh 201601 # will run through pixelLists data of January 2016
#============================

export env_year=$1
export env_path_out='/Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs'

# if it is a directory 
if [ -d "$env_path_out" ]
  then 
      echo "$env_path_out" directory exists
  else
      echo "ERROR: $env_path_out" directory does not exist
      exit
fi  


# loop through dates in $year
for i_date in $env_path_out/$env_year*
do
   # if it is a directory 
   if [ -d "$i_date" ]
      then
		# loop through stat files
		n_file=0
		for i_file in  $i_date/bias/*-stat.txt
		do
		    # if file exists
		    if [ -e "$i_file" ]
		       then
			  export env_filename_stat=$i_file
			  echo "env_filename_stat: ${env_filename_stat}"
			  # find clusters
		          python ana_pixelLists.py 
		    fi  
		    ((n_file +=1))
		done 
		echo "total number of files: $n_file for $i_date analysed"
   fi   
done
