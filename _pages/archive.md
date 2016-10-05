---
layout: archive
permalink: /blog/
author_profile: false
sidebar: false
share: true
comments: false
---

{% include base_path %}

<h3 class="archive__subtitle">Recent Posts</h3>

{% for post in site.posts %}
  {% include archive-single.html %}
{% endfor %}
