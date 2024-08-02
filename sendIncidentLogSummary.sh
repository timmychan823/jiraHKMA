. sendIncidentLogSummary.config
yourfilenames=`ls sendIncidentLogSummary/*.xlsx`
echo $recipientMailAddress #add this to sendmail later
for eachfile in $yourfilenames
do
   echo $eachfile #replace it with sendmail
   rm $eachfile
done