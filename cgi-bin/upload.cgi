#!/usr/bin/perl -w
#!C:\xampp\perl\bin\perl -w

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

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

if ( !$filename )
{
    print $query->header ( );
    print "There was a problem uploading your file.";
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
    die "Filename contains disallowed characters";
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
<link href="../static/css/bootstrap.min.css" rel="stylesheet">
<link href="../starter-template.css" rel="stylesheet">
<title>Thanks!</title>
<style type="text/css">
img {border: none;}
</style>
</head>
<body>
<div class="container">
<div class="starter-template">
<h1>Thanks for uploading your file!</h1>
<p class="lead"> Your file can be found <a href="$upload_dir_relative_to_this_script/$filename">here</a>
</div>
</div>
<script src="../static/js/jquery-1.11.1.min.js"></script>
<script src="../static/js/bootstrap.min.js"></script>
</body>
</html>
END_HTML
