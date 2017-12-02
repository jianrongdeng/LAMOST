#!/bin/bash
#============================
# ana_image.sh
#============================
#	date: 20170813 by Jianrong Deng
#	purpose:
#		bash script to run through raw bias data
#        usage: ./ana_image.sh $year $run_flag
#        example1: 
#                    ./ana_image.sh 2016 0
#               note:
#                    test run without running the python analysis code, just checking the script loops
#                     test run: 		             run_flag = 0
#                   
#        example2: 
#                    nohup ./ana_image.sh 2016 1 > ../log/run0_2017/2016.txt
#               note: 
#                    data analysis run :                     run_flag = 1
#============================

env_rawdata_year=$1; export env_rawdata_year
run_flag=$2
echo "env_rawdata_year = " $env_rawdata_year
echo "run_flag = " $run_flag

# 32 CCD dets
dets=(
rb-01r rb-01b 
rb-02r rb-02b 
rb-03r rb-03b
rb-04r rb-04b
rb-05r rb-05b
rb-06r rb-06b
rb-07r rb-07b
rb-08r rb-08b
rb-09r rb-09b
rb-10r rb-10b
rb-11r rb-11b 
rb-12r rb-12b 
rb-13r rb-13b
rb-14r rb-14b
rb-15r rb-15b
rb-16r rb-16b); export dets

export env_rawdata_path='/Users/jdeng/baiduCloudDisk/LAMOST/data'
export env_path_out='/Users/jdeng/baiduCloudDisk/LAMOST/ana/outputs'

# if it is a directory 
if [ -d "$env_rawdata_path" ]
  then 
      echo "$env_rawdata_path" directory exists
  else
      echo "ERROR: $env_rawdata_path" directory does not exist
fi  

# check total number of days analysized and to be analysized
total_days=0
total_days_analysized=0

# loop through dates in $year
for i_date in $env_rawdata_path/$env_rawdata_year*
do
   # if it is a directory 
   if [ -d "$i_date" ]
      then
          #echo "i_date = " $i_date
	  env_rawdata_date=$i_date; export env_rawdata_date
	  n_det=0
	  # loop through 32 dets
	  while [ "$n_det" -lt 32 ]
	     do
	        #echo "$n_det" ${dets[$n_det]}
		env_rawdata_det=${dets[$n_det]}; export env_rawdata_det
		env_rawdata_files=()
		# loop through bias files for one det
		n_file=0
		for i_file in  $env_rawdata_date/bias/$env_rawdata_det*
		do
		    # if file exists
		    if [ -e "$i_file" ]
		       then
		          env_rawdata_files[$n_file]=$i_file
		          #echo ${env_rawdata_files[$n_file]}
			  # get path name
			  export env_rawdata_onlypath=$(dirname ${env_rawdata_files[$n_file]})
			  # get filename
			  onlyfilenames[$n_file]=$(basename ${env_rawdata_files[$n_file]})
		    fi  
		    ((n_file +=1))
		done 
		#echo "only pathname: "
		#echo ${env_rawdata_onlypath}
		#echo "onlyfilenames: "
		#echo ${onlyfilenames[*]}
		declare -x env_rawdata_onlyfilenames_0=${onlyfilenames[0]}
		declare -x env_rawdata_onlyfilenames_1=${onlyfilenames[1]}
		declare -x env_rawdata_onlyfilenames_2=${onlyfilenames[2]}
		declare -x env_rawdata_onlyfilenames_3=${onlyfilenames[3]}
		declare -x env_rawdata_onlyfilenames_4=${onlyfilenames[4]}
		#echo "raw files : "  ${env_rawdata_onlyfilenames}
		#echo "total number of files"  ${n_file} "for det " $env_rawdata_det 
		#python3 test_filename.py
		# check the test flag, if test=true, skip the python command
	       if [ $run_flag == 1 ]
		  then
		#	    python ana_image.py 
		           echo "run_flag ="  $run_flag
	       fi   # if test_flag
		((n_det +=1))
	     done # loop through 32 dets
             ((total_days_analysized +=1))
   fi   # if it is a directory 
done # loop through dates in $year
echo "total number of days analyzed = "  ${total_days_analysized} "for year " $env_rawdata_year 

