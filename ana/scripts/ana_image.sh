#!/bin/bash
#============================
# ana_image.sh
#============================
#   date: 20170813 by Jianrong Deng
#   purpose:
#   	bash script to run through raw bias data
#    usage: ./ana_image.sh $run_flag $date $path_out [verbose]
#    example1: 
#      ./ana_image.sh 0 2016 
#           note:
#                debug run without running the python analysis code, just checking the script loops
#                 debug run: run_flag = 0
#               
#    example2: 
#      nohup ./ana_image.sh 1 201601 /home/jdeng/LAMOST/ana/outputs/run1_20171205 > ../log/ana_image/run1_20171205/test_201601.txt
#           note:
#                short test run, run through 5-day data ( in this example, run the first 5 days in January 2016)
#                 short test run: 		             
#                             run_flag = 1  env_path_out=/home/jdeng/LAMOST/ana/outputs/run1_20171205
#    example3: 
#      nohup ./ana_image.sh 2 2016 /home/jdeng/LAMOST/ana/outputs/run1_20171205 > ../log/ana_image/run1_20171205/fullRun_2016.txt
#        note: 
#             data analysis run :   
#                          run_flag = 2  env_path_out=/home/jdeng/LAMOST/ana/outputs/run1_20171205
#============================

if test $# -eq 0
    then
        echo "Usage: ./ana_image.sh $run_flag $date $path_out [$verbose] [$nice_flag]" 1>&2 #  note: "1>&2": redirect its output to standard error
	echo " Note: examples of acceptable formats for 'date': 2016, 201601, 20160101, 2016010[1-5]"
	echo " Note1: $1 = run_flag (0, 1, 2)"
        echo "   0 (test run, see ex1, only checking the flow of script loops) "
        echo "   1 (test data run, see ex2, only checking the first five days)  "
        echo "   2 (data run, see ex3)  "
	echo " Note2: $4 = verbose"
        echo "   0  off"
        echo "   1: on "
	echo " Note3: $5 = nice_flag"
        echo "   0  off"
        echo "   1: on "
fi    

# reprint the shell script command executed
echo $0 $@

run_flag=$1
echo "run_flag = " $run_flag
env_rawdata_year=$2; export env_rawdata_year
echo "env_rawdata_year = " $env_rawdata_year

#export env_path_out='/home/jdeng/LAMOST/ana/outputs'
export env_path_out=$3
echo "env_path_out=" $env_path_out

