IronPython Tutorial Example Code
================================

This folder contains the example code for the "Developing with IronPython Tutorial".

By Christian Muirhead, Menno Smits, Michael Foord

For the ultimate guide to developing with IronPython check out "IronPython in
Action":

    http://www.ironpythoninaction.com/
    
The example code here is a very simple desktop Twitter client called "Stutter".
It uses Windows Forms for the user interface and will work on Windows, Linux or
Apple Mac OS X.

For Windows you need .NET 2.0 Service Pack 1 and either IronPython 1 or 2.

For Linux or the Mac you need Mono 1.9 or 2.0 (for the Mac Mono 2.0 is better).
Mono comes with both IronPython 1 and 2 (launched with ipy and ipy2 from the
terminal).

You will also need the Python standard library as well. This comes as standard
with the version of IronPython shipped with Mono. On Windows it is simplest to
install IronPython from the 2.0b4 installer which also comes with the Python
standard library.

You will also need a database; any of sqlite 3, MySQL, PostgreSQL or SQL
Server.


The 'complete' folder contains the code for the full version of Stutter. In
this folder is a sqlite database and the sqlite binary plus data connector
assembly for Windows. DONT LOOK AT THIS UNTIL AFTER THE TUTORIAL!

If you are using a Mac or Linux then you probably already have sqlite 3 and
Mono comes with support for sqlite. You can safely delete 'sqlite3.exe' and
'System.Data.SQLite.DLL'.

To use an alternative database you will need to set it up - sql scripts to do
this are in the 'db' folder. You will also need to modify 'stutter.ini'
appropriately.

You will also need to put your Twitter username and password into
'stutter.ini'.

If you are attending the tutorial (or following it from the notes), then a
'skeleton' of the application is in the 'tutorial' folder. We will be adding
code to this version to complete the functionality.



Notes For Windows Users
=======================

You'll need a data provider for all databases other than SQL Server
(System.Data.SqlClient comes with the .NET framework).


Notes For Mac Users
===================

Both Mono 1.9 and Mono 2.0 work fine, but Mono 2.0 is slightly better.


Notes For Linux Users
=====================

If your distribution ships with Mono 1.9 (eg. Fedora Core 9) then you should be
ready to go. Just check that 'mono --version' reports the correct version and
that you get the IronPython prompt when running the 'ipy' command.

If your distribution doesn't support Mono or has an older version, you can use
the excellent stand-alone installer.
http://ftp.novell.com/pub/mono/archive/1.9.1/linux-installer/2/mono-1.9.1_2-installer.bin

This installer can even be used alongside an already installed version from
your distro. To minimise the chance of interference with an existing version,
choose to not have the 1.9 version added to your path when asked. For sessions
where you'd like to use the new version run 'source
/opt/mono-1.9.1/bin/setup.sh'. This will add the new version to your $PATH for
that shell only.

Mono 2.0 Preview 2 or 3 also works fine.
http://mono.ximian.com/monobuild/preview/download-preview/

The standalone Mono installer ships with data providers for both sqlite and
Postgresql so you shouldn't need to install these. If you'd like to use the
MySQL provider you'll need to install it separately. Download the Windows
binaries (yes this works) as a .zip and extract. Install MySql.Data.dll using
something like

    gacutil -i MySql.Data.dll -gacdir /opt/mono-1.9.1

Replace the directory with the base directory of your Mono installation.

Data Provider links

    * SQLite

            The SQLite command line application (so you can run the SQL script
            that creates the database) - this is often installed already on
            Linux or Mac OS X http://www.sqlite.org/download.html

            The System.Data.SQLite data provider for your platform (if you're
            using Mono, it comes with the framework)
            http://sqlite.phxsoftware.com/
            
    * PostgreSQL
    
            The Npgsql data provider - more recent Postgres packages come with
            the Stack Builder application which can get this automatically.
            http://pgfoundry.org/projects/npgsql
            
    * MySQL

            The MySql connector for .NET
            http://dev.mysql.com/downloads/connector/net/5.0.html


Topics Covered
==============

Topics the example application illustrates include:

    * The clr module and basic .NET types
    * Using .NET types from IronPython
    * GUI applications with Windows Forms
    * Network access
    * Handling XML
    * Databases
    * Webservices
    * Threading
   
