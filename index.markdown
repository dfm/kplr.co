---
    layout: base
    title: Crowdsourced Kepler API documentation
---

The Kepler MAST API documentation *sucks*. Let's fix that here. Here's the
most useful [link](http://archive.stsci.edu/vo/mast_services.html).


Getting started
---------------

The root URL for the Kepler MAST API is:

{% highlight bash %}
http://archive.stsci.edu/kepler/{0}/search.php
{% endhighlight %}

where `{0}` is chosen from one of the table names. For example, to get a list
of all the KOIs, you would do something like:

{% highlight bash %}
http://archive.stsci.edu/kepler/koi/search.php?action=Search&outputformat=JSON
{% endhighlight %}

To filter by a specific Kepler ID, you would append [`&kepid=8559644`](
http://archive.stsci.edu/kepler/koi/search.php?action=Search&outputformat=JSON
&kepid=8559644) to the above URL.

