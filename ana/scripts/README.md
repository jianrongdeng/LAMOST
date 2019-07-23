# LAMOST
lamost CCD analyse package

==20171226 
   Reorganize package structure. 

============================
ROOT-plotting/
============================
  date: 20171228 by Jianrong Deng
  Purpose: module to plot histograms 
============================

============================
clusterClassified/
============================
  date: 20190619 by Jianrong Deng
  Purpose: clusterClassified module
  Data Input: cluster class data files
  Size: 1.3G for 2016 data
  Output: classify various eventtypes, including: 
       1. hot-strip clusters
       2. muon tracks
       3. gamma -> electron position conversion tracks
       4. non-track clusters: gamma / x-rays ? / alpha particles? / ...
  Output data format: 
       A. track classes 
          a. muon track class
	  b. conversion tracks class
       B. clusters classes: 
          a. gamma cluster

============================


============================
cluster/
============================
  date: 20171226 by Jianrong Deng
  Purpose: cluster module
============================

============================
image/
============================
  date: 20171226 by Jianrong Deng
  Purpose: image module
============================

============================
pixel/
============================
  date: 20171226 by Jianrong Deng
  Purpose: pixel module
============================

============================
jobSubmission/
============================
  date: 20171226 by Jianrong Deng
  Purpose: shell scripts to submit jobs
============================

============================
data-sanity-check/
============================
  date: 20180116 by Jianrong Deng
  Purpose: data sanity check module
============================

============================
EventDisplay
============================
  date: 20190427 by Jianrong Deng
  Purpose: Display selected events
============================

============================
hist
============================
  date: 20190515 by Jianrong Deng
  Purpose: classes handling histograms/ntuples/rootfiles
============================


============================
common/
============================
  date: 20180116 by Jianrong Deng
  Purpose: common tools, such as file input/output, stat calculation 
============================

============================
test/
============================
  date: 20180116 by Jianrong Deng
  Purpose: test various codes/modules
============================



============================
20171226-oldfiles/
============================
  date: 20171226 by Jianrong Deng
  Purpose: oldfiles (release v1.0-beta)
  WARNING: since the directory structure is changed, scripts in this directory might not run due to errors such as a module import error, or a file not found error etc.  Please use in caution.
============================

