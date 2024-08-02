. sendToVendor.config
echo $recipientMailAddress #add this to sendmail later
yourfilenames=`ls sendToVendor/*.zip`
for eachfile in $yourfilenames
do
   echo $eachfile #replace it with sendmail
   rm $eachfile
done