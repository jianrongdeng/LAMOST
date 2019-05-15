#!/bin/bash
#============================
# ana_cluster.sh
#============================
#   date: 20190408 by Jianrong Deng
#   copy from ana_pixelLists.sh 
#   purpose:
#   	bash script to run through clusterLists data, analyze cluster and save muon candidates
#   usage: ./ana_cluster.sh $run_flag $date $env_path_out [$verbose_level]
#       Note:
#          1. $date: acceptable format: 2016, 201612, 20161201
#          2. input data directory = output data directory = $env_path_out
#          3. run_flag: 
#                 0 (test run, see ex1, only checking the flow of script loops)
#                 1 (test data run, see ex2, ex3, only checking the first five (out of 32) dets)  
#                 2 (data run, see ex3)  
#
#       example1: 
#                ./ana_cluster.sh 0 2016  /home/jdeng/LAMOST/ana/outputs/run1_20171205
#                ./ana_cluster.sh 0 2016  /Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs/run1_20171205
#           note:
#                test run without running the python analysis code, just checking the script loops
#              test run: 		             
#                       run_flag = 0
#                       year = 2016 (loop through data of year 2016)
#			env_path_out=/home/jdeng/LAMOST/ana/outputs/run1_20171205
#            
#   example2: 
#               nohup ./ana_cluster.sh 1 201601 /home/jdeng/LAMOST/ana/outputs/run1_20171205 > ../../log/ana_cluster/run1_20171205/test_201601.txt
#          note: 
#            short test run on data: run through the first 5 detectors in each date
#                       run_flag = 1
#                       year = 201601 (loop through data of January 2016)
#
#   example3: 
#               nohup ./ana_cluster.sh 1 20160601 /home/jdeng/LAMOST/ana/outputs/run1_20171205 > ../../log/ana_cluster/run1_20171205/test_20160601.txt 1
#               nohup ./ana_cluster.sh 1 20160601 /Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs/run1_20171205 > ../../log/ana_cluster/run1_20171205/test_20160601.txt 1
#          note: 
#            data run: 		             
#                       run_flag = 1
#                       verbose_level = 1
#
#   example4: 
#               nohup ./ana_cluster.sh 2 201601 /home/jdeng/LAMOST/ana/outputs/run1_20171205 > ../../log/ana_cluster/run1_20171205/test_201601.txt
#               nohup ./ana_cluster.sh 2 201601 /Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs/run1_20171205 > ../../log/ana_cluster/run1_20171205/test_201601.txt
#          note: 
#            data run: run through the full data
#                       run_flag = 2
#                       year = 201601 (loop through data of January 2016)
#			env_path_out=/home/jdeng/LAMOST/ana/outputs/run1_20171205
#                     
#============================

#               NOTE: 
#               $0: returns bash command executed
#               $1, $i, $n: returns the ith argument
#               $#: returns the total number of input arguments to the bash script
#               $@: returns the list of input arguments to the bash script
if test $# -eq 0
    then
        echo "Usage: $0 $run_flag $date $path_out [$verbose]" 1>&2 #  note: "1>&2": redirect its output to standard error
	echo " Note: examples of acceptable formats for 'date': 2016, 201601, 20160101, 2016010[1-5]"
	echo " Note1: run_flag (0, 1, 2)"
        echo "   0 (test run, see ex1, only checking the flow of script loops) "
        echo "   1 (test data run, see ex2, ex3, only checking the first five (out of 32) dets)  "
        echo "   2 (data run, see ex4)  "
fi    

# reprint the shell script command executed
echo $0 $@


run_flag=$1
export env_year=$2
#export env_path_out='/home/jdeng/LAMOST/ana/outputs'
export env_path_out=$3
# reading the optional arguments if any
if [ $# -le 3 ]
    then
       verbose=0
    else
       verbose=$4
fi    


# if it is a directory 
if [ -d "$env_path_out" ]
  then 
      echo Data Directory = "$env_path_out" 
  else
      echo "ERROR: $env_path_out" directory does not exist
      exit
fi  

# check total number of days analyzed and to be analyzed
total_days=0
total_days_dets=0
total_days_analyzed=0
total_days_dets_analyzed=0
total_dets=32

# loop through dates in $year
for i_date in $env_path_out/$env_year*
do

   if [ $verbose == 1 ]
      then 
         echo "date = $i_date"
   fi	 #if [ $verbose == 1 ]

   # if it is a directory 
   if [ -d "$i_date/bias" ]
      then

	if [ $verbose == 1 ]
	  then 
	     echo "bias directory of  $i_date exists"
	fi	 #if [ $verbose == 1 ]

	# if there are bias data, check data
	# echo "checking the clusters data on :" $i_date
	# loop through clusters files of 32 CCD dets
	n_file=0 # counting the number of clusters files
	for i_file in  $i_date/bias/*-stat.dat
	do
	    # if file exists
	    if [ -e "$i_file" ]
	       then
	          ((n_file +=1))
		  ((total_days_dets +=1))
		  export env_filename_stat=$i_file
		  if [ $verbose == 1 ]
		      then 
		         echo "env_filename_stat: ${env_filename_clusters}"
		  fi	 
		  # check the run flag, if run_flag>=1, run the python analysis process
		  if [ $run_flag -ge 1 ]
		     then
		        # -u     Force the binary I/O layers of stdout and stderr to be unbuffered.  
			# stdin is always  buffered.  The text I/O layer will still be line-buffered.
		        # find clusters
		        python3 -u ana_cluster.py 
                        ((total_days_dets_analyzed +=1))
		        if [ ${run_flag} -eq 1 ]
		           then
		           if [ ${n_file} -ge 5 ]
		              then
			          # in debug mode, go to next day after checking data of 5 dets  of the current day
		                  break
		           fi  #if [ ${n_file} -ge 5 ]
		        fi	  #if [ ${run_flag} -eq 1 ]
		  fi  #if [ $run_flag -ge 1 ]
	    fi  # if [ -e "$i_file" ]
	done #for i_file in  $i_date/bias/*-stat.dat
	echo "total number of clusters files = $n_file in $i_date"
   fi   # if it is a directory 
done # loop through dates in $year
# print out days analyzed.
let total_days=${total_days_dets}/${total_dets}
let total_days_analyzed=${total_days_dets_analyzed}/${total_dets}
echo "total_days * total_number_of_dets = " ${total_days_dets}
echo "total number of days with data = "  ${total_days} "for " $env_year 
echo "total_days_analyzed * total_number_of_dets = " ${total_days_dets_analyzed}
echo "total number of days analyzed = "  ${total_days_analyzed} "for " $env_year 
