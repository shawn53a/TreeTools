#xml files created via: esearch -db sra -query "Chiroptera" | efilter -query "biomol rna [PROP]" | efilter -query "platform illumina [PROP]" | efetch -format xml > bats.xml

$file="xmlLam";

open(fh, '<', $file);


$E=0;
@ROW=();

#&& @ROW[4]=~/leaf/i


while(<fh>)
{
	if ($_ =~ /<EXPERIMENT_PACKAGE>/)
	{
		$E+=1;
		@ROW=();
		$TI=0;
		$SN=0;
		$T=0;
		$SR=0;

	}

	elsif ($_ =~ /<\/EXPERIMENT_PACKAGE>/){
		if ($E == 1)
		{
			if (scalar @ROW >= 1){
				print @ROW;
			}
			$E=0
			# @ROW=();
			# $TI=0;
			# $SN=0;
			# $T=0;
			# $SR=0;
		}
		# elsif ($E==2) 
		# {
		# 	$E =0;
		# }
		# else{
		# 	print $E;
		# }
	}

	elsif ($_ =~ /TAXON_ID/ && $TI==0) #print taxon ID
	{
		$_ =~ /([0-9]{3,6})/;
		#print($1,"\t");
		push(@ROW, $1, "\t");
		$TI+=1;
	}

	elsif ($_ =~ /SCIENTIFIC_NAME/ && $SN==0) #print scientific name
	{
		$_ =~ /([A-Z][a-z]{2,}( )?([a-z]{2,})?)/;
		#print($1,"\t");
		push(@ROW, $1, "\t");
		$SN+=1;
	}

	elsif ($_ =~ />tissue|>organism part/ && $T==0) #is there a tissue type?
	{	
		$T=1;
	}

	elsif ($T==1) #if tissue type present, print tissue
	{
		$_ =~ /(>[A-Za-z]{2,} ?(?:[A-Za-z]{2,})?)/;
		#$_ =~ /.*/;
		#print($_);
		#print($1 =~ /([A-Za-z]{2,}.?(?:[A-Za-z]{2,})?)/,"\t");
		push(@ROW,$1 =~ /([A-Za-z]{2,}.?(?:[A-Za-z]{2,})?)/,"\t");
		#push(@ROW,$1 =~ /.*/,"\t");
		$T=2;
	}

	elsif ($_ =~ /PRIMARY_ID>.RR/ && $SR==0) #print SRR number and print N/A for tissue type if it is not present
	{
		if ($T!=2)
		{
			#print("N/A","\t");
		}
		$_ =~ /([A-Z]{3}[0-9]{4,10})/;
		#print($1,"\n");
		push(@ROW,$1,"\n");
		$SR+=1;
		$T=0;
	}


}















