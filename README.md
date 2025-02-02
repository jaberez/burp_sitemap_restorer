# burp_sitemap
Burp Sitemap Restorer: A easy tool to restore the sitemap in Burp Suite from a saved sitemap file.

# Why
I lost my work and couldn’t find a working solution to restore my sitemap.

# How to use
## Save sitemap
In Burp Suite go to the Target/Site Map and select site(s) you need to save. Right click ans select `Save selected items`. 
> [!IMPORTANT]
> Don't forget to save your map periodically.

## Restore sitemap
Usage is very simple.

Create a bearer variable using `export` unix command.

<code>export BEARER=eyJiLCJhbGciOiJSUzI1NiJ9.eyJzdGF0dXMiOiJzdWNjZXNzI.iwiZGF0YSI6eyJpZCI</code>

Run the script
<code>$./restore_sitemap.py ~/Documents/Juice/site-map-juice.xml "$BEARER" </code>

The script takes two parameters: "a saved sitemap in XML format" and "an authorization token". 
> [!TIP]
> Use export to set the variable. This makes it easier to rerun the command or change the token if you need to run it with more than one.

> [!WARNING]
> If the script gets stuck on any request, use `Ctrl-C` to continue.