# reading the optional arguments if any
if [ $# -le 3 ]
    then
       verbose=0
       nice_flag=0
    else
      if [ $# -le 4 ]
         then
            verbose=$4
	 else    
	    nice_flag=$5
      fi	    
fi    

# 32 CCD dets
total_dets=32
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

export env_rawdata_path='/data2/rawdata'

# if it is a directory 
if [ -d "$env_rawdata_path" ]
  then 
      echo Data Directory = "$env_rawdata_path" 
  else
      echo "ERROR: $env_rawdata_path" directory does not exist
fi  

# check total number of days analyzed and to be analyzed
total_days=0
total_days_dets=0
total_days_analyzed=0
total_days_dets_analyzed=0

# loop through dates in $year
for i_date in $env_rawdata_path/$env_rawdata_year*
do
   # check if there are bias data taken during the current date
   if [ -d "$i_date/bias" ] # "-d": exists and is a direcotry
      then
		  # if there are bias data, check data
		  echo "checking the bias data taken on :" $i_date
		  env_rawdata_date=$i_date; export env_rawdata_date
		  n_det=-1
		  # loop through 32 dets
		  while [ "$n_det" -lt 31 ]
		     do
			((n_det +=1))
			#echo "$n_det" ${dets[$n_det]}
			env_rawdata_det=${dets[$n_det]}; export env_rawdata_det
			env_rawdata_files=()
			# loop through bias files for one det
			n_file=-1
			for i_file in  $env_rawdata_date/bias/$env_rawdata_det*
			do
			    ((n_file +=1)) # usually there will be FIVE bias data files for each det
			    # if file exists
			    if [ -e "$i_file" ] # "-e": exists 
			       then
				  env_rawdata_files[$n_file]=$i_file
				  #echo ${env_rawdata_files[$n_file]}
				  # get path name
				  export env_rawdata_onlypath=$(dirname ${env_rawdata_files[$n_file]})
				  # get filename
				  onlyfilenames[$n_file]=$(basename ${env_rawdata_files[$n_file]})
			       else
			          #if [ ${verbose}==1 ]
				  #   then
			          #       echo "$i_file does not exist"
				  #       #echo "number of bias files, n_file" = $n_file
				  #fi 
	                          continue # no bias data file, continue to next i_file
			    fi  
			done #for i_file in  $env_rawdata_date/bias/$env_rawdata_det*
			# counting the total number of days with 5 bias data files
		        if [ ${n_file} -eq 4 ]  # n_file is counted from 0
			   then
		               #echo "There are 5 bias data files on:" $i_date
			       ((total_days_dets +=1))
			   else  
			      if [ ${n_file} -eq 0 ] # empty directory, no data file
			         then
		                     echo "WARNING: no bias data file on: $i_date for the det: ${env_rawdata_det}"
			         else
		                     echo "WARNING: only ((${n_file} + 1))  bias data files on: $i_date for the det: ${env_rawdata_det}"
		             fi	# if [ ${n_file} -eq 0 ] # empty directory, no data file
			     continue  # < 5 bias files, continue to next det
		        fi	# if [ ${n_file} -eq 4 ]  # n_file is counted from 0
			#echo "only pathname: "
			#echo ${env_rawdata_onlypath}
			#echo "onlyfilenames: "
			#echo ${onlyfilenames[*]}
			# each det has 5 bias data files
			declare -x env_rawdata_onlyfilenames_0=${onlyfilenames[0]}
			declare -x env_rawdata_onlyfilenames_1=${onlyfilenames[1]}
			declare -x env_rawdata_onlyfilenames_2=${onlyfilenames[2]}
			declare -x env_rawdata_onlyfilenames_3=${onlyfilenames[3]}
			declare -x env_rawdata_onlyfilenames_4=${onlyfilenames[4]}
			#echo "raw files : "  ${env_rawdata_onlyfilenames}
			#echo "total number of files"  ${n_file} "for det " $env_rawdata_det 
			#python3 test_filename.py
			# check the run flag, if run_flag=1, run the python analysis process

                        # if short test run, print out evn variables
		        #if [ ${run_flag} -eq 1 ]
			#   then
		        #       if [ ${n_det} -eq 1 ]
			#           then
			#	       echo "n_file = " ${n_file}
			#               echo "env_rawdata_onlypath = " ${env_rawdata_onlypath}
			#       fi #if [ ${n_det} -eq 1 ]
		        #fi #if [ ${run_flag} -eq 1 ]

                        # execute python analysis script
		        if [ $run_flag -ge 1 ]
			   then
			       # the rawdata must be set before running data analysis script
			       if [ "${env_rawdata_onlypath}" = "" ]
			          then 
				     echo "{env_rawdata_onlypath} =" ${env_rawdata_onlypath}
			             echo "WARNING: data of date = $i_date, det = $env_rawdata_det does not exist"
				  else
				  if [ ${nice_flag} -eq 1 ]
				      then 
			                 nice python3 ana_image.py 
			              else		 
				         python3 ana_image.py  
			          fi		 # if [ ${nice_flag} -eq 1 ]
		                  ((total_days_dets_analyzed +=1))
			       fi	     
		        fi   # if [ $run_flag -ge 1 ]
		     done # loop through 32 dets


		     # in short test run, only run through data of the first five days
		     if [ ${run_flag} -eq 1 ]
			then
			if [ ${total_days_analyzed} -ge 5 ]
			   then
			       break
			fi  # if [ ${total_days_analyzed} -gt 5 ]
		     fi	  #if [ ${run_flag} -eq 1 ]
       else
	   echo "no bias directory for" $i_date
   fi # if [ -d "$i_date/bias" ]
done # loop through dates in $year
let total_days=${total_days_dets}/${total_dets}
let total_days_analyzed=${total_days_dets_analyzed}/${total_dets}
echo "total_days * total_number_of_dets = " ${total_days_dets}
echo "total_days_analyzed * total_number_of_dets = " ${total_days_dets_analyzed}
echo "total number of days with data = "  ${total_days} "for year " $env_rawdata_year 
echo "total number of days analyzed = "  ${total_days_analyzed} "for year " $env_rawdata_year 



