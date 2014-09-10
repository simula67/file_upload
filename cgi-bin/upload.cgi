#!/usr/bin/perl -w

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;

#$CGI::POST_MAX = 1024 * 5000;
my $safe_filename_characters = "a-zA-Z0-9_.-";
my $upload_dir_relative_to_this_script = "../uploaded_files";
my $upload_dir = dirname( __FILE__ ) . "/" .$upload_dir_relative_to_this_script;

my $query = new CGI;
my $filename = $query->param("upload_file_name");
my $email_address = $query->param("email_address");

if ( !$filename )
{
    print $query->header ( );
    print "There was a problem uploading your file (try a smaller file).";
    exit;
}

my ( $name, $path, $extension ) = fileparse ( $filename, '..*' );
$filename = $name . $extension;
$filename =~ tr/ /_/;
$filename =~ s/[^$safe_filename_characters]//g;

if ( $filename =~ /^([$safe_filename_characters]+)$/ )
{
    $filename = $1;
}
else
{
    die "Filename contains invalid characters";
}

my $upload_filehandle = $query->upload("upload_file_name");

open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "$!";
binmode UPLOADFILE;

while ( <$upload_filehandle> )
{
    print UPLOADFILE;
}

close UPLOADFILE;

print $query->header ( );
print <<END_HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Thanks!</title>
<style type="text/css">
img {border: none;}
</style>
</head>
<body>
<p>Thanks for uploading your file!</p>
<p> Your file can be found <a href="$upload_dir_relative_to_this_script/$filename">here</a>
<p>Your email address: $email_address</p>
</body>
</html>
END_HTML